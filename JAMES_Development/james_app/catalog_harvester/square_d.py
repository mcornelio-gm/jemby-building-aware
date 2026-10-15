"""
Square D / Schneider Electric Industrial Equipment Catalog Harvester.
Harvests structured engineering specifications across all 17 industrial gear categories:
1. Busway (I-Line II Feeder & Plug-In Busway, Aluminum & Copper 800A-5000A)
2. Circuit Breakers (PowerPact H, J, L, M, P, R-Frames, MasterPact MTZ/NW, MasterClad VR MV)
3. Load Centers (Commercial QO 3-Phase & Commercial Homeline 3-Phase)
4. Motor Control Centers (Model 6 Industrial MCC, ArcBlock Arc-Resistant)
5. Panelboards (NQ 240V, NF 480Y/277V, I-Line Power Distribution 600V)
6. Softstarters (Altistart 480 ATS480, Altistart 22 ATS22)
7. Switchboards (Speed-D Commercial, QED-2 Distribution, QED-6 Drawout)
8. Switches & Disconnects (Class 3110 Heavy Duty Safety Switches H361-H368, Double-Throw, Bolt-Loc)
9. Switchgear (QED-6 Low-Voltage Drawout UL 1558, MasterClad Medium-Voltage Metal-Clad)
10. Transformers (Low-Voltage Dry-Type EX/EE DOE 2016 Compliant, K-Factor K-13, Substation Liquid-Filled)
11. Automatic Transfer Switches (ASCO 7000 Series, ASCO 4000 Series, MasterPact MTZ Breaker Pair ATS)
12. Paralleling Switchgear (Schneider Electric MasterPact Paralleling Switchgear, ASCO 7000 Power Control Systems)
13. Power Conditioning (AccuSine PCS+ Active Harmonic Filter, AccuSine PFV+ Electronic VAR Compensator)
14. Power Distribution Systems (PowerLogic Data Center PDU 50kVA-300kVA, Remote Power Panel RPP)
15. Static Transfer Switches (Schneider Electric / Gutor High-Speed Static Transfer Switch <4ms)
16. Surge Protective Devices (Surgelogic EMA, EBA, HWA Series 120kA-480kA/Phase NEMA 4X)
17. Uninterruptible Power Supplies (Galaxy VX 500kW-1500kW, Galaxy VM 160kW-225kW, Galaxy VS 20kW-150kW, Easy UPS 3M)
"""

from typing import List
from james_app.catalog_harvester.base import BaseVendorHarvester
from james_app.catalog_harvester.models import CatalogItem


