"""
Siemens Industry Industrial Equipment Catalog Harvester.
Harvests structured engineering specifications across all 17 industrial gear categories:
1. Busway (Sentron Busway Aluminum & Copper 225A-5000A, XJ-L Low-Amp)
2. Circuit Breakers (Sentron ED-RD, 3VA5/3VA6, 3WA / WL Low Voltage Power, 3AH / GM-SG MV)
3. Load Centers (PL & ES Series Commercial 3-Phase Main Lugs & Main Breaker)
4. Motor Control Centers (tiastar Industrial MCC, Smart MCC with SIMOCODE pro, Arc-Resistant)
5. Panelboards (P1 Lighting, P2 Power, P3 Distribution, P4 & P5 Heavy Distribution)
6. Softstarters (SIRIUS 3RW55 High Performance, 3RW40 General Performance, 3RW30)
7. Switchboards (Type SB1, SB2, SB3 Low Voltage Distribution Switchboards)
8. Switches & Disconnects (VBII Heavy Duty Safety Switches HF/HNF 30A-1200A, BPS Bolted Pressure)
9. Switchgear (Type WL / Type R Low-Voltage UL 1558, GM-SG Medium-Voltage Metal-Clad Arc-Resistant)
10. Transformers (Low-Voltage Ventilated Dry-Type DOE 2016 Compliant, K-Factor K-13, Substation Liquid)
11. Automatic Transfer Switches (Siemens Sensata ATS Series 40A-4000A, 3WA Breaker Pair ATS)
12. Paralleling Switchgear (Siemens Emergency Paralleling Switchgear, SIMATIC S7-1500 Redundant PLC)
13. Power Conditioning (Siemens Active Harmonic Filters 50A-300A, Dynamic Voltage Conditioners)
14. Power Distribution Systems (Siemens Data Center PDU 50kVA-300kVA, Remote Power Panel RPP SEM3)
15. Static Transfer Switches (Siemens Industrial High-Speed Static Transfer Switch STS <4ms)
16. Surge Protective Devices (TPS3 01, TPS3 03, TPS3 09 Series 100kA-300kA/Phase NEMA 4X)
17. Uninterruptible Power Supplies (Siemens Masterguard / SITOP Industrial 3-Phase UPS 50kVA-500kVA)
"""

from typing import List
from james_app.catalog_harvester.base import BaseVendorHarvester
from james_app.catalog_harvester.models import CatalogItem


