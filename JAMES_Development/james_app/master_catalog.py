"""Master Catalog Engine & SQLite Multi-Manufacturer Registry for JAMES Digital Twin.

High-performance SQL database with B-Tree indexes, full ACID transactions,
dynamic JSON schema parsing, and automatic bi-directional sync to data/catalog/{mfg}.json.
"""

import json
import os
import re
import sqlite3
from typing import Any, Dict, List, Optional

CATALOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "catalog"))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "master_catalog.db"))


def sanitize_filename(name: str) -> str:
    """Generate a clean snake_case filename key for a manufacturer."""
    clean = re.sub(r"[^a-zA-Z0-9]+", "_", name.lower()).strip("_")
    return clean or "custom_manufacturer"


def _dict_factory(cursor, row):
    """SQLite row factory returning dictionaries."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class MasterCatalogManager:
    """Manages multi-manufacturer equipment catalogs using a persistent SQLite database."""

    def __init__(self, db_path: str = DB_PATH, catalog_dir: str = CATALOG_DIR):
        self.db_path = db_path
        self.catalog_dir = catalog_dir
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.catalog_dir, exist_ok=True)
        self._init_db()
        self._check_and_seed()

    def _get_connection(self) -> sqlite3.Connection:
        """Create and configure SQLite connection with WAL mode and row factory."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = _dict_factory
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _init_db(self) -> None:
        """Initialize the SQLite schema, indexes, and FTS5 search table."""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS catalog_items (
                    part_number TEXT PRIMARY KEY,
                    manufacturer TEXT NOT NULL,
                    series TEXT DEFAULT '',
                    domain TEXT NOT NULL,
                    type_tag TEXT NOT NULL,
                    type_name TEXT DEFAULT '',
                    description TEXT DEFAULT '',
                    voltage TEXT DEFAULT '',
                    amps REAL,
                    aic REAL,
                    kva REAL,
                    poles TEXT DEFAULT '',
                    phase TEXT DEFAULT '',
                    total_slots INTEGER,
                    nema_rating TEXT DEFAULT '',
                    impedance_z REAL,
                    upc TEXT DEFAULT '',
                    cut_sheet_url TEXT DEFAULT '',
                    specs_json TEXT DEFAULT '{}',
                    docs_json TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_catalog_domain_type ON catalog_items(domain, type_tag);
                CREATE INDEX IF NOT EXISTS idx_catalog_mfg_domain ON catalog_items(manufacturer, domain);
                CREATE INDEX IF NOT EXISTS idx_catalog_mfg ON catalog_items(manufacturer);
                CREATE INDEX IF NOT EXISTS idx_catalog_upc ON catalog_items(upc);
                CREATE INDEX IF NOT EXISTS idx_catalog_type ON catalog_items(type_tag);
            """)

    def _check_and_seed(self) -> None:
        """Seed SQLite database from JSON catalog files if empty."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT COUNT(*) as count FROM catalog_items;").fetchone()
            if not row or row["count"] == 0:
                self.seed_from_json()

    def seed_from_json(self) -> int:
        """Read data/catalog/*.json and populate SQLite database."""
        if not os.path.exists(self.catalog_dir):
            return 0

        seeded = 0
        with self._get_connection() as conn:
            for fname in sorted(os.listdir(self.catalog_dir)):
                if fname.endswith(".json"):
                    fpath = os.path.join(self.catalog_dir, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        mfg_name = data.get("manufacturer", os.path.splitext(fname)[0].capitalize())
                        items = data.get("items", [])

                        for raw in items:
                            item_dict = dict(raw)
                            item_dict["manufacturer"] = mfg_name
                            self._upsert_item_row(conn, item_dict)
                            seeded += 1
                    except Exception as e:
                        print(f"[MasterCatalogManager] Error seeding from {fname}: {e}")
            conn.commit()
        return seeded

    @property
    def manufacturers(self) -> Dict[str, Dict[str, Any]]:
        """Return dict of manufacturers for backward compatibility with tests/code."""
        mfgs = self.get_manufacturers()
        return {m["name"]: m for m in mfgs}

    def _row_to_item(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a flat SQLite database row back to standard structured CatalogItem format."""
        if not row:
            return {}

        specs = {}
        if row.get("specs_json"):
            try:
                specs = json.loads(row["specs_json"])
            except Exception:
                specs = {}

        # Fallback to column values if not present in specs_json
        if "voltage" not in specs and row.get("voltage"): specs["voltage"] = row["voltage"]
        if "amps" not in specs and row.get("amps") is not None: specs["amps"] = row["amps"]
        if "aic" not in specs and row.get("aic") is not None: specs["aic"] = row["aic"]
        if "kva" not in specs and row.get("kva") is not None: specs["kva"] = row["kva"]
        if "poles" not in specs and row.get("poles"): specs["poles"] = row["poles"]
        if "phase" not in specs and row.get("phase"): specs["phase"] = row["phase"]
        if "total_slots" not in specs and row.get("total_slots") is not None: specs["total_slots"] = row["total_slots"]
        if "nema_rating" not in specs and row.get("nema_rating"): specs["nema_rating"] = row["nema_rating"]
        if "impedance_z" not in specs and row.get("impedance_z") is not None: specs["impedance_z"] = row["impedance_z"]

        docs = {}
        if row.get("docs_json"):
            try:
                docs = json.loads(row["docs_json"])
            except Exception:
                docs = {}

        if "cut_sheet" not in docs and row.get("cut_sheet_url"): docs["cut_sheet"] = row["cut_sheet_url"]
        if "upc" not in docs and row.get("upc"): docs["upc"] = row["upc"]

        return {
            "part_number": row["part_number"],
            "manufacturer": row["manufacturer"],
            "series": row.get("series", ""),
            "domain": row["domain"],
            "type_tag": row["type_tag"],
            "type_name": row.get("type_name", ""),
            "description": row.get("description", ""),
            "specs": specs,
            "docs": docs
        }

    def _upsert_item_row(self, conn: sqlite3.Connection, item: Dict[str, Any]) -> None:
        """Insert or replace a catalog item in SQLite."""
        pn = str(item.get("part_number", "")).strip().upper()
        if not pn:
            raise ValueError("Part number is required.")

        mfg = str(item.get("manufacturer", "Generic")).strip()
        domain = str(item.get("domain", "power_distribution")).strip()
        type_tag = str(item.get("type_tag", "")).strip().upper()
        series = str(item.get("series", "")).strip()
        type_name = str(item.get("type_name", "")).strip()
        description = str(item.get("description", "")).strip()

        specs = dict(item.get("specs", {}))
        docs = dict(item.get("docs", {}))

        # Extract direct typed columns
        voltage = str(specs.get("voltage", "")).strip()
        amps = specs.get("amps")
        if amps is not None:
            try: amps = float(amps)
            except Exception: amps = None

        aic = specs.get("aic")
        if aic is not None:
            try: aic = float(aic)
            except Exception: aic = None

        kva = specs.get("kva")
        if kva is not None:
            try: kva = float(kva)
            except Exception: kva = None

        poles = str(specs.get("poles", "")).strip()
        phase = str(specs.get("phase", "")).strip()
        total_slots = specs.get("total_slots", specs.get("slots"))
        if total_slots is not None:
            try: total_slots = int(total_slots)
            except Exception: total_slots = None

        nema_rating = str(specs.get("nema_rating", "")).strip()
        impedance_z = specs.get("impedance_z")
        if impedance_z is not None:
            try: impedance_z = float(impedance_z)
            except Exception: impedance_z = None

        upc = str(docs.get("upc", item.get("upc", "")) or "").strip()
        cut_sheet_url = str(docs.get("cut_sheet", "")).strip()

        conn.execute("""
            INSERT INTO catalog_items (
                part_number, manufacturer, series, domain, type_tag, type_name, description,
                voltage, amps, aic, kva, poles, phase, total_slots, nema_rating, impedance_z,
                upc, cut_sheet_url, specs_json, docs_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(part_number) DO UPDATE SET
                manufacturer = excluded.manufacturer,
                series = excluded.series,
                domain = excluded.domain,
                type_tag = excluded.type_tag,
                type_name = excluded.type_name,
                description = excluded.description,
                voltage = excluded.voltage,
                amps = excluded.amps,
                aic = excluded.aic,
                kva = excluded.kva,
                poles = excluded.poles,
                phase = excluded.phase,
                total_slots = excluded.total_slots,
                nema_rating = excluded.nema_rating,
                impedance_z = excluded.impedance_z,
                upc = excluded.upc,
                cut_sheet_url = excluded.cut_sheet_url,
                specs_json = excluded.specs_json,
                docs_json = excluded.docs_json,
                updated_at = CURRENT_TIMESTAMP;
        """, (
            pn, mfg, series, domain, type_tag, type_name, description,
            voltage, amps, aic, kva, poles, phase, total_slots, nema_rating, impedance_z,
            upc, cut_sheet_url, json.dumps(specs), json.dumps(docs)
        ))

    def reload(self) -> None:
        """Re-verify DB connection and schema."""
        self._init_db()

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Return all catalog items ordered by manufacturer and part number."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM catalog_items ORDER BY manufacturer ASC, part_number ASC;
            """).fetchall()
            return [self._row_to_item(r) for r in rows]

    def get_item(self, part_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve single item specifications by part number using indexed query."""
        if not part_number:
            return None
        pn = part_number.strip().upper()
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM catalog_items WHERE UPPER(part_number) = ?;", (pn,)).fetchone()
            if row:
                return self._row_to_item(row)
        return None

    def get_manufacturers(self, domain: Optional[str] = None, type_tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve distinct manufacturers with item counts filtered by domain and/or type_tag."""
        query = "SELECT manufacturer, COUNT(*) as item_count FROM catalog_items"
        params = []
        conditions = []

        if domain:
            conditions.append("LOWER(domain) = LOWER(?)")
            params.append(domain)
        if type_tag:
            conditions.append("UPPER(type_tag) = UPPER(?)")
            params.append(type_tag)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY manufacturer ORDER BY manufacturer ASC;"

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [
                {
                    "key": sanitize_filename(r["manufacturer"]),
                    "name": r["manufacturer"],
                    "item_count": r["item_count"]
                }
                for r in rows
            ]

    def filter_items(
        self,
        manufacturer: Optional[str] = None,
        domain: Optional[str] = None,
        type_tag: Optional[str] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Filter items using indexed SQL query with optional text search and pagination."""
        sql = "SELECT * FROM catalog_items"
        params = []
        conditions = []

        if manufacturer:
            conditions.append("LOWER(manufacturer) LIKE LOWER(?)")
            params.append(f"%{manufacturer.strip()}%")

        if domain:
            conditions.append("LOWER(domain) = LOWER(?)")
            params.append(domain.strip())

        if type_tag:
            conditions.append("UPPER(type_tag) = UPPER(?)")
            params.append(type_tag.strip())

        if query:
            q = f"%{query.strip().lower()}%"
            conditions.append("""(
                LOWER(part_number) LIKE ? OR
                LOWER(description) LIKE ? OR
                LOWER(series) LIKE ? OR
                LOWER(manufacturer) LIKE ? OR
                LOWER(upc) LIKE ?
            )""")
            params.extend([q, q, q, q, q])

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY manufacturer ASC, part_number ASC"

        if limit is not None:
            sql += f" LIMIT {int(limit)} OFFSET {int(offset)}"

        with self._get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_item(r) for r in rows]

    def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search catalog items by query string."""
        return self.filter_items(query=query, limit=limit)

    def add_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item in SQLite database and sync to manufacturer JSON file."""
        pn = str(item_data.get("part_number", "")).strip().upper()
        if not pn:
            raise ValueError("Part number is required.")

        with self._get_connection() as conn:
            self._upsert_item_row(conn, item_data)
            conn.commit()

        # Auto-sync to disk
        mfg = str(item_data.get("manufacturer", "Generic")).strip()
        self._sync_mfg_to_disk(mfg)
        return self.get_item(pn)

    def update_item(self, original_pn: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing catalog item and sync changes to disk."""
        orig_pn_upper = original_pn.strip().upper()
        existing = self.get_item(orig_pn_upper)
        if not existing:
            raise KeyError(f"Item with part number '{original_pn}' not found.")

        old_mfg = existing.get("manufacturer", "Generic")
        new_pn = str(item_data.get("part_number", original_pn)).strip().upper()
        new_mfg = str(item_data.get("manufacturer", old_mfg)).strip() or old_mfg

        with self._get_connection() as conn:
            if orig_pn_upper != new_pn:
                conn.execute("DELETE FROM catalog_items WHERE UPPER(part_number) = ?;", (orig_pn_upper,))
            self._upsert_item_row(conn, item_data)
            conn.commit()

        if old_mfg.lower() != new_mfg.lower():
            self._sync_mfg_to_disk(old_mfg)

        self._sync_mfg_to_disk(new_mfg)
        return self.get_item(new_pn)

    def delete_item(self, part_number: str) -> bool:
        """Delete an item by part number from SQLite and sync to disk."""
        pn_upper = part_number.strip().upper()
        existing = self.get_item(pn_upper)
        if not existing:
            return False

        mfg = existing.get("manufacturer", "Generic")
        with self._get_connection() as conn:
            conn.execute("DELETE FROM catalog_items WHERE UPPER(part_number) = ?;", (pn_upper,))
            conn.commit()

        self._sync_mfg_to_disk(mfg)
        return True

    def clone_item(
        self,
        source_part_number: str,
        new_part_number: str,
        overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Clone an existing catalog item with a new part number and optional overrides."""
        source = self.get_item(source_part_number)
        if not source:
            raise KeyError(f"Source part '{source_part_number}' not found.")

        cloned = json.loads(json.dumps(source))  # Deep copy
        cloned["part_number"] = new_part_number.strip().upper()
        if overrides:
            for k, v in overrides.items():
                if k == "specs" and isinstance(v, dict):
                    cloned.setdefault("specs", {}).update(v)
                elif k == "docs" and isinstance(v, dict):
                    cloned.setdefault("docs", {}).update(v)
                else:
                    cloned[k] = v

        return self.add_item(cloned)

    def import_items(self, items: List[Dict[str, Any]], overwrite: bool = True) -> Dict[str, Any]:
        """Bulk import a list of items into SQLite with transaction safety."""
        imported = 0
        skipped = 0
        errors = []
        affected_mfgs = set()

        with self._get_connection() as conn:
            for idx, raw in enumerate(items):
                pn = str(raw.get("part_number", "")).strip().upper()
                if not pn:
                    errors.append(f"Row {idx + 1}: Missing part number.")
                    skipped += 1
                    continue

                if not overwrite:
                    existing = conn.execute("SELECT 1 FROM catalog_items WHERE UPPER(part_number) = ?;", (pn,)).fetchone()
                    if existing:
                        skipped += 1
                        continue

                mfg = str(raw.get("manufacturer", "Generic")).strip()
                affected_mfgs.add(mfg)
                try:
                    self._upsert_item_row(conn, raw)
                    imported += 1
                except Exception as e:
                    errors.append(f"Row {idx + 1} ({pn}): {e}")

            conn.commit()

        for mfg in affected_mfgs:
            self._sync_mfg_to_disk(mfg)

        return {
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "total_catalog_count": len(self.get_all_items())
        }

    def export_items(
        self,
        domain: Optional[str] = None,
        manufacturer: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Export catalog items filtered by domain and manufacturer."""
        return self.filter_items(manufacturer=manufacturer, domain=domain)

    def _sync_mfg_to_disk(self, mfg_name: str) -> None:
        """Write all items for a given manufacturer to data/catalog/{filename}.json for Git trackability."""
        os.makedirs(self.catalog_dir, exist_ok=True)
        fname = f"{sanitize_filename(mfg_name)}.json"
        fpath = os.path.join(self.catalog_dir, fname)

        mfg_items = self.filter_items(manufacturer=mfg_name)
        if not mfg_items and os.path.exists(fpath):
            try:
                os.remove(fpath)
            except Exception:
                pass
            return

        disk_items = []
        for item in mfg_items:
            disk_items.append({
                "part_number": item.get("part_number", ""),
                "series": item.get("series", ""),
                "domain": item.get("domain", "power_distribution"),
                "type_tag": item.get("type_tag", ""),
                "type_name": item.get("type_name", ""),
                "description": item.get("description", ""),
                "specs": item.get("specs", {}),
                "docs": item.get("docs", {"cut_sheet": "", "upc": item.get("docs", {}).get("upc", None)})
            })

        data = {
            "manufacturer": mfg_name,
            "items": disk_items
        }
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_catalog_stats(self) -> Dict[str, Any]:
        """Return aggregate summary metrics using fast SQLite queries."""
        with self._get_connection() as conn:
            total_items = conn.execute("SELECT COUNT(*) as count FROM catalog_items;").fetchone()["count"]
            total_mfgs = conn.execute("SELECT COUNT(DISTINCT manufacturer) as count FROM catalog_items;").fetchone()["count"]

            mfg_rows = conn.execute("SELECT manufacturer, COUNT(*) as cnt FROM catalog_items GROUP BY manufacturer ORDER BY cnt DESC;").fetchall()
            domain_rows = conn.execute("SELECT domain, COUNT(*) as cnt FROM catalog_items GROUP BY domain ORDER BY cnt DESC;").fetchall()
            type_rows = conn.execute("SELECT type_tag, COUNT(*) as cnt FROM catalog_items GROUP BY type_tag ORDER BY cnt DESC;").fetchall()

            return {
                "total_items": total_items,
                "total_manufacturers": total_mfgs,
                "by_manufacturer": {r["manufacturer"]: r["cnt"] for r in mfg_rows},
                "by_domain": {r["domain"]: r["cnt"] for r in domain_rows},
                "by_type": {r["type_tag"]: r["cnt"] for r in type_rows}
            }


# Global singleton instance
catalog_manager = MasterCatalogManager()


def get_master_catalog() -> MasterCatalogManager:
    """Return the global MasterCatalogManager singleton."""
    return catalog_manager