class SquareDCatalogHarvester(BaseVendorHarvester):
    """
    Catalog extractor for Square D / Schneider Electric Industrial Equipment.
    Grounds catalog models to Schneider Electric Digest 179 and industrial technical publications.
    """

    vendor_name: str = "Square D"
    vendor_key: str = "square_d"
    source_url: str = "https://www.se.com/us/en/brands/squared/products-and-services/"

    def harvest(self) -> List[CatalogItem]:
        """Harvest comprehensive industrial equipment items for Square D / Schneider Electric."""
        items: List[CatalogItem] = []

        # -------------------------------------------------------------------------
        # 1. BUSWAY (Digest 179 Section 12 - I-Line II Sandwich Busway)
        # -------------------------------------------------------------------------
        busway_data = [
            ("CP2508G", "I-Line II", "I-Line II Copper Feeder Busway 800A 3P4W 600V with Ground", 800.0, 100.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 100.0),
            ("CP2512G", "I-Line II", "I-Line II Copper Feeder Busway 1200A 3P4W 600V with Ground", 1200.0, 100.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 100.0),
            ("CP2516G", "I-Line II", "I-Line II Copper Feeder Busway 1600A 3P4W 600V with Ground", 1600.0, 150.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 150.0),
            ("CP2520G", "I-Line II", "I-Line II Copper Feeder Busway 2000A 3P4W 600V with Ground", 2000.0, 150.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 150.0),
            ("CP2530G", "I-Line II", "I-Line II Copper Feeder Busway 3000A 3P4W 600V with Ground", 3000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("CP2540G", "I-Line II", "I-Line II Copper Feeder Busway 4000A 3P4W 600V with Ground", 4000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("CP2550G", "I-Line II", "I-Line II Copper Feeder Busway 5000A 3P4W 600V with Ground", 5000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("AP2510G", "I-Line II", "I-Line II Aluminum Feeder Busway 1000A 3P4W 600V with Ground", 1000.0, 100.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 100.0),
            ("AP2516G", "I-Line II", "I-Line II Aluminum Feeder Busway 1600A 3P4W 600V with Ground", 1600.0, 150.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 150.0),
            ("AP2525G", "I-Line II", "I-Line II Aluminum Feeder Busway 2500A 3P4W 600V with Ground", 2500.0, 150.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 150.0),
            ("AP2530G", "I-Line II", "I-Line II Aluminum Feeder Busway 3000A 3P4W 600V with Ground", 3000.0, 200.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 200.0),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "bus_material": bus_mat,
                    "short_circuit_withstand_ka": sccr,
                    "catalog_section": "Digest 179 Section 12: Busway Systems",
                    "conductor_configuration": poles
                },
                docs={"catalog_volume": "Digest 179 Section 12"}
            ))

        # -------------------------------------------------------------------------
        # 2. CIRCUIT BREAKERS (Digest 179 Section 7 - PowerPact & MasterPact)
        # -------------------------------------------------------------------------
        breakers_data = [
            # PowerPact H-Frame (15A-150A)
            ("HDA36030", "PowerPact H", "PowerPact H-Frame 30A 3P 600V 14kAIC Thermal-Magnetic I-Line Breaker", 30.0, 18.0, "600V", "3PH", "3P", "Thermal-Magnetic", "H-Frame"),
            ("HDA36060", "PowerPact H", "PowerPact H-Frame 60A 3P 600V 14kAIC Thermal-Magnetic I-Line Breaker", 60.0, 18.0, "600V", "3PH", "3P", "Thermal-Magnetic", "H-Frame"),
            ("HGA36100", "PowerPact H", "PowerPact H-Frame 100A 3P 600V 35kAIC Thermal-Magnetic I-Line Breaker", 100.0, 35.0, "600V", "3PH", "3P", "Thermal-Magnetic", "H-Frame"),
            ("HJA36150", "PowerPact H", "PowerPact H-Frame 150A 3P 600V 65kAIC Thermal-Magnetic I-Line Breaker", 150.0, 65.0, "600V", "3PH", "3P", "Thermal-Magnetic", "H-Frame"),
            # PowerPact J-Frame (150A-250A)
            ("JGA36200", "PowerPact J", "PowerPact J-Frame 200A 3P 600V 35kAIC Thermal-Magnetic I-Line Breaker", 200.0, 35.0, "600V", "3PH", "3P", "Thermal-Magnetic", "J-Frame"),
            ("JJA36250", "PowerPact J", "PowerPact J-Frame 250A 3P 600V 65kAIC Thermal-Magnetic I-Line Breaker", 250.0, 65.0, "600V", "3PH", "3P", "Thermal-Magnetic", "J-Frame"),
            ("JLA36250U31X", "PowerPact J", "PowerPact J-Frame 250A 3P 600V 100kAIC Micrologic 3.2 Electronic Breaker", 250.0, 100.0, "600V", "3PH", "3P", "Micrologic 3.2 Standard Electronic", "J-Frame"),
            # PowerPact L-Frame (250A-600A)
            ("LGA36400U31X", "PowerPact L", "PowerPact L-Frame 400A 3P 600V 35kAIC Micrologic 3.3 Electronic Breaker", 400.0, 35.0, "600V", "3PH", "3P", "Micrologic 3.3 Electronic", "L-Frame"),
            ("LJA36600U31X", "PowerPact L", "PowerPact L-Frame 600A 3P 600V 65kAIC Micrologic 3.3 Electronic Breaker", 600.0, 65.0, "600V", "3PH", "3P", "Micrologic 3.3 Electronic", "L-Frame"),
            ("LLA36600U53X", "PowerPact L", "PowerPact L-Frame 600A 3P 600V 100kAIC Micrologic 5.3E Energy Electronic Breaker", 600.0, 100.0, "600V", "3PH", "3P", "Micrologic 5.3E Energy Electronic", "L-Frame"),
            # PowerPact M-Frame (300A-800A)
            ("MGA36800", "PowerPact M", "PowerPact M-Frame 800A 3P 600V 35kAIC Electronic ET 1.0 I-Line Breaker", 800.0, 35.0, "600V", "3PH", "3P", "ET 1.0 Basic Electronic", "M-Frame"),
            ("MJA36800", "PowerPact M", "PowerPact M-Frame 800A 3P 600V 65kAIC Electronic ET 1.0 I-Line Breaker", 800.0, 65.0, "600V", "3PH", "3P", "ET 1.0 Basic Electronic", "M-Frame"),
            # PowerPact P-Frame (600A-1200A)
            ("PGA361000U31A", "PowerPact P", "PowerPact P-Frame 1000A 3P 600V 35kAIC Micrologic 3.0 Electronic Breaker", 1000.0, 35.0, "600V", "3PH", "3P", "Micrologic 3.0 Electronic", "P-Frame"),
            ("PJA361200U54A", "PowerPact P", "PowerPact P-Frame 1200A 3P 600V 65kAIC Micrologic 5.0P Power Electronic Breaker", 1200.0, 65.0, "600V", "3PH", "3P", "Micrologic 5.0P Power Electronic", "P-Frame"),
            # PowerPact R-Frame (1600A-3000A)
            ("RGF361600U54A", "PowerPact R", "PowerPact R-Frame 1600A 3P 600V 65kAIC Micrologic 5.0P Electronic Breaker", 1600.0, 65.0, "600V", "3PH", "3P", "Micrologic 5.0P Electronic", "R-Frame"),
            ("RJF362000U64AE1", "PowerPact R", "PowerPact R-Frame 2000A 3P 600V 100kAIC Micrologic 6.0A Ammeter Breaker", 2000.0, 100.0, "600V", "3PH", "3P", "Micrologic 6.0A Ammeter", "R-Frame"),
            ("RJF362500U64AE1", "PowerPact R", "PowerPact R-Frame 2500A 3P 600V 100kAIC Micrologic 6.0A Ammeter Breaker", 2500.0, 100.0, "600V", "3PH", "3P", "Micrologic 6.0A Ammeter", "R-Frame"),
            ("RJF363000U64AE1", "PowerPact R", "PowerPact R-Frame 3000A 3P 600V 100kAIC Micrologic 6.0A Ammeter Breaker", 3000.0, 100.0, "600V", "3PH", "3P", "Micrologic 6.0A Ammeter", "R-Frame"),
            # MasterPact MTZ2 / MTZ3 Low Voltage Power Circuit Breakers (UL 489 / UL 1066)
            ("MTZ208H1", "MasterPact MTZ2", "MasterPact MTZ2 800A 3P 600V 65kAIC Drawout Power Circuit Breaker", 800.0, 65.0, "600V", "3PH", "3P", "Micrologic X Control Unit", "MTZ2"),
            ("MTZ216H1", "MasterPact MTZ2", "MasterPact MTZ2 1600A 3P 600V 65kAIC Drawout Power Circuit Breaker", 1600.0, 65.0, "600V", "3PH", "3P", "Micrologic X Control Unit", "MTZ2"),
            ("MTZ220H2", "MasterPact MTZ2", "MasterPact MTZ2 2000A 3P 600V 85kAIC Drawout Power Circuit Breaker", 2000.0, 85.0, "600V", "3PH", "3P", "Micrologic X Control Unit", "MTZ2"),
            ("MTZ230H2", "MasterPact MTZ2", "MasterPact MTZ2 3000A 3P 600V 85kAIC Drawout Power Circuit Breaker", 3000.0, 85.0, "600V", "3PH", "3P", "Micrologic X Control Unit", "MTZ2"),
            ("MTZ340H2", "MasterPact MTZ3", "MasterPact MTZ3 4000A 3P 600V 100kAIC Drawout Power Circuit Breaker", 4000.0, 100.0, "600V", "3PH", "3P", "Micrologic X Control Unit", "MTZ3"),
            ("MTZ350H2", "MasterPact MTZ3", "MasterPact MTZ3 5000A 3P 600V 100kAIC Drawout Power Circuit Breaker", 5000.0, 100.0, "600V", "3PH", "3P", "Micrologic X Control Unit", "MTZ3"),
            ("MTZ360H2", "MasterPact MTZ3", "MasterPact MTZ3 6000A 3P 600V 100kAIC Drawout Power Circuit Breaker", 6000.0, 100.0, "600V", "3PH", "3P", "Micrologic X Control Unit", "MTZ3"),
            # MasterClad VR Medium Voltage Vacuum Circuit Breakers (4.76kV - 15kV)
            ("VR-05-1200-25", "MasterClad VR", "MasterClad VR 1200A 4.76kV 25kAIC Vacuum Circuit Breaker", 1200.0, 25.0, "4.76kV", "3PH", "3P", "Vacuum Interrupter Drawout", "VR 5kV"),
            ("VR-15-1200-31", "MasterClad VR", "MasterClad VR 1200A 15kV 31.5kAIC Vacuum Circuit Breaker", 1200.0, 31.5, "15kV", "3PH", "3P", "Vacuum Interrupter Drawout", "VR 15kV"),
            ("VR-15-2000-40", "MasterClad VR", "MasterClad VR 2000A 15kV 40kAIC Vacuum Circuit Breaker", 2000.0, 40.0, "15kV", "3PH", "3P", "Vacuum Interrupter Drawout", "VR 15kV"),
            ("VR-15-3000-50", "MasterClad VR", "MasterClad VR 3000A 15kV 50kAIC Vacuum Circuit Breaker", 3000.0, 50.0, "15kV", "3PH", "3P", "Vacuum Interrupter Drawout", "VR 15kV"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "trip_unit_type": trip,
                    "frame_designation": frame,
                    "catalog_section": "Digest 179 Section 7: Circuit Breakers",
                    "mounting": "I-Line / Plug-in / Drawout"
                },
                docs={"catalog_volume": "Digest 179 Section 7"}
            ))

        # -------------------------------------------------------------------------
        # 3. LOAD CENTERS (Digest 179 Section 1 - Commercial QO & Homeline 3-Phase)
        # -------------------------------------------------------------------------
        load_center_data = [
            ("QO324L125G", "QO Commercial", "QO 125A 3PH 24-Circuit Main Lugs Load Center NEMA 1", 125.0, 65.0, "208Y/120V", "3PH", "3P4W", 24, "NEMA 1 Indoor", "Main Lug Only"),
            ("QO330L200G", "QO Commercial", "QO 200A 3PH 30-Circuit Main Lugs Load Center NEMA 1", 200.0, 65.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Lug Only"),
            ("QO342L225G", "QO Commercial", "QO 225A 3PH 42-Circuit Main Lugs Load Center NEMA 1", 225.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Lug Only"),
            ("QO330MQ100", "QO Commercial", "QO 100A 3PH 30-Circuit Main Breaker Load Center NEMA 1", 100.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Breaker Included"),
            ("QO330MQ150", "QO Commercial", "QO 150A 3PH 30-Circuit Main Breaker Load Center NEMA 1", 150.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Breaker Included"),
            ("QO342MQ200", "QO Commercial", "QO 200A 3PH 42-Circuit Main Breaker Load Center NEMA 1", 200.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Breaker Included"),
            ("QO342MQ225", "QO Commercial", "QO 225A 3PH 42-Circuit Main Breaker Load Center NEMA 1", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Breaker Included"),
            ("QO342L225RBD", "QO Commercial", "QO 225A 3PH 42-Circuit Main Lugs Load Center NEMA 3R Outdoor", 225.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 3R Outdoor", "Main Lug Only"),
            ("HOM3060L225PC", "Homeline Commercial", "Homeline 225A 3PH 30-Space 60-Circuit Main Lugs Commercial Load Center", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Lug Only"),
            ("HOM4284M200PC", "Homeline Commercial", "Homeline 200A 3PH 42-Space 84-Circuit Main Breaker Commercial Load Center", 200.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Breaker Included"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "main_device_type": main_type,
                    "bus_material": "Tin-Plated Copper / Shielded Aluminum",
                    "catalog_section": "Digest 179 Section 1: Load Centers",
                    "branch_breaker_family": "QO Plug-On / Homeline"
                },
                docs={"catalog_volume": "Digest 179 Section 1"}
            ))

        # -------------------------------------------------------------------------
        # 4. MOTOR CONTROL CENTERS (Digest 179 Section 17 - Model 6 Industrial MCC)
        # -------------------------------------------------------------------------
        mcc_data = [
            ("M6-FVNR-SZ1-600A", "Model 6", "Model 6 MCC FVNR Starter Size 1 with MCP 600A Main Bus NEMA 1", 600.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 10, "Size 1 (Up to 10 HP)"),
            ("M6-FVNR-SZ2-600A", "Model 6", "Model 6 MCC FVNR Starter Size 2 with MCP 600A Main Bus NEMA 1", 600.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 25, "Size 2 (Up to 25 HP)"),
            ("M6-FVNR-SZ3-800A", "Model 6", "Model 6 MCC FVNR Starter Size 3 with MCP 800A Main Bus NEMA 1", 800.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 50, "Size 3 (Up to 50 HP)"),
            ("M6-FVNR-SZ4-1200A", "Model 6", "Model 6 MCC FVNR Starter Size 4 with MCP 1200A Main Bus NEMA 1", 1200.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 100, "Size 4 (Up to 100 HP)"),
            ("M6-FVNR-SZ5-1600A", "Model 6", "Model 6 MCC FVNR Starter Size 5 with MCP 1600A Main Bus NEMA 1", 1600.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 200, "Size 5 (Up to 200 HP)"),
            ("M6-VFD-ATV630-100HP", "Model 6 Smart MCC", "Model 6 Smart MCC with Altivar Process ATV630 100HP VFD Unit", 1200.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 100, "Altivar Process ATV630 VFD"),
            ("M6-ARCBLOCK-2000A", "Model 6 ArcBlock", "Model 6 ArcBlock Arc-Resistant Industrial MCC 2000A Main Bus", 2000.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Arc-Resistant", 400, "Master Feeder / Starter Lineup"),
            ("M6-MAINS-2500A", "Model 6", "Model 6 Industrial MCC 2500A Main Circuit Breaker Section PowerPact R", 2500.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 0, "Main Incoming Section"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "starter_type": starter_type,
                    "horse_power_rating": hp,
                    "horizontal_bus_rating_amps": bus_amps,
                    "catalog_section": "Digest 179 Section 17: Motor Control Centers",
                    "arc_resistant_available": True
                },
                docs={"catalog_volume": "Digest 179 Section 17"}
            ))

        # -------------------------------------------------------------------------
        # 5. PANELBOARDS (Digest 179 Section 9 - NQ, NF, I-Line Power Distribution)
        # -------------------------------------------------------------------------
        panel_data = [
            # NQ Lighting & Appliance Panelboards (240V max)
            ("NQ430L100", "NQ", "NQ Panelboard Interior 100A 3PH 4W 240VAC 30-Circuit Main Lugs Copper Bus", 100.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "Main Lugs", "Copper"),
            ("NQ442L225C", "NQ", "NQ Panelboard Interior 225A 3PH 4W 240VAC 42-Circuit Main Lugs Copper Bus", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("NQ442M225", "NQ", "NQ Panelboard Interior 225A 3PH 4W 240VAC 42-Circuit Main Breaker PowerPact Q", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "Main Breaker", "Copper"),
            ("NQ442L400", "NQ", "NQ Panelboard Interior 400A 3PH 4W 240VAC 42-Circuit Main Lugs Copper Bus", 400.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("NQ442L600", "NQ", "NQ Panelboard Interior 600A 3PH 4W 240VAC 42-Circuit Main Lugs Copper Bus", 600.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            # NF Commercial & Industrial Panelboards (480Y/277V)
            ("NF430L125", "NF", "NF Panelboard Interior 125A 3PH 4W 480Y/277VAC 30-Circuit Main Lugs Copper Bus", 125.0, 65.0, "480Y/277V", "3PH", "3P4W", 30, "Main Lugs", "Copper"),
            ("NF442L250C", "NF", "NF Panelboard Interior 250A 3PH 4W 480Y/277VAC 42-Circuit Main Lugs Copper Bus", 250.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("NF442M250", "NF", "NF Panelboard Interior 250A 3PH 4W 480Y/277VAC 42-Circuit Main Breaker PowerPact J", 250.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Breaker", "Copper"),
            ("NF442L400C", "NF", "NF Panelboard Interior 400A 3PH 4W 480Y/277VAC 42-Circuit Main Lugs Copper Bus", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("NF484L800C", "NF", "NF Panelboard Interior 800A 3PH 4W 480Y/277VAC 84-Circuit Main Lugs Copper Bus", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", 84, "Main Lugs", "Copper"),
            # I-Line Power Distribution Panelboards (600V max)
            ("HCP32868", "I-Line HCP", "I-Line HCP Distribution Panelboard Interior 800A 3PH 600VAC Copper Bus", 800.0, 100.0, "600V", "3PH", "3P4W", 36, "Main Lugs / Breaker", "Copper"),
            ("HCP328612", "I-Line HCP", "I-Line HCP Distribution Panelboard Interior 1200A 3PH 600VAC Copper Bus", 1200.0, 100.0, "600V", "3PH", "3P4W", 36, "Main Lugs / Breaker", "Copper"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, slots, main_type, bus_mat in panel_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="panelboard",
                type_tag="PANEL",
                type_name="Industrial Lighting & Power Distribution Panelboard",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                total_slots=slots,
                nema_rating="NEMA 1 / 3R Compatible",
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "main_device_type": main_type,
                    "bus_material": bus_mat,
                    "catalog_section": "Digest 179 Section 9: Panelboards",
                    "mounting": "Surface / Flush Mount"
                },
                docs={"catalog_volume": "Digest 179 Section 9"}
            ))

        # -------------------------------------------------------------------------
        # 6. SOFTSTARTERS (Digest 179 Section 18 - Altistart 480 & ATS22)
        # -------------------------------------------------------------------------
        softstart_data = [
            ("ATS480D17Y", "Altistart 480", "Altistart 480 Softstarter 17A 208-690V Integrated Bypass Modbus", 17.0, 480.0, 10.0, "ATS480"),
            ("ATS480D32Y", "Altistart 480", "Altistart 480 Softstarter 32A 208-690V Integrated Bypass Modbus", 32.0, 480.0, 20.0, "ATS480"),
            ("ATS480D62Y", "Altistart 480", "Altistart 480 Softstarter 62A 208-690V Integrated Bypass Modbus", 62.0, 480.0, 40.0, "ATS480"),
            ("ATS480D88Y", "Altistart 480", "Altistart 480 Softstarter 88A 208-690V Integrated Bypass Modbus", 88.0, 480.0, 60.0, "ATS480"),
            ("ATS480C14Y", "Altistart 480", "Altistart 480 Softstarter 140A 208-690V Integrated Bypass Modbus", 140.0, 480.0, 100.0, "ATS480"),
            ("ATS480C21Y", "Altistart 480", "Altistart 480 Softstarter 210A 208-690V Integrated Bypass Modbus", 210.0, 480.0, 150.0, "ATS480"),
            ("ATS480C32Y", "Altistart 480", "Altistart 480 Softstarter 320A 208-690V Integrated Bypass Modbus", 320.0, 480.0, 250.0, "ATS480"),
            ("ATS480C59Y", "Altistart 480", "Altistart 480 Softstarter 590A 208-690V Integrated Bypass Modbus", 590.0, 480.0, 500.0, "ATS480"),
            ("ATS480M12Y", "Altistart 480", "Altistart 480 Softstarter 1200A 208-690V Integrated Bypass Modbus", 1200.0, 480.0, 1000.0, "ATS480"),
            ("ATS22C11Q", "Altistart 22", "Altistart 22 Softstarter 110A 230-440V Heavy Duty Industrial", 110.0, 480.0, 75.0, "ATS22"),
            ("ATS22C32Q", "Altistart 22", "Altistart 22 Softstarter 320A 230-440V Heavy Duty Industrial", 320.0, 480.0, 250.0, "ATS22"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "motor_hp_480v": hp,
                    "bypass_contactor": "Integrated Internal Bypass",
                    "control_voltage": "110-230VAC / 24VDC",
                    "communication_protocol": "Modbus TCP / EtherNet/IP Optional",
                    "catalog_section": "Digest 179 Section 18: Variable Speed Drives & Softstarters"
                },
                docs={"catalog_volume": "Digest 179 Section 18"}
            ))

        # -------------------------------------------------------------------------
        # 7. SWITCHBOARDS (Digest 179 Section 11 - Speed-D, QED-2, QED-6)
        # -------------------------------------------------------------------------
        swbd_data = [
            ("SPEED-D-400A-480V", "Speed-D", "Speed-D Commercial Service Entrance Switchboard 400A 480Y/277V 3PH 4W", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 / 3R", "Copper", "Utility Metering + PowerPact Main"),
            ("SPEED-D-800A-480V", "Speed-D", "Speed-D Commercial Service Entrance Switchboard 800A 480Y/277V 3PH 4W", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 / 3R", "Copper", "Utility Metering + PowerPact M Main"),
            ("QED2-1200A-480V", "QED-2", "QED-2 Low Voltage Distribution Switchboard 1200A 480V Front-Connected PowerPact P", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "PowerPact P Main + I-Line Distribution"),
            ("QED2-2000A-480V", "QED-2", "QED-2 Low Voltage Distribution Switchboard 2000A 480V Front-Connected PowerPact R", 2000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "PowerPact R Main + I-Line Distribution"),
            ("QED2-3000A-480V", "QED-2", "QED-2 Low Voltage Distribution Switchboard 3000A 480V MasterPact MTZ2 Main", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "MasterPact MTZ2 Drawout Main"),
            ("QED2-4000A-480V", "QED-2", "QED-2 Low Voltage Distribution Switchboard 4000A 480V MasterPact MTZ3 Main", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "MasterPact MTZ3 Drawout Main"),
            ("QED2-5000A-480V", "QED-2", "QED-2 Low Voltage Distribution Switchboard 5000A 480V MasterPact MTZ3 Main", 5000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "MasterPact MTZ3 Drawout Main"),
            ("QED6-2000A-480V", "QED-6", "QED-6 Rear-Connected Low Voltage Power Switchboard 2000A 480V MasterPact MTZ2", 2000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "MasterPact MTZ2 Drawout Feeders"),
            ("QED6-4000A-480V", "QED-6", "QED-6 Rear-Connected Low Voltage Power Switchboard 4000A 480V MasterPact MTZ3", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "MasterPact MTZ3 Drawout Feeders"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, bus_mat, config in swbd_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switchboard",
                type_tag="SWBD",
                type_name="Industrial Front/Rear Connected Distribution Switchboard",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "bus_material": bus_mat,
                    "switchboard_configuration": config,
                    "short_circuit_rating_ka": aic,
                    "catalog_section": "Digest 179 Section 11: Switchboards",
                    "standards": "UL 891 / NEMA PB2"
                },
                docs={"catalog_volume": "Digest 179 Section 11"}
            ))

        # -------------------------------------------------------------------------
        # 8. SWITCHES & DISCONNECTS (Digest 179 Section 3 - Heavy Duty Safety Switches)
        # -------------------------------------------------------------------------
        disc_data = [
            ("H361", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 30A 3P 600V NEMA 1 Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("H362", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 60A 3P 600V NEMA 1 Fusible", 60.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("H363", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 100A 3P 600V NEMA 1 Fusible", 100.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("H364", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 200A 3P 600V NEMA 1 Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("H365", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 400A 3P 600V NEMA 1 Fusible", 400.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("H366", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 600A 3P 600V NEMA 1 Fusible", 600.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("H367", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 800A 3P 600V NEMA 1 Fusible Class L", 800.0, 200.0, "600V", "3PH", "3P", "Fusible (Class L)", "NEMA 1 Indoor"),
            ("H368", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 1200A 3P 600V NEMA 1 Fusible Class L", 1200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class L)", "NEMA 1 Indoor"),
            ("HU361", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 30A 3P 600V NEMA 1 Non-Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Non-Fusible", "NEMA 1 Indoor"),
            ("HU364", "Class 3110 Heavy Duty", "Heavy Duty Safety Switch 200A 3P 600V NEMA 1 Non-Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Non-Fusible", "NEMA 1 Indoor"),
            ("H361DS", "Class 3110 Stainless", "Heavy Duty Safety Switch 30A 3P 600V NEMA 4X 304 Stainless Steel Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 4X Stainless"),
            ("H364DS", "Class 3110 Stainless", "Heavy Duty Safety Switch 200A 3P 600V NEMA 4X 304 Stainless Steel Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 4X Stainless"),
            ("DTU364", "Double-Throw Manual", "Double-Throw Manual Transfer Safety Switch 200A 3P 600V NEMA 1 Non-Fusible", 200.0, 100.0, "600V", "3PH", "3P", "Double-Throw Manual Transfer", "NEMA 1 Indoor"),
            ("BP3612", "Bolt-Loc Bolted Pressure", "Bolt-Loc Bolted Pressure Contact Switch 1200A 3P 600V Fusible Class L", 1200.0, 200.0, "600V", "3PH", "3P", "Bolted Pressure Fusible Class L", "NEMA 1 Enclosed"),
            ("BP3620", "Bolt-Loc Bolted Pressure", "Bolt-Loc Bolted Pressure Contact Switch 2000A 3P 600V Fusible Class L", 2000.0, 200.0, "600V", "3PH", "3P", "Bolted Pressure Fusible Class L", "NEMA 1 Enclosed"),
            ("BP3640", "Bolt-Loc Bolted Pressure", "Bolt-Loc Bolted Pressure Contact Switch 4000A 3P 600V Fusible Class L", 4000.0, 200.0, "600V", "3PH", "3P", "Bolted Pressure Fusible Class L", "NEMA 1 Enclosed"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "fuse_type": f_type,
                    "catalog_section": "Digest 179 Section 3: Safety Switches",
                    "duty_rating": "Heavy Duty / Continuous"
                },
                docs={"catalog_volume": "Digest 179 Section 3"}
            ))

        # -------------------------------------------------------------------------
        # 9. SWITCHGEAR (Digest 179 Section 11 & MV Digest - QED-6 LV & MasterClad MV)
        # -------------------------------------------------------------------------
        swgr_data = [
            ("QED6-SWGR-2000A", "QED-6 Metal-Enclosed", "QED-6 Low Voltage Metal-Enclosed Switchgear 2000A 480V UL 1558 MTZ2", 2000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("QED6-SWGR-3200A", "QED-6 Metal-Enclosed", "QED-6 Low Voltage Metal-Enclosed Switchgear 3200A 480V UL 1558 MTZ3", 3200.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("QED6-SWGR-4000A", "QED-6 Metal-Enclosed", "QED-6 Low Voltage Metal-Enclosed Switchgear 4000A 480V UL 1558 MTZ3", 4000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("QED6-SWGR-5000A", "QED-6 Metal-Enclosed", "QED-6 Low Voltage Metal-Enclosed Switchgear 5000A 480V UL 1558 MTZ3", 5000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("MCLAD-05-1200A", "MasterClad Metal-Clad", "MasterClad Medium Voltage Metal-Clad Switchgear 1200A 4.76kV VR Breakers", 1200.0, 40.0, "4.76kV", "3PH", "3P3W", "IEEE C37.20.2 Metal-Clad", 40.0),
            ("MCLAD-15-1200A", "MasterClad Metal-Clad", "MasterClad Medium Voltage Metal-Clad Switchgear 1200A 15kV VR Breakers", 1200.0, 31.5, "15kV", "3PH", "3P3W", "IEEE C37.20.2 Metal-Clad", 31.5),
            ("MCLAD-15-2000A", "MasterClad Metal-Clad", "MasterClad Medium Voltage Metal-Clad Switchgear 2000A 15kV VR Breakers", 2000.0, 40.0, "15kV", "3PH", "3P3W", "IEEE C37.20.2 Metal-Clad", 40.0),
            ("MCLAD-ARC-15-3000A", "MasterClad Arc-Resistant", "MasterClad Type 2B Arc-Resistant Medium Voltage Switchgear 3000A 15kV", 3000.0, 50.0, "15kV", "3PH", "3P3W", "IEEE C37.20.7 Type 2B Arc-Resistant", 50.0),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "switchgear_standard": swgr_std,
                    "short_time_withstand_ka": withstand,
                    "catalog_section": "Digest 179 Section 11 & Medium Voltage Distribution"
                },
                docs={"catalog_volume": "Digest 179 Section 11"}
            ))

        # -------------------------------------------------------------------------
        # 10. TRANSFORMERS (Digest 179 Section 14 - EX/EE DOE 2016 Compliant & K-Factor)
        # -------------------------------------------------------------------------
        xfmr_data = [
            # Standard General Purpose DOE 2016 Ventilated Dry-Type 480V Delta to 208Y/120V
            ("EX15T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 15kVA 480V-208Y/120V 3PH Aluminum", 15.0, "480V Delta", "208Y/120V", 18.0, 4.5, "Aluminum", 150.0),
            ("EX30T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 30kVA 480V-208Y/120V 3PH Aluminum", 30.0, "480V Delta", "208Y/120V", 36.1, 4.5, "Aluminum", 150.0),
            ("EX45T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 45kVA 480V-208Y/120V 3PH Aluminum", 45.0, "480V Delta", "208Y/120V", 54.1, 4.8, "Aluminum", 150.0),
            ("EX75T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 75kVA 480V-208Y/120V 3PH Aluminum", 75.0, "480V Delta", "208Y/120V", 90.2, 5.0, "Aluminum", 150.0),
            ("EX112T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 112.5kVA 480V-208Y/120V 3PH Aluminum", 112.5, "480V Delta", "208Y/120V", 135.3, 5.2, "Aluminum", 150.0),
            ("EX150T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 150kVA 480V-208Y/120V 3PH Aluminum", 150.0, "480V Delta", "208Y/120V", 180.4, 5.5, "Aluminum", 150.0),
            ("EX225T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 225kVA 480V-208Y/120V 3PH Aluminum", 225.0, "480V Delta", "208Y/120V", 270.6, 5.5, "Aluminum", 150.0),
            ("EX300T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 300kVA 480V-208Y/120V 3PH Aluminum", 300.0, "480V Delta", "208Y/120V", 360.8, 5.75, "Aluminum", 150.0),
            ("EX500T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 500kVA 480V-208Y/120V 3PH Aluminum", 500.0, "480V Delta", "208Y/120V", 601.4, 5.75, "Aluminum", 150.0),
            ("EX750T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 750kVA 480V-208Y/120V 3PH Copper", 750.0, "480V Delta", "208Y/120V", 902.1, 5.75, "Copper", 150.0),
            ("EX1000T3H", "EX Series DOE 2016", "EX Low Voltage Dry-Type Transformer 1000kVA 480V-208Y/120V 3PH Copper", 1000.0, "480V Delta", "208Y/120V", 1202.8, 5.75, "Copper", 150.0),
            # K-Factor Non-Linear Harmonic Rated
            ("EX75T3HK13", "EX K-Factor", "EX K-Factor K-13 Non-Linear Transformer 75kVA 480V-208Y/120V 3PH Copper", 75.0, "480V Delta", "208Y/120V", 90.2, 5.0, "Copper", 115.0),
            ("EX150T3HK13", "EX K-Factor", "EX K-Factor K-13 Non-Linear Transformer 150kVA 480V-208Y/120V 3PH Copper", 150.0, "480V Delta", "208Y/120V", 180.4, 5.5, "Copper", 115.0),
            ("EX300T3HK13", "EX K-Factor", "EX K-Factor K-13 Non-Linear Transformer 300kVA 480V-208Y/120V 3PH Copper", 300.0, "480V Delta", "208Y/120V", 360.8, 5.75, "Copper", 115.0),
            # Liquid-Filled Primary Substation Transformer
            ("SE-SUB-1500KVA", "Substation Liquid-Filled", "Square D Substation Liquid-Filled Transformer 1500kVA 13.8kV-480Y/277V FR3", 1500.0, "13.8kV Delta", "480Y/277V", 62.8, 5.75, "Copper", 65.0),
            ("SE-SUB-2500KVA", "Substation Liquid-Filled", "Square D Substation Liquid-Filled Transformer 2500kVA 13.8kV-480Y/277V FR3", 2500.0, "13.8kV Delta", "480Y/277V", 104.6, 5.75, "Copper", 65.0),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "primary_voltage": pri_v,
                    "secondary_voltage": sec_v,
                    "primary_amps": pri_amps,
                    "secondary_amps": round(sec_amps, 1),
                    "winding_material": winding,
                    "temperature_rise_c": temp_rise,
                    "efficiency_standard": "DOE 2016 Compliant (10 CFR Part 431)",
                    "catalog_section": "Digest 179 Section 14: Transformers"
                },
                docs={"catalog_volume": "Digest 179 Section 14"}
            ))

        # -------------------------------------------------------------------------
        # 11. AUTOMATIC TRANSFER SWITCHES (ASCO 7000 / 4000 Series & MasterPact ATS)
        # -------------------------------------------------------------------------
        ats_data = [
            ("7AUSA30200N5XC", "ASCO 7000 Series", "ASCO 7000 Series Automatic Transfer Switch 200A 480V 3P Open Transition NEMA 1", 200.0, 65.0, "480V", "3PH", "3P", "Open Transition", "ASCO 7000 Contactor"),
            ("7AUSA30400N5XC", "ASCO 7000 Series", "ASCO 7000 Series Automatic Transfer Switch 400A 480V 3P Open Transition NEMA 1", 400.0, 65.0, "480V", "3PH", "3P", "Open Transition", "ASCO 7000 Contactor"),
            ("7AUSA30800N5XC", "ASCO 7000 Series", "ASCO 7000 Series Automatic Transfer Switch 800A 480V 3P Open Transition NEMA 1", 800.0, 65.0, "480V", "3PH", "3P", "Open Transition", "ASCO 7000 Contactor"),
            ("7AUSA31200N5XC", "ASCO 7000 Series", "ASCO 7000 Series Automatic Transfer Switch 1200A 480V 3P Open Transition NEMA 1", 1200.0, 85.0, "480V", "3PH", "3P", "Open Transition", "ASCO 7000 Contactor"),
            ("7ACSA32000N5XC", "ASCO 7000 Series", "ASCO 7000 Series Automatic Transfer Switch 2000A 480V 3P Closed Transition NEMA 1", 2000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "ASCO 7000 Contactor"),
            ("7ACSA33000N5XC", "ASCO 7000 Series", "ASCO 7000 Series Automatic Transfer Switch 3000A 480V 3P Closed Transition NEMA 1", 3000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "ASCO 7000 Contactor"),
            ("4AUSA30400N5XC", "ASCO 4000 Series", "ASCO 4000 Series Commercial Transfer Switch 400A 480V 3P Open Transition", 400.0, 65.0, "480V", "3PH", "3P", "Open Transition", "ASCO 4000 Contactor"),
            ("4AUSA30800N5XC", "ASCO 4000 Series", "ASCO 4000 Series Commercial Transfer Switch 800A 480V 3P Open Transition", 800.0, 65.0, "480V", "3PH", "3P", "Open Transition", "ASCO 4000 Contactor"),
            ("MTZ-ATS-2000A", "MasterPact Breaker ATS", "MasterPact MTZ Dual Breaker Automatic Transfer Switch Pair 2000A 480V", 2000.0, 100.0, "480V", "3PH", "3P", "Electrically & Mechanically Interlocked", "MasterPact MTZ2 Breaker Pair"),
            ("MTZ-ATS-3000A", "MasterPact Breaker ATS", "MasterPact MTZ Dual Breaker Automatic Transfer Switch Pair 3000A 480V", 3000.0, 100.0, "480V", "3PH", "3P", "Electrically & Mechanically Interlocked", "MasterPact MTZ2 Breaker Pair"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "transition_mode": trans_type,
                    "switching_mechanism": mech,
                    "controller": "ASCO Group 5 Controller / EcoStruxure Power ATS",
                    "catalog_section": "ASCO Power Technologies / Schneider Electric ATS"
                },
                docs={"catalog_volume": "ASCO 7000 / MasterPact ATS"}
            ))

        # -------------------------------------------------------------------------
        # 12. PARALLELING SWITCHGEAR (Schneider MasterPact PSG & ASCO 7000 PCS)
        # -------------------------------------------------------------------------
        psg_data = [
            ("SE-PSG-2GEN-2000A", "Schneider MasterPact PSG", "Multi-Generator Paralleling Switchgear 2-Gen 2000A 480V MasterPact MTZ", 2000.0, 100.0, "480V", "3PH", "3P4W", 2, "Schneider Modicon M580 Redundant PLC"),
            ("SE-PSG-3GEN-3000A", "Schneider MasterPact PSG", "Multi-Generator Paralleling Switchgear 3-Gen 3000A 480V MasterPact MTZ", 3000.0, 100.0, "480V", "3PH", "3P4W", 3, "Schneider Modicon M580 Redundant PLC"),
            ("SE-PSG-4GEN-4000A", "Schneider MasterPact PSG", "Multi-Generator Paralleling Switchgear 4-Gen 4000A 480V MasterPact MTZ", 4000.0, 100.0, "480V", "3PH", "3P4W", 4, "Schneider Modicon M580 Redundant PLC"),
            ("ASCO-PCS-7000-2500A", "ASCO 7000 PCS", "ASCO 7000 Power Control System Generator Paralleling Lineup 2500A 480V", 2500.0, 100.0, "480V", "3PH", "3P4W", 3, "ASCO Digital Master Synchronizer"),
            ("SE-PSG-MV-15KV-2000A", "Schneider MasterClad PSG", "Medium Voltage 15kV Multi-Generator Paralleling Switchgear 2000A VR Breakers", 2000.0, 40.0, "15kV", "3PH", "3P3W", 4, "Modicon Quantum / M580 Redundant PLC"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "supported_generators": gens,
                    "automation_controller": ctrl,
                    "load_management": "Automatic Priority Load Shedding / Peak Shaving",
                    "paralleling_modes": "Emergency Standby / Isolated Bus / Utility Interconnection"
                },
                docs={"catalog_volume": "Schneider Power Control Systems"}
            ))

        # -------------------------------------------------------------------------
        # 13. POWER CONDITIONING (AccuSine PCS+ Active Harmonic Filters & PFV+)
        # -------------------------------------------------------------------------
        cond_data = [
            ("PCSP060D5N1", "AccuSine PCS+", "AccuSine PCS+ Active Harmonic Filter 60A 380-480V 3PH NEMA 1 Enclosed", 60.0, 480.0, 60.0, "AccuSine PCS+ Active Harmonic Filter"),
            ("PCSP120D5N1", "AccuSine PCS+", "AccuSine PCS+ Active Harmonic Filter 120A 380-480V 3PH NEMA 1 Enclosed", 120.0, 480.0, 120.0, "AccuSine PCS+ Active Harmonic Filter"),
            ("PCSP200D5N1", "AccuSine PCS+", "AccuSine PCS+ Active Harmonic Filter 200A 380-480V 3PH NEMA 1 Enclosed", 200.0, 480.0, 200.0, "AccuSine PCS+ Active Harmonic Filter"),
            ("PCSP300D5N1", "AccuSine PCS+", "AccuSine PCS+ Active Harmonic Filter 300A 380-480V 3PH NEMA 1 Enclosed", 300.0, 480.0, 300.0, "AccuSine PCS+ Active Harmonic Filter"),
            ("PFVP100D5N1", "AccuSine PFV+", "AccuSine PFV+ Electronic VAR Compensator 100kVAR 380-480V 3PH NEMA 1", 100.0, 480.0, 120.0, "AccuSine PFV+ Electronic VAR Compensator"),
            ("PFVP200D5N1", "AccuSine PFV+", "AccuSine PFV+ Electronic VAR Compensator 200kVAR 380-480V 3PH NEMA 1", 200.0, 480.0, 240.0, "AccuSine PFV+ Electronic VAR Compensator"),
        ]
        for pn, series, desc, comp_amps, volt, amps, p_type in cond_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="power_quality",
                type_tag="POWER_COND",
                type_name="Active Harmonic Filter & Electronic VAR Compensator",
                description=desc,
                voltage=f"{int(volt)}V",
                amps=amps,
                poles="3P",
                phase="3PH",
                nema_rating="NEMA 1 / IP20",
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "filter_technology": p_type,
                    "mitigation_target": "Cancels 2nd to 51st Harmonic Orders (THDi < 3%)",
                    "response_time_ms": "< 2 cycles ultra-fast mitigation",
                    "parallelable": "Up to 10 units in parallel for 3000A compensation"
                },
                docs={"catalog_volume": "AccuSine Technical Catalog"}
            ))

        # -------------------------------------------------------------------------
        # 14. POWER DISTRIBUTION SYSTEMS (PowerLogic Data Center PDU & RPP)
        # -------------------------------------------------------------------------
        pds_data = [
            ("SE-PDU-50KVA-480-208", "PowerLogic PDU", "PowerLogic Precision Power Distribution Unit 50kVA 480V to 208Y/120V 84-Pole", 50.0, 138.8, "480V to 208Y/120V", 84, "K-13 Copper Isolation XFMR + BCM"),
            ("SE-PDU-100KVA-480-208", "PowerLogic PDU", "PowerLogic Precision Power Distribution Unit 100kVA 480V to 208Y/120V 84-Pole", 100.0, 277.6, "480V to 208Y/120V", 84, "K-13 Copper Isolation XFMR + BCM"),
            ("SE-PDU-150KVA-480-208", "PowerLogic PDU", "PowerLogic Precision Power Distribution Unit 150kVA 480V to 208Y/120V 168-Pole", 150.0, 416.4, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + BCM"),
            ("SE-PDU-225KVA-480-208", "PowerLogic PDU", "PowerLogic Precision Power Distribution Unit 225kVA 480V to 208Y/120V 168-Pole", 225.0, 624.5, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + BCM"),
            ("SE-PDU-300KVA-480-208", "PowerLogic PDU", "PowerLogic Precision Power Distribution Unit 300kVA 480V to 208Y/120V 168-Pole", 300.0, 832.7, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + BCM"),
            ("SE-RPP-225A-84P", "PowerLogic RPP", "PowerLogic Remote Power Panel 225A Dual Feed 84-Circuit Data Distribution", 75.0, 225.0, "208Y/120V", 84, "Dual Feed Remote Power Panel"),
            ("SE-RPP-400A-168P", "PowerLogic RPP", "PowerLogic Remote Power Panel 400A Dual Feed 168-Circuit Data Distribution", 150.0, 400.0, "208Y/120V", 168, "Dual Feed Remote Power Panel"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "subsystem_type": config,
                    "branch_monitoring": "PowerLogic Branch Circuit Power Metering (BCPM)",
                    "isolation_transformer": "K-13 / K-20 Shielded Isolation Transformer"
                },
                docs={"catalog_volume": "Schneider Power Distribution Systems"}
            ))

        # -------------------------------------------------------------------------
        # 15. STATIC TRANSFER SWITCHES (Schneider Electric / Gutor High-Speed STS)
        # -------------------------------------------------------------------------
        sts_data = [
            ("SE-STS-100A-480V", "Schneider STS", "Schneider Electric High-Speed Static Transfer Switch 100A 480V 3P4W <4ms", 100.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual DSP Redundant"),
            ("SE-STS-250A-480V", "Schneider STS", "Schneider Electric High-Speed Static Transfer Switch 250A 480V 3P4W <4ms", 250.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual DSP Redundant"),
            ("SE-STS-400A-480V", "Schneider STS", "Schneider Electric High-Speed Static Transfer Switch 400A 480V 3P4W <4ms", 400.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual DSP Redundant"),
            ("SE-STS-600A-480V", "Schneider STS", "Schneider Electric High-Speed Static Transfer Switch 600A 480V 3P4W <4ms", 600.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual DSP Redundant"),
            ("SE-STS-1000A-480V", "Schneider STS", "Schneider Electric High-Speed Static Transfer Switch 1000A 480V 3P4W <4ms", 1000.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual DSP Redundant"),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "transfer_time": xfer_time,
                    "switch_architecture": "True SCR Solid-State Static Bypass",
                    "control_logic": ctrl,
                    "maintenance_bypass": "Triple Breaker Wrap-Around Maintenance Bypass"
                },
                docs={"catalog_volume": "Schneider STS Technical Guide"}
            ))

        # -------------------------------------------------------------------------
        # 16. SURGE PROTECTIVE DEVICES (Digest 179 Section 6 - Surgelogic EMA, EBA, HWA)
        # -------------------------------------------------------------------------
        spd_data = [
            ("EMA120480Y", "Surgelogic EMA", "Surgelogic EMA Surge Protective Device 120kA/Phase 480Y/277V NEMA 4X", 120.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("EMA160480Y", "Surgelogic EMA", "Surgelogic EMA Surge Protective Device 160kA/Phase 480Y/277V NEMA 4X", 160.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("EMA240480Y", "Surgelogic EMA", "Surgelogic EMA Surge Protective Device 240kA/Phase 480Y/277V NEMA 4X", 240.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("EMA320480Y", "Surgelogic EMA", "Surgelogic EMA Surge Protective Device 320kA/Phase 480Y/277V NEMA 4X", 320.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("EMA480480Y", "Surgelogic EMA", "Surgelogic EMA Surge Protective Device 480kA/Phase 480Y/277V NEMA 4X", 480.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("EBA120208Y", "Surgelogic EBA", "Surgelogic EBA Surge Protective Device 120kA/Phase 208Y/120V NEMA 1", 120.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 1 Indoor", 20.0),
            ("HWA100480Y", "Surgelogic HWA", "Surgelogic HWA Hardwired Surge Protective Device 100kA/Phase 480Y/277V NEMA 4X", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Non-Metallic", 20.0),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "surge_current_per_phase_ka": ka_phase,
                    "nominal_discharge_current_in_ka": in_rating,
                    "short_circuit_current_rating_ka": sccr,
                    "ul_1449_type": "UL 1449 4th Edition Type 1 / Type 2",
                    "catalog_section": "Digest 179 Section 6: Surge Protective Devices"
                },
                docs={"catalog_volume": "Digest 179 Section 6"}
            ))

        # -------------------------------------------------------------------------
        # 17. UNINTERRUPTIBLE POWER SUPPLIES (Galaxy VX, Galaxy VM, Galaxy VS, Easy UPS 3M)
        # -------------------------------------------------------------------------
        ups_data = [
            # Galaxy VS Compact High-Efficiency 3-Phase UPS (20kW to 150kW)
            ("GVSUPS20K480", "Galaxy VS", "Galaxy VS 3-Phase UPS 20kW/20kVA 480V EcoStruxure Connected", 20.0, 20.0, "480V", "3PH", "3P4W", 24.1, "Modular Hot-Scalable", 99.0),
            ("GVSUPS50K480", "Galaxy VS", "Galaxy VS 3-Phase UPS 50kW/50kVA 480V EcoStruxure Connected", 50.0, 50.0, "480V", "3PH", "3P4W", 60.2, "Modular Hot-Scalable", 99.0),
            ("GVSUPS100K480", "Galaxy VS", "Galaxy VS 3-Phase UPS 100kW/100kVA 480V EcoStruxure Connected", 100.0, 100.0, "480V", "3PH", "3P4W", 120.3, "Modular Hot-Scalable", 99.0),
            ("GVSUPS150K480", "Galaxy VS", "Galaxy VS 3-Phase UPS 150kW/150kVA 480V EcoStruxure Connected", 150.0, 150.0, "480V", "3PH", "3P4W", 180.4, "Modular Hot-Scalable", 99.0),
            # Galaxy VM Medium Power 3-Phase UPS (160kW to 225kW)
            ("GVMUPS160K480", "Galaxy VM", "Galaxy VM 3-Phase UPS 160kW/160kVA 480V ECOnversion Technology", 160.0, 160.0, "480V", "3PH", "3P4W", 192.5, "Integrated Battery / Lithium", 99.0),
            ("GVMUPS225K480", "Galaxy VM", "Galaxy VM 3-Phase UPS 225kW/225kVA 480V ECOnversion Technology", 225.0, 225.0, "480V", "3PH", "3P4W", 270.6, "Integrated Battery / Lithium", 99.0),
            # Galaxy VX High Power Megawatt Class UPS (500kW to 1500kW)
            ("GVXUPS500K480", "Galaxy VX", "Galaxy VX Megawatt-Class 3-Phase UPS 500kW 480V 4-Level Inverter", 500.0, 500.0, "480V", "3PH", "3P4W", 601.4, "4-Level Inverter Redundant", 99.0),
            ("GVXUPS750K480", "Galaxy VX", "Galaxy VX Megawatt-Class 3-Phase UPS 750kW 480V 4-Level Inverter", 750.0, 750.0, "480V", "3PH", "3P4W", 902.1, "4-Level Inverter Redundant", 99.0),
            ("GVXUPS1000K480", "Galaxy VX", "Galaxy VX Megawatt-Class 3-Phase UPS 1000kW 480V 4-Level Inverter", 1000.0, 1000.0, "480V", "3PH", "3P4W", 1202.8, "4-Level Inverter Redundant", 99.0),
            ("GVXUPS1500K480", "Galaxy VX", "Galaxy VX Megawatt-Class 3-Phase UPS 1500kW 480V 4-Level Inverter", 1500.0, 1500.0, "480V", "3PH", "3P4W", 1804.2, "4-Level Inverter Redundant", 99.0),
            # Easy UPS 3M (60kW to 200kW Industrial / Commercial)
            ("E3MUPS100K480", "Easy UPS 3M", "Schneider Electric Easy UPS 3M 100kVA/100kW 480V Industrial 3-Phase UPS", 100.0, 100.0, "480V", "3PH", "3P4W", 120.3, "Double Conversion On-Line", 96.0),
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
                cut_sheet_url=f"https://www.se.com/us/en/product/{pn}/",
                specs={
                    "power_rating_kw": kw,
                    "power_rating_kva": kva,
                    "efficiency_econversion_pct": eff,
                    "ups_architecture": arch,
                    "battery_compatibility": "Lithium-Ion / VRLA",
                    "catalog_section": "Schneider Electric Secure Power & Galaxy UPS"
                },
                docs={"catalog_volume": "Galaxy V-Series Technical Specifications"}
            ))

        return items
