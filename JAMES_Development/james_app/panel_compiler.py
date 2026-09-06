"""Graphviz DOT Compiler for Focused Panelboard Digital Twins."""

import html
from typing import Dict, List, Optional, Set
from james_app.panel_twin import BreakerObject, BreakerStatus, PanelTwin


def _escape(text: str) -> str:
    """Escape text for Graphviz HTML labels."""
    return html.escape(str(text))


def _format_left_cell(bkr: BreakerObject, slot_num: int) -> str:
    """Format HTML table cell content for the left column (odd circuits)."""
    slot_tag = ",".join(str(s) for s in bkr.occupied_slots)
    
    if bkr.status == BreakerStatus.SPARE:
        return f'<FONT COLOR="#744210">[SPARE] {bkr.description}</FONT>'
    elif bkr.status == BreakerStatus.SPACE:
        return f'<FONT COLOR="#94A3B8">[SPACE] Blank</FONT>'
    else:
        poles_str = f" ({bkr.poles}P {bkr.amps}A)" if bkr.poles > 1 else f" ({bkr.amps}A)"
        status_tag = f"[{bkr.status.value}] "
        return f'<B>{_escape(status_tag)}{_escape(slot_tag)}: {_escape(bkr.description)}{_escape(poles_str)}</B>'


def _format_right_cell(bkr: BreakerObject, slot_num: int) -> str:
    """Format HTML table cell content for the right column (even circuits)."""
    slot_tag = ",".join(str(s) for s in bkr.occupied_slots)
    
    if bkr.status == BreakerStatus.SPARE:
        return f'<FONT COLOR="#744210">[SPARE] {bkr.description}</FONT>'
    elif bkr.status == BreakerStatus.SPACE:
        return f'<FONT COLOR="#94A3B8">[SPACE] Blank</FONT>'
    else:
        poles_str = f" ({bkr.poles}P {bkr.amps}A)" if bkr.poles > 1 else f" ({bkr.amps}A)"
        status_tag = f" [{bkr.status.value}]"
        return f'<B>{_escape(bkr.description)}{_escape(poles_str)} :{_escape(slot_tag)}{_escape(status_tag)}</B>'


