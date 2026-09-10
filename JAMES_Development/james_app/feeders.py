"""
Feeder & Cable Management Service for BuildingAware (JAMES).
Extracts, updates, and computes engineering metrics for all electrical connection runs
across the facility digital twin.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from sqlalchemy.orm import Session

from james_app.db import (
    get_session,
    NodeRecord,
    EdgeRecord,
    export_to_jsonl,
    DEFAULT_CLIENT,
    DEFAULT_FACILITY
)
from james_app.core.feeder_calculator import (
    calculate_voltage_drop,
    suggest_feeder_conductors,
    get_egc_size,
    STANDARD_GAUGES
)


def get_facility_feeders(client_id: str = DEFAULT_CLIENT, facility_id: str = DEFAULT_FACILITY) -> List[Dict[str, Any]]:
    """
    Retrieves all active feeder connection edges in the facility.
    Builds rich connection objects from node 'fed_from' relationships and explicit EdgeRecords,
    computing NEC ampacity and real-time voltage drop for each run.
    """
    session = get_session(client_id, facility_id)
    feeders: List[Dict[str, Any]] = []

    try:
        nodes = session.query(NodeRecord).all()
        node_map = {n.tag: n for n in nodes if n.tag}
        id_map = {n.id: n for n in nodes if n.id}

        # Query explicit edges if any exist
        edges = session.query(EdgeRecord).all()
        edge_map = {(e.from_node_tag, e.to_node_tag): e for e in edges}

        # Build feeder run for every node that has a valid 'fed_from' upstream link
        for node in nodes:
            fed_from = node.fed_from
            if not fed_from or fed_from in ("-- None / Service Entrance --", "None", "null", ""):
                continue

            # Resolve parent node
            parent_node = node_map.get(fed_from) or id_map.get(fed_from)
            from_tag = parent_node.tag if parent_node else fed_from
            to_tag = node.tag

            edge_key = (from_tag, to_tag)
            edge_rec = edge_map.get(edge_key)

            # Node attrs feeder dictionary or fallback
            node_attrs = node.attributes or {}
            feeder_data = node_attrs.get("feeder") or (edge_rec.conductor_spec if edge_rec else {}) or {}

            # Extract or default electrical physics
            current_amps = float(node.amps or (node_attrs.get("bus_rating_a") or node_attrs.get("mca") or 20.0))
            voltage_str = str(node.voltage or parent_node.voltage if parent_node else "480V")
            
            # Determine voltage magnitude and 3-phase status
            is_three_phase = ("3Ø" in voltage_str or "3Ph" in voltage_str or "480" in voltage_str or "208" in voltage_str)
            nom_voltage = 480.0 if "480" in voltage_str else (208.0 if "208" in voltage_str else (120.0 if "120" in voltage_str else 480.0))

            # Conductor defaults
            conductor_size = feeder_data.get("conductor_size") or ("500 kcmil" if current_amps >= 300 else ("4/0 AWG" if current_amps >= 175 else ("1/0 AWG" if current_amps >= 100 else ("#4 AWG" if current_amps >= 60 else "12 AWG"))))
            material = feeder_data.get("material") or "Cu"
            sets = int(feeder_data.get("sets") or (4 if current_amps >= 1200 else (2 if current_amps >= 600 else 1)))
            conduit_type = feeder_data.get("conduit_type") or "EMT"
            conduit_size = feeder_data.get("conduit_size") or ("4\"" if sets > 1 or "500" in conductor_size else "2.5\"")
            length_ft = float(feeder_data.get("length_ft") or 65.0)
            insulation = feeder_data.get("insulation") or "THHN/THWN-2"
            cable_tag = feeder_data.get("cable_tag") or f"FDR-{from_tag}-{to_tag}"
            ground_size = feeder_data.get("ground_size") or get_egc_size(current_amps, material)
            notes = feeder_data.get("notes") or ""

            # Check if there is a matching breaker in parent's schedule
            breaker_info = None
            if parent_node and parent_node.attributes and "schedule" in parent_node.attributes:
                parent_sched = parent_node.attributes.get("schedule", [])
                for row in parent_sched:
                    if row.get("leftTargetLoad") == to_tag:
                        breaker_info = f"{row.get('leftTrip', '')}A {row.get('leftPoles', 1)}P ({row.get('leftType', 'MCCB')})"
                        break
                    elif row.get("rightTargetLoad") == to_tag:
                        breaker_info = f"{row.get('rightTrip', '')}A {row.get('rightPoles', 1)}P ({row.get('rightType', 'MCCB')})"
                        break

            # Calculate live engineering voltage drop
            v_drop_calc = calculate_voltage_drop(
                voltage=nom_voltage,
                current_amps=current_amps,
                length_ft=length_ft,
                conductor_size=conductor_size,
                material=material,
                sets=sets,
                conduit_type=conduit_type,
                is_three_phase=is_three_phase
            )

            # Format human summary run
            if sets == 1:
                run_summary = f"1x (3-{conductor_size} {material} + 1#{ground_size})"
            else:
                run_summary = f"{sets}x (3-{conductor_size} {material} + 1#{ground_size})"

            edge_id = edge_rec.id if edge_rec else f"edge_{from_tag}_{to_tag}"

            feeders.append({
                "id": edge_id,
                "cable_tag": cable_tag,
                "from_tag": from_tag,
                "from_name": parent_node.name if parent_node else from_tag,
                "from_domain": parent_node.domain if parent_node else "sources",
                "from_room": parent_node.room if parent_node else "",
                "to_tag": to_tag,
                "to_name": node.name or to_tag,
                "to_domain": node.domain or "panels",
                "to_room": node.room or "",
                "voltage": voltage_str,
                "current_amps": current_amps,
                "conductor_size": conductor_size,
                "material": material,
                "sets": sets,
                "conduit_type": conduit_type,
                "conduit_size": conduit_size,
                "length_ft": length_ft,
                "insulation": insulation,
                "ground_size": ground_size,
                "run_summary": run_summary,
                "breaker_info": breaker_info,
                "notes": notes,
                "calculation": v_drop_calc
            })

    finally:
        session.close()

    return feeders


def update_feeder_edge(
    edge_id: str,
    from_tag: str,
    to_tag: str,
    data: Dict[str, Any],
    client_id: str = DEFAULT_CLIENT,
    facility_id: str = DEFAULT_FACILITY
) -> Dict[str, Any]:
    """
    Updates or inserts feeder conductor data for a connection edge.
    Persists to SQLite and companion model.jsonl.
    """
    session = get_session(client_id, facility_id)
    try:
        # 1. Update downstream node's attributes['feeder']
        to_node = session.query(NodeRecord).filter(NodeRecord.tag == to_tag).first()
        if to_node:
            attrs = dict(to_node.attributes or {})
            attrs["feeder"] = {
                "cable_tag": data.get("cable_tag"),
                "conductor_size": data.get("conductor_size"),
                "material": data.get("material", "Cu"),
                "sets": int(data.get("sets") or 1),
                "conduit_type": data.get("conduit_type", "EMT"),
                "conduit_size": data.get("conduit_size"),
                "length_ft": float(data.get("length_ft") or 50.0),
                "insulation": data.get("insulation", "THHN/THWN-2"),
                "ground_size": data.get("ground_size"),
                "notes": data.get("notes", "")
            }
            to_node.attributes = attrs

        # 2. Update or create EdgeRecord in equipment_edges table
        edge_rec = session.query(EdgeRecord).filter(
            (EdgeRecord.from_node_tag == from_tag) & (EdgeRecord.to_node_tag == to_tag)
        ).first()

        if not edge_rec:
            edge_rec = EdgeRecord(
                id=edge_id or f"edge_{from_tag}_{to_tag}",
                from_node_tag=from_tag,
                to_node_tag=to_tag,
                conductor_spec=data
            )
            session.add(edge_rec)
        else:
            edge_rec.conductor_spec = data

        session.commit()
        export_to_jsonl(client_id, facility_id)

    finally:
        session.close()

    # Return refreshed feeders list
    all_feeders = get_facility_feeders(client_id, facility_id)
    updated = next((f for f in all_feeders if f["from_tag"] == from_tag and f["to_tag"] == to_tag), None)
    return updated or (all_feeders[0] if all_feeders else {})
