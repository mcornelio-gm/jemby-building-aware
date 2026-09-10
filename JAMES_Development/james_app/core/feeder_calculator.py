"""
NEC Conductor Physics & Voltage Drop Engine for BuildingAware (JAMES).
Provides NEC 310.16 Ampacity lookups, Chapter 9 Table 8/9 AC Resistance & Reactance,
and exact 3-Phase / Single-Phase Percentage Voltage Drop calculations.
"""

import math
from typing import Dict, Any, Optional, Tuple, List


# -----------------------------------------------------------------------------
# NEC 310.16 Allowable Ampacities of Insulated Conductors (3 Current-Carrying in Raceway)
# -----------------------------------------------------------------------------
NEC_310_16_AMPACITY: Dict[str, Dict[str, Dict[int, int]]] = {
    "Cu": {
        "14 AWG": {60: 15, 75: 20, 90: 25},
        "12 AWG": {60: 20, 75: 25, 90: 30},
        "10 AWG": {60: 30, 75: 35, 90: 40},
        "8 AWG": {60: 40, 75: 50, 90: 55},
        "6 AWG": {60: 55, 75: 65, 90: 75},
        "4 AWG": {60: 70, 75: 85, 90: 95},
        "3 AWG": {60: 85, 75: 100, 90: 115},
        "2 AWG": {60: 95, 75: 115, 90: 130},
        "1 AWG": {60: 110, 75: 130, 90: 145},
        "1/0 AWG": {60: 125, 75: 150, 90: 170},
        "2/0 AWG": {60: 145, 75: 175, 90: 195},
        "3/0 AWG": {60: 165, 75: 200, 90: 225},
        "4/0 AWG": {60: 195, 75: 230, 90: 260},
        "250 kcmil": {60: 215, 75: 255, 90: 290},
        "300 kcmil": {60: 240, 75: 285, 90: 320},
        "350 kcmil": {60: 260, 75: 310, 90: 350},
        "400 kcmil": {60: 280, 75: 335, 90: 380},
        "500 kcmil": {60: 320, 75: 380, 90: 430},
        "600 kcmil": {60: 350, 75: 420, 90: 475},
        "750 kcmil": {60: 400, 75: 475, 90: 535},
        "1000 kcmil": {60: 455, 75: 545, 90: 615},
    },
    "Al": {
        "12 AWG": {60: 15, 75: 20, 90: 25},
        "10 AWG": {60: 25, 75: 30, 90: 35},
        "8 AWG": {60: 35, 75: 40, 90: 45},
        "6 AWG": {60: 40, 75: 50, 90: 60},
        "4 AWG": {60: 55, 75: 65, 90: 75},
        "3 AWG": {60: 65, 75: 75, 90: 85},
        "2 AWG": {60: 75, 75: 90, 90: 100},
        "1 AWG": {60: 85, 75: 100, 90: 115},
        "1/0 AWG": {60: 100, 75: 120, 90: 135},
        "2/0 AWG": {60: 115, 75: 135, 90: 150},
        "3/0 AWG": {60: 130, 75: 155, 90: 175},
        "4/0 AWG": {60: 150, 75: 180, 90: 205},
        "250 kcmil": {60: 170, 75: 205, 90: 230},
        "300 kcmil": {60: 195, 75: 230, 90: 260},
        "350 kcmil": {60: 210, 75: 250, 90: 280},
        "400 kcmil": {60: 225, 75: 270, 90: 305},
        "500 kcmil": {60: 260, 75: 310, 90: 350},
        "600 kcmil": {60: 285, 75: 340, 90: 385},
        "750 kcmil": {60: 320, 75: 385, 90: 435},
        "1000 kcmil": {60: 375, 75: 445, 90: 500},
    }
}

# Standard Conductor Ordering for Selection Dropdowns
STANDARD_GAUGES = [
    "14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG", "4 AWG", "3 AWG", "2 AWG", "1 AWG",
    "1/0 AWG", "2/0 AWG", "3/0 AWG", "4/0 AWG",
    "250 kcmil", "300 kcmil", "350 kcmil", "400 kcmil", "500 kcmil", "600 kcmil", "750 kcmil", "1000 kcmil"
]

