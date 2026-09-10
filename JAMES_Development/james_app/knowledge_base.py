"""
Build Aware Knowledge Base & Multi-Format Document Ingestor
Provides SQLite FTS5 full-text search, multi-format file parsing (MD, PDF, HTML, TXT),
semantic chunking, BM25 relevance ranking, and highlighted snippet extraction.
"""

import os
import re
import sqlite3
import html
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "knowledge_base.db")


class SimpleHTMLTextExtractor(HTMLParser):
    """Clean HTML text extractor that preserves semantic heading structure."""
    def __init__(self):
        super().__init__()
        self.chunks: List[Dict[str, Any]] = []
        self.current_tag: Optional[str] = None
        self.current_heading: str = ""
        self.current_text: List[str] = []
        self.in_script_or_style: bool = False
        self.page_title: str = ""

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower in ("script", "style", "noscript"):
            self.in_script_or_style = True
            return
        if tag_lower in ("h1", "h2", "h3", "h4", "title"):
            # Flush existing text before starting new heading section
            self._flush_chunk()
            self.current_tag = tag_lower

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in ("script", "style", "noscript"):
            self.in_script_or_style = False
            return
        if tag_lower in ("h1", "h2", "h3", "h4", "title"):
            heading_str = " ".join(self.current_text).strip()
            if tag_lower == "title" and not self.page_title:
                self.page_title = heading_str
            else:
                self.current_heading = heading_str
            self.current_text = []
            self.current_tag = None

    def handle_data(self, data):
        if self.in_script_or_style:
            return
        text = data.strip()
        if text:
            self.current_text.append(text)

    def _flush_chunk(self):
        text_content = " ".join(self.current_text).strip()
        if text_content and len(text_content) >= 20:
            self.chunks.append({
                "heading": self.current_heading or "General Content",
                "text": text_content
            })
        self.current_text = []

    def close(self):
        super().close()
        self._flush_chunk()


