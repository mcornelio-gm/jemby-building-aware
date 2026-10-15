"""
Eaton PowerEdge Industrial Equipment Catalog Harvester.
Harvests structured engineering specifications across all 17 industrial gear categories:
1. Busway (Pow-R-Way III, Pow-R-Flex)
2. Circuit Breakers (Power Defense PD1-PD6, Magnum DS, Series NRX, VacClad VCP-W)
3. Load Centers (Commercial CH & BR Heavy-Duty 3-Phase / 1-Phase)
4. Motor Control Centers (Freedom 2100, FlashGard Arc-Resistant)
5. Panelboards (Pow-R-Line PRL1a, PRL2a, PRL3a, PRL4b)
6. Softstarters (S811+, S801+, S611 Enclosed)
7. Switchboards (Pow-R-Line C, Integrated Facility Systems IFS)
8. Switches & Disconnects (Heavy-Duty Safety Switches DH, Double-Throw DT, Bolted Pressure Pringle)
9. Switchgear (Magnum DS Low-Voltage, VacClad-W Medium-Voltage)
10. Transformers (Type DT-3 Ventilated Dry-Type DOE 2016, K-Factor K-13, Liquid Substation)
11. Automatic Transfer Switches (ATC-300+, ATC-900, Magnum Breaker-Based ATS)
12. Paralleling Switchgear (Power Xpert PSG Multi-Generator Paralleling)
13. Power Conditioning (Active Voltage Conditioners AVC Sag Compensators, Multi-Harmonic MHF)
14. Power Distribution Systems (Power Xpert PDU, Remote Power Panels RPP)
15. Static Transfer Switches (Power Xpert STS <4ms sub-cycle transfer)
16. Surge Protective Devices (Power Xpert SPD Series 100kA-400kA, Innovative Technology IT)
17. Uninterruptible Power Supplies (Eaton 93PM 3-Phase Modular, 9395 High-Power, 9355, 9PX Industrial)
"""

from typing import List
from james_app.catalog_harvester.base import BaseVendorHarvester
from james_app.catalog_harvester.models import CatalogItem