# -----------------------------------------------------------------------------
# NEC Chapter 9 Table 9: AC Resistance (R) & Reactance (XL) at 60Hz, 75°C (Ohms / 1000 ft)
# -----------------------------------------------------------------------------
# Values formatted as: (R_pvc, R_aluminum, R_steel, XL_all)
NEC_CH9_TABLE_9_CU: Dict[str, Tuple[float, float, float, float]] = {
    "14 AWG": (3.10, 3.10, 3.10, 0.058),
    "12 AWG": (2.00, 2.00, 2.00, 0.054),
    "10 AWG": (1.20, 1.20, 1.20, 0.050),
    "8 AWG": (0.78, 0.78, 0.78, 0.052),
    "6 AWG": (0.49, 0.49, 0.49, 0.051),
    "4 AWG": (0.31, 0.31, 0.31, 0.048),
    "3 AWG": (0.25, 0.25, 0.25, 0.047),
    "2 AWG": (0.19, 0.20, 0.20, 0.045),
    "1 AWG": (0.15, 0.16, 0.16, 0.046),
    "1/0 AWG": (0.12, 0.13, 0.13, 0.044),
    "2/0 AWG": (0.10, 0.10, 0.10, 0.043),
    "3/0 AWG": (0.077, 0.082, 0.082, 0.042),
    "4/0 AWG": (0.062, 0.067, 0.067, 0.041),
    "250 kcmil": (0.054, 0.058, 0.057, 0.041),
    "300 kcmil": (0.045, 0.049, 0.049, 0.041),
    "350 kcmil": (0.039, 0.043, 0.043, 0.040),
    "400 kcmil": (0.035, 0.039, 0.039, 0.040),
    "500 kcmil": (0.029, 0.032, 0.032, 0.039),
    "600 kcmil": (0.025, 0.028, 0.028, 0.038),
    "750 kcmil": (0.021, 0.024, 0.024, 0.038),
    "1000 kcmil": (0.017, 0.019, 0.019, 0.037),
}

NEC_CH9_TABLE_9_AL: Dict[str, Tuple[float, float, float, float]] = {
    "12 AWG": (3.20, 3.20, 3.20, 0.054),
    "10 AWG": (2.00, 2.00, 2.00, 0.050),
    "8 AWG": (1.30, 1.30, 1.30, 0.052),
    "6 AWG": (0.81, 0.81, 0.81, 0.051),
    "4 AWG": (0.51, 0.51, 0.51, 0.048),
    "3 AWG": (0.40, 0.40, 0.40, 0.047),
    "2 AWG": (0.32, 0.32, 0.32, 0.045),
    "1 AWG": (0.25, 0.26, 0.26, 0.046),
    "1/0 AWG": (0.20, 0.21, 0.21, 0.044),
    "2/0 AWG": (0.16, 0.17, 0.17, 0.043),
    "3/0 AWG": (0.13, 0.13, 0.14, 0.042),
    "4/0 AWG": (0.10, 0.11, 0.11, 0.041),
    "250 kcmil": (0.086, 0.090, 0.090, 0.041),
    "300 kcmil": (0.072, 0.076, 0.076, 0.041),
    "350 kcmil": (0.063, 0.067, 0.067, 0.040),
    "400 kcmil": (0.056, 0.059, 0.060, 0.040),
    "500 kcmil": (0.046, 0.049, 0.050, 0.039),
    "600 kcmil": (0.039, 0.043, 0.043, 0.038),
    "750 kcmil": (0.033, 0.036, 0.037, 0.038),
    "1000 kcmil": (0.026, 0.029, 0.030, 0.037),
}

