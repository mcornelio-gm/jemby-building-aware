"""
IEEE 315 / ANSI Y32.2 Electrical Standard CAD Symbol Block Library
Constructs reusable parametric AutoCAD BLOCK definitions using ezdxf.
"""

from typing import Any, Dict
import ezdxf
from ezdxf.document import Drawing


def register_all_cad_symbols(doc: Drawing) -> None:
    """Register all IEEE 315 standard electrical symbols as AutoCAD BLOCKs in the DXF drawing."""
    blocks = doc.blocks

    # -------------------------------------------------------------
    # 1. Connection Junction Dot
    # -------------------------------------------------------------
    if "SYM_JUNCTION_DOT" not in blocks:
        blk = blocks.new(name="SYM_JUNCTION_DOT")
        blk.add_circle((0, 0), radius=1.0, dxfattribs={"layer": "E-ELEC-BUS"})
        # Hatch / solid fill (BYLAYER = 256 so it follows E-ELEC-BUS theme color)
        hatch = blk.add_hatch(color=256, dxfattribs={"layer": "E-ELEC-BUS"})
        hatch.paths.add_polyline_path([(-1.0, 0), (0, 1.0), (1.0, 0), (0, -1.0)], is_closed=True)

    # -------------------------------------------------------------
    # 2. Utility Grid Service Connection
    # -------------------------------------------------------------
    if "SYM_UTILITY_SOURCE" not in blocks:
        blk = blocks.new(name="SYM_UTILITY_SOURCE")
        # Tower / Grid Symbol: Central line and 3 horizontal rungs
        blk.add_line((0, 0), (0, 10), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-5, 10), (5, 10), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-3.5, 7), (3.5, 7), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-2, 4), (2, 4), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_text("UTILITY", dxfattribs={"layer": "E-ANNO-TEXT", "height": 2.2}).set_placement((0, 12), align=ezdxf.enums.TextEntityAlignment.BOTTOM_CENTER)

    # -------------------------------------------------------------
    # 3. Emergency Generator Source
    # -------------------------------------------------------------
    if "SYM_GENERATOR" not in blocks:
        blk = blocks.new(name="SYM_GENERATOR")
        blk.add_circle((0, 0), radius=6.0, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_text("G", dxfattribs={"layer": "E-ELEC-SYMB", "height": 5.0}).set_placement((0, 0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        # Terminal lead
        blk.add_line((0, -6), (0, -10), dxfattribs={"layer": "E-ELEC-FEED"})

    # -------------------------------------------------------------
    # 4. Solar PV Inverter / Array
    # -------------------------------------------------------------
    if "SYM_SOLAR_PV" not in blocks:
        blk = blocks.new(name="SYM_SOLAR_PV")
        # Inverter Box with diagonal slash (DC on left, AC on right)
        blk.add_lwpolyline([(-6, -6), (6, -6), (6, 6), (-6, 6)], close=True, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-6, -6), (6, 6), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_text("=", dxfattribs={"layer": "E-ELEC-SYMB", "height": 3.0}).set_placement((-3, 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        blk.add_text("~", dxfattribs={"layer": "E-ELEC-SYMB", "height": 3.5}).set_placement((3, -2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # -------------------------------------------------------------
    # 5. Battery Storage (BESS)
    # -------------------------------------------------------------
    if "SYM_BESS" not in blocks:
        blk = blocks.new(name="SYM_BESS")
        # Battery plate symbols: Long plate, short plate
        blk.add_line((-6, 3), (6, 3), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-3, 1), (3, 1), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-6, -1), (6, -1), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-3, -3), (3, -3), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((0, 6), (0, 3), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_line((0, -3), (0, -6), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_text("+", dxfattribs={"layer": "E-ANNO-TEXT", "height": 2.5}).set_placement((5, 4))
        blk.add_text("-", dxfattribs={"layer": "E-ANNO-TEXT", "height": 2.5}).set_placement((5, -4))

    # -------------------------------------------------------------
    # 6. IEEE 2-Winding Transformer (Delta-Wye / Two Circles)
    # -------------------------------------------------------------
    if "SYM_TRANSFORMER_2W" not in blocks:
        blk = blocks.new(name="SYM_TRANSFORMER_2W")
        # Top Circle (Primary)
        blk.add_circle((0, 4), radius=5.0, dxfattribs={"layer": "E-ELEC-SYMB"})
        # Bottom Circle (Secondary)
        blk.add_circle((0, -4), radius=5.0, dxfattribs={"layer": "E-ELEC-SYMB"})
        # Leads
        blk.add_line((0, 9), (0, 13), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_line((0, -9), (0, -13), dxfattribs={"layer": "E-ELEC-FEED"})
        # Delta & Wye notation
        blk.add_text("Δ", dxfattribs={"layer": "E-ANNO-TEXT", "height": 3.0}).set_placement((0, 4), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        blk.add_text("Y", dxfattribs={"layer": "E-ANNO-TEXT", "height": 3.0}).set_placement((0, -4), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # -------------------------------------------------------------
    # 7. Molded Case Circuit Breaker (MCCB)
    # -------------------------------------------------------------
    if "SYM_CB_MOLDED_CASE" not in blocks:
        blk = blocks.new(name="SYM_CB_MOLDED_CASE")
        # Square with diagonal cross
        blk.add_lwpolyline([(-3, -3), (3, -3), (3, 3), (-3, 3)], close=True, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-3, -3), (3, 3), dxfattribs={"layer": "E-ELEC-SYMB"})
        # Connection stabs
        blk.add_line((0, 3), (0, 6), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_line((0, -3), (0, -6), dxfattribs={"layer": "E-ELEC-FEED"})

    # -------------------------------------------------------------
    # 8. Drawout Power Circuit Breaker (LVPCB / MV)
    # -------------------------------------------------------------
    if "SYM_CB_DRAWOUT" not in blocks:
        blk = blocks.new(name="SYM_CB_DRAWOUT")
        # Central square
        blk.add_lwpolyline([(-3.5, -3.5), (3.5, -3.5), (3.5, 3.5), (-3.5, 3.5)], close=True, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-3.5, -3.5), (3.5, 3.5), dxfattribs={"layer": "E-ELEC-SYMB"})
        # Drawout disconnect arrows (upper and lower stabs)
        blk.add_line((0, 3.5), (0, 7.5), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_lwpolyline([(-2, 5.5), (0, 7.5), (2, 5.5)], dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((0, -3.5), (0, -7.5), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_lwpolyline([(-2, -5.5), (0, -7.5), (2, -5.5)], dxfattribs={"layer": "E-ELEC-SYMB"})

    # -------------------------------------------------------------
    # 9. Fused Disconnect Switch
    # -------------------------------------------------------------
    if "SYM_FUSED_DISCONNECT" not in blocks:
        blk = blocks.new(name="SYM_FUSED_DISCONNECT")
        # Blade switch (open angle)
        blk.add_circle((0, 5), radius=0.6, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_circle((0, 0), radius=0.6, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((0, 0), (3, 4.5), dxfattribs={"layer": "E-ELEC-SYMB"})
        # Fuse cartridge rectangle below switch
        blk.add_lwpolyline([(-1.8, -5), (1.8, -5), (1.8, -1), (-1.8, -1)], close=True, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((0, -5), (0, -1), dxfattribs={"layer": "E-ELEC-SYMB"})
        # Leads
        blk.add_line((0, 5), (0, 8), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_line((0, -5), (0, -8), dxfattribs={"layer": "E-ELEC-FEED"})

    # -------------------------------------------------------------
    # 10. Automatic Transfer Switch (ATS)
    # -------------------------------------------------------------
    if "SYM_ATS" not in blocks:
        blk = blocks.new(name="SYM_ATS")
        # Enclosure Box
        blk.add_lwpolyline([(-8, -6), (8, -6), (8, 6), (-8, 6)], close=True, dxfattribs={"layer": "E-ELEC-SYMB"})
        # Normal & Emergency input stabs
        blk.add_line((-4, 6), (-4, 9), dxfattribs={"layer": "E-ELEC-FEED"})
        blk.add_line((4, 6), (4, 9), dxfattribs={"layer": "E-ELEC-FEED"})
        # Output load stab
        blk.add_line((0, -6), (0, -9), dxfattribs={"layer": "E-ELEC-FEED"})
        # Selector blade & interlock line
        blk.add_line((-4, 2), (0, -2), dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_line((-4, 2), (4, 2), dxfattribs={"layer": "E-ELEC-SYMB", "linetype": "DASHED"})
        blk.add_text("N", dxfattribs={"layer": "E-ANNO-TEXT", "height": 2.0}).set_placement((-4, 3.5), align=ezdxf.enums.TextEntityAlignment.BOTTOM_CENTER)
        blk.add_text("E", dxfattribs={"layer": "E-ANNO-TEXT", "height": 2.0}).set_placement((4, 3.5), align=ezdxf.enums.TextEntityAlignment.BOTTOM_CENTER)
        blk.add_text("ATS", dxfattribs={"layer": "E-ANNO-TEXT", "height": 2.2}).set_placement((0, 0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # -------------------------------------------------------------
    # 11. Motor / Pump / Chiller Load
    # -------------------------------------------------------------
    if "SYM_MOTOR_LOAD" not in blocks:
        blk = blocks.new(name="SYM_MOTOR_LOAD")
        blk.add_circle((0, 0), radius=5.0, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_text("M", dxfattribs={"layer": "E-ELEC-SYMB", "height": 4.5}).set_placement((0, 0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        blk.add_line((0, 5), (0, 9), dxfattribs={"layer": "E-ELEC-FEED"})

    # -------------------------------------------------------------
    # 12. Power Meter / Monitoring
    # -------------------------------------------------------------
    if "SYM_POWER_METER" not in blocks:
        blk = blocks.new(name="SYM_POWER_METER")
        blk.add_circle((0, 0), radius=3.5, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_text("M", dxfattribs={"layer": "E-ELEC-SYMB", "height": 3.0}).set_placement((0, 0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # -------------------------------------------------------------
    # 13. Surge Protective Device (SPD / TVSS)
    # -------------------------------------------------------------
    if "SYM_SPD" not in blocks:
        blk = blocks.new(name="SYM_SPD")
        blk.add_lwpolyline([(-4, -3), (4, -3), (4, 3), (-4, 3)], close=True, dxfattribs={"layer": "E-ELEC-SYMB"})
        blk.add_text("SPD", dxfattribs={"layer": "E-ANNO-TEXT", "height": 2.0}).set_placement((0, 0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        blk.add_line((0, 3), (0, 6), dxfattribs={"layer": "E-ELEC-FEED"})

    # -------------------------------------------------------------
    # 14. Off-Page Continuation Reference Arrow
    # -------------------------------------------------------------
    if "SYM_OFFPAGE_REF" not in blocks:
        blk = blocks.new(name="SYM_OFFPAGE_REF")
        # Pointing downward / outgoing arrow flag: pentagon pointing down
        blk.add_lwpolyline([(-4, 4), (4, 4), (4, -2), (0, -7), (-4, -2)], close=True, dxfattribs={"layer": "E-ANNO-CABL"})
        blk.add_line((0, 4), (0, 8), dxfattribs={"layer": "E-ELEC-FEED"})