class KnowledgeBaseManager:
    """Manages the SQLite FTS5 Knowledge Base and Document Ingestion Pipeline."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        con.execute("PRAGMA journal_mode = WAL")
        return con

    def _init_db(self):
        with self._get_connection() as con:
            # 1. Physical document chunks table
            con.execute("""
                CREATE TABLE IF NOT EXISTS kb_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_file TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    section_heading TEXT,
                    page_number INTEGER,
                    body_text TEXT NOT NULL,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Virtual Full-Text Search Table (FTS5) with Porter Stemmer
            con.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS kb_fts USING fts5(
                    title,
                    section_heading,
                    body_text,
                    tags,
                    content='kb_documents',
                    content_rowid='id',
                    tokenize='porter unicode61'
                );
            """)

            # 3. Triggers for real-time synchronization between physical & FTS tables
            con.execute("""
                CREATE TRIGGER IF NOT EXISTS kb_ai AFTER INSERT ON kb_documents BEGIN
                    INSERT INTO kb_fts(rowid, title, section_heading, body_text, tags)
                    VALUES (new.id, new.title, new.section_heading, new.body_text, new.tags);
                END;
            """)
            con.execute("""
                CREATE TRIGGER IF NOT EXISTS kb_ad AFTER DELETE ON kb_documents BEGIN
                    INSERT INTO kb_fts(kb_fts, rowid, title, section_heading, body_text, tags)
                    VALUES('delete', old.id, old.title, old.section_heading, old.body_text, old.tags);
                END;
            """)
            con.execute("""
                CREATE TRIGGER IF NOT EXISTS kb_au AFTER UPDATE ON kb_documents BEGIN
                    INSERT INTO kb_fts(kb_fts, rowid, title, section_heading, body_text, tags)
                    VALUES('delete', old.id, old.title, old.section_heading, old.body_text, old.tags);
                    INSERT INTO kb_fts(rowid, title, section_heading, body_text, tags)
                    VALUES (new.id, new.title, new.section_heading, new.body_text, new.tags);
                END;
            """)

    # -------------------------------------------------------------------------
    # MULTI-FORMAT DOCUMENT PARSERS & CHUNKERS
    # -------------------------------------------------------------------------

    @staticmethod
    def parse_markdown(content: str, filename: str) -> List[Dict[str, Any]]:
        """Parses Markdown content into semantically segmented chunks based on headings."""
        lines = content.splitlines()
        chunks: List[Dict[str, Any]] = []
        
        # 1. Extract primary document title (# Title or frontmatter)
        doc_title = Path(filename).stem.replace("_", " ").title()
        for line in lines[:20]:
            if line.startswith("# "):
                doc_title = line.lstrip("# ").strip()
                break

        current_heading = "Overview"
        current_lines: List[str] = []
        
        # Tag extractor pattern (#tag or keyword tags)
        tag_pattern = re.compile(r"#([A-Za-z0-9_-]+)")
        
        def flush(heading: str, body_lines: List[str]):
            body = "\n".join(body_lines).strip()
            if body and len(body) >= 25:
                # Clean up excess markdown markers for indexing
                found_tags = list(set(tag_pattern.findall(body)))
                chunks.append({
                    "title": doc_title,
                    "section_heading": heading,
                    "body_text": body,
                    "tags": ", ".join(found_tags),
                    "page_number": None
                })

        for line in lines:
            # Check for H2 or H3 heading boundaries
            h_match = re.match(r"^(#{2,4})\s+(.+)$", line)
            if h_match:
                flush(current_heading, current_lines)
                current_heading = h_match.group(2).strip()
                current_lines = []
            else:
                current_lines.append(line)

        flush(current_heading, current_lines)
        return chunks

    @staticmethod
    def parse_pdf(file_path_or_bytes: Any, filename: str) -> List[Dict[str, Any]]:
        """Extracts text from PDF documents page by page with paragraph chunking."""
        chunks: List[Dict[str, Any]] = []
        try:
            import pypdf
        except ImportError:
            print("Warning: pypdf not installed. Skipping PDF parsing.")
            return chunks

        doc_title = Path(filename).stem.replace("_", " ").title()
        
        try:
            reader = pypdf.PdfReader(file_path_or_bytes)
            for page_idx, page in enumerate(reader.pages, start=1):
                raw_text = page.extract_text() or ""
                paragraphs = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) >= 30]
                
                if not paragraphs and len(raw_text.strip()) >= 30:
                    paragraphs = [raw_text.strip()]
                
                for p_idx, paragraph in enumerate(paragraphs):
                    first_line = paragraph.splitlines()[0][:60].strip()
                    section_name = f"Page {page_idx} - {first_line}" if first_line else f"Page {page_idx}"
                    chunks.append({
                        "title": doc_title,
                        "section_heading": section_name,
                        "body_text": paragraph,
                        "tags": f"pdf, page_{page_idx}",
                        "page_number": page_idx
                    })
        except Exception as e:
            print(f"Error reading PDF {filename}: {e}")

        return chunks

    @staticmethod
    def parse_html(content: str, filename: str) -> List[Dict[str, Any]]:
        """Extracts clean structured text sections from HTML files."""
        parser = SimpleHTMLTextExtractor()
        parser.feed(content)
        parser.close()
        
        doc_title = parser.page_title or Path(filename).stem.replace("_", " ").title()
        chunks: List[Dict[str, Any]] = []
        
        for item in parser.chunks:
            chunks.append({
                "title": doc_title,
                "section_heading": item["heading"],
                "body_text": item["text"],
                "tags": "html_guide",
                "page_number": None
            })
        return chunks

    @staticmethod
    def parse_plaintext(content: str, filename: str) -> List[Dict[str, Any]]:
        """Extracts paragraph chunks from plaintext files."""
        doc_title = Path(filename).stem.replace("_", " ").title()
        paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) >= 30]
        chunks: List[Dict[str, Any]] = []
        
        for idx, p in enumerate(paragraphs, start=1):
            chunks.append({
                "title": doc_title,
                "section_heading": f"Section {idx}",
                "body_text": p,
                "tags": "text",
                "page_number": None
            })
        return chunks

    @staticmethod
    def parse_csv(content: str, filename: str) -> List[Dict[str, Any]]:
        """Parses CSV files (including standard inspection checklists) into semantic chunks."""
        import csv
        import io
        chunks: List[Dict[str, Any]] = []
        reader = csv.DictReader(io.StringIO(content))
        doc_title = Path(filename).stem.replace("_", " ").title()
        
        for idx, row in enumerate(reader, 1):
            chk_title = row.get("Checklist_Title") or doc_title
            chk_id = row.get("Checklist_ID") or ""
            item_no = row.get("Item_No") or str(idx)
            std_ref = row.get("Standard_Ref") or row.get("NEC_Ref") or ""
            prompt = row.get("Inspection_Prompt") or row.get("Prompt") or row.get("Question") or ""
            criteria = row.get("Verification_Criteria") or row.get("Criteria") or ""
            severity = row.get("Severity") or ""
            guidance = row.get("Guidance_Notes") or row.get("Notes") or ""
            freq = row.get("Standard_Frequency") or row.get("Frequency") or ""
            cat = row.get("Category") or ""

            if prompt or criteria:
                body_parts = []
                if prompt:
                    body_parts.append(f"Inspection Item: {prompt}")
                if criteria:
                    body_parts.append(f"Verification Criteria: {criteria}")
                if std_ref:
                    body_parts.append(f"Standard / Code Reference: {std_ref}")
                if severity:
                    body_parts.append(f"Severity: {severity}")
                if freq:
                    body_parts.append(f"Frequency: {freq}")
                if guidance:
                    body_parts.append(f"Guidance / Notes: {guidance}")

                heading = f"Item {item_no}" + (f": {std_ref}" if std_ref else "")
                full_title = f"{chk_title}" + (f" ({chk_id})" if chk_id else "")
                tags_list = ["checklist"]
                if cat:
                    tags_list.append(cat.lower())
                if severity:
                    tags_list.append(severity.lower())
                if std_ref:
                    tags_list.append(std_ref.lower().replace(" ", "_"))

                chunks.append({
                    "title": full_title,
                    "section_heading": heading,
                    "body_text": "\n".join(body_parts),
                    "tags": ", ".join(tags_list),
                    "page_number": int(item_no) if item_no.isdigit() else idx
                })
            else:
                # Generic CSV row
                row_str = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
                if len(row_str) >= 20:
                    chunks.append({
                        "title": doc_title,
                        "section_heading": f"Row {idx}",
                        "body_text": row_str,
                        "tags": "csv_data",
                        "page_number": idx
                    })
        return chunks

    @staticmethod
    def parse_excel(file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Parses Excel (.xlsx) workbooks into semantic inspection chunks."""
        chunks: List[Dict[str, Any]] = []
        try:
            import openpyxl
        except ImportError:
            print("Warning: openpyxl not installed. Skipping Excel parsing.")
            return chunks

        doc_title = Path(filename).stem.replace("_", " ").title()
        try:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            for sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                rows = list(ws.iter_rows(values_only=True))
                if not rows or len(rows) < 2:
                    continue

                headers = [str(h).strip() if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]
                
                for idx, r_vals in enumerate(rows[1:], 1):
                    row = {headers[i]: (str(v).strip() if v is not None else "") for i, v in enumerate(r_vals) if i < len(headers)}
                    
                    chk_title = row.get("Checklist_Title") or sheet_name or doc_title
                    chk_id = row.get("Checklist_ID") or ""
                    item_no = row.get("Item_No") or str(idx)
                    std_ref = row.get("Standard_Ref") or row.get("NEC_Ref") or ""
                    prompt = row.get("Inspection_Prompt") or row.get("Prompt") or row.get("Question") or ""
                    criteria = row.get("Verification_Criteria") or row.get("Criteria") or ""
                    severity = row.get("Severity") or ""
                    guidance = row.get("Guidance_Notes") or row.get("Notes") or ""
                    freq = row.get("Standard_Frequency") or row.get("Frequency") or ""
                    cat = row.get("Category") or ""

                    if prompt or criteria:
                        body_parts = []
                        if prompt:
                            body_parts.append(f"Inspection Item: {prompt}")
                        if criteria:
                            body_parts.append(f"Verification Criteria: {criteria}")
                        if std_ref:
                            body_parts.append(f"Standard / Code Reference: {std_ref}")
                        if severity:
                            body_parts.append(f"Severity: {severity}")
                        if freq:
                            body_parts.append(f"Frequency: {freq}")
                        if guidance:
                            body_parts.append(f"Guidance / Notes: {guidance}")

                        heading = f"Item {item_no}" + (f": {std_ref}" if std_ref else "")
                        full_title = f"{chk_title}" + (f" ({chk_id})" if chk_id else "")
                        tags_list = ["checklist"]
                        if cat:
                            tags_list.append(cat.lower())
                        if severity:
                            tags_list.append(severity.lower())
                        if std_ref:
                            tags_list.append(std_ref.lower().replace(" ", "_"))

                        chunks.append({
                            "title": full_title,
                            "section_heading": heading,
                            "body_text": "\n".join(body_parts),
                            "tags": ", ".join(tags_list),
                            "page_number": int(item_no) if str(item_no).isdigit() else idx
                        })
                    else:
                        row_str = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
                        if len(row_str) >= 20:
                            chunks.append({
                                "title": f"{doc_title} - {sheet_name}",
                                "section_heading": f"Row {idx}",
                                "body_text": row_str,
                                "tags": "excel_data",
                                "page_number": idx
                            })
        except Exception as e:
            print(f"Error reading Excel file {filename}: {e}")

        return chunks

    # -------------------------------------------------------------------------
    # INGESTION API
    # -------------------------------------------------------------------------

    def ingest_chunk(
        self,
        source_file: str,
        source_type: str,
        category: str,
        title: str,
        section_heading: Optional[str],
        body_text: str,
        tags: Optional[str] = None,
        page_number: Optional[int] = None
    ) -> int:
        """Inserts a single chunk into the Knowledge Base."""
        with self._get_connection() as con:
            cur = con.execute("""
                INSERT INTO kb_documents (source_file, source_type, category, title, section_heading, page_number, body_text, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (source_file, source_type, category, title, section_heading or "General", page_number, body_text, tags or ""))
            con.commit()
            return cur.lastrowid

    def ingest_file(self, file_path: str, category: Optional[str] = None) -> int:
        """Parses a local file and ingests all extracted chunks."""
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower().lstrip(".")
        filename = path.name
        cat = category or self._infer_category(path)
        chunks: List[Dict[str, Any]] = []

        if ext in ("md", "markdown"):
            content = path.read_text(encoding="utf-8", errors="ignore")
            chunks = self.parse_markdown(content, filename)
        elif ext == "pdf":
            chunks = self.parse_pdf(str(path), filename)
        elif ext in ("html", "htm"):
            content = path.read_text(encoding="utf-8", errors="ignore")
            chunks = self.parse_html(content, filename)
        elif ext == "csv":
            content = path.read_text(encoding="utf-8", errors="ignore")
            chunks = self.parse_csv(content, filename)
        elif ext in ("xlsx", "xlsm", "xltx"):
            chunks = self.parse_excel(str(path), filename)
        elif ext in ("txt", "log", "json"):
            content = path.read_text(encoding="utf-8", errors="ignore")
            chunks = self.parse_plaintext(content, filename)
        else:
            print(f"Unsupported file format: {ext}")
            return 0

        # Remove previous chunks for this file if re-indexing
        self.remove_file(filename)

        inserted_count = 0
        with self._get_connection() as con:
            for c in chunks:
                con.execute("""
                    INSERT INTO kb_documents (source_file, source_type, category, title, section_heading, page_number, body_text, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (filename, ext, cat, c["title"], c.get("section_heading"), c.get("page_number"), c["body_text"], c.get("tags", "")))
                inserted_count += 1
            con.commit()

        return inserted_count

    def ingest_directory(self, dir_path: str, recursive: bool = True, category: Optional[str] = None) -> Dict[str, int]:
        """Scans a directory and ingests all supported files.
        When both a .pdf and a companion .md exist with the same name, prefers the .pdf
        to avoid duplicate search results and provide direct page-level PDF viewer links.
        """
        dir_p = Path(dir_path)
        if not dir_p.exists() or not dir_p.is_dir():
            raise NotADirectoryError(f"Directory not found: {dir_path}")

        pattern = "**/*" if recursive else "*"
        supported_exts = {".md", ".markdown", ".pdf", ".html", ".htm", ".txt", ".csv", ".xlsx"}
        results: Dict[str, int] = {}

        all_files = [f for f in dir_p.glob(pattern) if f.is_file() and f.suffix.lower() in supported_exts]
        pdf_stems = {f.stem.lower() for f in all_files if f.suffix.lower() == ".pdf"}

        for file_p in all_files:
            # If a companion .pdf exists for this markdown file, prefer the PDF
            if file_p.suffix.lower() in (".md", ".markdown") and file_p.stem.lower() in pdf_stems:
                # Ensure any stale markdown chunks are removed from the database
                self.remove_file(file_p.name)
                continue

            try:
                count = self.ingest_file(str(file_p), category=category)
                results[file_p.name] = count
            except Exception as e:
                print(f"Error ingesting {file_p}: {e}")
                results[file_p.name] = 0

        return results

    def remove_file(self, filename: str) -> int:
        """Removes all indexed chunks for a given file name."""
        with self._get_connection() as con:
            cur = con.execute("DELETE FROM kb_documents WHERE source_file = ?", (filename,))
            con.commit()
            return cur.rowcount

    def clear(self):
        """Clears the entire Knowledge Base."""
        with self._get_connection() as con:
            con.execute("DELETE FROM kb_documents")
            con.commit()

    @staticmethod
    def _infer_category(path: Path) -> str:
        name = str(path).lower()
        parts = [p.lower() for p in path.parts]
        for idx, part in enumerate(parts):
            if part in ("faq", "knowledge_base") and idx + 1 < len(parts) - 1:
                return parts[idx + 1].replace("-", "_").replace(" ", "_")

        if "safety" in name or "arc" in name:
            return "safety"
        if "prd" in name or "spec" in name or "layout" in name:
            return "specs"
        if "conops" in name or "guide" in name or "workflow" in name:
            return "workflow"
        if "nec" in name or "code" in name or "rule" in name:
            return "nec_code"
        if "object" in name or "breaker" in name or "panel" in name or "transformer" in name:
            return "objects"
        if "catalog" in name:
            return "catalog"
        if "faq" in name:
            return "faq"
        return "general"

    # -------------------------------------------------------------------------
    # SEARCH & SNIPPET EXTRACTION
    # -------------------------------------------------------------------------

    def search(self, query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Executes a Full-Text Search against the Knowledge Base using FTS5 and BM25 ranking.
        Returns matched documents with highlighted contextual snippets.
        """
        clean_q = self._sanitize_fts_query(query)
        if not clean_q:
            return []

        with self._get_connection() as con:
            if category and category != "all":
                sql = """
                    SELECT 
                        d.id,
                        d.source_file,
                        d.source_type,
                        d.category,
                        d.title,
                        d.section_heading,
                        d.page_number,
                        d.tags,
                        snippet(kb_fts, 2, '<mark class=\"bg-amber-200 dark:bg-amber-900/80 text-amber-950 dark:text-amber-100 font-bold px-1 rounded\">', '</mark>', '...', 28) AS snippet,
                        bm25(kb_fts) AS rank
                    FROM kb_fts
                    JOIN kb_documents d ON kb_fts.rowid = d.id
                    WHERE kb_fts MATCH ? AND d.category = ?
                    ORDER BY rank ASC
                    LIMIT ?
                """
                params = (clean_q, category, limit)
            else:
                sql = """
                    SELECT 
                        d.id,
                        d.source_file,
                        d.source_type,
                        d.category,
                        d.title,
                        d.section_heading,
                        d.page_number,
                        d.tags,
                        snippet(kb_fts, 2, '<mark class=\"bg-amber-200 dark:bg-amber-900/80 text-amber-950 dark:text-amber-100 font-bold px-1 rounded\">', '</mark>', '...', 28) AS snippet,
                        bm25(kb_fts) AS rank
                    FROM kb_fts
                    JOIN kb_documents d ON kb_fts.rowid = d.id
                    WHERE kb_fts MATCH ?
                    ORDER BY rank ASC
                    LIMIT ?
                """
                params = (clean_q, limit)

            try:
                rows = con.execute(sql, params).fetchall()
                results = []
                for r in rows:
                    results.append({
                        "id": r["id"],
                        "source_file": r["source_file"],
                        "source_type": r["source_type"],
                        "category": r["category"],
                        "title": r["title"],
                        "section_heading": r["section_heading"],
                        "page_number": r["page_number"],
                        "tags": [t.strip() for t in (r["tags"] or "").split(",") if t.strip()],
                        "snippet": r["snippet"],
                        "rank": round(float(r["rank"]), 3)
                    })
                return results
            except sqlite3.OperationalError as e:
                print(f"FTS Search Operational Error for query '{clean_q}': {e}")
                return []

    @staticmethod
    def _sanitize_fts_query(query: str) -> str:
        """
        Sanitizes user input into valid SQLite FTS5 query format.
        Filters conversational stopwords and uses OR expansion with prefix matching for high-recall ranking.
        """
        stopwords = {
            "how", "do", "i", "can", "the", "a", "an", "to", "is", "what", "in", "for",
            "of", "and", "or", "about", "with", "my", "on", "it", "are", "be", "at", "by", "from"
        }
        tokens = [t.lower() for t in re.findall(r"[A-Za-z0-9_]+", query)]
        if not tokens:
            return ""

        content_tokens = [t for t in tokens if t not in stopwords]
        target_tokens = content_tokens if content_tokens else tokens
        
        # Multi-term query: combine with OR and prefix matching for BM25 ranking
        return " OR ".join(f'"{tok}"*' for tok in target_tokens)

    def get_stats(self) -> Dict[str, Any]:
        """Returns Knowledge Base statistics."""
        with self._get_connection() as con:
            total_chunks = con.execute("SELECT COUNT(*) FROM kb_documents").fetchone()[0]
            distinct_files = con.execute("SELECT COUNT(DISTINCT source_file) FROM kb_documents").fetchone()[0]
            categories = [r[0] for r in con.execute("SELECT DISTINCT category FROM kb_documents").fetchall()]
            
            files_breakdown = []
            for row in con.execute("SELECT source_file, source_type, category, COUNT(*) as chunks FROM kb_documents GROUP BY source_file"):
                files_breakdown.append({
                    "file": row["source_file"],
                    "type": row["source_type"],
                    "category": row["category"],
                    "chunks": row["chunks"]
                })

            return {
                "total_chunks": total_chunks,
                "distinct_files": distinct_files,
                "categories": categories,
                "files": files_breakdown
            }