# Standard Recommended Equipment Grounding Conductor (NEC Table 250.122)
NEC_250_122_EGC: List[Tuple[int, str, str]] = [
    (15, "#14 AWG Cu", "#12 AWG Al"),
    (20, "#12 AWG Cu", "#10 AWG Al"),
    (60, "#10 AWG Cu", "#8 AWG Al"),
    (100, "#8 AWG Cu", "#6 AWG Al"),
    (200, "#6 AWG Cu", "#4 AWG Al"),
    (300, "#4 AWG Cu", "#2 AWG Al"),
    (400, "#3 AWG Cu", "#1 AWG Al"),
    (500, "#2 AWG Cu", "1/0 AWG Al"),
    (600, "#1 AWG Cu", "2/0 AWG Al"),
    (800, "1/0 AWG Cu", "3/0 AWG Al"),
    (1000, "2/0 AWG Cu", "4/0 AWG Al"),
    (1200, "3/0 AWG Cu", "250 kcmil Al"),
    (1600, "4/0 AWG Cu", "350 kcmil Al"),
    (2000, "250 kcmil Cu", "400 kcmil Al"),
    (2500, "350 kcmil Cu", "600 kcmil Al"),
    (3000, "400 kcmil Cu", "600 kcmil Al"),
    (4000, "500 kcmil Cu", "800 kcmil Al"),
]


def get_egc_size(rating_amps: float, material: str = "Cu") -> str:
    """Returns NEC Table 250.122 Equipment Grounding Conductor size for a given trip rating."""
    amps = float(rating_amps or 20)
    for max_amps, cu_size, al_size in NEC_250_122_EGC:
        if amps <= max_amps:
            return cu_size if material == "Cu" else al_size
    return "500 kcmil Cu" if material == "Cu" else "800 kcmil Al"


def get_conduit_ac_impedance(
    gauge: str,
    material: str = "Cu",
    conduit_type: str = "EMT"
) -> Tuple[float, float]:
    """
    Returns (Resistance R, Reactance X) per 1000 ft from NEC Ch 9 Table 9.
    conduit_type: 'PVC', 'Aluminum', 'Steel' / 'EMT' / 'RMC' / 'Tray'
    """
    table = NEC_CH9_TABLE_9_CU if material == "Cu" else NEC_CH9_TABLE_9_AL
    vals = table.get(gauge, table.get("4/0 AWG", (0.062, 0.067, 0.067, 0.041)))

    c_upper = str(conduit_type or "EMT").upper()
    if "PVC" in c_upper or "NON-MAGNETIC" in c_upper or "TRAY" in c_upper:
        r_val = vals[0]
    elif "ALUM" in c_upper:
        r_val = vals[1]
    else:  # Steel / EMT / RMC / IMC
        r_val = vals[2]

    xl_val = vals[3]
    return r_val, xl_val


def calculate_voltage_drop(
    voltage: float,
    current_amps: float,
    length_ft: float,
    conductor_size: str,
    material: str = "Cu",
    sets: int = 1,
    conduit_type: str = "EMT",
    power_factor: float = 0.85,
    is_three_phase: bool = True
) -> Dict[str, Any]:
    """
    Calculates exact AC voltage drop and percentage drop according to IEEE & NEC standards.
    
    Formula:
        V_drop (3-phase) = [sqrt(3) * I * L * (R*cos(theta) + X*sin(theta))] / (1000 * sets)
        V_drop (1-phase) = [2 * I * L * (R*cos(theta) + X*sin(theta))] / (1000 * sets)
        % V_drop = (V_drop / V_nominal) * 100
    """
    v_nom = max(float(voltage or 480.0), 1.0)
    i_load = max(float(current_amps or 1.0), 0.1)
    len_ft = max(float(length_ft or 50.0), 1.0)
    n_sets = max(int(sets or 1), 1)
    pf = max(min(float(power_factor or 0.85), 1.0), 0.1)
    sin_theta = math.sqrt(max(0.0, 1.0 - (pf ** 2)))

    r_val, x_val = get_conduit_ac_impedance(conductor_size, material, conduit_type)
    effective_z = (r_val * pf) + (x_val * sin_theta)

    phase_multiplier = math.sqrt(3) if is_three_phase else 2.0
    v_drop_volts = (phase_multiplier * i_load * len_ft * effective_z) / (1000.0 * n_sets)
    pct_drop = (v_drop_volts / v_nom) * 100.0

    # NEC Compliance Status
    if pct_drop <= 3.0:
        status = "COMPLIANT"
        status_color = "emerald"
        status_label = "Optimal (< 3%)"
    elif pct_drop <= 5.0:
        status = "ACCEPTABLE"
        status_color = "amber"
        status_label = "Acceptable (< 5%)"
    else:
        status = "EXCESSIVE"
        status_color = "rose"
        status_label = "Excessive (> 5%)"

    # Ampacity Rating (NEC 310.16 @ 75C)
    base_ampacity = NEC_310_16_AMPACITY.get(material, {}).get(conductor_size, {}).get(75, 100)
    total_ampacity = base_ampacity * n_sets

    return {
        "nominal_voltage": v_nom,
        "load_amperage": i_load,
        "length_ft": len_ft,
        "conductor_size": conductor_size,
        "material": material,
        "sets": n_sets,
        "conduit_type": conduit_type,
        "power_factor": pf,
        "is_three_phase": is_three_phase,
        "r_ohms_per_1000ft": r_val,
        "x_ohms_per_1000ft": x_val,
        "effective_z_ohms": round(effective_z, 5),
        "voltage_drop_volts": round(v_drop_volts, 2),
        "voltage_drop_pct": round(pct_drop, 2),
        "end_voltage": round(v_nom - v_drop_volts, 1),
        "status": status,
        "status_color": status_color,
        "status_label": status_label,
        "conductor_ampacity_75c": total_ampacity,
        "egc_recommended": get_egc_size(i_load, material)
    }


