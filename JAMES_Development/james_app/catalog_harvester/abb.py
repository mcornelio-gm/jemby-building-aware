"""
ABB Electrification Industrial Equipment Catalog Harvester.
Harvests structured engineering specifications across all 17 industrial gear categories:
1. Busway (Spectra Series & ReliaGear Sandwich Busway, Aluminum & Copper 225A-5000A)
2. Circuit Breakers (Tmax XT1-XT7, Formula DSP, Emax 2 E1.2-E6.2, AMVAC MV Vacuum Breakers)
3. Load Centers (ReliaGear Pro-Stock Commercial 3-Phase, PowerMark Gold Commercial)
4. Motor Control Centers (ReliaGear MCC, Evolution Series Industrial MCC, SafeT Arc-Resistant)
5. Panelboards (ReliaGear neXT Plug-In, Pro-Stock A-Series AQ 240V & AE 480Y/277V)
6. Softstarters (PSTX Advanced Softstarter, PSE Efficient, PSR Compact)
7. Switchboards (ReliaGear SB Distribution, Evolution Series Commercial Switchboard)
8. Switches & Disconnects (Spec-Setter Heavy Duty Safety Switches TH3361-TH3368, OT Disconnects, HPC Bolted Pressure)
9. Switchgear (ReliaGear ND Low-Voltage UL 1558, SafeGear Medium-Voltage Metal-Clad Arc-Resistant)
10. Transformers (Type QL Low-Voltage Ventilated Dry-Type DOE 2016 Compliant, K-Factor K-13, Substation Liquid-Filled)
11. Automatic Transfer Switches (Zenith ZTS Heavy-Duty, Zenith ZTG Standard, Zenith ZTX Commercial)
12. Paralleling Switchgear (ABB Zenith Paralleling Switchgear Lineup, Generator Master Sync)
13. Power Conditioning (TruWave Active Harmonic Filter PQFS/PQFM, PCS100 AVC Active Voltage Conditioner)
14. Power Distribution Systems (Cyberex Precision Data PDU 50kVA-300kVA, Cyberex Remote Power Panel RPP)
15. Static Transfer Switches (Cyberex SuperSwitch 4 SS4 Digital High-Speed Static Transfer Switch <4ms)
16. Surge Protective Devices (TPME Series, OVR Series Facility Wide SPD 100kA-300kA/Phase NEMA 4X)
17. Uninterruptible Power Supplies (MegaFlex DPA 250kW-1500kW, TLE Series High Power, Conceptpower DPA 500)
"""

from typing import List
from james_app.catalog_harvester.base import BaseVendorHarvester
from james_app.catalog_harvester.models import CatalogItem