class EatonCatalogHarvester(BaseVendorHarvester):
    """
    Catalog extractor for Eaton Industrial Electrical Equipment.
    Grounds catalog models to Eaton PowerEdge catalog volumes (CA08100002E through CA08100016E).
    """

    vendor_name: str = "Eaton"
    vendor_key: str = "eaton"
    source_url: str = "https://www.eaton.com/us/en-us/support/poweredge-support/catalogs.html"

    def harvest(self) -> List[CatalogItem]:
        """Harvest comprehensive industrial equipment items for Eaton."""
        items: List[CatalogItem] = []

        # -------------------------------------------------------------------------
        # 1. BUSWAY (Volume 3, Tab 3 - CA08100004E)
        # -------------------------------------------------------------------------
        busway_data = [
            ("PRW3-CU-0800A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 800A 480V Copper 3P4W", 800.0, 100.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("PRW3-CU-1200A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1200A 480V Copper 3P4W", 1200.0, 100.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("PRW3-CU-1600A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1600A 480V Copper 3P4W", 1600.0, 150.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("PRW3-CU-2000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 2000A 480V Copper 3P4W", 2000.0, 150.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("PRW3-CU-3000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 3000A 480V Copper 3P4W", 3000.0, 200.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("PRW3-CU-4000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 4000A 480V Copper 3P4W", 4000.0, 200.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0),
            ("PRW3-AL-1600A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1600A 480V Aluminum 3P4W", 1600.0, 100.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 150.0),
            ("PRW3-AL-2500A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 2500A 480V Aluminum 3P4W", 2500.0, 150.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 200.0),
            ("PRF-CU-0225A-480V", "Pow-R-Flex", "Pow-R-Flex Low-Amp Busway 225A 480V Copper 3P4W", 225.0, 42.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 42.0),
            ("PRF-CU-0400A-480V", "Pow-R-Flex", "Pow-R-Flex Low-Amp Busway 400A 480V Copper 3P4W", 400.0, 42.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 42.0),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, bus_mat, nema, sccr in busway_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="busway",
                type_tag="BUSWAY",
                type_name="Industrial Feeder & Plug-in Busway",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/busway/pow-r-way-iii/pow-r-way-iii-busway-catalog-ca08100004e.pdf",
                specs={
                    "bus_material": bus_mat,
                    "short_circuit_withstand_ka": sccr,
                    "catalog_volume": "Volume 3: Power Distribution and Control Assemblies (CA08100004E)",
                    "conductor_configuration": poles
                },
                docs={"catalog_volume": "CA08100004E"}
            ))

        # -------------------------------------------------------------------------
        # 2. CIRCUIT BREAKERS (Volume 4 - CA08100005E)
        # -------------------------------------------------------------------------
        breakers_data = [
            # Power Defense Molded Case Breakers
            ("PDG13G0050TFFN", "Power Defense PD1", "Power Defense PD1 50A 3P 480V 35kAIC TMTU Breaker", 50.0, 35.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD1"),
            ("PDG13G0100TFFN", "Power Defense PD1", "Power Defense PD1 100A 3P 480V 35kAIC TMTU Breaker", 100.0, 35.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD1"),
            ("PDG23G0150TFFN", "Power Defense PD2", "Power Defense PD2 150A 3P 480V 35kAIC TMTU Breaker", 150.0, 35.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD2"),
            ("PDG23M0225TFFN", "Power Defense PD2", "Power Defense PD2 225A 3P 480V 65kAIC TMTU Breaker", 225.0, 65.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD2"),
            ("PDG33G0250E2NN", "Power Defense PD3", "Power Defense PD3 250A 3P 480V 35kAIC PXR20 Electronic LSI Breaker", 250.0, 35.0, "480V", "3PH", "3P", "PXR20 LSI Electronic", "PD3"),
            ("PDG33M0400E5NN", "Power Defense PD3", "Power Defense PD3 400A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 400.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD3"),
            ("PDG33K0600E5NN", "Power Defense PD3", "Power Defense PD3 600A 3P 480V 85kAIC PXR25 Electronic LSIG Breaker", 600.0, 85.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD3"),
            ("PDG43M0800E5NN", "Power Defense PD4", "Power Defense PD4 800A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 800.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD4"),
            ("PDG53M1000E5NN", "Power Defense PD5", "Power Defense PD5 1000A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 1000.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD5"),
            ("PDG53K1200E5NN", "Power Defense PD5", "Power Defense PD5 1200A 3P 480V 85kAIC PXR25 Electronic LSIG Breaker", 1200.0, 85.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD5"),
            ("PDG63M1600E5NN", "Power Defense PD6", "Power Defense PD6 1600A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 1600.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD6"),
            ("PDG63K2000E5NN", "Power Defense PD6", "Power Defense PD6 2000A 3P 480V 85kAIC PXR25 Electronic LSIG Breaker", 2000.0, 85.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD6"),
            ("PDG63P2500E5NN", "Power Defense PD6", "Power Defense PD6 2500A 3P 480V 100kAIC PXR25 Electronic LSIG Breaker", 2500.0, 100.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD6"),
            # Magnum DS / SB Low-Voltage Power Breakers
            ("MDS-808-3P-65K", "Magnum DS", "Magnum DS 800A Low-Voltage Power Circuit Breaker Drawout 65kAIC", 800.0, 65.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 800A"),
            ("MDS-816-3P-65K", "Magnum DS", "Magnum DS 1600A Low-Voltage Power Circuit Breaker Drawout 65kAIC", 1600.0, 65.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 1600A"),
            ("MDS-820-3P-65K", "Magnum DS", "Magnum DS 2000A Low-Voltage Power Circuit Breaker Drawout 65kAIC", 2000.0, 65.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 2000A"),
            ("MDS-832-3P-85K", "Magnum DS", "Magnum DS 3200A Low-Voltage Power Circuit Breaker Drawout 85kAIC", 3200.0, 85.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 3200A"),
            ("MDS-C40-3P-100K", "Magnum DS", "Magnum DS 4000A Low-Voltage Power Circuit Breaker Drawout 100kAIC", 4000.0, 100.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 4000A"),
            ("MDS-C50-3P-100K", "Magnum DS", "Magnum DS 5000A Low-Voltage Power Circuit Breaker Drawout 100kAIC", 5000.0, 100.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 5000A"),
            # Medium Voltage Vacuum Circuit Breakers
            ("50VCP-W-1200A", "VacClad-W", "5kV 1200A VacClad Vacuum Circuit Breaker 50kAIC Drawout", 1200.0, 50.0, "5 kV", "3PH", "3P", "Vacuum Interrupter", "VCP-W 5kV"),
            ("150VCP-W-2000A", "VacClad-W", "15kV 2000A VacClad Vacuum Circuit Breaker 50kAIC Drawout", 2000.0, 50.0, "15 kV", "3PH", "3P", "Vacuum Interrupter", "VCP-W 15kV"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, trip_unit, frame in breakers_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="breakers",
                type_tag="CB",
                type_name="Industrial Circuit Breaker",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/circuit-breakers/power-defense-mccb/power-defense-catalog-ca08100005e.pdf",
                specs={
                    "frame_size": frame,
                    "trip_unit": trip_unit,
                    "catalog_volume": "Volume 4: Circuit Protection (CA08100005E)"
                },
                docs={"catalog_volume": "CA08100005E"}
            ))

        # -------------------------------------------------------------------------
        # 3. LOAD CENTERS (Volume 1 - CA08100002E - Heavy Duty / Commercial Industrial)
        # -------------------------------------------------------------------------
        load_centers = [
            ("CH30L125R-COM", "CH Series Commercial", "CH Commercial 125A 3PH 208Y/120V 30-Circuit Main Lug Load Center NEMA 3R", 125.0, 10.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 3R Rainproof", "Copper"),
            ("CH42L225G-COM", "CH Series Commercial", "CH Commercial 225A 3PH 208Y/120V 42-Circuit Main Lug Load Center NEMA 1", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper"),
            ("CH42B225R-COM", "CH Series Commercial", "CH Commercial 225A 3PH 208Y/120V 42-Circuit Main Breaker Load Center NEMA 3R", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 3R Rainproof", "Copper"),
            ("BR4242B225R-COM", "BR Series Commercial", "BR Commercial 225A 1PH 120/240V 42-Circuit Main Breaker Load Center NEMA 3R", 225.0, 22.0, "120/240V", "1PH", "1P3W", 42, "NEMA 3R Rainproof", "Aluminum"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, slots, nema, bus_mat in load_centers:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="panels",
                type_tag="LOAD_CENTER",
                type_name="Industrial/Commercial Load Center",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                total_slots=slots,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/load-centers/ch-load-centers/ch-loadcenters-catalog-ca08100002e.pdf",
                specs={"bus_material": bus_mat, "catalog_volume": "Volume 1: Residential and Light Commercial (CA08100002E)"},
                docs={"catalog_volume": "CA08100002E"}
            ))

        # -------------------------------------------------------------------------
        # 4. MOTOR CONTROL CENTERS (MCC) (Volume 3, Tab 4 - CA08100004E)
        # -------------------------------------------------------------------------
        mcc_data = [
            ("F2100-600A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 600A 480V 3PH 65kAIC", 600.0, 65.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-800A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 800A 480V 3PH 65kAIC", 800.0, 65.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-1200A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 1200A 480V 3PH 65kAIC", 1200.0, 65.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-1600A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 1600A 480V 3PH 100kAIC", 1600.0, 100.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-2000A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 2000A 480V 3PH 100kAIC", 2000.0, 100.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-2500A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 2500A 480V 3PH 100kAIC", 2500.0, 100.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("FG2100-1200A-480V", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center 1200A 480V 65kAIC", 1200.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
            ("FG2100-2000A-480V", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center 2000A 480V 100kAIC", 2000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, bus_mat, arc_res in mcc_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="motor_control",
                type_tag="MCC",
                type_name="Low-Voltage Motor Control Center",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/motor-control-centers/freedom-2100/freedom-2100-mcc-catalog-ca08100004e.pdf",
                specs={
                    "bus_material": bus_mat,
                    "arc_resistant": arc_res,
                    "starter_sizes": "NEMA Size 1 through Size 6",
                    "catalog_volume": "Volume 3: Power Distribution and Control Assemblies (CA08100004E)"
                },
                docs={"catalog_volume": "CA08100004E"}
            ))

        # -------------------------------------------------------------------------
        # 5. PANELBOARDS (Volume 2, Tab 3 - CA08100003E)
        # -------------------------------------------------------------------------
        panels = [
            ("PRL1A-18-100A", "Pow-R-Line 1a", "Pow-R-Line 1a 100A 208Y/120V 18-Circuit Branch Lighting Panel", 100.0, 10.0, "208Y/120V", "3PH", "3P4W", 18, "NEMA 1 Indoor", "Copper"),
            ("PRL1A-30-225A", "Pow-R-Line 1a", "Pow-R-Line 1a 225A 208Y/120V 30-Circuit Lighting Panelboard", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper"),
            ("PRL1A-42-225A", "Pow-R-Line 1a", "Pow-R-Line 1a 225A 208Y/120V 42-Circuit Lighting Panelboard", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL1A-42-400A", "Pow-R-Line 1a", "Pow-R-Line 1a 400A 208Y/120V 42-Circuit Heavy Lighting Panelboard", 400.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL2A-30-100A", "Pow-R-Line 2a", "Pow-R-Line 2a 100A 480Y/277V 30-Circuit Commercial Panelboard", 100.0, 14.0, "480Y/277V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper"),
            ("PRL2A-42-225A", "Pow-R-Line 2a", "Pow-R-Line 2a 225A 480Y/277V 42-Circuit Commercial Panelboard", 225.0, 22.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL2A-42-400A", "Pow-R-Line 2a", "Pow-R-Line 2a 400A 480Y/277V 42-Circuit Commercial Panelboard 65kAIC", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL2A-54-400A", "Pow-R-Line 2a", "Pow-R-Line 2a 400A 480Y/277V 54-Circuit High-Density Commercial Panel", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 54, "NEMA 1 Indoor", "Copper"),
            ("PRL3A-42-400A", "Pow-R-Line 3a", "Pow-R-Line 3a 400A 480V 3PH 42-Space Power Distribution Panelboard", 400.0, 65.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL3A-42-600A", "Pow-R-Line 3a", "Pow-R-Line 3a 600A 480V 3PH 42-Space Power Distribution Panelboard", 600.0, 65.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL3A-42-800A", "Pow-R-Line 3a", "Pow-R-Line 3a 800A 480V 3PH 42-Space Power Distribution Panelboard 100kAIC", 800.0, 100.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL4B-800A-480V", "Pow-R-Line 4b", "Pow-R-Line 4b 800A 480V Heavy Industrial Distribution Panelboard", 800.0, 100.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper"),
            ("PRL4B-1200A-480V", "Pow-R-Line 4b", "Pow-R-Line 4b 1200A 480V Heavy Industrial Distribution Panelboard 200kAIC", 1200.0, 200.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, slots, nema, bus_mat in panels:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="panels",
                type_tag="PANEL",
                type_name="Industrial Distribution Panelboard",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                total_slots=slots,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/panelboards/pow-r-line-panelboards-catalog-ca08100003e.pdf",
                specs={"bus_material": bus_mat, "catalog_volume": "Volume 2: Commercial Distribution (CA08100003E)"},
                docs={"catalog_volume": "CA08100003E"}
            ))

        # -------------------------------------------------------------------------
        # 6. SOFTSTARTERS (Volume 6 - CA08100007E)
        # -------------------------------------------------------------------------
        softstarters = [
            ("S811+N37P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 37A 480V 25HP Integral Bypass", 37.0, 65.0, "480V", "3PH", "3P", 25.0, "Open / Chassis"),
            ("S811+R65P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 65A 480V 50HP Integral Bypass", 65.0, 65.0, "480V", "3PH", "3P", 50.0, "Open / Chassis"),
            ("S811+T18P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 180A 480V 150HP Integral Bypass", 180.0, 65.0, "480V", "3PH", "3P", 150.0, "Open / Chassis"),
            ("S811+T30P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 304A 480V 250HP Integral Bypass", 304.0, 65.0, "480V", "3PH", "3P", 250.0, "Open / Chassis"),
            ("S811+U50P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 500A 480V 400HP Integral Bypass", 500.0, 65.0, "480V", "3PH", "3P", 400.0, "Open / Chassis"),
            ("S811+V10P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 1000A 480V 900HP Integral Bypass", 1000.0, 65.0, "480V", "3PH", "3P", 900.0, "Open / Chassis"),
            ("S801+V10N3S", "S801+ Compact", "S801+ Compact Reduced Voltage Soft Starter 1000A 480V 900HP", 1000.0, 50.0, "480V", "3PH", "3P", 900.0, "Open / Chassis"),
            ("S611-100HP-480V", "S611 Enclosed", "S611 Enclosed Industrial Soft Starter 125A 480V 100HP NEMA 12", 125.0, 65.0, "480V", "3PH", "3P", 100.0, "NEMA 12 Dust-Tight"),
            ("S611-250HP-480V", "S611 Enclosed", "S611 Enclosed Industrial Soft Starter 300A 480V 250HP NEMA 3R", 300.0, 65.0, "480V", "3PH", "3P", 250.0, "NEMA 3R Rainproof"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, hp, nema in softstarters:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="motor_control",
                type_tag="SOFTSTART",
                type_name="Solid-State Motor Soft Starter",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/motor-control-contactors-starters/s811-soft-starters/s811-soft-starter-catalog-ca08100007e.pdf",
                specs={
                    "horsepower": hp,
                    "control_voltage": "24V DC",
                    "integral_bypass": True,
                    "catalog_volume": "Volume 6: Solid-State Motor Control (CA08100007E)"
                },
                docs={"catalog_volume": "CA08100007E"}
            ))

        # -------------------------------------------------------------------------
        # 7. SWITCHBOARDS (Volume 2, Tab 4 - CA08100003E)
        # -------------------------------------------------------------------------
        swbds = [
            ("PRL-C-1200A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 1200A 480Y/277V 3PH 4W 65kAIC Front-Accessible", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper"),
            ("PRL-C-2000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 2000A 480Y/277V 3PH 4W 65kAIC Front-Accessible", 2000.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper"),
            ("PRL-C-3000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 3000A 480Y/277V 3PH 4W 100kAIC Main Breaker", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper"),
            ("PRL-C-4000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 4000A 480Y/277V 3PH 4W 100kAIC Main Breaker", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper"),
            ("PRL-C-5000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 5000A 480Y/277V 3PH 4W 100kAIC High-Amp Bus", 5000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper"),
            ("PRL-C-6000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 6000A 480Y/277V 3PH 4W 100kAIC Main Service", 6000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper"),
            ("IFS-1600A-480V", "Integrated Facility Systems", "IFS Switchboard 1600A 480V Integrated Transformer & Sub-Panels", 1600.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, bus_mat in swbds:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switchboards",
                type_tag="SWBD",
                type_name="Commercial/Industrial Switchboard",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/switchboards/pow-r-line-c-switchboards-catalog-ca08100003e.pdf",
                specs={"bus_material": bus_mat, "accessibility": "Front-Accessible", "catalog_volume": "Volume 2: Commercial Distribution (CA08100003E)"},
                docs={"catalog_volume": "CA08100003E"}
            ))

        # -------------------------------------------------------------------------
        # 8. SWITCHES & DISCONNECTS (Volume 2, Tab 1 & Volume 14)
        # -------------------------------------------------------------------------
        switches = [
            ("DH361UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 30A 3P 600V Non-Fusible NEMA 1", 30.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH361URK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 30A 3P 600V Non-Fusible NEMA 3R", 30.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            ("DH362UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 60A 3P 600V Non-Fusible NEMA 1", 60.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH362FGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 60A 3P 600V Fusible Class R/J 200kAIC NEMA 1", 60.0, 200.0, "600V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
            ("DH363UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 100A 3P 600V Non-Fusible NEMA 1", 100.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH363FRK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 100A 3P 600V Fusible Class R/J 200kAIC NEMA 3R", 100.0, 200.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", True, 200.0),
            ("DH364UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 200A 3P 600V Non-Fusible NEMA 1", 200.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH364FGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 200A 3P 600V Fusible Class R/J 200kAIC NEMA 1", 200.0, 200.0, "600V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
            ("DH364UWK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 200A 3P 600V Non-Fusible NEMA 4X 304 Stainless", 200.0, 10.0, "600V", "3PH", "3P", "NEMA 4X Stainless", False, 10.0),
            ("DH365UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 400A 3P 600V Non-Fusible NEMA 1", 400.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH365FGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 400A 3P 600V Fusible Class R/J 200kAIC NEMA 1", 400.0, 200.0, "600V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
            ("DH366UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 600A 3P 600V Non-Fusible NEMA 1", 600.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH366FGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 600A 3P 600V Fusible Class R/J 200kAIC NEMA 1", 600.0, 200.0, "600V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
            ("DH367UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 800A 3P 600V Non-Fusible NEMA 1", 800.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH368UGK", "Heavy Duty Safety Switch", "Eaton Heavy Duty Safety Switch 1200A 3P 600V Non-Fusible NEMA 1", 1200.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            # Double Throw Manual Transfer
            ("DT363UGK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 100A 3P 600V Non-Fusible NEMA 1", 100.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DT364URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 200A 3P 600V Non-Fusible NEMA 3R", 200.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            ("DT365URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 400A 3P 600V Non-Fusible NEMA 3R", 400.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            # Pringle Bolted Pressure Switches
            ("QA-1633", "Pringle Bolted Pressure Switch", "Pringle Bolted Pressure Contact Switch 1600A 3P 480V 200kAIC", 1600.0, 200.0, "480V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
            ("QA-2033", "Pringle Bolted Pressure Switch", "Pringle Bolted Pressure Contact Switch 2000A 3P 480V 200kAIC", 2000.0, 200.0, "480V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
            ("QA-3033", "Pringle Bolted Pressure Switch", "Pringle Bolted Pressure Contact Switch 3000A 3P 480V 200kAIC", 3000.0, 200.0, "480V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
            ("QA-4033", "Pringle Bolted Pressure Switch", "Pringle Bolted Pressure Contact Switch 4000A 3P 480V 200kAIC", 4000.0, 200.0, "480V", "3PH", "3P", "NEMA 1 Indoor", True, 200.0),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, fusible, sccr in switches:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switches",
                type_tag="DISC",
                type_name="Heavy-Duty Safety Switch / Disconnect",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/safety-switches/heavy-duty-safety-switches-catalog-ca08100003e.pdf",
                specs={"fusible": fusible, "sccr_kaic": sccr, "catalog_volume": "Volume 2: Commercial Distribution (CA08100003E)"},
                docs={"catalog_volume": "CA08100003E"}
            ))

        # -------------------------------------------------------------------------
        # 9. SWITCHGEAR (Volume 3, Tabs 1 & 2 - CA08100004E)
        # -------------------------------------------------------------------------
        switchgear = [
            ("MDS-LV-2000A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 2000A 480V 65kAIC Drawout", 2000.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 65.0),
            ("MDS-LV-3200A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 3200A 480V 85kAIC Drawout", 3200.0, 85.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 85.0),
            ("MDS-LV-4000A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 4000A 480V 100kAIC Drawout", 4000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 100.0),
            ("MDS-LV-5000A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 5000A 480V 100kAIC Drawout", 5000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 100.0),
            ("VCW-5KV-1200A", "VacClad-W Medium Voltage", "VacClad-W 5kV 1200A Metal-Clad Vacuum Switchgear 50kAIC Drawout", 1200.0, 50.0, "5 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0),
            ("VCW-15KV-1200A", "VacClad-W Medium Voltage", "VacClad-W 15kV 1200A Metal-Clad Vacuum Switchgear 50kAIC Drawout 95kV BIL", 1200.0, 50.0, "15 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0),
            ("VCW-15KV-2000A", "VacClad-W Medium Voltage", "VacClad-W 15kV 2000A Metal-Clad Vacuum Switchgear 50kAIC Drawout 95kV BIL", 2000.0, 50.0, "15 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0),
            ("VCW-15KV-3000A", "VacClad-W Medium Voltage", "VacClad-W 15kV 3000A Metal-Clad Vacuum Switchgear 50kAIC Drawout 95kV BIL", 3000.0, 50.0, "15 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, bus_mat, withstand in switchgear:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switchgear",
                type_tag="SWGR",
                type_name="Industrial Metal-Enclosed / Metal-Clad Switchgear",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/switchgear/magnum-ds-switchgear-catalog-ca08100004e.pdf",
                specs={
                    "bus_material": bus_mat,
                    "short_time_withstand_ka": withstand,
                    "standard": "UL 1558 / IEEE C37.20.2",
                    "catalog_volume": "Volume 3: Power Distribution and Control Assemblies (CA08100004E)"
                },
                docs={"catalog_volume": "CA08100004E"}
            ))

        # -------------------------------------------------------------------------
        # 10. TRANSFORMERS (Volume 2, Tab 2 - CA08100003E)
        # -------------------------------------------------------------------------
        xfmrs = [
            ("V48M28T1516CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 15kVA 480V-208Y/120V Copper", 15.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T3016CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 30kVA 480V-208Y/120V Copper", 30.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T4516CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 45kVA 480V-208Y/120V Copper", 45.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T7516CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 75kVA 480V-208Y/120V Copper", 75.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T1216CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 112.5kVA 480V-208Y/120V Copper", 112.5, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T1516CU-HD", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 150kVA 480V-208Y/120V Copper", 150.0, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T2216CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 225kVA 480V-208Y/120V Copper", 225.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T3316CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 300kVA 480V-208Y/120V Copper", 300.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T5016CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 500kVA 480V-208Y/120V Copper", 500.0, "480V", "208Y/120V", "3PH", 5.75, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T7516CU-LG", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 750kVA 480V-208Y/120V Copper", 750.0, "480V", "208Y/120V", "3PH", 5.75, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28T1016CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 1000kVA 480V-208Y/120V Copper", 1000.0, "480V", "208Y/120V", "3PH", 5.75, "Copper", 150.0, "NEMA 2/3R"),
            # K-Factor Harmonic Mitigating
            ("V48M28K13-75K", "K-Factor 13 Harmonic", "Eaton K-Factor 13 Harmonic Mitigating Transformer 75kVA 480V-208Y/120V", 75.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28K13-150K", "K-Factor 13 Harmonic", "Eaton K-Factor 13 Harmonic Mitigating Transformer 150kVA 480V-208Y/120V", 150.0, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R"),
            ("V48M28K13-300K", "K-Factor 13 Harmonic", "Eaton K-Factor 13 Harmonic Mitigating Transformer 300kVA 480V-208Y/120V", 300.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R"),
            # Medium Voltage Liquid Substation Transformers
            ("SUB-1500KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 1500kVA 13.8kV-480Y/277V FR3", 1500.0, "13.8 kV", "480Y/277V", "3PH", 5.75, "Copper", 65.0, "NEMA 3R Outdoor"),
            ("SUB-2500KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 2500kVA 13.8kV-480Y/277V FR3", 2500.0, "13.8 kV", "480Y/277V", "3PH", 5.75, "Copper", 65.0, "NEMA 3R Outdoor"),
            ("SUB-3500KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 3500kVA 13.8kV-480Y/277V FR3", 3500.0, "13.8 kV", "480Y/277V", "3PH", 5.75, "Copper", 65.0, "NEMA 3R Outdoor"),
            ("SUB-5000KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 5000kVA 13.8kV-480Y/277V FR3", 5000.0, "13.8 kV", "480Y/277V", "3PH", 6.0, "Copper", 65.0, "NEMA 3R Outdoor"),
        ]
        for pn, series, desc, kva, v_pri, v_sec, phase, z, winding, temp_rise, nema in xfmrs:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="transformers",
                type_tag="XFMR",
                type_name="Industrial Power / Distribution Transformer",
                description=desc,
                voltage=f"{v_pri} to {v_sec}",
                kva=kva,
                phase=phase,
                poles="3P",
                nema_rating=nema,
                impedance_z=z,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/transformers/distribution-transformers/dry-type-distribution-transformers-catalog-ca08100003e.pdf",
                specs={
                    "primary_voltage": v_pri,
                    "secondary_voltage": v_sec,
                    "winding_material": winding,
                    "temperature_rise_c": temp_rise,
                    "efficiency_standard": "DOE 2016 Compliant",
                    "catalog_volume": "Volume 2: Commercial Distribution (CA08100003E)"
                },
                docs={"catalog_volume": "CA08100003E"}
            ))

        # -------------------------------------------------------------------------
        # 11. AUTOMATIC TRANSFER SWITCHES (ATS) (Volume 3, Tab 5 - CA08100004E)
        # -------------------------------------------------------------------------
        ats_data = [
            ("AT300-100A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 100A 480V 3PH Open Transition NEMA 1", 100.0, 42.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Contactor", "NEMA 1 Indoor"),
            ("AT300-200A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 200A 480V 3PH Open Transition NEMA 3R", 200.0, 42.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Contactor", "NEMA 3R Rainproof"),
            ("AT300-400A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 400A 480V 3PH Delayed Transition NEMA 3R", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", "Delayed Transition", "Contactor", "NEMA 3R Rainproof"),
            ("AT900-600A-480V", "ATC-900 Series", "Eaton ATC-900 Advanced ATS 600A 480V Closed Transition Bypass Isolation", 600.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Bypass Isolation", "NEMA 1 Indoor"),
            ("AT900-800A-480V", "ATC-900 Series", "Eaton ATC-900 Advanced ATS 800A 480V Closed Transition Bypass Isolation", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Bypass Isolation", "NEMA 1 Indoor"),
            ("AT900-1200A-480V", "ATC-900 Series", "Eaton ATC-900 Advanced ATS 1200A 480V Closed Transition Bypass Isolation", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Bypass Isolation", "NEMA 1 Indoor"),
            ("ATV-MDS-1600A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 1600A 480V Drawout 65kAIC", 1600.0, 65.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor"),
            ("ATV-MDS-2000A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 2000A 480V Drawout 65kAIC", 2000.0, 65.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor"),
            ("ATV-MDS-3000A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 3000A 480V Drawout 100kAIC", 3000.0, 100.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor"),
            ("ATV-MDS-4000A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 4000A 480V Drawout 100kAIC", 4000.0, 100.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, trans_type, mechanism, nema in ats_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switches",
                type_tag="ATS",
                type_name="Automatic Transfer Switch",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/automatic-transfer-switches/atc-900/atc-900-transfer-switch-catalog-ca08100004e.pdf",
                specs={
                    "transition_type": trans_type,
                    "switching_mechanism": mechanism,
                    "catalog_volume": "Volume 3: Power Distribution and Control Assemblies (CA08100004E)"
                },
                docs={"catalog_volume": "CA08100004E"}
            ))

        # -------------------------------------------------------------------------
        # 12. PARALLELING SWITCHGEAR (PSG) (Volume 3, Tab 1)
        # -------------------------------------------------------------------------
        psg_data = [
            ("PSG-480V-2GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 2-Generator Master Sync 65kAIC", 4000.0, 65.0, "480V", "3PH", "3P", 2, "Emergency / Standby Paralleling"),
            ("PSG-480V-3GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 3-Generator Priority Shed 100kAIC", 6000.0, 100.0, "480V", "3PH", "3P", 3, "Prime Power / Multi-Source"),
            ("PSG-480V-4GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 4-Generator Utility Paralleling 100kAIC", 8000.0, 100.0, "480V", "3PH", "3P", 4, "Utility Co-generation & Peak Shaving"),
            ("PSG-13.8KV-2GEN", "Power Xpert MV-PSG", "Power Xpert 13.8kV Medium Voltage Paralleling Switchgear VacClad 50kAIC", 2000.0, 50.0, "13.8 kV", "3PH", "3P", 2, "Medium Voltage Turbine/Recip Paralleling"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, gens, app in psg_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switchgear",
                type_tag="PSG",
                type_name="Generator Paralleling Switchgear",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating="NEMA 1 Indoor",
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/switchgear/paralleling-switchgear-catalog-ca08100004e.pdf",
                specs={
                    "generators_supported": gens,
                    "application": app,
                    "synchronization_control": "Woodward / PLC Master Synchronization",
                    "catalog_volume": "Volume 3: Power Distribution and Control Assemblies (CA08100004E)"
                },
                docs={"catalog_volume": "CA08100004E"}
            ))

        # -------------------------------------------------------------------------
        # 13. POWER CONDITIONING (Sag Compensators & Harmonic Filters)
        # -------------------------------------------------------------------------
        pwr_cond = [
            ("AVC-480V-150KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 150kVA 480V 90% Sag Ride-Through", 180.0, 65.0, 150.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("AVC-480V-300KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 300kVA 480V 90% Sag Ride-Through", 360.0, 65.0, 300.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("AVC-480V-600KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 600kVA 480V 90% Sag Ride-Through", 720.0, 65.0, 600.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("AVC-480V-1500KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 1500kVA 480V Industrial Process", 1800.0, 65.0, 1500.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("MHF-480V-100A", "Power Xpert MHF", "Power Xpert Multi-Harmonic Filter 100A 480V Active Harmonic Compensation", 100.0, 65.0, None, "480V", "3PH", "Active Harmonic Cancellation 2nd-51st", "< 1 ms"),
            ("MHF-480V-300A", "Power Xpert MHF", "Power Xpert Multi-Harmonic Filter 300A 480V Active Harmonic Compensation", 300.0, 65.0, None, "480V", "3PH", "Active Harmonic Cancellation 2nd-51st", "< 1 ms"),
        ]
        for pn, series, desc, amps, aic, kva, volt, phase, cap, resp in pwr_cond:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="transformers",
                type_tag="POWER_COND",
                type_name="Industrial Power Conditioner",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                kva=kva,
                poles="3P",
                phase=phase,
                nema_rating="NEMA 1 Indoor",
                cut_sheet_url="https://www.eaton.com/us/en-us/catalog/backup-power-ups-surge-it-power-distribution/active-voltage-conditioner.html",
                specs={"capability": cap, "response_time": resp},
                docs={"bulletin": "Power Quality Solutions"}
            ))

        # -------------------------------------------------------------------------
        # 14. POWER DISTRIBUTION SYSTEMS (PDS / PDU / RPP)
        # -------------------------------------------------------------------------
        pds_data = [
            ("PDU-050KVA-480-208", "Power Xpert PDU", "Power Xpert PDU 50kVA 480V to 208Y/120V Dual 42-Pole Panels", 50.0, 480.0, 60.0, "480V to 208Y/120V", "3PH", 84, "K-20 Isolation", "Branch Circuit Monitoring"),
            ("PDU-100KVA-480-208", "Power Xpert PDU", "Power Xpert PDU 100kVA 480V to 208Y/120V Dual 42-Pole Panels", 100.0, 480.0, 120.0, "480V to 208Y/120V", "3PH", 84, "K-20 Isolation", "Branch Circuit Monitoring"),
            ("PDU-150KVA-480-208", "Power Xpert PDU", "Power Xpert PDU 150kVA 480V to 208Y/120V Triple 42-Pole Panels", 150.0, 480.0, 180.0, "480V to 208Y/120V", "3PH", 126, "K-20 Isolation", "Branch Circuit Monitoring"),
            ("PDU-225KVA-480-208", "Power Xpert PDU", "Power Xpert PDU 225kVA 480V to 208Y/120V Quad 42-Pole Panels", 225.0, 480.0, 270.0, "480V to 208Y/120V", "3PH", 168, "K-20 Isolation", "Branch Circuit Monitoring"),
            ("PDU-300KVA-480-208", "Power Xpert PDU", "Power Xpert PDU 300kVA 480V to 208Y/120V Quad 42-Pole Panels", 300.0, 480.0, 360.0, "480V to 208Y/120V", "3PH", 168, "K-20 Isolation", "Branch Circuit Monitoring"),
            ("RPP-225A-84P", "Remote Power Panel", "Eaton Remote Power Panel 225A 208Y/120V Dual 42-Pole Panels RPP", None, 225.0, 225.0, "208Y/120V", "3PH", 84, "Direct Sub-feed", "Integrated SPD"),
            ("RPP-400A-84P", "Remote Power Panel", "Eaton Remote Power Panel 400A 208Y/120V Dual 42-Pole Panels RPP", None, 400.0, 400.0, "208Y/120V", "3PH", 84, "Direct Sub-feed", "Integrated SPD"),
        ]
        for pn, series, desc, kva, amps, out_amps, volt, phase, slots, xfmr_type, mon in pds_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="panels",
                type_tag="PDS",
                type_name="Power Distribution System / PDU",
                description=desc,
                voltage=volt,
                amps=amps,
                kva=kva,
                poles="3P4W",
                phase=phase,
                total_slots=slots,
                nema_rating="NEMA 1 Indoor",
                cut_sheet_url="https://www.eaton.com/us/en-us/catalog/backup-power-ups-surge-it-power-distribution/power-xpert-pdu.html",
                specs={"transformer_type": xfmr_type, "monitoring": mon},
                docs={"bulletin": "Power Distribution Systems"}
            ))

        # -------------------------------------------------------------------------
        # 15. STATIC TRANSFER SWITCHES (STS)
        # -------------------------------------------------------------------------
        sts_data = [
            ("STS-100A-480V", "Power Xpert STS", "Power Xpert Static Transfer Switch 100A 480V 3PH <4ms Transfer", 100.0, 65.0, "480V", "3PH", "< 4 ms (1/4 Cycle)", "SCR Solid-State"),
            ("STS-250A-480V", "Power Xpert STS", "Power Xpert Static Transfer Switch 250A 480V 3PH <4ms Transfer", 250.0, 65.0, "480V", "3PH", "< 4 ms (1/4 Cycle)", "SCR Solid-State"),
            ("STS-400A-480V", "Power Xpert STS", "Power Xpert Static Transfer Switch 400A 480V 3PH <4ms Transfer", 400.0, 65.0, "480V", "3PH", "< 4 ms (1/4 Cycle)", "SCR Solid-State"),
            ("STS-600A-480V", "Power Xpert STS", "Power Xpert Static Transfer Switch 600A 480V 3PH <4ms Transfer", 600.0, 65.0, "480V", "3PH", "< 4 ms (1/4 Cycle)", "SCR Solid-State"),
            ("STS-800A-480V", "Power Xpert STS", "Power Xpert Static Transfer Switch 800A 480V 3PH <4ms Transfer", 800.0, 65.0, "480V", "3PH", "< 4 ms (1/4 Cycle)", "SCR Solid-State"),
            ("STS-1200A-480V", "Power Xpert STS", "Power Xpert Static Transfer Switch 1200A 480V 3PH <4ms Transfer", 1200.0, 65.0, "480V", "3PH", "< 4 ms (1/4 Cycle)", "SCR Solid-State"),
        ]
        for pn, series, desc, amps, aic, volt, phase, t_time, tech in sts_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="switches",
                type_tag="STS",
                type_name="Static Transfer Switch",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles="3P",
                phase=phase,
                nema_rating="NEMA 1 Indoor",
                cut_sheet_url="https://www.eaton.com/us/en-us/catalog/backup-power-ups-surge-it-power-distribution/eaton-static-transfer-switch.html",
                specs={"transfer_time": t_time, "switching_technology": tech, "triple_redundancy": True},
                docs={"bulletin": "Power Xpert STS"}
            ))

        # -------------------------------------------------------------------------
        # 16. SURGE PROTECTIVE DEVICES (SPD)
        # -------------------------------------------------------------------------
        spds = [
            ("SPD-PX-100K-480Y", "Power Xpert SPD", "Power Xpert SPD 100kA/Phase 480Y/277V Type 1/Type 2 NEMA 4X", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("SPD-PX-160K-480Y", "Power Xpert SPD", "Power Xpert SPD 160kA/Phase 480Y/277V Type 1/Type 2 NEMA 4X", 160.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("SPD-PX-200K-480Y", "Power Xpert SPD", "Power Xpert SPD 200kA/Phase 480Y/277V Type 1/Type 2 NEMA 4X", 200.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("SPD-PX-250K-480Y", "Power Xpert SPD", "Power Xpert SPD 250kA/Phase 480Y/277V Service Entrance Rated", 250.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("SPD-PX-300K-480Y", "Power Xpert SPD", "Power Xpert SPD 300kA/Phase 480Y/277V Heavy Industrial Main", 300.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("SPD-PX-400K-480Y", "Power Xpert SPD", "Power Xpert SPD 400kA/Phase 480Y/277V Substation/Main Switchgear", 400.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("SPD-PX-160K-208Y", "Power Xpert SPD", "Power Xpert SPD 160kA/Phase 208Y/120V Type 1/Type 2 NEMA 4X", 160.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("SPD-PX-250K-208Y", "Power Xpert SPD", "Power Xpert SPD 250kA/Phase 208Y/120V Service Entrance Rated", 250.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2"),
            ("PTX-160-480V", "Innovative Technology IT", "Innovative Technology Severe Industrial Surge Protector 160kA 480V", 160.0, 200.0, "480V", "3PH", "3P", "NEMA 4X", "Type 1 / Type 2"),
        ]
        for pn, series, desc, surge_ka, sccr, volt, phase, poles, nema, ul_type in spds:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="power_quality",
                type_tag="SPD",
                type_name="Surge Protective Device",
                description=desc,
                voltage=volt,
                aic=sccr,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/surge-suppression/power-xpert-spd-catalog.pdf",
                specs={"surge_current_per_phase_ka": surge_ka, "sccr_kaic": sccr, "ul_1449_type": ul_type},
                docs={"bulletin": "Power Xpert SPD"}
            ))

        # -------------------------------------------------------------------------
        # 17. UNINTERRUPTIBLE POWER SUPPLIES (UPS)
        # -------------------------------------------------------------------------
        ups_data = [
            ("93PM-050KW-480V", "Eaton 93PM", "Eaton 93PM 3-Phase Modular Scalable UPS 50kW / 50kVA 480V", 50.0, 50.0, 60.0, "480V", "3PH", "99% Energy Saver System (ESS)", "Lithium-Ion / VRLA"),
            ("93PM-100KW-480V", "Eaton 93PM", "Eaton 93PM 3-Phase Modular Scalable UPS 100kW / 100kVA 480V", 100.0, 100.0, 120.0, "480V", "3PH", "99% Energy Saver System (ESS)", "Lithium-Ion / VRLA"),
            ("93PM-150KW-480V", "Eaton 93PM", "Eaton 93PM 3-Phase Modular Scalable UPS 150kW / 150kVA 480V", 150.0, 150.0, 180.0, "480V", "3PH", "99% Energy Saver System (ESS)", "Lithium-Ion / VRLA"),
            ("93PM-200KW-480V", "Eaton 93PM", "Eaton 93PM 3-Phase Modular Scalable UPS 200kW / 200kVA 480V", 200.0, 200.0, 240.0, "480V", "3PH", "99% Energy Saver System (ESS)", "Lithium-Ion / VRLA"),
            ("93PM-300KW-480V", "Eaton 93PM", "Eaton 93PM 3-Phase Modular Scalable UPS 300kW / 300kVA 480V", 300.0, 300.0, 360.0, "480V", "3PH", "99% Energy Saver System (ESS)", "Lithium-Ion / VRLA"),
            ("93PM-400KW-480V", "Eaton 93PM", "Eaton 93PM 3-Phase Modular Scalable UPS 400kW / 400kVA 480V", 400.0, 400.0, 480.0, "480V", "3PH", "99% Energy Saver System (ESS)", "Lithium-Ion / VRLA"),
            ("9395-500KVA-480V", "Power Xpert 9395", "Power Xpert 9395 High-Power Industrial UPS 500kVA / 450kW 480V", 500.0, 450.0, 600.0, "480V", "3PH", "Double Conversion Online", "VRLA / Lithium-Ion"),
            ("9395-750KVA-480V", "Power Xpert 9395", "Power Xpert 9395 High-Power Industrial UPS 750kVA / 675kW 480V", 750.0, 675.0, 900.0, "480V", "3PH", "Double Conversion Online", "VRLA / Lithium-Ion"),
            ("9395-1000KVA-480V", "Power Xpert 9395", "Power Xpert 9395 High-Power Industrial UPS 1000kVA / 900kW 480V", 1000.0, 900.0, 1200.0, "480V", "3PH", "Double Conversion Online", "VRLA / Lithium-Ion"),
            ("9395-1500KVA-480V", "Power Xpert 9395", "Power Xpert 9395 High-Power Industrial UPS 1500kVA / 1350kW 480V", 1500.0, 1350.0, 1800.0, "480V", "3PH", "Double Conversion Online", "VRLA / Lithium-Ion"),
            ("9355-15KVA-208V", "Eaton 9355", "Eaton 9355 Mid-Range 3-Phase UPS 15kVA / 13.5kW 208V", 15.0, 13.5, 42.0, "208Y/120V", "3PH", "Double Conversion Online", "Internal VRLA"),
            ("9355-30KVA-208V", "Eaton 9355", "Eaton 9355 Mid-Range 3-Phase UPS 30kVA / 27kW 208V", 30.0, 27.0, 83.0, "208Y/120V", "3PH", "Double Conversion Online", "Internal VRLA"),
            ("9PX-6K-208V", "Eaton 9PX", "Eaton 9PX Heavy-Duty Rack/Tower UPS 6kVA / 5.4kW 208V", 6.0, 5.4, 26.0, "208V", "1PH", "Double Conversion Online", "Hot-Swappable VRLA"),
            ("9PX-11K-208V", "Eaton 9PX", "Eaton 9PX Heavy-Duty Rack/Tower UPS 11kVA / 10kW 208V", 11.0, 10.0, 48.0, "208V", "1PH", "Double Conversion Online", "Hot-Swappable VRLA"),
        ]
        for pn, series, desc, kva, kw, amps, volt, phase, eff, batt in ups_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="power_quality",
                type_tag="UPS",
                type_name="Uninterruptible Power Supply",
                description=desc,
                voltage=volt,
                amps=amps,
                kva=kva,
                poles="3P4W" if "3PH" in phase else "1P3W",
                phase=phase,
                nema_rating="NEMA 1 Indoor",
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-93pm-ups-catalog.pdf",
                specs={"kw": kw, "efficiency": eff, "battery_type": batt, "topology": "Double-Conversion Online"},
                docs={"bulletin": "Eaton 3-Phase UPS"}
            ))

        return items