def suggest_feeder_conductors(
    amperage: float,
    voltage: float = 480.0,
    length_ft: float = 100.0,
    material: str = "Cu",
    max_voltage_drop_pct: float = 3.0,
    is_three_phase: bool = True
) -> Dict[str, Any]:
    """
    Suggests the optimal conductor gauge and number of parallel sets to satisfy both
    NEC 310.16 continuous thermal ampacity AND max voltage drop budget.
    """
    amps = max(float(amperage or 20.0), 10.0)
    target_ampacity = amps * 1.25  # Standard 125% continuous rating

    # 1. Determine sets & gauge for thermal rating
    table = NEC_310_16_AMPACITY.get(material, NEC_310_16_AMPACITY["Cu"])
    best_gauge = "12 AWG"
    best_sets = 1

    # Single conductor up to 400A if possible
    found = False
    for gauge in STANDARD_GAUGES:
        if table.get(gauge, {}).get(75, 0) >= target_ampacity:
            best_gauge = gauge
            best_sets = 1
            found = True
            break

    if not found:
        # Multi-set parallel feeder (e.g. 500 kcmil sets)
        for sets in range(2, 7):
            capacity_per_set = target_ampacity / sets
            for gauge in ["350 kcmil", "500 kcmil", "600 kcmil", "750 kcmil"]:
                if table.get(gauge, {}).get(75, 0) >= capacity_per_set:
                    best_gauge = gauge
                    best_sets = sets
                    found = True
                    break
            if found:
                break

    # 2. Verify voltage drop and upscale if necessary
    res = calculate_voltage_drop(
        voltage=voltage,
        current_amps=amps,
        length_ft=length_ft,
        conductor_size=best_gauge,
        material=material,
        sets=best_sets,
        is_three_phase=is_three_phase
    )

    while res["voltage_drop_pct"] > max_voltage_drop_pct:
        # Upsize gauge or add parallel set
        current_idx = STANDARD_GAUGES.index(best_gauge) if best_gauge in STANDARD_GAUGES else -1
        if current_idx >= 0 and current_idx < len(STANDARD_GAUGES) - 1 and best_sets == 1 and current_idx < 17:
            best_gauge = STANDARD_GAUGES[current_idx + 1]
        else:
            best_sets += 1
            if best_sets > 6:
                break
        res = calculate_voltage_drop(
            voltage=voltage,
            current_amps=amps,
            length_ft=length_ft,
            conductor_size=best_gauge,
            material=material,
            sets=best_sets,
            is_three_phase=is_three_phase
        )

    # Format human description
    ground = get_egc_size(amps, material)
    if best_sets == 1:
        run_desc = f"1x (3-{best_gauge} {material} + 1#{ground})"
    else:
        run_desc = f"{best_sets}x (3-{best_gauge} {material} + 1#{ground})"

    return {
        "conductor_size": best_gauge,
        "sets": best_sets,
        "material": material,
        "ground_size": ground,
        "run_description": run_desc,
        "calculation": res
    }