class ABBCatalogHarvester(BaseVendorHarvester):
    """
    Catalog extractor for ABB Electrification Industrial Equipment.
    Grounds catalog models to ABB BuyLog catalog sections (Section 1 to Section 24) and ABB technical docs.
    """

    vendor_name: str = "ABB"
    vendor_key: str = "abb"
    source_url: str = "https://electrification.us.abb.com/buylog_pdf"

    def harvest(self) -> List[CatalogItem]:
        """Harvest comprehensive industrial equipment items for ABB Electrification."""
        items: List[CatalogItem] = []

        # -------------------------------------------------------------------------
        # 1. BUSWAY (BuyLog Section 15 - Spectra & ReliaGear Sandwich Busway)
        # -------------------------------------------------------------------------
        busway_data = [
            ("RGB-CU-0800A", "ReliaGear Busway", "ReliaGear Copper Feeder Busway 800A 3P4W 600V with Internal Ground", 800.0, 100.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 100.0),
            ("RGB-CU-1200A", "ReliaGear Busway", "ReliaGear Copper Feeder Busway 1200A 3P4W 600V with Internal Ground", 1200.0, 100.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 100.0),
            ("RGB-CU-1600A", "ReliaGear Busway", "ReliaGear Copper Feeder Busway 1600A 3P4W 600V with Internal Ground", 1600.0, 150.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 150.0),
            ("RGB-CU-2000A", "ReliaGear Busway", "ReliaGear Copper Feeder Busway 2000A 3P4W 600V with Internal Ground", 2000.0, 150.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 150.0),
            ("RGB-CU-3000A", "ReliaGear Busway", "ReliaGear Copper Feeder Busway 3000A 3P4W 600V with Internal Ground", 3000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 200.0),
            ("RGB-CU-4000A", "ReliaGear Busway", "ReliaGear Copper Feeder Busway 4000A 3P4W 600V with Internal Ground", 4000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 200.0),
            ("RGB-CU-5000A", "ReliaGear Busway", "ReliaGear Copper Feeder Busway 5000A 3P4W 600V with Internal Ground", 5000.0, 200.0, "600V", "3PH", "3P4W", "Copper", "NEMA 1 / IP40", 200.0),
            ("RGB-AL-1000A", "ReliaGear Busway", "ReliaGear Aluminum Feeder Busway 1000A 3P4W 600V with Internal Ground", 1000.0, 100.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 100.0),
            ("RGB-AL-1600A", "ReliaGear Busway", "ReliaGear Aluminum Feeder Busway 1600A 3P4W 600V with Internal Ground", 1600.0, 150.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 150.0),
            ("RGB-AL-2500A", "ReliaGear Busway", "ReliaGear Aluminum Feeder Busway 2500A 3P4W 600V with Internal Ground", 2500.0, 150.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 150.0),
            ("RGB-AL-3000A", "ReliaGear Busway", "ReliaGear Aluminum Feeder Busway 3000A 3P4W 600V with Internal Ground", 3000.0, 200.0, "600V", "3PH", "3P4W", "Aluminum", "NEMA 1 / IP40", 200.0),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/busway/{pn}",
                specs={
                    "bus_material": bus_mat,
                    "short_circuit_withstand_ka": sccr,
                    "catalog_section": "BuyLog Section 15: Busway",
                    "conductor_configuration": poles
                },
                docs={"catalog_volume": "BuyLog Section 15"}
            ))

        # -------------------------------------------------------------------------
        # 2. CIRCUIT BREAKERS (BuyLog Section 6 & 7 - Tmax XT, Emax 2, AMVAC MV)
        # -------------------------------------------------------------------------
        breakers_data = [
            # Tmax XT Molded Case Breakers (XT1 - XT7)
            ("XT1NU3030AFF000XXX", "Tmax XT1", "Tmax XT1 30A 3P 600V 25kAIC Thermal-Magnetic Fixed Breaker", 30.0, 25.0, "600V", "3PH", "3P", "TMD Thermal-Magnetic", "XT1"),
            ("XT1NU3060AFF000XXX", "Tmax XT1", "Tmax XT1 60A 3P 600V 25kAIC Thermal-Magnetic Fixed Breaker", 60.0, 25.0, "600V", "3PH", "3P", "TMD Thermal-Magnetic", "XT1"),
            ("XT2NU3100EFF000XXX", "Tmax XT2", "Tmax XT2 100A 3P 600V 25kAIC Ekip Dip LSI Electronic Breaker", 100.0, 25.0, "600V", "3PH", "3P", "Ekip Dip LSI Electronic", "XT2"),
            ("XT2HU3125EFF000XXX", "Tmax XT2", "Tmax XT2 125A 3P 600V 65kAIC Ekip Touch LSI Electronic Breaker", 125.0, 65.0, "600V", "3PH", "3P", "Ekip Touch LSI Electronic", "XT2"),
            ("XT3NU3225AFF000XXX", "Tmax XT3", "Tmax XT3 225A 3P 600V 25kAIC Thermal-Magnetic Fixed Breaker", 225.0, 25.0, "600V", "3PH", "3P", "TMD Thermal-Magnetic", "XT3"),
            ("XT4NU3250EFF000XXX", "Tmax XT4", "Tmax XT4 250A 3P 600V 25kAIC Ekip Dip LSI Electronic Breaker", 250.0, 25.0, "600V", "3PH", "3P", "Ekip Dip LSI Electronic", "XT4"),
            ("XT4HU3250EFF000XXX", "Tmax XT4", "Tmax XT4 250A 3P 600V 65kAIC Ekip Touch LSI Electronic Breaker", 250.0, 65.0, "600V", "3PH", "3P", "Ekip Touch LSI Electronic", "XT4"),
            ("XT5NU3400BFF000XXX", "Tmax XT5", "Tmax XT5 400A 3P 600V 35kAIC Ekip Dip LS/I Electronic Breaker", 400.0, 35.0, "600V", "3PH", "3P", "Ekip Dip LS/I Electronic", "XT5"),
            ("XT5HU3600BFF000XXX", "Tmax XT5", "Tmax XT5 600A 3P 600V 65kAIC Ekip Touch LSIG Electronic Breaker", 600.0, 65.0, "600V", "3PH", "3P", "Ekip Touch LSIG Electronic", "XT5"),
            ("XT6NU3800BFF000XXX", "Tmax XT6", "Tmax XT6 800A 3P 600V 35kAIC Ekip Dip LS/I Electronic Breaker", 800.0, 35.0, "600V", "3PH", "3P", "Ekip Dip LS/I Electronic", "XT6"),
            ("XT7HU3100EFF000XXX", "Tmax XT7", "Tmax XT7 1000A 3P 600V 65kAIC Ekip Touch LSIG Electronic Breaker", 1000.0, 65.0, "600V", "3PH", "3P", "Ekip Touch LSIG Electronic", "XT7"),
            ("XT7HU3120EFF000XXX", "Tmax XT7", "Tmax XT7 1200A 3P 600V 65kAIC Ekip Hi-Touch LSIG Breaker", 1200.0, 65.0, "600V", "3PH", "3P", "Ekip Hi-Touch LSIG Electronic", "XT7"),
            # Emax 2 Low Voltage Power Air Circuit Breakers (UL 1066 / UL 489)
            ("E1.2B-0800A-3P", "Emax 2 E1.2", "Emax 2 E1.2 800A 3P 600V 42kAIC Drawout Air Circuit Breaker", 800.0, 42.0, "600V", "3PH", "3P", "Ekip Touch LSIG Electronic", "Emax 2 E1.2"),
            ("E2.2N-1200A-3P", "Emax 2 E2.2", "Emax 2 E2.2 1200A 3P 600V 65kAIC Drawout Air Circuit Breaker", 1200.0, 65.0, "600V", "3PH", "3P", "Ekip Touch LSIG Electronic", "Emax 2 E2.2"),
            ("E2.2H-1600A-3P", "Emax 2 E2.2", "Emax 2 E2.2 1600A 3P 600V 85kAIC Drawout Air Circuit Breaker", 1600.0, 85.0, "600V", "3PH", "3P", "Ekip Touch LSIG Electronic", "Emax 2 E2.2"),
            ("E2.2V-2000A-3P", "Emax 2 E2.2", "Emax 2 E2.2 2000A 3P 600V 100kAIC Drawout Air Circuit Breaker", 2000.0, 100.0, "600V", "3PH", "3P", "Ekip Hi-Touch LSIG Electronic", "Emax 2 E2.2"),
            ("E4.2V-3200A-3P", "Emax 2 E4.2", "Emax 2 E4.2 3200A 3P 600V 100kAIC Drawout Air Circuit Breaker", 3200.0, 100.0, "600V", "3PH", "3P", "Ekip Hi-Touch LSIG Electronic", "Emax 2 E4.2"),
            ("E6.2X-4000A-3P", "Emax 2 E6.2", "Emax 2 E6.2 4000A 3P 600V 150kAIC Drawout Air Circuit Breaker", 4000.0, 150.0, "600V", "3PH", "3P", "Ekip Hi-Touch LSIG Electronic", "Emax 2 E6.2"),
            ("E6.2X-5000A-3P", "Emax 2 E6.2", "Emax 2 E6.2 5000A 3P 600V 150kAIC Drawout Air Circuit Breaker", 5000.0, 150.0, "600V", "3PH", "3P", "Ekip Hi-Touch LSIG Electronic", "Emax 2 E6.2"),
            ("E6.2X-6000A-3P", "Emax 2 E6.2", "Emax 2 E6.2 6000A 3P 600V 150kAIC Drawout Air Circuit Breaker", 6000.0, 150.0, "600V", "3PH", "3P", "Ekip Hi-Touch LSIG Electronic", "Emax 2 E6.2"),
            # Medium Voltage Vacuum Circuit Breakers (AMVAC / ADVAC)
            ("AMVAC-05-1200-25", "AMVAC MV", "AMVAC Magnetically Actuated Medium Voltage Vacuum Breaker 1200A 4.76kV 25kAIC", 1200.0, 25.0, "4.76kV", "3PH", "3P", "Magnetic Actuator Vacuum", "AMVAC 5kV"),
            ("AMVAC-15-1200-31", "AMVAC MV", "AMVAC Magnetically Actuated Medium Voltage Vacuum Breaker 1200A 15kV 31.5kAIC", 1200.0, 31.5, "15kV", "3PH", "3P", "Magnetic Actuator Vacuum", "AMVAC 15kV"),
            ("AMVAC-15-2000-40", "AMVAC MV", "AMVAC Magnetically Actuated Medium Voltage Vacuum Breaker 2000A 15kV 40kAIC", 2000.0, 40.0, "15kV", "3PH", "3P", "Magnetic Actuator Vacuum", "AMVAC 15kV"),
            ("AMVAC-15-3000-50", "AMVAC MV", "AMVAC Magnetically Actuated Medium Voltage Vacuum Breaker 3000A 15kV 50kAIC", 3000.0, 50.0, "15kV", "3PH", "3P", "Magnetic Actuator Vacuum", "AMVAC 15kV"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/circuit-breakers/{pn}",
                specs={
                    "trip_unit_type": trip,
                    "frame_designation": frame,
                    "catalog_section": "BuyLog Section 6: Molded Case Breakers & Section 7: Low Voltage Power Breakers",
                    "mounting": "Fixed / Plug-in / Drawout"
                },
                docs={"catalog_volume": "BuyLog Section 6 & 7"}
            ))

        # -------------------------------------------------------------------------
        # 3. LOAD CENTERS (BuyLog Section 1 - ReliaGear Pro-Stock & PowerMark Gold)
        # -------------------------------------------------------------------------
        load_center_data = [
            ("TLM3212CLU", "PowerMark Gold Commercial", "PowerMark Gold 125A 3PH 12-Circuit Main Lugs Commercial Load Center", 125.0, 65.0, "208Y/120V", "3PH", "3P4W", 12, "NEMA 1 Indoor", "Main Lug Only"),
            ("TLM3220CCU", "PowerMark Gold Commercial", "PowerMark Gold 200A 3PH 24-Circuit Main Lugs Commercial Load Center", 200.0, 65.0, "208Y/120V", "3PH", "3P4W", 24, "NEMA 1 Indoor", "Main Lug Only"),
            ("TLM3222CCU", "PowerMark Gold Commercial", "PowerMark Gold 225A 3PH 42-Circuit Main Lugs Commercial Load Center", 225.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Lug Only"),
            ("TLM3220RCU", "PowerMark Gold Commercial", "PowerMark Gold 200A 3PH 30-Circuit Main Lugs NEMA 3R Outdoor Load Center", 200.0, 65.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 3R Outdoor", "Main Lug Only"),
            ("TM3220CCU", "PowerMark Gold Commercial", "PowerMark Gold 200A 3PH 30-Circuit Main Breaker Commercial Load Center", 200.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Main Breaker Included"),
            ("TM3222CCU", "PowerMark Gold Commercial", "PowerMark Gold 225A 3PH 42-Circuit Main Breaker Commercial Load Center", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Breaker Included"),
            ("TMP3220CCU", "ReliaGear Pro-Stock Commercial", "ReliaGear Pro-Stock Commercial Load Center 200A 3PH 42-Circuit Main Breaker", 200.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Breaker Included"),
            ("TMP3222CCU", "ReliaGear Pro-Stock Commercial", "ReliaGear Pro-Stock Commercial Load Center 225A 3PH 42-Circuit Main Lug", 225.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Main Lug Only"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/load-centers/{pn}",
                specs={
                    "main_device_type": main_type,
                    "bus_material": "100% Copper Bus Bars",
                    "catalog_section": "BuyLog Section 1: Load Centers",
                    "branch_breaker_family": "THQL / THQP Plug-In Breakers"
                },
                docs={"catalog_volume": "BuyLog Section 1"}
            ))

        # -------------------------------------------------------------------------
        # 4. MOTOR CONTROL CENTERS (BuyLog Section 13 - ReliaGear MCC & Evolution)
        # -------------------------------------------------------------------------
        mcc_data = [
            ("RGMCC-FVNR-SZ1-600A", "ReliaGear MCC", "ReliaGear MCC FVNR Starter Size 1 Tmax XT2 MCP 600A Bus NEMA 1", 600.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 10, "Size 1 (Up to 10 HP)"),
            ("RGMCC-FVNR-SZ2-600A", "ReliaGear MCC", "ReliaGear MCC FVNR Starter Size 2 Tmax XT2 MCP 600A Bus NEMA 1", 600.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 25, "Size 2 (Up to 25 HP)"),
            ("RGMCC-FVNR-SZ3-800A", "ReliaGear MCC", "ReliaGear MCC FVNR Starter Size 3 Tmax XT4 MCP 800A Bus NEMA 1", 800.0, 65.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 50, "Size 3 (Up to 50 HP)"),
            ("RGMCC-FVNR-SZ4-1200A", "ReliaGear MCC", "ReliaGear MCC FVNR Starter Size 4 Tmax XT5 MCP 1200A Bus NEMA 1", 1200.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 100, "Size 4 (Up to 100 HP)"),
            ("RGMCC-FVNR-SZ5-1600A", "ReliaGear MCC", "ReliaGear MCC FVNR Starter Size 5 Tmax XT6 MCP 1600A Bus NEMA 1", 1600.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 200, "Size 5 (Up to 200 HP)"),
            ("RGMCC-VFD-ACS580-100HP", "ReliaGear Smart MCC", "ReliaGear Smart MCC with ACS580 100HP General Purpose VFD Unit", 1200.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 100, "ABB ACS580 Industrial VFD"),
            ("RGMCC-SAFET-ARC-2000A", "ReliaGear SafeT MCC", "ReliaGear SafeT Arc-Resistant Industrial MCC Lineup 2000A Copper Bus", 2000.0, 100.0, "480V", "3PH", "3P3W", "IEEE C37.20.7 Arc-Resistant", 400, "Master Feeder / Starter Lineup"),
            ("RGMCC-MAIN-EMAX2-2500A", "ReliaGear MCC", "ReliaGear MCC 2500A Main Circuit Breaker Section Emax 2 Air Breaker", 2500.0, 100.0, "480V", "3PH", "3P3W", "NEMA 1 Gasketed", 0, "Main Incoming Section"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/motor-control-centers/{pn}",
                specs={
                    "starter_type": starter_type,
                    "horse_power_rating": hp,
                    "horizontal_bus_rating_amps": bus_amps,
                    "catalog_section": "BuyLog Section 13: Motor Control Centers",
                    "smart_relay": "ABB UMC100.3 Intelligent Motor Controller"
                },
                docs={"catalog_volume": "BuyLog Section 13"}
            ))

        # -------------------------------------------------------------------------
        # 5. PANELBOARDS (BuyLog Section 9 - ReliaGear neXT & Pro-Stock A-Series)
        # -------------------------------------------------------------------------
        panel_data = [
            # ReliaGear neXT Plug-In Power Panelboards (Up to 1200A)
            ("RNX-400A-480Y", "ReliaGear neXT", "ReliaGear neXT Power Panelboard Interior 400A 480Y/277V Copper Bus", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs / Breaker", "Copper"),
            ("RNX-800A-480Y", "ReliaGear neXT", "ReliaGear neXT Power Panelboard Interior 800A 480Y/277V Copper Bus", 800.0, 100.0, "480Y/277V", "3PH", "3P4W", 60, "Main Lugs / Breaker", "Copper"),
            ("RNX-1200A-480Y", "ReliaGear neXT", "ReliaGear neXT Power Panelboard Interior 1200A 480Y/277V Copper Bus", 1200.0, 100.0, "480Y/277V", "3PH", "3P4W", 72, "Main Lugs / Breaker", "Copper"),
            # Pro-Stock A-Series AQ Panelboards (240V max)
            ("AQ330L125", "A-Series AQ", "Pro-Stock AQ Lighting Panelboard 125A 3PH 4W 240VAC 30-Circuit Main Lugs", 125.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "Main Lugs", "Copper"),
            ("AQ342L225", "A-Series AQ", "Pro-Stock AQ Lighting Panelboard 225A 3PH 4W 240VAC 42-Circuit Main Lugs", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("AQ342M225", "A-Series AQ", "Pro-Stock AQ Lighting Panelboard 225A 3PH 4W 240VAC 42-Circuit Main Breaker", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "Main Breaker", "Copper"),
            ("AQ342L400", "A-Series AQ", "Pro-Stock AQ Lighting Panelboard 400A 3PH 4W 240VAC 42-Circuit Main Lugs", 400.0, 65.0, "208Y/120V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            # Pro-Stock A-Series AE Panelboards (480Y/277V)
            ("AE330L125", "A-Series AE", "Pro-Stock AE Distribution Panelboard 125A 3PH 4W 480Y/277VAC 30-Circuit Main Lugs", 125.0, 65.0, "480Y/277V", "3PH", "3P4W", 30, "Main Lugs", "Copper"),
            ("AE342L250", "A-Series AE", "Pro-Stock AE Distribution Panelboard 250A 3PH 4W 480Y/277VAC 42-Circuit Main Lugs", 250.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("AE342M250", "A-Series AE", "Pro-Stock AE Distribution Panelboard 250A 3PH 4W 480Y/277VAC 42-Circuit Main Breaker", 250.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Breaker", "Copper"),
            ("AE342L400", "A-Series AE", "Pro-Stock AE Distribution Panelboard 400A 3PH 4W 480Y/277VAC 42-Circuit Main Lugs", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
            ("AE342L600", "A-Series AE", "Pro-Stock AE Distribution Panelboard 600A 3PH 4W 480Y/277VAC 42-Circuit Main Lugs", 600.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Main Lugs", "Copper"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/panelboards/{pn}",
                specs={
                    "main_device_type": main_type,
                    "bus_material": bus_mat,
                    "catalog_section": "BuyLog Section 9: Panelboards",
                    "branch_breaker_family": "Tmax XT / THQB / TEY"
                },
                docs={"catalog_volume": "BuyLog Section 9"}
            ))

        # -------------------------------------------------------------------------
        # 6. SOFTSTARTERS (BuyLog Section 5 - PSTX, PSE, PSR Series)
        # -------------------------------------------------------------------------
        softstart_data = [
            ("PSTX30-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 30A 208-600V Built-In Bypass & Coated PCB", 30.0, 480.0, 20.0, "PSTX"),
            ("PSTX60-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 60A 208-600V Built-In Bypass & Coated PCB", 60.0, 480.0, 40.0, "PSTX"),
            ("PSTX105-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 105A 208-600V Built-In Bypass & Coated PCB", 105.0, 480.0, 75.0, "PSTX"),
            ("PSTX170-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 170A 208-600V Built-In Bypass & Coated PCB", 170.0, 480.0, 125.0, "PSTX"),
            ("PSTX250-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 250A 208-600V Built-In Bypass & Coated PCB", 250.0, 480.0, 200.0, "PSTX"),
            ("PSTX370-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 370A 208-600V Built-In Bypass & Coated PCB", 370.0, 480.0, 300.0, "PSTX"),
            ("PSTX570-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 570A 208-600V Built-In Bypass & Coated PCB", 570.0, 480.0, 450.0, "PSTX"),
            ("PSTX840-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 840A 208-600V Built-In Bypass & Coated PCB", 840.0, 480.0, 700.0, "PSTX"),
            ("PSTX1250-600-70", "PSTX Advanced", "PSTX Advanced Softstarter 1250A 208-600V Built-In Bypass & Coated PCB", 1250.0, 480.0, 1000.0, "PSTX"),
            ("PSE105-600-70", "PSE Efficient", "PSE Efficient Softstarter 105A 208-600V Built-In Bypass Torque Control", 105.0, 480.0, 75.0, "PSE"),
            ("PSE370-600-70", "PSE Efficient", "PSE Efficient Softstarter 370A 208-600V Built-In Bypass Torque Control", 370.0, 480.0, 300.0, "PSE"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/softstarters/{pn}",
                specs={
                    "motor_hp_480v": hp,
                    "bypass_contactor": "Built-In Electrical Bypass Contactor",
                    "torque_control": "Eliminates Water Hammer in Pump Applications",
                    "fieldbus_support": "Modbus RTU / Anybus Fieldbus Modules",
                    "catalog_section": "BuyLog Section 5: Control Components & Softstarters"
                },
                docs={"catalog_volume": "BuyLog Section 5"}
            ))

        # -------------------------------------------------------------------------
        # 7. SWITCHBOARDS (BuyLog Section 11 - ReliaGear SB & Evolution Commercial)
        # -------------------------------------------------------------------------
        swbd_data = [
            ("RGSB-800A-480V", "ReliaGear SB", "ReliaGear SB Distribution Switchboard 800A 480V 3PH 4W Tmax XT7 Main", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "Tmax XT7 Main + ReliaGear neXT Feeders"),
            ("RGSB-1200A-480V", "ReliaGear SB", "ReliaGear SB Distribution Switchboard 1200A 480V 3PH 4W Tmax XT7 Main", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "Tmax XT7 Main + ReliaGear neXT Feeders"),
            ("RGSB-2000A-480V", "ReliaGear SB", "ReliaGear SB Distribution Switchboard 2000A 480V 3PH 4W Emax 2 E2.2 Main", 2000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "Emax 2 E2.2 Main + Tmax XT Feeders"),
            ("RGSB-3000A-480V", "ReliaGear SB", "ReliaGear SB Distribution Switchboard 3000A 480V 3PH 4W Emax 2 E4.2 Main", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "Emax 2 E4.2 Main + Tmax XT Feeders"),
            ("RGSB-4000A-480V", "ReliaGear SB", "ReliaGear SB Distribution Switchboard 4000A 480V 3PH 4W Emax 2 E6.2 Main", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "Emax 2 E6.2 Main + Tmax XT Feeders"),
            ("RGSB-5000A-480V", "ReliaGear SB", "ReliaGear SB Distribution Switchboard 5000A 480V 3PH 4W Emax 2 E6.2 Main", 5000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Silver-Plated Copper", "Emax 2 E6.2 Main + Tmax XT Feeders"),
            ("EVO-SWBD-2000A", "Evolution Series", "Evolution Commercial Service Entrance Switchboard 2000A 480V Utility Metering", 2000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 / 3R", "Copper", "Utility Metering Compartment + Emax 2 Main"),
            ("EVO-SWBD-4000A", "Evolution Series", "Evolution Commercial Service Entrance Switchboard 4000A 480V Utility Metering", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 / 3R", "Copper", "Utility Metering Compartment + Emax 2 Main"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/switchboards/{pn}",
                specs={
                    "bus_material": bus_mat,
                    "switchboard_configuration": config,
                    "short_circuit_rating_ka": aic,
                    "catalog_section": "BuyLog Section 11: Switchboards",
                    "standards": "UL 891 / NEMA PB2"
                },
                docs={"catalog_volume": "BuyLog Section 11"}
            ))

        # -------------------------------------------------------------------------
        # 8. SWITCHES & DISCONNECTS (BuyLog Section 2 - Spec-Setter Heavy Duty & HPC)
        # -------------------------------------------------------------------------
        disc_data = [
            ("TH3361", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 30A 3P 600V NEMA 1 Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("TH3362", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 60A 3P 600V NEMA 1 Fusible", 60.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("TH3363", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 100A 3P 600V NEMA 1 Fusible", 100.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("TH3364", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 200A 3P 600V NEMA 1 Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("TH3365", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 400A 3P 600V NEMA 1 Fusible", 400.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("TH3366", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 600A 3P 600V NEMA 1 Fusible", 600.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 1 Indoor"),
            ("TH3367", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 800A 3P 600V NEMA 1 Fusible Class L", 800.0, 200.0, "600V", "3PH", "3P", "Fusible (Class L)", "NEMA 1 Indoor"),
            ("TH3368", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 1200A 3P 600V NEMA 1 Fusible Class L", 1200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class L)", "NEMA 1 Indoor"),
            ("THN3361", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 30A 3P 600V NEMA 1 Non-Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Non-Fusible", "NEMA 1 Indoor"),
            ("THN3364", "Spec-Setter Heavy Duty", "Spec-Setter Heavy Duty Safety Switch 200A 3P 600V NEMA 1 Non-Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Non-Fusible", "NEMA 1 Indoor"),
            ("TH3361SS", "Spec-Setter Stainless", "Spec-Setter Heavy Duty Switch 30A 3P 600V NEMA 4X 304 Stainless Fusible", 30.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 4X Stainless"),
            ("TH3364SS", "Spec-Setter Stainless", "Spec-Setter Heavy Duty Switch 200A 3P 600V NEMA 4X 304 Stainless Fusible", 200.0, 200.0, "600V", "3PH", "3P", "Fusible (Class R/J)", "NEMA 4X Stainless"),
            ("HPC3608", "HPC Bolted Pressure", "HPC High Pressure Contact Switch 800A 3P 600V Fusible Class L", 800.0, 200.0, "600V", "3PH", "3P", "High Pressure Contact Class L", "NEMA 1 Enclosed"),
            ("HPC3620", "HPC Bolted Pressure", "HPC High Pressure Contact Switch 2000A 3P 600V Fusible Class L", 2000.0, 200.0, "600V", "3PH", "3P", "High Pressure Contact Class L", "NEMA 1 Enclosed"),
            ("HPC3640", "HPC Bolted Pressure", "HPC High Pressure Contact Switch 4000A 3P 600V Fusible Class L", 4000.0, 200.0, "600V", "3PH", "3P", "High Pressure Contact Class L", "NEMA 1 Enclosed"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, f_type, nema in disc_data:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="disconnect",
                type_tag="DISC",
                type_name="Heavy-Duty Safety Switch / High Pressure Contact Switch",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url=f"https://electrification.us.abb.com/products/switches-disconnects/{pn}",
                specs={
                    "fuse_type": f_type,
                    "catalog_section": "BuyLog Section 2: Enclosed Switches",
                    "duty_rating": "Heavy Duty / 200kA Withstand"
                },
                docs={"catalog_volume": "BuyLog Section 2"}
            ))

        # -------------------------------------------------------------------------
        # 9. SWITCHGEAR (BuyLog Section 11 & MV ReliaGear ND & SafeGear Arc-Resistant)
        # -------------------------------------------------------------------------
        swgr_data = [
            ("RGND-SWGR-2000A", "ReliaGear ND", "ReliaGear ND Narrow Design Low Voltage Metal-Enclosed Switchgear 2000A Emax 2", 2000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("RGND-SWGR-3200A", "ReliaGear ND", "ReliaGear ND Narrow Design Low Voltage Metal-Enclosed Switchgear 3200A Emax 2", 3200.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("RGND-SWGR-4000A", "ReliaGear ND", "ReliaGear ND Narrow Design Low Voltage Metal-Enclosed Switchgear 4000A Emax 2", 4000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("RGND-SWGR-5000A", "ReliaGear ND", "ReliaGear ND Narrow Design Low Voltage Metal-Enclosed Switchgear 5000A Emax 2", 5000.0, 100.0, "480V", "3PH", "3P4W", "UL 1558 LV Switchgear", 100.0),
            ("SAFEGEAR-05-1200A", "SafeGear Arc-Resistant", "SafeGear Metal-Clad Arc-Resistant MV Switchgear 1200A 4.76kV ADVAC", 1200.0, 40.0, "4.76kV", "3PH", "3P3W", "IEEE C37.20.7 Type 2B Arc-Resistant", 40.0),
            ("SAFEGEAR-15-1200A", "SafeGear Arc-Resistant", "SafeGear Metal-Clad Arc-Resistant MV Switchgear 1200A 15kV AMVAC", 1200.0, 31.5, "15kV", "3PH", "3P3W", "IEEE C37.20.7 Type 2B Arc-Resistant", 31.5),
            ("SAFEGEAR-15-2000A", "SafeGear Arc-Resistant", "SafeGear Metal-Clad Arc-Resistant MV Switchgear 2000A 15kV AMVAC", 2000.0, 40.0, "15kV", "3PH", "3P3W", "IEEE C37.20.7 Type 2B Arc-Resistant", 40.0),
            ("SAFEGEAR-15-3000A", "SafeGear Arc-Resistant", "SafeGear Metal-Clad Arc-Resistant MV Switchgear 3000A 15kV AMVAC", 3000.0, 50.0, "15kV", "3PH", "3P3W", "IEEE C37.20.7 Type 2B Arc-Resistant", 50.0),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/switchgear/{pn}",
                specs={
                    "switchgear_standard": swgr_std,
                    "short_time_withstand_ka": withstand,
                    "catalog_section": "BuyLog Section 11 & Medium Voltage Switchgear",
                    "arc_resistant_rating": "IEEE C37.20.7 Accessibility Type 2B"
                },
                docs={"catalog_volume": "BuyLog Section 11"}
            ))

        # -------------------------------------------------------------------------
        # 10. TRANSFORMERS (BuyLog Section 10 - Type QL DOE 2016 Compliant & K-Factor)
        # -------------------------------------------------------------------------
        xfmr_data = [
            # Type QL General Purpose DOE 2016 Ventilated Dry-Type 480V Delta to 208Y/120V
            ("9T10A1001", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 15kVA 480V-208Y/120V 3PH Aluminum", 15.0, "480V Delta", "208Y/120V", 18.0, 4.5, "Aluminum", 150.0),
            ("9T10A1002", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 30kVA 480V-208Y/120V 3PH Aluminum", 30.0, "480V Delta", "208Y/120V", 36.1, 4.5, "Aluminum", 150.0),
            ("9T10A1003", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 45kVA 480V-208Y/120V 3PH Aluminum", 45.0, "480V Delta", "208Y/120V", 54.1, 4.8, "Aluminum", 150.0),
            ("9T10A1004", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 75kVA 480V-208Y/120V 3PH Aluminum", 75.0, "480V Delta", "208Y/120V", 90.2, 5.0, "Aluminum", 150.0),
            ("9T10A1005", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 112.5kVA 480V-208Y/120V 3PH Aluminum", 112.5, "480V Delta", "208Y/120V", 135.3, 5.2, "Aluminum", 150.0),
            ("9T10A1006", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 150kVA 480V-208Y/120V 3PH Aluminum", 150.0, "480V Delta", "208Y/120V", 180.4, 5.5, "Aluminum", 150.0),
            ("9T10A1007", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 225kVA 480V-208Y/120V 3PH Aluminum", 225.0, "480V Delta", "208Y/120V", 270.6, 5.5, "Aluminum", 150.0),
            ("9T10A1008", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 300kVA 480V-208Y/120V 3PH Aluminum", 300.0, "480V Delta", "208Y/120V", 360.8, 5.75, "Aluminum", 150.0),
            ("9T10A1009", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 500kVA 480V-208Y/120V 3PH Aluminum", 500.0, "480V Delta", "208Y/120V", 601.4, 5.75, "Aluminum", 150.0),
            ("9T10A1010", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 750kVA 480V-208Y/120V 3PH Copper", 750.0, "480V Delta", "208Y/120V", 902.1, 5.75, "Copper", 150.0),
            ("9T10A1011", "Type QL DOE 2016", "Type QL Low Voltage Dry-Type Transformer 1000kVA 480V-208Y/120V 3PH Copper", 1000.0, "480V Delta", "208Y/120V", 1202.8, 5.75, "Copper", 150.0),
            # K-Factor Non-Linear Harmonic Rated
            ("9T10C1004", "Type QL K-Factor", "Type QL K-Factor K-13 Non-Linear Transformer 75kVA 480V-208Y/120V Copper", 75.0, "480V Delta", "208Y/120V", 90.2, 5.0, "Copper", 115.0),
            ("9T10C1006", "Type QL K-Factor", "Type QL K-Factor K-13 Non-Linear Transformer 150kVA 480V-208Y/120V Copper", 150.0, "480V Delta", "208Y/120V", 180.4, 5.5, "Copper", 115.0),
            ("9T10C1008", "Type QL K-Factor", "Type QL K-Factor K-13 Non-Linear Transformer 300kVA 480V-208Y/120V Copper", 300.0, "480V Delta", "208Y/120V", 360.8, 5.75, "Copper", 115.0),
            # Liquid-Filled Primary Substation Transformer
            ("ABB-SUB-1500KVA", "Substation Liquid-Filled", "ABB Primary Substation Liquid-Filled Transformer 1500kVA 13.8kV-480Y/277V", 1500.0, "13.8kV Delta", "480Y/277V", 62.8, 5.75, "Copper", 65.0),
            ("ABB-SUB-2500KVA", "Substation Liquid-Filled", "ABB Primary Substation Liquid-Filled Transformer 2500kVA 13.8kV-480Y/277V", 2500.0, "13.8kV Delta", "480Y/277V", 104.6, 5.75, "Copper", 65.0),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/transformers/{pn}",
                specs={
                    "primary_voltage": pri_v,
                    "secondary_voltage": sec_v,
                    "primary_amps": pri_amps,
                    "secondary_amps": round(sec_amps, 1),
                    "winding_material": winding,
                    "temperature_rise_c": temp_rise,
                    "efficiency_standard": "DOE 2016 Compliant (10 CFR Part 431)",
                    "catalog_section": "BuyLog Section 10: Transformers"
                },
                docs={"catalog_volume": "BuyLog Section 10"}
            ))

        # -------------------------------------------------------------------------
        # 11. AUTOMATIC TRANSFER SWITCHES (Zenith ZTS / ZTG / ZTX Series)
        # -------------------------------------------------------------------------
        ats_data = [
            ("ZTS0200-480V", "Zenith ZTS Heavy-Duty", "Zenith ZTS Heavy-Duty Automatic Transfer Switch 200A 480V 3P Open Transition", 200.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Zenith Heavy-Duty Contactor"),
            ("ZTS0400-480V", "Zenith ZTS Heavy-Duty", "Zenith ZTS Heavy-Duty Automatic Transfer Switch 400A 480V 3P Open Transition", 400.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Zenith Heavy-Duty Contactor"),
            ("ZTS0800-480V", "Zenith ZTS Heavy-Duty", "Zenith ZTS Heavy-Duty Automatic Transfer Switch 800A 480V 3P Open Transition", 800.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Zenith Heavy-Duty Contactor"),
            ("ZTS1200-480V", "Zenith ZTS Heavy-Duty", "Zenith ZTS Heavy-Duty Automatic Transfer Switch 1200A 480V 3P Open Transition", 1200.0, 85.0, "480V", "3PH", "3P", "Open Transition", "Zenith Heavy-Duty Contactor"),
            ("ZTS2000-480V-CT", "Zenith ZTS Heavy-Duty", "Zenith ZTS Heavy-Duty Automatic Transfer Switch 2000A 480V 3P Closed Transition", 2000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "Zenith Heavy-Duty Contactor"),
            ("ZTS3000-480V-CT", "Zenith ZTS Heavy-Duty", "Zenith ZTS Heavy-Duty Automatic Transfer Switch 3000A 480V 3P Closed Transition", 3000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "Zenith Heavy-Duty Contactor"),
            ("ZTG0400-480V", "Zenith ZTG Standard", "Zenith ZTG Standard Automatic Transfer Switch 400A 480V 3P Open Transition", 400.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Zenith Contactor"),
            ("ZTG0800-480V", "Zenith ZTG Standard", "Zenith ZTG Standard Automatic Transfer Switch 800A 480V 3P Open Transition", 800.0, 65.0, "480V", "3PH", "3P", "Open Transition", "Zenith Contactor"),
            ("EMAX2-ATS-2000A", "Emax 2 Breaker ATS", "Emax 2 Dual Breaker Automatic Transfer Switch Pair 2000A 480V Interlocked", 2000.0, 100.0, "480V", "3PH", "3P", "Electrically & Mechanically Interlocked", "Emax 2 E2.2 Breaker Pair"),
            ("EMAX2-ATS-3000A", "Emax 2 Breaker ATS", "Emax 2 Dual Breaker Automatic Transfer Switch Pair 3000A 480V Interlocked", 3000.0, 100.0, "480V", "3PH", "3P", "Electrically & Mechanically Interlocked", "Emax 2 E4.2 Breaker Pair"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/automatic-transfer-switches/{pn}",
                specs={
                    "transition_mode": trans_type,
                    "switching_mechanism": mech,
                    "controller": "ABB Zenith MX350 Microprocessor Controller",
                    "catalog_section": "BuyLog Section 8: Automatic Transfer Switches"
                },
                docs={"catalog_volume": "BuyLog Section 8"}
            ))

        # -------------------------------------------------------------------------
        # 12. PARALLELING SWITCHGEAR (ABB Zenith Paralleling Switchgear PSG)
        # -------------------------------------------------------------------------
        psg_data = [
            ("ZEN-PSG-2GEN-2000A", "ABB Zenith PSG", "Multi-Generator Paralleling Switchgear 2-Gen 2000A 480V Emax 2 Breakers", 2000.0, 100.0, "480V", "3PH", "3P4W", 2, "ABB AC500 Dual Redundant PLC"),
            ("ZEN-PSG-3GEN-3000A", "ABB Zenith PSG", "Multi-Generator Paralleling Switchgear 3-Gen 3000A 480V Emax 2 Breakers", 3000.0, 100.0, "480V", "3PH", "3P4W", 3, "ABB AC500 Dual Redundant PLC"),
            ("ZEN-PSG-4GEN-4000A", "ABB Zenith PSG", "Multi-Generator Paralleling Switchgear 4-Gen 4000A 480V Emax 2 Breakers", 4000.0, 100.0, "480V", "3PH", "3P4W", 4, "ABB AC500 Dual Redundant PLC"),
            ("ZEN-PSG-MV-15KV-2000A", "ABB Zenith SafeGear PSG", "Medium Voltage 15kV Multi-Generator Paralleling Switchgear 2000A AMVAC", 2000.0, 40.0, "15kV", "3PH", "3P3W", 4, "ABB AC500 Redundant Industrial PLC"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/paralleling-switchgear/{pn}",
                specs={
                    "supported_generators": gens,
                    "automation_controller": ctrl,
                    "load_management": "Automated Priority Load Add/Drop & Random Access Sync",
                    "paralleling_modes": "Emergency Standby / Isolated Bus / Co-Generation Import/Export"
                },
                docs={"catalog_volume": "Zenith PSG Technical Guide"}
            ))

        # -------------------------------------------------------------------------
        # 13. POWER CONDITIONING (TruWave Active Harmonic Filters & PCS100 AVC)
        # -------------------------------------------------------------------------
        cond_data = [
            ("PQFS-060A-480V", "TruWave PQFS", "TruWave PQFS Compact Active Harmonic Filter 60A 208-480V 3PH Enclosed", 60.0, 480.0, 60.0, "TruWave Active Harmonic Filter"),
            ("PQFM-100A-480V", "TruWave PQFM", "TruWave PQFM Industrial Active Harmonic Filter 100A 208-480V 3PH Enclosed", 100.0, 480.0, 100.0, "TruWave Active Harmonic Filter"),
            ("PQFM-150A-480V", "TruWave PQFM", "TruWave PQFM Industrial Active Harmonic Filter 150A 208-480V 3PH Enclosed", 150.0, 480.0, 150.0, "TruWave Active Harmonic Filter"),
            ("PQFI-300A-480V", "TruWave PQFI", "TruWave PQFI Heavy Industrial Active Harmonic Filter 300A 480V 3PH Enclosed", 300.0, 480.0, 300.0, "TruWave Active Harmonic Filter"),
            ("PCS100-AVC-300KVA", "PCS100 AVC", "PCS100 Active Voltage Conditioner 300kVA 480V Continuous Sag Correction", 300.0, 480.0, 360.8, "PCS100 Active Voltage Conditioner"),
            ("PCS100-AVC-1000KVA", "PCS100 AVC", "PCS100 Active Voltage Conditioner 1000kVA 480V Continuous Sag Correction", 1000.0, 480.0, 1202.8, "PCS100 Active Voltage Conditioner"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/power-conditioning/{pn}",
                specs={
                    "filter_technology": p_type,
                    "mitigation_target": "Selective Harmonic Filtering up to 50th Order (THDi < 5%)",
                    "response_time_ms": "< 1/2 cycle instantaneous compensation",
                    "parallelable": "Modular master-slave paralleling up to 8 units"
                },
                docs={"catalog_volume": "TruWave / PCS100 Technical Specifications"}
            ))

        # -------------------------------------------------------------------------
        # 14. POWER DISTRIBUTION SYSTEMS (Cyberex Precision Data PDU & RPP)
        # -------------------------------------------------------------------------
        pds_data = [
            ("CYB-PDU-50KVA-480-208", "Cyberex PDU", "Cyberex Precision Power Distribution Unit 50kVA 480V to 208Y/120V 84-Pole", 50.0, 138.8, "480V to 208Y/120V", 84, "K-13 Copper Isolation XFMR + BCM"),
            ("CYB-PDU-100KVA-480-208", "Cyberex PDU", "Cyberex Precision Power Distribution Unit 100kVA 480V to 208Y/120V 84-Pole", 100.0, 277.6, "480V to 208Y/120V", 84, "K-13 Copper Isolation XFMR + BCM"),
            ("CYB-PDU-150KVA-480-208", "Cyberex PDU", "Cyberex Precision Power Distribution Unit 150kVA 480V to 208Y/120V 168-Pole", 150.0, 416.4, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + BCM"),
            ("CYB-PDU-225KVA-480-208", "Cyberex PDU", "Cyberex Precision Power Distribution Unit 225kVA 480V to 208Y/120V 168-Pole", 225.0, 624.5, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + BCM"),
            ("CYB-PDU-300KVA-480-208", "Cyberex PDU", "Cyberex Precision Power Distribution Unit 300kVA 480V to 208Y/120V 168-Pole", 300.0, 832.7, "480V to 208Y/120V", 168, "K-13 Copper Isolation XFMR + BCM"),
            ("CYB-RPP-225A-84P", "Cyberex RPP", "Cyberex Remote Power Panel 225A Dual Feed 84-Circuit Data Center Server PDU", 75.0, 225.0, "208Y/120V", 84, "Dual Feed Remote Power Panel"),
            ("CYB-RPP-400A-168P", "Cyberex RPP", "Cyberex Remote Power Panel 400A Dual Feed 168-Circuit Data Center Server PDU", 150.0, 400.0, "208Y/120V", 168, "Dual Feed Remote Power Panel"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/power-distribution/{pn}",
                specs={
                    "subsystem_type": config,
                    "branch_monitoring": "Cyberex Advanced Branch Circuit Monitoring (BCM)",
                    "isolation_transformer": "K-13 / K-20 Shielded All-Copper Isolation Transformer"
                },
                docs={"catalog_volume": "Cyberex PDU Technical Guide"}
            ))

        # -------------------------------------------------------------------------
        # 15. STATIC TRANSFER SWITCHES (Cyberex SuperSwitch 4 SS4 Digital STS)
        # -------------------------------------------------------------------------
        sts_data = [
            ("SS4-100A-480V", "Cyberex SuperSwitch 4", "Cyberex SuperSwitch 4 Digital Static Transfer Switch 100A 480V 3P4W <4ms", 100.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SS4-250A-480V", "Cyberex SuperSwitch 4", "Cyberex SuperSwitch 4 Digital Static Transfer Switch 250A 480V 3P4W <4ms", 250.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SS4-400A-480V", "Cyberex SuperSwitch 4", "Cyberex SuperSwitch 4 Digital Static Transfer Switch 400A 480V 3P4W <4ms", 400.0, 65.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SS4-600A-480V", "Cyberex SuperSwitch 4", "Cyberex SuperSwitch 4 Digital Static Transfer Switch 600A 480V 3P4W <4ms", 600.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SS4-800A-480V", "Cyberex SuperSwitch 4", "Cyberex SuperSwitch 4 Digital Static Transfer Switch 800A 480V 3P4W <4ms", 800.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
            ("SS4-1200A-480V", "Cyberex SuperSwitch 4", "Cyberex SuperSwitch 4 Digital Static Transfer Switch 1200A 480V 3P4W <4ms", 1200.0, 100.0, "480V", "3PH", "3P4W", "< 4ms (< 1/4 cycle)", "Dual Redundant Digital DSP"),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/static-transfer-switches/{pn}",
                specs={
                    "transfer_time": xfer_time,
                    "switch_architecture": "True SCR Solid-State Static Transfer Switch",
                    "control_logic": ctrl,
                    "maintenance_bypass": "Integrated Triple Breaker Bypass Isolation"
                },
                docs={"catalog_volume": "Cyberex SuperSwitch 4 Technical Guide"}
            ))

        # -------------------------------------------------------------------------
        # 16. SURGE PROTECTIVE DEVICES (BuyLog Section 19 - TPME & OVR Series)
        # -------------------------------------------------------------------------
        spd_data = [
            ("TPME120480Y", "TPME Series", "ABB TPME Surge Protective Device 120kA/Phase 480Y/277V NEMA 4X Metallic", 120.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("TPME160480Y", "TPME Series", "ABB TPME Surge Protective Device 160kA/Phase 480Y/277V NEMA 4X Metallic", 160.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("TPME200480Y", "TPME Series", "ABB TPME Surge Protective Device 200kA/Phase 480Y/277V NEMA 4X Metallic", 200.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("TPME300480Y", "TPME Series", "ABB TPME Surge Protective Device 300kA/Phase 480Y/277V NEMA 4X Metallic", 300.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X Metallic", 20.0),
            ("OVR-100K-480Y", "OVR Facility Series", "ABB OVR Surge Protective Device 100kA/Phase 480Y/277V NEMA 1 Enclosed", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", 20.0),
            ("OVR-200K-208Y", "OVR Facility Series", "ABB OVR Surge Protective Device 200kA/Phase 208Y/120V NEMA 4X Enclosed", 200.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 4X Non-Metallic", 20.0),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/surge-protection/{pn}",
                specs={
                    "surge_current_per_phase_ka": ka_phase,
                    "nominal_discharge_current_in_ka": in_rating,
                    "short_circuit_current_rating_ka": sccr,
                    "ul_1449_type": "UL 1449 4th Edition Type 1 / Type 2",
                    "catalog_section": "BuyLog Section 19: Surge Protective Devices"
                },
                docs={"catalog_volume": "BuyLog Section 19"}
            ))

        # -------------------------------------------------------------------------
        # 17. UNINTERRUPTIBLE POWER SUPPLIES (MegaFlex DPA, TLE Series, Conceptpower DPA)
        # -------------------------------------------------------------------------
        ups_data = [
            # MegaFlex DPA High-Efficiency Modular 3-Phase UPS (250kW to 1500kW)
            ("MEGAFLEX-250K480", "MegaFlex DPA", "MegaFlex DPA Modular 3-Phase UPS 250kW/250kVA 480V 97.4% Efficiency", 250.0, 250.0, "480V", "3PH", "3P4W", 300.7, "Decentralized Parallel Architecture (DPA)", 97.4),
            ("MEGAFLEX-500K480", "MegaFlex DPA", "MegaFlex DPA Modular 3-Phase UPS 500kW/500kVA 480V 97.4% Efficiency", 500.0, 500.0, "480V", "3PH", "3P4W", 601.4, "Decentralized Parallel Architecture (DPA)", 97.4),
            ("MEGAFLEX-750K480", "MegaFlex DPA", "MegaFlex DPA Modular 3-Phase UPS 750kW/750kVA 480V 97.4% Efficiency", 750.0, 750.0, "480V", "3PH", "3P4W", 902.1, "Decentralized Parallel Architecture (DPA)", 97.4),
            ("MEGAFLEX-1000K480", "MegaFlex DPA", "MegaFlex DPA Modular 3-Phase UPS 1000kW/1000kVA 480V 97.4% Efficiency", 1000.0, 1000.0, "480V", "3PH", "3P4W", 1202.8, "Decentralized Parallel Architecture (DPA)", 97.4),
            ("MEGAFLEX-1500K480", "MegaFlex DPA", "MegaFlex DPA Modular 3-Phase UPS 1500kW/1500kVA 480V 97.4% Efficiency", 1500.0, 1500.0, "480V", "3PH", "3P4W", 1804.2, "Decentralized Parallel Architecture (DPA)", 97.4),
            # TLE Series Monolithic High-Power 3-Phase UPS (160kW to 1000kW)
            ("TLE-160K480", "TLE Series", "ABB TLE Series Monolithic 3-Phase UPS 160kW/160kVA 480V High Power Factor", 160.0, 160.0, "480V", "3PH", "3P4W", 192.5, "Monolithic Double Conversion", 96.5),
            ("TLE-300K480", "TLE Series", "ABB TLE Series Monolithic 3-Phase UPS 300kW/300kVA 480V High Power Factor", 300.0, 300.0, "480V", "3PH", "3P4W", 360.8, "Monolithic Double Conversion", 96.5),
            ("TLE-500K480", "TLE Series", "ABB TLE Series Monolithic 3-Phase UPS 500kW/500kVA 480V High Power Factor", 500.0, 500.0, "480V", "3PH", "3P4W", 601.4, "Monolithic Double Conversion", 96.5),
            # Conceptpower DPA 500 (100kW to 500kW Modular UPS)
            ("DPA500-100K480", "Conceptpower DPA 500", "Conceptpower DPA 500 Modular UPS 100kW/100kVA 480V Hot-Swappable", 100.0, 100.0, "480V", "3PH", "3P4W", 120.3, "Hot-Swappable DPA Modules", 96.0),
            ("DPA500-300K480", "Conceptpower DPA 500", "Conceptpower DPA 500 Modular UPS 300kW/300kVA 480V Hot-Swappable", 300.0, 300.0, "480V", "3PH", "3P4W", 360.8, "Hot-Swappable DPA Modules", 96.0),
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
                cut_sheet_url=f"https://electrification.us.abb.com/products/ups-power-conditioning/{pn}",
                specs={
                    "power_rating_kw": kw,
                    "power_rating_kva": kva,
                    "efficiency_pct": eff,
                    "ups_architecture": arch,
                    "battery_compatibility": "Lithium-Ion / VRLA Battery Cabinets",
                    "catalog_section": "ABB Critical Power & High Reliability UPS"
                },
                docs={"catalog_volume": "MegaFlex DPA / TLE Technical Catalog"}
            ))

        return items