def compile_panel_to_dot(panel: PanelTwin) -> str:
    """Compile a PanelTwin object into standard Graphviz DOT syntax."""
    dot_lines = [
        "digraph PanelTwin {",
        '    graph [rankdir=TB, splines=polyline, nodesep=0.8, ranksep=0.8, fontname="Helvetica", bgcolor="transparent"];',
        '    node [shape=none, fontname="Helvetica", fontsize=9];',
        '    edge [dir=forward, arrowhead=vee, arrowsize=0.7, penwidth=1.2, color="#1E293B", fontname="Helvetica", fontsize=8];',
        ""
    ]

    total_rows = panel.total_spaces // 2
    
    # Map each slot number to its governing BreakerObject
    slot_to_bkr: Dict[int, BreakerObject] = {}
    for start_slot, bkr in panel.breakers.items():
        for s in bkr.occupied_slots:
            slot_to_bkr[s] = bkr

    # Track which slots have their load cell already rendered by a preceding ROWSPAN
    spanned_left_slots: Set[int] = set()
    spanned_right_slots: Set[int] = set()

    table_rows = []

    # 1. Main Header: Panel Name and Spaces
    table_rows.append(
        '            <TR>'
        f'<TD COLSPAN="4" BGCOLOR="#1A365D" PORT="main">'
        f'<FONT COLOR="WHITE" POINT-SIZE="11"><B>{_escape(panel.name.upper())} ({panel.total_spaces} SPACES)</B></FONT>'
        '</TD></TR>'
    )

    # 2. Subheader: Mains Rating and Voltage System
    sub_title = f"[ {panel.mains_rating_amps}A {panel.mains_type.value} - {panel.system_type.value} ]"
    table_rows.append(
        '            <TR>'
        f'<TD COLSPAN="4" BGCOLOR="#2A4365">'
        f'<FONT COLOR="WHITE" POINT-SIZE="9"><B>{_escape(sub_title)}</B></FONT>'
        '</TD></TR>'
    )

    # 3. Iterate rows (Row 1..total_rows)
    for row_idx in range(total_rows):
        left_slot = 2 * row_idx + 1   # 1, 3, 5, ...
        right_slot = 2 * row_idx + 2  # 2, 4, 6, ...

        left_bkr = slot_to_bkr.get(left_slot)
        right_bkr = slot_to_bkr.get(right_slot)

        row_tds = []

        # --- Left Column (Odd Circuit) ---
        if left_slot in spanned_left_slots:
            # Skip load cell because previous row used ROWSPAN
            pass
        elif left_bkr and left_bkr.slot_start == left_slot:
            rowspan_attr = f' ROWSPAN="{left_bkr.poles}"' if left_bkr.poles > 1 else ""
            port_id = f"ckt_{'_'.join(str(s) for s in left_bkr.occupied_slots)}"
            bg_attr = ' BGCOLOR="#FEFCBF"' if left_bkr.status == BreakerStatus.SPARE else ""
            cell_content = _format_left_cell(left_bkr, left_slot)
            row_tds.append(
                f'<TD ALIGN="LEFT"{rowspan_attr}{bg_attr} PORT="{port_id}">{cell_content}</TD>'
            )
            # Mark subsequent slots as spanned
            for s in left_bkr.occupied_slots[1:]:
                spanned_left_slots.add(s)
        else:
            # Fallback single spare cell
            row_tds.append(f'<TD ALIGN="LEFT" BGCOLOR="#FEFCBF" PORT="ckt_{left_slot}"><FONT COLOR="#744210">[SPARE] Unused :{left_slot}</FONT></TD>')

        # Numeric Slot: Left
        row_tds.append(f'<TD BGCOLOR="#E2E8F0"><B>{left_slot}</B></TD>')

        # Numeric Slot: Right
        row_tds.append(f'<TD BGCOLOR="#E2E8F0"><B>{right_slot}</B></TD>')

        # --- Right Column (Even Circuit) ---
        if right_slot in spanned_right_slots:
            # Skip load cell because previous row used ROWSPAN
            pass
        elif right_bkr and right_bkr.slot_start == right_slot:
            rowspan_attr = f' ROWSPAN="{right_bkr.poles}"' if right_bkr.poles > 1 else ""
            port_id = f"ckt_{'_'.join(str(s) for s in right_bkr.occupied_slots)}"
            bg_attr = ' BGCOLOR="#FEFCBF"' if right_bkr.status == BreakerStatus.SPARE else ""
            cell_content = _format_right_cell(right_bkr, right_slot)
            row_tds.append(
                f'<TD ALIGN="RIGHT"{rowspan_attr}{bg_attr} PORT="{port_id}">{cell_content}</TD>'
            )
            # Mark subsequent slots as spanned
            for s in right_bkr.occupied_slots[1:]:
                spanned_right_slots.add(s)
        else:
            # Fallback single spare cell
            row_tds.append(f'<TD ALIGN="RIGHT" BGCOLOR="#FEFCBF" PORT="ckt_{right_slot}"><FONT COLOR="#744210">[SPARE] Unused :{right_slot}</FONT></TD>')

        table_rows.append(f"            <TR>{''.join(row_tds)}</TR>")

    table_content = "\n".join(table_rows)
    table_label = (
        '<\n'
        '        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" COLOR="#1A365D" BGCOLOR="#FFFFFF">\n'
        f'{table_content}\n'
        '        </TABLE>\n'
        '    >'
    )

    dot_lines.append(f'    Panel_{panel.panel_id} [')
    dot_lines.append(f'        id="node_panel_{panel.panel_id}",')
    dot_lines.append(f'        label={table_label}')
    dot_lines.append('    ];\n')

    # 4. Optional Upstream Source Node and Feed Edge
    if panel.upstream_feed:
        feed = panel.upstream_feed
        dot_lines.append(f'    {feed.source_id} [')
        dot_lines.append(f'        shape=box, style="rounded,filled", fillcolor="#E2E8F0", color="#475569",')
        dot_lines.append(f'        label=<\n            <b>{_escape(feed.name)}</b><br/>\n            <font point-size="8" color="#64748B">({_escape(feed.voltage_label)})</font>\n        >')
        dot_lines.append('    ];\n')
        dot_lines.append(f'    {feed.source_id} -> Panel_{panel.panel_id}:main [label=" Service Feed "];\n')

    # 5. Optional Downstream Load Nodes and Branch Edges
    for start_slot, bkr in panel.breakers.items():
        if bkr.target_load_id and bkr.target_load_id in panel.downstream_loads:
            load = panel.downstream_loads[bkr.target_load_id]
            port_id = f"ckt_{'_'.join(str(s) for s in bkr.occupied_slots)}"
            
            dot_lines.append(f'    Load_{load.load_id} [')
            dot_lines.append(f'        shape=box, style="rounded,filled", fillcolor="#E2E8F0", color="#475569",')
            dot_lines.append(f'        label=<\n            <b>{_escape(load.name)}</b><br/>\n            <font point-size="8" color="#64748B">({_escape(load.rating_label)})</font>\n        >')
            dot_lines.append('    ];\n')

            edge_label = f" {bkr.amps}A Cir {start_slot} " if bkr.poles == 1 else f" {bkr.amps}A Cir {start_slot}/{start_slot+2} "
            dot_lines.append(f'    Panel_{panel.panel_id}:{port_id} -> Load_{load.load_id} [label="{_escape(edge_label)}"];\n')

    dot_lines.append("}\n")
    return "\n".join(dot_lines)