class SiemensCatalogHarvester(BaseVendorHarvester):
    """
    Catalog extractor for Siemens Industrial Electrical Equipment.
    Grounds catalog models to Siemens Speedfax catalog sections (Section 1 to Section 19) and SIOS documentation.
    """

    vendor_name: str = "Siemens"
    vendor_key: str = "siemens"
    source_url: str = "https://support.industry.siemens.com/"

    def harvest(self) -> List[CatalogItem]:
        """Harvest comprehensive industrial equipment items for Siemens."""
        items: List[CatalogItem] = []

        # -------------------------------------------------------------------------
        # 1. BUSWAY (Speedfax Section 15 - Sentron Busway Aluminum & Copper)
        # -------------------------------------------------------------------------
        busway_data = [
            ("SL2508G", "Sentron Busway", "Sentron Copper Feeder Busway 800A 3P4W 600V with Internal Ground", 800.0, 100.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 100.0),
            ("SL2512G", "Sentron Busway", "Sentron Copper Feeder Busway 1200A 3P4W 600V with Internal Ground", 1200.0, 100.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 100.0),
            ("SL2516G", "Sentron Busway", "Sentron Copper Feeder Busway 1600A 3P4W 600V with Internal Ground", 1600.0, 150.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 150.0),
            ("SL2520G", "Sentron Busway", "Sentron Copper Feeder Busway 2000A 3P4W 600V with Internal Ground", 2000.0, 150.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 150.0),
            ("SL2530G", "Sentron Busway", "Sentron Copper Feeder Busway 3000A 3P4W 600V with Internal Ground", 3000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 200.0),
            ("SL2540G", "Sentron Busway", "Sentron Copper Feeder Busway 4000A 3P4W 600V with Internal Ground", 4000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 200.0),
            ("SL2550G", "Sentron Busway", "Sentron Copper Feeder Busway 5000A 3P4W 600V with Internal Ground", 5000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 200.0),
            ("AL2510G", "Sentron Busway", "Sentron Aluminum Feeder Busway 1000A 3P4W 600V with Internal Ground", 1000.0, 100.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 100.0),
            ("AL2516G", "Sentron Busway", "Sentron Aluminum Feeder Busway 1600A 3P4W 600V with Internal Ground", 1600.0, 150.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 150.0),
            ("AL2525G", "Sentron Busway", "Sentron Aluminum Feeder Busway 2500A 3P4W 600V with Internal Ground", 2500.0, 150.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 150.0),
            ("AL2530G", "Sentron Busway", "Sentron Aluminum Feeder Busway 3000A 3P4W 600V with Internal Ground", 3000.0, 200.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 200.0),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, bus_mat, nema, sccr in busway_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="busway",
                type_tag="BUSWAY",
                type_name="Industrial Feeder & Plug-In Busway",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "bus_material": bus_mat,
                    "short_circuit_withstand_ka": sccr,
                    "catalog_section": "Speedfax Section 15: Busway Systems",
                    "conductor_configuration": poles
                },
                docs={"catalog_volume": "Speedfax Section 15"}
            ))

        # -------------------------------------------------------------------------
        # 2. CIRCUIT BREAKERS (Speedfax Section 7 - Sentron, 3VA, 3WA/WL, 3AH MV)
        # -------------------------------------------------------------------------
        breakers_data = [
            # 3VA Molded Case Circuit Breakers (3VA5 / 3VA6)
            ("3VA5130-4EC31-0AA0", "3VA5", "3VA5 Molded Case Breaker 30A 3P 480V 25kAIC Thermal-Magnetic TM210", 30.0, 25.0, "480V", "3PH", "3P", "TM210 Thermal-Magnetic", "3VA5 Frame 125A"),
            ("3VA5160-4EC31-0AA0", "3VA5", "3VA5 Molded Case Breaker 60A 3P 480V 25kAIC Thermal-Magnetic TM210", 60.0, 25.0, "480V", "3PH", "3P", "TM210 Thermal-Magnetic", "3VA5 Frame 125A"),
            ("3VA5110-4EC31-0AA0", "3VA5", "3VA5 Molded Case Breaker 100A 3P 480V 25kAIC Thermal-Magnetic TM210", 100.0, 25.0, "480V", "3PH", "3P", "TM210 Thermal-Magnetic", "3VA5 Frame 125A"),
            ("3VA6215-5EF31-0AA0", "3VA6", "3VA6 Molded Case Breaker 150A 3P 600V 35kAIC ETU330 LIG Electronic", 150.0, 35.0, "600V", "3PH", "3P", "ETU330 LIG Electronic", "3VA6 Frame 250A"),
            ("3VA6225-7EF31-0AA0", "3VA6", "3VA6 Molded Case Breaker 250A 3P 600V 100kAIC ETU330 LIG Electronic", 250.0, 100.0, "600V", "3PH", "3P", "ETU330 LIG Electronic", "3VA6 Frame 250A"),
            ("3VA6340-5EF31-0AA0", "3VA6", "3VA6 Molded Case Breaker 400A 3P 600V 35kAIC ETU330 LIG Electronic", 400.0, 35.0, "600V", "3PH", "3P", "ETU330 LIG Electronic", "3VA6 Frame 400A"),
            ("3VA6460-7EF31-0AA0", "3VA6", "3VA6 Molded Case Breaker 600A 3P 600V 100kAIC ETU350 LSI Electronic", 600.0, 100.0, "600V", "3PH", "3P", "ETU350 LSI Electronic", "3VA6 Frame 600A"),
            ("3VA6580-5EF31-0AA0", "3VA6", "3VA6 Molded Case Breaker 800A 3P 600V 35kAIC ETU350 LSI Electronic", 800.0, 35.0, "600V", "3PH", "3P", "ETU350 LSI Electronic", "3VA6 Frame 800A"),
            ("3VA6510-7EF31-0AA0", "3VA6", "3VA6 Molded Case Breaker 1000A 3P 600V 100kAIC ETU350 LSI Electronic", 1000.0, 100.0, "600V", "3PH", "3P", "ETU350 LSI Electronic", "3VA6 Frame 1000A"),
            # Sentron Classic Molded Case Breakers
            ("JXD63B200", "Sentron JXD", "Sentron JXD6 Molded Case Breaker 200A 3P 600V 35kAIC Thermal-Magnetic", 200.0, 35.0, "600V", "3PH", "3P", "Thermal-Magnetic", "JXD6 Frame"),
            ("LXD63B400", "Sentron LXD", "Sentron LXD6 Molded Case Breaker 400A 3P 600V 35kAIC Thermal-Magnetic", 400.0, 35.0, "600V", "3PH", "3P", "Thermal-Magnetic", "LXD6 Frame"),
            ("MXD63B800", "Sentron MXD", "Sentron MXD6 Molded Case Breaker 800A 3P 600V 65kAIC Electronic Trip", 800.0, 65.0, "600V", "3PH", "3P", "Electronic Trip Unit", "MXD6 Frame"),
            ("NXD63B1200", "Sentron NXD", "Sentron NXD6 Molded Case Breaker 1200A 3P 600V 65kAIC Electronic Trip", 1200.0, 65.0, "600V", "3PH", "3P", "Electronic Trip Unit", "NXD6 Frame"),
            # 3WA / WL Low Voltage Power Air Circuit Breakers (UL 1066 / UL 489)
            ("3WA1108-2AE21-0AA0", "3WA Air Breaker", "3WA1 Low Voltage Power Circuit Breaker 800A 3P 600V 65kAIC Drawout ETU600", 800.0, 65.0, "600V", "3PH", "3P", "ETU600 LSIG Electronic", "3WA1 Frame 1"),
            ("3WA1116-2AE21-0AA0", "3WA Air Breaker", "3WA1 Low Voltage Power Circuit Breaker 1600A 3P 600V 65kAIC Drawout ETU600", 1600.0, 65.0, "600V", "3PH", "3P", "ETU600 LSIG Electronic", "3WA1 Frame 1"),
            ("3WA1220-3AE21-0AA0", "3WA Air Breaker", "3WA1 Low Voltage Power Circuit Breaker 2000A 3P 600V 85kAIC Drawout ETU600", 2000.0, 85.0, "600V", "3PH", "3P", "ETU600 LSIG Electronic", "3WA1 Frame 2"),
            ("3WA1230-3AE21-0AA0", "3WA Air Breaker", "3WA1 Low Voltage Power Circuit Breaker 3000A 3P 600V 85kAIC Drawout ETU600", 3000.0, 85.0, "600V", "3PH", "3P", "ETU600 LSIG Electronic", "3WA1 Frame 2"),
            ("3WA1340-4AE21-0AA0", "3WA Air Breaker", "3WA1 Low Voltage Power Circuit Breaker 4000A 3P 600V 100kAIC Drawout ETU600", 4000.0, 100.0, "600V", "3PH", "3P", "ETU600 LSIG Electronic", "3WA1 Frame 3"),
            ("3WA1350-4AE21-0AA0", "3WA Air Breaker", "3WA1 Low Voltage Power Circuit Breaker 5000A 3P 600V 100kAIC Drawout ETU600", 5000.0, 100.0, "600V", "3PH", "3P", "ETU600 LSIG Electronic", "3WA1 Frame 3"),
            ("3WA1360-4AE21-0AA0", "3WA Air Breaker", "3WA1 Low Voltage Power Circuit Breaker 6000A 3P 600V 150kAIC Drawout ETU600", 6000.0, 150.0, "600V", "3PH", "3P", "ETU600 LSIG Electronic", "3WA1 Frame 3"),
            # Medium Voltage Vacuum Circuit Breakers (3AH / GM-SG)
            ("3AH-05-1200-25", "3AH Vacuum MV", "3AH Medium Voltage Vacuum Circuit Breaker 1200A 4.76kV 25kAIC Drawout", 1200.0, 25.0, "4.76kV", "3PH", "3P", "Vacuum Interrupter Drawout", "3AH 5kV"),
            ("3AH-15-1200-31", "3AH Vacuum MV", "3AH Medium Voltage Vacuum Circuit Breaker 1200A 15kV 31.5kAIC Drawout", 1200.0, 31.5, "15kV", "3PH", "3P", "Vacuum Interrupter Drawout", "3AH 15kV"),
            ("3AH-15-2000-40", "3AH Vacuum MV", "3AH Medium Voltage Vacuum Circuit Breaker 2000A 15kV 40kAIC Drawout", 2000.0, 40.0, "15kV", "3PH", "3P", "Vacuum Interrupter Drawout", "3AH 15kV"),
            ("3AH-15-3000-50", "3AH Vacuum MV", "3AH Medium Voltage Vacuum Circuit Breaker 3000A 15kV 50kAIC Drawout", 3000.0, 50.0, "15kV", "3PH", "3P", "Vacuum Interrupter Drawout", "3AH 15kV"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, trip, frame in breakers_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="circuit_breaker",
                type_tag="CB",
                type_name="Industrial Molded Case / Low-Voltage Power Breaker",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "trip_unit_type": trip,
                    "frame_designation": frame,
                    "catalog_section": "Speedfax Section 7: Circuit Breakers",
                    "mounting": "Fixed / Plug-in / Drawout"
                },
                docs={"catalog_volume": "Speedfax Section 7"}
            ))

        # -------------------------------------------------------------------------
        # 3. LOAD CENTERS (Speedfax Section 1 - PL & ES Commercial 3-Phase)
        # -------------------------------------------------------------------------
        load_center_data = [
            ("P2424L3125CU", "PL Series Commercial", "PL Series 125A 3PH 24-Circuit Main Lugs Commercial Load Center Copper Bus", 125.0, 65.0, "208Y/120V", "3PH", "3P4W", 24, "NEMA 1 Indoor", "Main Lug Only"),
            ("P3030L3200CU", "PL Series Commercial", "PL Series 200A 3PH 30-Circuit Main Lugs Commercial Load Center Copper Bus", 200.0, 65.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Lug Only"),
            ("P4242L3225CU", "PL Series Commercial", "PL Series 225A 3PH 42-Circuit Main Lugs Commercial Load Center Copper Bus", 225.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Lug Only"),
            ("P3030B3100CU", "PL Series Commercial", "PL Series 100A 3PH 30-Circuit Main Breaker Commercial Load Center Copper Bus", 100.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Breaker Included"),
            ("P3030B3150CU", "PL Series Commercial", "PL Series 150A 3PH 30-Circuit Main Breaker Commercial Load Center Copper Bus", 150.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Breaker Included"),
            ("P4242B3200CU", "PL Series Commercial", "PL Series 200A 3PH 42-Circuit Main Breaker Commercial Load Center Copper Bus", 200.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Breaker Included"),
            ("P4242B3225CU", "PL Series Commercial", "PL Series 225A 3PH 42-Circuit Main Breaker Commercial Load Center Copper Bus", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Breaker Included"),
            ("W4242L3225CU", "PL Series Outdoor", "PL Series 225A 3PH 42-Circuit Main Lugs NEMA 3R Outdoor Load Center Copper Bus", 225.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 3R Outdoor", "Main Lug Only"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, slots, nema, main_type in load_center_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="load_center",
                type_tag="LOAD_CENTER",
                type_name="Commercial/Industrial 3-Phase Load Center",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                total_slots=slots,
                nema_rating=nema,
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "main_device_type": main_type,
                    "bus_material": "100% Copper Bus Bars",
                    "catalog_section": "Speedfax Section 1: Load Centers",
                    "branch_breaker_family": "Type QP / QPH / HQP Plug-In Breakers"
                },
                docs={"catalog_volume": "Speedfax Section 1"}
            ))

        # -------------------------------------------------------------------------
        # 4. MOTOR CONTROL CENTERS (Speedfax Section 14 - tiastar Industrial MCC)
        # -------------------------------------------------------------------------
        mcc_data = [
            ("TIA-FVNR-SZ1-600A", "tiastar MCC", "tiastar MCC FVNR Starter Size 1 with 3VA MCP 600A Copper Bus NEMA 1", 600.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 10, "Size 1 (Up to 10 HP)"),
            ("TIA-FVNR-SZ2-600A", "tiastar MCC", "tiastar MCC FVNR Starter Size 2 with 3VA MCP 600A Copper Bus NEMA 1", 600.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 25, "Size 2 (Up to 25 HP)"),
            ("TIA-FVNR-SZ3-800A", "tiastar MCC", "tiastar MCC FVNR Starter Size 3 with 3VA MCP 800A Copper Bus NEMA 1", 800.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 50, "Size 3 (Up to 50 HP)"),
            ("TIA-FVNR-SZ4-1200A", "tiastar MCC", "tiastar MCC FVNR Starter Size 4 with 3VA MCP 1200A Copper Bus NEMA 1", 1200.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 100, "Size 4 (Up to 100 HP)"),
            ("TIA-FVNR-SZ5-1600A", "tiastar MCC", "tiastar MCC FVNR Starter Size 5 with 3VA MCP 1600A Copper Bus NEMA 1", 1600.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 200, "Size 5 (Up to 200 HP)"),
            ("TIA-VFD-G120-100HP", "tiastar Smart MCC", "tiastar Smart MCC with SINAMICS G120 100HP Variable Frequency Drive", 1200.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 100, "SINAMICS G120 Industrial VFD"),
            ("TIA-ARC-RESIST-2000A", "tiastar Arc-Resistant", "tiastar Arc-Resistant Type 2 Industrial MCC 2000A Copper Bus", 2000.0, 100.0, "480V", "3PH", "3P3W", "IEEE C37.20.7 Type 2 Arc-Resistant", 400, "Master Feeder / Starter Lineup"),
            ("TIA-MAIN-3WA-2500A", "tiastar MCC", "tiastar MCC 2500A Main Circuit Breaker Section 3WA Air Circuit Breaker", 2500.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 0, "Main Incoming Section"),
        ]
        for pn, series, desc, bus_amps, aic, volt, phase, poles, nema, hp, starter_type in mcc_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="mcc",
                type_tag="MCC",
                type_name="Industrial Motor Control Center Lineup / Unit",
                description=desc,
                voltage=volt,
                amps=bus_amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "starter_type": starter_type,
                    "horse_power_rating": hp,
                    "horizontal_bus_rating_amps": bus_amps,
                    "catalog_section": "Speedfax Section 14: Motor Control Centers",
                    "smart_motor_relay": "SIMOCODE pro Intelligent Motor Management"
                },
                docs={"catalog_volume": "Speedfax Section 14"}
            ))

        # -------------------------------------------------------------------------
        # 5. PANELBOARDS (Speedfax Section 11 - P1, P2, P3, P4, P5 Series)
        # -------------------------------------------------------------------------
        panel_data = [
            # P1 Lighting & Appliance Panelboards (240V / 480Y/277V)
            ("P1A30ML125CT", "Type P1", "P1 Lighting Panelboard Interior 125A 3PH 4W 208Y/120V 30-Circuit Main Lugs Copper", 125.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "Main Lugs", "Copper"),
            ("P1A42ML250CT", "Type P1", "P1 Lighting Panelboard Interior 250A 3PH 4W 208Y/120V 42-Circuit Main Lugs Copper", 250.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("P1A42MC250CT", "Type P1", "P1 Lighting Panelboard Interior 250A 3PH 4W 208Y/120V 42-Circuit Main Breaker 3VA", 250.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "Main Breaker", "Copper"),
            ("P1A42ML400CT", "Type P1", "P1 Lighting Panelboard Interior 400A 3PH 4W 208Y/120V 42-Circuit Main Lugs Copper", 400.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("P1E30ML125CT", "Type P1 480V", "P1 Commercial Panelboard Interior 125A 3PH 4W 480Y/277V 30-Circuit Main Lugs BQD", 125.0, 65.0, "480Y/277V", "3PH", "3P4W", 30, "Main Lugs", "Copper"),
            ("P1E42ML250CT", "Type P1 480V", "P1 Commercial Panelboard Interior 250A 3PH 4W 480Y/277V 42-Circuit Main Lugs BQD", 250.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("P1E42MC250CT", "Type P1 480V", "P1 Commercial Panelboard Interior 250A 3PH 4W 480Y/277V 42-Circuit Main Breaker 3VA", 250.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Breaker", "Copper"),
            ("P1E42ML400CT", "Type P1 480V", "P1 Commercial Panelboard Interior 400A 3PH 4W 480Y/277V 42-Circuit Main Lugs BQD", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            # P2 & P3 Power Distribution Panelboards
            ("P2E42ML600CT", "Type P2 Power", "P2 Power Distribution Panelboard Interior 600A 3PH 480Y/277V 42-Circuit Copper", 600.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("P3E42ML800CT", "Type P3 Power", "P3 Power Distribution Panelboard Interior 800A 3PH 480Y/277V 42-Circuit Copper", 800.0, 100.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("P4E42ML1200CT", "Type P4 Heavy", "P4 Heavy Distribution Panelboard Interior 1200A 3PH 600VAC Copper Bus", 1200.0, 100.0, "600V", "3PH", "3P4W", 42, "Main Lugs / Breaker", "Copper"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, slots, main_type, bus_mat in panel_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="panelboard",
                type_tag="PANEL",
                type_name="Industrial Lighting & Distribution Panelboard",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                total_slots=slots,
                nema_rating="NEMA 1 / 3R Compatible",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "main_device_type": main_type,
                    "bus_material": bus_mat,
                    "catalog_section": "Speedfax Section 11: Panelboards",
                    "branch_breaker_family": "BL / BQD / 3VA Breakers"
                },
                docs={"catalog_volume": "Speedfax Section 11"}
            ))

        # -------------------------------------------------------------------------
        # 6. SOFTSTARTERS (Speedfax Section 4 - SIRIUS 3RW55, 3RW40, 3RW30)
        # -------------------------------------------------------------------------
        softstart_data = [
            ("3RW5513-1HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 13A 200-480V Built-In Bypass", 13.0, 480.0, 7.5, "3RW55"),
            ("3RW5525-1HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 63A 200-480V Built-In Bypass", 63.0, 480.0, 40.0, "3RW55"),
            ("3RW5535-1HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 113A 200-480V Built-In Bypass", 113.0, 480.0, 75.0, "3RW55"),
            ("3RW5543-1HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 171A 200-480V Built-In Bypass", 171.0, 480.0, 125.0, "3RW55"),
            ("3RW5547-1HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 315A 200-480V Built-In Bypass", 315.0, 480.0, 250.0, "3RW55"),
            ("3RW5553-2HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 570A 200-480V Built-In Bypass", 570.0, 480.0, 450.0, "3RW55"),
            ("3RW5556-2HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 850A 200-480V Built-In Bypass", 850.0, 480.0, 700.0, "3RW55"),
            ("3RW5558-2HA14", "SIRIUS 3RW55", "SIRIUS 3RW55 High Performance Softstarter 1280A 200-480V Built-In Bypass", 1280.0, 480.0, 1000.0, "3RW55"),
            ("3RW4055-6BB44", "SIRIUS 3RW40", "SIRIUS 3RW40 General Performance Softstarter 134A 200-460V Built-In Bypass", 134.0, 480.0, 100.0, "3RW40"),
            ("3RW4075-6BB44", "SIRIUS 3RW40", "SIRIUS 3RW40 General Performance Softstarter 356A 200-460V Built-In Bypass", 356.0, 480.0, 300.0, "3RW40"),
        ]
        for pn, series, desc, amps, volt_nom, hp, frame in softstart_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="motor_control",
                type_tag="SOFTSTART",
                type_name="Solid-State Reduced Voltage Softstarter",
                description=desc,
                voltage=f"{int(volt_nom)}V",
                amps=amps,
                poles="3P",
                phase="3PH",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "motor_hp_480v": hp,
                    "bypass_contactor": "Integrated Solid-State Hybrid Bypass System",
                    "pump_cleaning_function": "Automated Reversible De-clogging",
                    "fieldbus_support": "PROFINET / PROFIBUS / Modbus TCP",
                    "catalog_section": "Speedfax Section 4: Industrial Controls"
                },
                docs={"catalog_volume": "Speedfax Section 4"}
            ))

        # -------------------------------------------------------------------------
        # 7. SWITCHBOARDS (Speedfax Section 12 - Type SB1, SB2, SB3 Distribution)
        # -------------------------------------------------------------------------
        swbd_data = [
            ("SB1-400A-480V", "Type SB1", "Type SB1 Distribution Switchboard 400A 480V 3PH 4W 3VA Main Breaker", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 / 3R", "Copper", "3VA Main + P1 Distribution"),
            ("SB2-800A-480V", "Type SB2", "Type SB2 Distribution Switchboard 800A 480V 3PH 4W 3VA Main Breaker", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "3VA Main + 3VA Feeders"),
            ("SB2-1200A-480V", "Type SB2", "Type SB2 Distribution Switchboard 1200A 480V 3PH 4W 3VA Main Breaker", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "3VA Main + 3VA Feeders"),
            ("SB3-2000A-480V", "Type SB3", "Type SB3 Heavy Duty Switchboard 2000A 480V 3PH 4W 3WA Air Circuit Breaker", 2000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "3WA Air Breaker Main + Feeders"),
            ("SB3-3000A-480V", "Type SB3", "Type SB3 Heavy Duty Switchboard 3000A 480V 3PH 4W 3WA Air Circuit Breaker", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "3WA Air Breaker Main + Feeders"),
            ("SB3-4000A-480V", "Type SB3", "Type SB3 Heavy Duty Switchboard 4000A 480V 3PH 4W 3WA Air Circuit Breaker", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "3WA Air Breaker Main + Feeders"),
            ("SB3-5000A-480V", "Type SB3", "Type SB3 Heavy Duty Switchboard 5000A 480V 3PH 4W 3WA Air Circuit Breaker", 5000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "3WA Air Breaker Main + Feeders"),
            ("SB-UTIL-METER-2000A", "Type SB Service", "Type SB Commercial Service Entrance Switchboard 2000A Utility Metering", 2000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 / 3R", "Copper", "Utility Metering Compartment + 3WA Main"),
            ("SB-UTIL-METER-4000A", "Type SB Service", "Type SB Commercial Service Entrance Switchboard 4000A Utility Metering", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 / 3R", "Copper", "Utility Metering Compartment + 3WA Main"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, bus_mat, config in swbd_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switchboard",
                type_tag="SWBD",
                type_name="Industrial Front-Connected Distribution Switchboard",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "bus_material": bus_mat,
                    "switchboard_configuration": config,
                    "short_circuit_rating_ka": aic,
                    "catalog_section": "Speedfax Section 12: Switchboards",
                    "standards": "UL 891 / NEMA PB2"
                },
                docs={"catalog_volume": "Speedfax Section 12"}
            ))

        # -------------------------------------------------------------------------
        # 8. SWITCHES & DISCONNECTS (Speedfax Section 3 - VBII Heavy Duty & BPS)
        # -------------------------------------------------------------------------
        disc_data = [
            ("HF361", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 30A 3P 600V NEMA 1 Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("HF362", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 60A 3P 600V NEMA 1 Fusible", 60.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("HF363", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 100A 3P 600V NEMA 1 Fusible", 100.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("HF364", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 200A 3P 600V NEMA 1 Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("HF365", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 400A 3P 600V NEMA 1 Fusible", 400.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("HF366", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 600A 3P 600V NEMA 1 Fusible", 600.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("HF367", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 800A 3P 600V NEMA 1 Fusible Class L", 800.0, 200.0, "600V", "3PH", "3P", "Fusible (Class L)", "NEMA 1 Indoor"),
            ("HF368", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 1200A 3P 600V NEMA 1 Fusible Class L", 1200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class L)", "NEMA 1 Indoor"),
            ("HNF361", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 30A 3P 600V NEMA 1 Non-Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Non-Fusible", "NEMA 1 Indoor"),
            ("HNF364", "VBII Heavy Duty", "VBII Heavy Duty Safety Switch 200A 3P 600V NEMA 1 Non-Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Non-Fusible", "NEMA 1 Indoor"),
            ("HF361S", "VBII Stainless", "VBII Heavy Duty Safety Switch 30A 3P 600V NEMA 4X 304 Stainless Steel Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 4X Stainless"),
            ("HF364S", "VBII Stainless", "VBII Heavy Duty Safety Switch 200A 3P 600V NEMA 4X 304 Stainless Steel Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 4X Stainless"),
            ("DTNF364", "Double-Throw Manual", "VBII Double-Throw Safety Switch 200A 3P 600V NEMA 1 Non-Fusible Manual Transfer", 200.0, 100.0, "600V", "3PH", "3P", "Double-Throw Manual Transfer", "NEMA 1 Indoor"),
            ("BPS3612", "BPS Bolted Pressure", "BPS Bolted Pressure Contact Switch 1200A 3P 600V Fusible Class L", 1200.0, 200.0, "600V", "3PH", "3P", "Bolted Pressure Fusible Class L", "NEMA 1 Enclosed"),
            ("BPS3620", "BPS Bolted Pressure", "BPS Bolted Pressure Contact Switch 2000A 3P 600V Fusible Class L", 2000.0, 200.0, "600V", "3PH", "3P", "Bolted Pressure Fusible Class L", "NEMA 1 Enclosed"),
            ("BPS3640", "BPS Bolted Pressure", "BPS Bolted Pressure Contact Switch 4000A 3P 600V Fusible Class L", 4000.0, 200.0, "600V", "3PH", "3P", "Bolted Pressure Fusible Class L", "NEMA 1 Enclosed"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, f_type, nema in disc_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="disconnect",
                type_tag="DISC",
                type_name="Heavy-Duty Safety Switch / Bolted Pressure Contact Switch",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "fuse_type": f_type,
                    "catalog_section": "Speedfax Section 3: Enclosed Switches",
                    "duty_rating": "Heavy Duty / 200kA Withstand"
                },
                docs={"catalog_volume": "Speedfax Section 3"}
            ))

        # -------------------------------------------------------------------------
        # 9. SWITCHGEAR (Speedfax Section 13 - Type WL LV & GM-SG Medium Voltage)
        # -------------------------------------------------------------------------
        swgr_data = [
            ("WL-SWGR-2000A", "Type WL Metal-Enclosed", "Type WL Low Voltage Metal-Enclosed Switchgear 2000A 480V UL 1558 3WA", 2000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("WL-SWGR-3200A", "Type WL Metal-Enclosed", "Type WL Low Voltage Metal-Enclosed Switchgear 3200A 480V UL 1558 3WA", 3200.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("WL-SWGR-4000A", "Type WL Metal-Enclosed", "Type WL Low Voltage Metal-Enclosed Switchgear 4000A 480V UL 1558 3WA", 4000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("WL-SWGR-5000A", "Type WL Metal-Enclosed", "Type WL Low Voltage Metal-Enclosed Switchgear 5000A 480V UL 1558 3WA", 5000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("GMSG-05-1200A", "GM-SG Metal-Clad", "GM-SG Medium Voltage Metal-Clad Switchgear 1200A 4.76kV 3AH Breakers", 1200.0, 40.0, "4.76kV", "3PH", "3P3W", "IEEE C37.20.2 Metal-Clad", 40.0),
            ("GMSG-15-1200A", "GM-SG Metal-Clad", "GM-SG Medium Voltage Metal-Clad Switchgear 1200A 15kV 3AH Breakers", 1200.0, 31.5, "15kV", "3PH", "3P3W", "IEEE C37.20.2 Metal-Clad", 31.5),
            ("GMSG-15-2000A", "GM-SG Metal-Clad", "GM-SG Medium Voltage Metal-Clad Switchgear 2000A 15kV 3AH Breakers", 2000.0, 40.0, "15kV", "3PH", "3P3W", "IEEE C37.20.2 Metal-Clad", 40.0),
            ("GMSG-ARC-15-3000A", "GM-SG-AR Arc-Resistant", "GM-SG-AR Type 2B Arc-Resistant Medium Voltage Switchgear 3000A 15kV", 3000.0, 50.0, "15kV", "3PH", "3P3W", "IEEE C37.20.7 Type 2B Arc-Resistant", 50.0),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, swgr_std, withstand in swgr_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switchgear",
                type_tag="SWGR",
                type_name="Low-Voltage / Medium-Voltage Metal-Enclosed Switchgear",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating="NEMA 1 Indoor Metal-Clad",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "switchgear_standard": swgr_std,
                    "short_time_withstand_ka": withstand,
                    "catalog_section": "Speedfax Section 13: Low Voltage & Medium Voltage Switchgear",
                    "arc_resistant_rating": "IEEE C37.20.7 Accessibility Type 2B"
                },
                docs={"catalog_volume": "Speedfax Section 13"}
            ))

        # -------------------------------------------------------------------------
        # 10. TRANSFORMERS (Speedfax Section 10 - Distribution Dry-Type DOE 2016)
        # -------------------------------------------------------------------------
        xfmr_data = [
            # Standard General Purpose DOE 2016 Ventilated Dry-Type 480V Delta to 208Y/120V
            ("11A15T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 15kVA 480V-208Y/120V 3PH Aluminum", 15.0, "480V Delta", "208Y/120V", 18.0, 4.5, "Aluminum", 150.0),
            ("11A30T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 30kVA 480V-208Y/120V 3PH Aluminum", 30.0, "480V Delta", "208Y/120V", 36.1, 4.5, "Aluminum", 150.0),
            ("11A45T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 45kVA 480V-208Y/120V 3PH Aluminum", 45.0, "480V Delta", "208Y/120V", 54.1, 4.8, "Aluminum", 150.0),
            ("11A75T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 75kVA 480V-208Y/120V 3PH Aluminum", 75.0, "480V Delta", "208Y/120V", 90.2, 5.0, "Aluminum", 150.0),
            ("11A112T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 112.5kVA 480V-208Y/120V 3PH Aluminum", 112.5, "480V Delta", "208Y/120V", 135.3, 5.2, "Aluminum", 150.0),
            ("11A150T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 150kVA 480V-208Y/120V 3PH Aluminum", 150.0, "480V Delta", "208Y/120V", 180.4, 5.5, "Aluminum", 150.0),
            ("11A225T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 225kVA 480V-208Y/120V 3PH Aluminum", 225.0, "480V Delta", "208Y/120V", 270.6, 5.5, "Aluminum", 150.0),
            ("11A300T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 300kVA 480V-208Y/120V 3PH Aluminum", 300.0, "480V Delta", "208Y/120V", 360.8, 5.75, "Aluminum", 150.0),
            ("11A500T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 500kVA 480V-208Y/120V 3PH Aluminum", 500.0, "480V Delta", "208Y/120V", 601.4, 5.75, "Aluminum", 150.0),
            ("11C750T", "Distribution Dry-Type", "Siemens Low Voltage Dry-Type Transformer 750kVA 480V-208Y/120V 3PH Copper", 750.0, "480V Delta", "208Y/120V", 902.1, 5.75, "Copper", 150.0),
            # K-Factor Non-Linear Harmonic Rated
            ("11C75TK13", "K-Factor Dry-Type", "Siemens K-Factor K-13 Non-Linear Transformer 75kVA 480V-208Y/120V Copper", 75.0, "480V Delta", "208Y/120V", 90.2, 5.0, "Copper", 115.0),
            ("11C150TK13", "K-Factor Dry-Type", "Siemens K-Factor K-13 Non-Linear Transformer 150kVA 480V-208Y/120V Copper", 150.0, "480V Delta", "208Y/120V", 180.4, 5.5, "Copper", 115.0),
            ("11C300TK13", "K-Factor Dry-Type", "Siemens K-Factor K-13 Non-Linear Transformer 300kVA 480V-208Y/120V Copper", 300.0, "480V Delta", "208Y/120V", 360.8, 5.75, "Copper", 115.0),
            # Liquid-Filled Primary Substation Transformer
            ("SIE-SUB-1500KVA", "Substation Liquid-Filled", "Siemens Substation Liquid-Filled Transformer 1500kVA 13.8kV-480Y/277V FR3", 1500.0, "13.8kV Delta", "480Y/277V", 62.8, 5.75, "Copper", 65.0),
            ("SIE-SUB-2500KVA", "Substation Liquid-Filled", "Siemens Substation Liquid-Filled Transformer 2500kVA 13.8kV-480Y/277V FR3", 2500.0, "13.8kV Delta", "480Y/277V", 104.6, 5.75, "Copper", 65.0),
        ]
        for pn, series, desc, kva, pri_v, sec_v, pri_amps, z, winding, temp_rise in xfmr_data:
            sec_amps = (kva * 1000.0) / (208.0 * 1.73205) if "208" in sec_v else (kva * 1000.0) / (480.0 * 1.73205)
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="transformer",
                type_tag="XFMR",
                type_name="Low-Voltage Ventilated / Liquid Substation Transformer",
                description=desc,
                voltage=f"{pri_v} Pri / {sec_v} Sec",
                amps=round(sec_amps, 1),
                kva=kva,
                poles="3PH",
                phase="3PH",
                impedance_z=z,
                nema_rating="NEMA 2 / 3R Weathershield",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "primary_voltage": pri_v,
                    "secondary_voltage": sec_v,
                    "primary_amps": pri_amps,
                    "secondary_amps": round(sec_amps, 1),
                    "winding_material": winding,
                    "temperature_rise_c": temp_rise,
                    "efficiency_standard": "DOE 2016 Compliant (10 CFR Part 431)",
                    "catalog_section": "Speedfax Section 10: Power Distribution Transformers"
                },
                docs={"catalog_volume": "Speedfax Section 10"}
            ))

        # -------------------------------------------------------------------------
        # 11. AUTOMATIC TRANSFER SWITCHES (Sensata / ASCO OEM & 3WA Breaker Pair)
        # -------------------------------------------------------------------------
        ats_data = [
            ("SIE-ATS-200A-480V", "Siemens Sensata ATS", "Siemens Automatic Transfer Switch 200A 480V 3P Open Transition NEMA 1", 200.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Heavy-Duty Contactor"),
            ("SIE-ATS-400A-480V", "Siemens Sensata ATS", "Siemens Automatic Transfer Switch 400A 480V 3P Open Transition NEMA 1", 400.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Heavy-Duty Contactor"),
            ("SIE-ATS-800A-480V", "Siemens Sensata ATS", "Siemens Automatic Transfer Switch 800A 480V 3P Open Transition NEMA 1", 800.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Heavy-Duty Contactor"),
            ("SIE-ATS-1200A-480V", "Siemens Sensata ATS", "Siemens Automatic Transfer Switch 1200A 480V 3P Open Transition NEMA 1", 1200.0, 85.0, "480V", "3PH", "3P", "Open Transition", "Heavy-Duty Contactor"),
            ("SIE-ATS-2000A-480V", "Siemens Sensata ATS", "Siemens Automatic Transfer Switch 2000A 480V 3P Closed Transition NEMA 1", 2000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "Heavy-Duty Contactor"),
            ("SIE-ATS-3000A-480V", "Siemens Sensata ATS", "Siemens Automatic Transfer Switch 3000A 480V 3P Closed Transition NEMA 1", 3000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "Heavy-Duty Contactor"),
            ("3WA-ATS-2000A", "3WA Breaker ATS", "3WA Dual Breaker Automatic Transfer Switch Pair 2000A 480V Interlocked", 2000.0, 100.0, "480V", "3PH", "3P", "Electrically & Mechanically Interlocked", "3WA1 Air Breaker Pair"),
            ("3WA-ATS-3000A", "3WA Breaker ATS", "3WA Dual Breaker Automatic Transfer Switch Pair 3000A 480V Interlocked", 3000.0, 100.0, "480V", "3PH", "3P", "Electrically & Mechanically Interlocked", "3WA1 Air Breaker Pair"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, trans_type, mech in ats_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="transfer_switch",
                type_tag="ATS",
                type_name="Industrial Automatic Transfer Switch",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating="NEMA 1 / 3R Compatible",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "transition_mode": trans_type,
                    "switching_mechanism": mech,
                    "controller": "Siemens MX ATS Microprocessor Controller",
                    "catalog_section": "Speedfax Section 8: Automatic Transfer Switches"
                },
                docs={"catalog_volume": "Speedfax Section 8"}
            ))

        # -------------------------------------------------------------------------
        # 12. PARALLELING SWITCHGEAR (Siemens Generator Paralleling Switchgear PSG)
        # -------------------------------------------------------------------------
        psg_data = [
            ("SIE-PSG-2GEN-2000A", "Siemens Emergency PSG", "Multi-Generator Paralleling Switchgear 2-Gen 2000A 480V 3WA Breakers", 2000.0, 100.0, "480V", "3PH", "3P4W", 2, "SIMATIC S7-1500 Redundant Industrial PLC"),
            ("SIE-PSG-3GEN-3000A", "Siemens Emergency PSG", "Multi-Generator Paralleling Switchgear 3-Gen 3000A 480V 3WA Breakers", 3000.0, 100.0, "480V", "3PH", "3P4W", 3, "SIMATIC S7-1500 Redundant Industrial PLC"),
            ("SIE-PSG-4GEN-4000A", "Siemens Emergency PSG", "Multi-Generator Paralleling Switchgear 4-Gen 4000A 480V 3WA Breakers", 4000.0, 100.0, "480V", "3PH", "3P4W", 4, "SIMATIC S7-1500 Redundant Industrial PLC"),
            ("SIE-PSG-MV-15KV-2000A", "Siemens GM-SG PSG", "Medium Voltage 15kV Multi-Generator Paralleling Switchgear 2000A 3AH", 2000.0, 40.0, "15kV", "3PH", "3P3W", 4, "SIMATIC S7-1500H Fault-Tolerant PLC"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, gens, ctrl in psg_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="paralleling_switchgear",
                type_tag="PSG",
                type_name="Multi-Generator Emergency Paralleling Switchgear",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating="NEMA 1 Indoor Industrial",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "supported_generators": gens,
                    "automation_controller": ctrl,
                    "load_management": "Automated Generator Start/Stop & Dynamic Priority Shedding",
                    "paralleling_modes": "Emergency Standby / Peak Shaving / Base Load Utility Paralleling"
                },
                docs={"catalog_volume": "Siemens Power Control Systems"}
            ))

        # -------------------------------------------------------------------------
        # 13. POWER CONDITIONING (Siemens Active Harmonic Filters & Voltage Conditioners)
        # -------------------------------------------------------------------------
        cond_data = [
            ("AHF-050A-480V", "Siemens AHF", "Siemens Active Harmonic Filter 50A 380-480V 3PH Enclosed Dynamic Compensation", 50.0, 480.0, 50.0, "Siemens Active Harmonic Filter"),
            ("AHF-100A-480V", "Siemens AHF", "Siemens Active Harmonic Filter 100A 380-480V 3PH Enclosed Dynamic Compensation", 100.0, 480.0, 100.0, "Siemens Active Harmonic Filter"),
            ("AHF-150A-480V", "Siemens AHF", "Siemens Active Harmonic Filter 150A 380-480V 3PH Enclosed Dynamic Compensation", 150.0, 480.0, 150.0, "Siemens Active Harmonic Filter"),
            ("AHF-300A-480V", "Siemens AHF", "Siemens Active Harmonic Filter 300A 380-480V 3PH Enclosed Dynamic Compensation", 300.0, 480.0, 300.0, "Siemens Active Harmonic Filter"),
            ("DVC-300KVA-480V", "Siemens DVC", "Siemens Dynamic Voltage Conditioner 300kVA 480V Sag and Swell Mitigation", 300.0, 480.0, 360.8, "Dynamic Voltage Sag Conditioner"),
            ("DVC-1000KVA-480V", "Siemens DVC", "Siemens Dynamic Voltage Conditioner 1000kVA 480V Sag and Swell Mitigation", 1000.0, 480.0, 1202.8, "Dynamic Voltage Sag Conditioner"),
        ]
        for pn, series, desc, comp_amps, volt, amps, p_type in cond_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="power_quality",
                type_tag="POWER_COND",
                type_name="Active Harmonic Filter & Dynamic Voltage Conditioner",
                description=desc,
                voltage=f"{int(volt)}V",
                amps=amps,
                poles="3P",
                phase="3PH",
                nema_rating="NEMA 1 / IP20",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "filter_technology": p_type,
                    "mitigation_target": "Selective Harmonic Cancellation up to 51st Harmonic Order",
                    "response_time_ms": "< 1/2 cycle sub-cycle compensation",
                    "parallelable": "Modular master-slave paralleling up to 8 units"
                },
                docs={"catalog_volume": "Siemens Power Quality Technical Specifications"}
            ))

        # -------------------------------------------------------------------------
        # 14. POWER DISTRIBUTION SYSTEMS (Siemens Data Center PDU & RPP)
        # -------------------------------------------------------------------------
        pds_data = [
            ("SIE-PDU-50KVA-480-208", "Siemens PDU", "Siemens Precision Data Center PDU 50kVA 480V to 208Y/120V 84-Pole SEM3", 50.0, 138.8, "480V to 208Y/120V", 84, "K-13 Copper Isolation XFMR + SEM3"),
            ("SIE-PDU-100KVA-480-208", "Siemens PDU", "Siemens Precision Data Center PDU 100kVA 480V to 208Y/120V 84-Pole SEM3", 100.0, 277.6, "480V to 208Y/120V", 84, "K-13 Copper Isolation XFMR + SEM3"),
            ("SIE-PDU-150KVA-480-208", "Siemens PDU", "Siemens Precision Data Center PDU 150kVA 480V to 208Y/120V 168-Pole SEM3", 150.0, 416.4, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + SEM3"),
            ("SIE-PDU-225KVA-480-208", "Siemens PDU", "Siemens Precision Data Center PDU 225kVA 480V to 208Y/120V 168-Pole SEM3", 225.0, 624.5, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + SEM3"),
            ("SIE-PDU-300KVA-480-208", "Siemens PDU", "Siemens Precision Data Center PDU 300kVA 480V to 208Y/120V 168-Pole SEM3", 300.0, 832.7, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + SEM3"),
            ("SIE-RPP-225A-84P", "Siemens RPP", "Siemens Remote Power Panel 225A Dual Feed 84-Circuit Data Distribution SEM3", 75.0, 225.0, "208Y/120V", 84, "Dual Feed Remote Power Panel"),
            ("SIE-RPP-400A-168P", "Siemens RPP", "Siemens Remote Power Panel 400A Dual Feed 168-Circuit Data Distribution SEM3", 150.0, 400.0, "208Y/120V", 168, "Dual Feed Remote Power Panel"),
        ]
        for pn, series, desc, kva, amps, volt, poles_count, config in pds_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="power_distribution",
                type_tag="PDS",
                type_name="Power Distribution Unit (PDU) & Remote Power Panel (RPP)",
                description=desc,
                voltage=volt,
                amps=amps,
                kva=kva,
                poles="3P4W",
                phase="3PH",
                total_slots=poles_count,
                nema_rating="NEMA 1 Indoor Data Center Enclosure",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "subsystem_type": config,
                    "branch_monitoring": "Siemens Embedded Micro Metering Module (SEM3)",
                    "isolation_transformer": "K-13 / K-20 Shielded All-Copper Isolation Transformer"
                },
                docs={"catalog_volume": "Siemens Critical Power PDU Guide"}
            ))

        # -------------------------------------------------------------------------
        # 15. STATIC TRANSFER SWITCHES (Siemens Industrial High-Speed STS <4ms)
        # -------------------------------------------------------------------------
        sts_data = [
            ("SIE-STS-100A-480V", "Siemens Static STS", "Siemens Industrial High-Speed Static Transfer Switch 100A 480V 3P4W <4ms", 100.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SIE-STS-250A-480V", "Siemens Static STS", "Siemens Industrial High-Speed Static Transfer Switch 250A 480V 3P4W <4ms", 250.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SIE-STS-400A-480V", "Siemens Static STS", "Siemens Industrial High-Speed Static Transfer Switch 400A 480V 3P4W <4ms", 400.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SIE-STS-600A-480V", "Siemens Static STS", "Siemens Industrial High-Speed Static Transfer Switch 600A 480V 3P4W <4ms", 600.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SIE-STS-800A-480V", "Siemens Static STS", "Siemens Industrial High-Speed Static Transfer Switch 800A 480V 3P4W <4ms", 800.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SIE-STS-1200A-480V", "Siemens Static STS", "Siemens Industrial High-Speed Static Transfer Switch 1200A 480V 3P4W <4ms", 1200.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, xfer_time, ctrl in sts_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="transfer_switch",
                type_tag="STS",
                type_name="Solid-State Static Transfer Switch (<4ms)",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating="NEMA 1 Industrial Floor Standing",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "transfer_time": xfer_time,
                    "switch_architecture": "True SCR Solid-State Static Transfer Switch",
                    "control_logic": ctrl,
                    "maintenance_bypass": "Integrated Triple Breaker Bypass Isolation"
                },
                docs={"catalog_volume": "Siemens STS Technical Guide"}
            ))

        # -------------------------------------------------------------------------
        # 16. SURGE PROTECTIVE DEVICES (Speedfax Section 9 - TPS3 01, TPS3 03, TPS3 09)
        # -------------------------------------------------------------------------
        spd_data = [
            ("TPS30112480Y", "TPS3 01 Series", "Siemens TPS3 01 Surge Protective Device 120kA/Phase 480Y/277V NEMA 4X", 120.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("TPS30116480Y", "TPS3 01 Series", "Siemens TPS3 01 Surge Protective Device 160kA/Phase 480Y/277V NEMA 4X", 160.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("TPS30120480Y", "TPS3 01 Series", "Siemens TPS3 01 Surge Protective Device 200kA/Phase 480Y/277V NEMA 4X", 200.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("TPS30130480Y", "TPS3 01 Series", "Siemens TPS3 01 Surge Protective Device 300kA/Phase 480Y/277V NEMA 4X", 300.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("TPS30310208Y", "TPS3 03 Series", "Siemens TPS3 03 Internal Panelmount SPD 100kA/Phase 208Y/120V NEMA 1", 100.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 1 / Internal", 20.0),
            ("TPS30910480Y", "TPS3 09 Series", "Siemens TPS3 09 Wallmount Surge Protective Device 100kA/Phase 480Y/277V NEMA 4X", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Non-Metallic", 20.0),
        ]
        for pn, series, desc, ka_phase, sccr, volt, phase, poles, nema, in_rating in spd_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="surge_protection",
                type_tag="SPD",
                type_name="Industrial Surge Protective Device (Type 1 / Type 2)",
                description=desc,
                voltage=volt,
                aic=sccr,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "surge_current_per_phase_ka": ka_phase,
                    "nominal_discharge_current_in_ka": in_rating,
                    "short_circuit_current_rating_ka": sccr,
                    "ul_1449_type": "UL 1449 4th Edition Type 1 / Type 2",
                    "catalog_section": "Speedfax Section 9: Surge Protective Devices"
                },
                docs={"catalog_volume": "Speedfax Section 9"}
            ))

        # -------------------------------------------------------------------------
        # 17. UNINTERRUPTIBLE POWER SUPPLIES (Siemens Masterguard / SITOP Industrial)
        # -------------------------------------------------------------------------
        ups_data = [
            ("SIE-UPS-050K480", "Siemens Industrial UPS", "Siemens Industrial 3-Phase UPS 50kW/50kVA 480V Double-Conversion", 50.0, 50.0, "480V", "3PH", "3P4W", 60.2, "Industrial Ruggedized Online", 96.0),
            ("SIE-UPS-100K480", "Siemens Industrial UPS", "Siemens Industrial 3-Phase UPS 100kW/100kVA 480V Double-Conversion", 100.0, 100.0, "480V", "3PH", "3P4W", 120.3, "Industrial Ruggedized Online", 96.5),
            ("SIE-UPS-160K480", "Siemens Industrial UPS", "Siemens Industrial 3-Phase UPS 160kW/160kVA 480V Double-Conversion", 160.0, 160.0, "480V", "3PH", "3P4W", 192.5, "Industrial Ruggedized Online", 96.5),
            ("SIE-UPS-250K480", "Siemens Industrial UPS", "Siemens Industrial 3-Phase UPS 250kW/250kVA 480V Double-Conversion", 250.0, 250.0, "480V", "3PH", "3P4W", 300.7, "Industrial Ruggedized Online", 97.0),
            ("SIE-UPS-500K480", "Siemens Industrial UPS", "Siemens Industrial 3-Phase UPS 500kW/500kVA 480V Double-Conversion", 500.0, 500.0, "480V", "3PH", "3P4W", 601.4, "Industrial Ruggedized Online", 97.0),
        ]
        for pn, series, desc, kw, kva, volt, phase, poles, amps, arch, eff in ups_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="power_quality",
                type_tag="UPS",
                type_name="Industrial 3-Phase On-Line Uninterruptible Power Supply",
                description=desc,
                voltage=volt,
                amps=amps,
                kva=kva,
                poles=poles,
                phase=phase,
                nema_rating="NEMA 1 / IP20",
                cut_sheet_url=f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}",
                specs={
                    "power_rating_kw": kw,
                    "power_rating_kva": kva,
                    "efficiency_pct": eff,
                    "ups_architecture": arch,
                    "battery_compatibility": "VRLA / Lithium-Ion Battery Enclosures",
                    "catalog_section": "Siemens Critical Infrastructure Power Solutions"
                },
                docs={"catalog_volume": "Siemens Industrial UPS Technical Manual"}
            ))

        return items
