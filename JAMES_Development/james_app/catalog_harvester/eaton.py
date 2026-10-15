"""
Eaton PowerEdge & Consultant Design Guide Industrial Equipment Catalog Harvester.
Harvests structured engineering specifications across all 17 industrial gear categories:
1. Busway (Pow-R-Way III, Pow-R-Flex, PowerWave 2 Track Busway)
2. Circuit Breakers (Power Defense PD1-PD6, Magnum DS, Magnum PXR Drawout, VacClad VCP-W, Classified)
3. Load Centers (Commercial CH Copper Bus, BR Heavy-Duty, Enclosed Circuit Breakers)
4. Motor Control Centers (Freedom 2100, FlashGard Arc-Resistant, VFD Sections)
5. Panelboards (Pow-R-Line PRL1X, PRL2X, PRL3X, PRL4X, PRL13E, PRL4F Fusible, PRL3FQS, Elevator, Column, Retrofit)
6. Softstarters & Drives (S811+, S801+, S611 Enclosed, PowerXL DG1 General Purpose VFDs)
7. Switchboards (Pow-R-Line C, Pow-R-Line Xpert, Quick Connect Generator Docking, Pow-R-Line XD Drawout, IFS, Instant)
8. Switches & Disconnects (Heavy-Duty DH, Double-Throw DT, Enviroline 316 Stainless, Shunt-Trip ST, Solar PV, Bolted Pressure Pringle)
9. Switchgear (Magnum PXR Front/Rear Access, Arc-Resistant Type 2B, Arc-Quenching AQD, VacClad-W MV)
10. Transformers (Type DT-3 DOE 2016, K-Factor K4/K13/K20, Mini-Power Centers MPC, Buck-Boost, Stainless Encapsulated, Liquid Substation)
11. Automatic Transfer Switches (Power Frame ATS, Molded Case Breaker ATS, Contactor ATS, ATC-900 / ATC-300+)
12. Paralleling Switchgear (Power Xpert PSG Multi-Generator Paralleling, MV Turbine/Recip Paralleling)
13. Power Conditioning (Active Voltage Conditioners AVC Sag Compensators, Electronic Voltage Regulators EVR, Multi-Harmonic MHF)
14. Power Distribution Systems (Power Xpert PDU, Remote Power Panels RPP)
15. Static Transfer Switches (Power Xpert STS <4ms sub-cycle transfer)
16. Surge Protective Devices (Power Xpert SPD Series 100kA-400kA, Aegis Hybrid Filter, Side-Mounted External, Integrated)
17. Uninterruptible Power Supplies (Eaton 93PM 3-Phase Modular, 9395 High-Power, 9355, 9PX Industrial)
"""

from typing import List
from james_app.catalog_harvester.base import BaseVendorHarvester
from james_app.catalog_harvester.models import CatalogItem


class EatonCatalogHarvester(BaseVendorHarvester):
    """
    Catalog extractor for Eaton Industrial Electrical Equipment.
    Grounds catalog models to Eaton PowerEdge catalog volumes and Consultant Design Guides (DG series).
    """

    vendor_name: str = "Eaton"
    vendor_key: str = "eaton"
    source_url: str = "https://www.eaton.com/us/en-us/support/poweredge-support/catalogs.html"

    def harvest(self) -> List[CatalogItem]:
        """Harvest comprehensive industrial equipment items for Eaton."""
        items: List[CatalogItem] = []

        # -------------------------------------------------------------------------
        # 1. BUSWAY (CA08100004E & DG017006EN / DG017002EN)
        # -------------------------------------------------------------------------
        busway_data = [
            ("PRW3-CU-0800A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 800A 480V Copper 3P4W", 800.0, 100.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-1000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1000A 480V Copper 3P4W", 1000.0, 100.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-1200A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1200A 480V Copper 3P4W", 1200.0, 100.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-1350A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1350A 480V Copper 3P4W", 1350.0, 150.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-1600A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1600A 480V Copper 3P4W", 1600.0, 150.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-2000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 2000A 480V Copper 3P4W", 2000.0, 150.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-2500A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 2500A 480V Copper 3P4W", 2500.0, 150.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-3000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 3000A 480V Copper 3P4W", 3000.0, 200.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-4000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 4000A 480V Copper 3P4W", 4000.0, 200.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-CU-5000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 5000A 480V Copper 3P4W", 5000.0, 200.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-AL-0800A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 800A 480V Aluminum 3P4W", 800.0, 100.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 100.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-AL-1200A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1200A 480V Aluminum 3P4W", 1200.0, 100.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 100.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-AL-1600A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 1600A 480V Aluminum 3P4W", 1600.0, 100.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 150.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-AL-2000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 2000A 480V Aluminum 3P4W", 2000.0, 150.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 150.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-AL-2500A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 2500A 480V Aluminum 3P4W", 2500.0, 150.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-AL-3000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 3000A 480V Aluminum 3P4W", 3000.0, 150.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRW3-AL-4000A-480V", "Pow-R-Way III", "Pow-R-Way III Sandwich Busway 4000A 480V Aluminum 3P4W", 4000.0, 200.0, "480Y/277V", "3PH", "3P4W", "Aluminum", "NEMA 1 Indoor", 200.0, "https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-busway-pow-r-way-design-guide-dg017002en.pdf", "DG017002EN"),
            ("PRF-CU-0225A-480V", "Pow-R-Flex", "Pow-R-Flex Low-Amp Busway 225A 480V Copper 3P4W", 225.0, 42.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 42.0, "https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/busway/pow-r-way-iii/pow-r-way-iii-busway-catalog-ca08100004e.pdf", "CA08100004E"),
            ("PRF-CU-0400A-480V", "Pow-R-Flex", "Pow-R-Flex Low-Amp Busway 400A 480V Copper 3P4W", 400.0, 42.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 42.0, "https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-control-systems/busway/pow-r-way-iii/pow-r-way-iii-busway-catalog-ca08100004e.pdf", "CA08100004E"),
            # PowerWave 2 Track Busway (DG017006EN)
            ("PW2-CU-0225A-480V", "PowerWave 2 Track Busway", "PowerWave 2 Data Center Track Busway 225A 480Y/277V Copper 3P4W Continuous Open Track", 225.0, 35.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 35.0, "https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-controls-systems/busway/eaton-powerwave-2-bus-system-design-guide-dg017006en-en-us.pdf", "DG017006EN"),
            ("PW2-CU-0400A-480V", "PowerWave 2 Track Busway", "PowerWave 2 Data Center Track Busway 400A 480Y/277V Copper 3P4W Continuous Open Track", 400.0, 42.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 42.0, "https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-controls-systems/busway/eaton-powerwave-2-bus-system-design-guide-dg017006en-en-us.pdf", "DG017006EN"),
            ("PW2-CU-0600A-480V", "PowerWave 2 Track Busway", "PowerWave 2 Data Center Track Busway 600A 480Y/277V Copper 3P4W Continuous Open Track", 600.0, 50.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 50.0, "https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-controls-systems/busway/eaton-powerwave-2-bus-system-design-guide-dg017006en-en-us.pdf", "DG017006EN"),
            ("PW2-CU-0800A-480V", "PowerWave 2 Track Busway", "PowerWave 2 Data Center Track Busway 800A 480Y/277V Copper 3P4W Continuous Open Track", 800.0, 50.0, "480Y/277V", "3PH", "3P4W", "Copper", "NEMA 1 Indoor", 50.0, "https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-controls-systems/busway/eaton-powerwave-2-bus-system-design-guide-dg017006en-en-us.pdf", "DG017006EN"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, bus_mat, nema, sccr, url, doc_code in busway_data:
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
                cut_sheet_url=url,
                specs={
                    "bus_material": bus_mat,
                    "short_circuit_withstand_ka": sccr,
                    "catalog_reference": doc_code,
                    "conductor_configuration": poles
                },
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 2. CIRCUIT BREAKERS (CA08100005E, Magnum PXR Portal & Bulletin 5651B63)
        # -------------------------------------------------------------------------
        breakers_data = [
            # Power Defense Molded Case Breakers
            ("PDG13G0050TFFN", "Power Defense PD1", "Power Defense PD1 50A 3P 480V 35kAIC TMTU Breaker", 50.0, 35.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD1", "CA08100005E"),
            ("PDG13G0100TFFN", "Power Defense PD1", "Power Defense PD1 100A 3P 480V 35kAIC TMTU Breaker", 100.0, 35.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD1", "CA08100005E"),
            ("PDG13M0060E2NN", "Power Defense PD1", "Power Defense PD1 60A 3P 480V 65kAIC PXR20 Electronic LSI Breaker", 60.0, 65.0, "480V", "3PH", "3P", "PXR20 LSI Electronic", "PD1", "CA08100005E"),
            ("PDG23G0150TFFN", "Power Defense PD2", "Power Defense PD2 150A 3P 480V 35kAIC TMTU Breaker", 150.0, 35.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD2", "CA08100005E"),
            ("PDG23M0225TFFN", "Power Defense PD2", "Power Defense PD2 225A 3P 480V 65kAIC TMTU Breaker", 225.0, 65.0, "480V", "3PH", "3P", "Fixed Thermal-Magnetic", "PD2", "CA08100005E"),
            ("PDG23K0100E2NN", "Power Defense PD2", "Power Defense PD2 100A 3P 480V 85kAIC PXR20 Electronic LSI Breaker", 100.0, 85.0, "480V", "3PH", "3P", "PXR20 LSI Electronic", "PD2", "CA08100005E"),
            ("PDG23K0225E2NN", "Power Defense PD2", "Power Defense PD2 225A 3P 480V 85kAIC PXR20 Electronic LSI Breaker", 225.0, 85.0, "480V", "3PH", "3P", "PXR20 LSI Electronic", "PD2", "CA08100005E"),
            ("PDG33G0250E2NN", "Power Defense PD3", "Power Defense PD3 250A 3P 480V 35kAIC PXR20 Electronic LSI Breaker", 250.0, 35.0, "480V", "3PH", "3P", "PXR20 LSI Electronic", "PD3", "CA08100005E"),
            ("PDG33M0400E5NN", "Power Defense PD3", "Power Defense PD3 400A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 400.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD3", "CA08100005E"),
            ("PDG33K0600E5NN", "Power Defense PD3", "Power Defense PD3 600A 3P 480V 85kAIC PXR25 Electronic LSIG Breaker", 600.0, 85.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD3", "CA08100005E"),
            ("PDG33P0400E5NN", "Power Defense PD3", "Power Defense PD3 400A 3P 480V 100kAIC PXR25 High-Interrupting Breaker", 400.0, 100.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD3", "CA08100005E"),
            ("PDG43M0800E5NN", "Power Defense PD4", "Power Defense PD4 800A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 800.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD4", "CA08100005E"),
            ("PDG43P0800E5NN", "Power Defense PD4", "Power Defense PD4 800A 3P 480V 100kAIC PXR25 Electronic LSIG Breaker", 800.0, 100.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD4", "CA08100005E"),
            ("PDG53M1000E5NN", "Power Defense PD5", "Power Defense PD5 1000A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 1000.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD5", "CA08100005E"),
            ("PDG53K1200E5NN", "Power Defense PD5", "Power Defense PD5 1200A 3P 480V 85kAIC PXR25 Electronic LSIG Breaker", 1200.0, 85.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD5", "CA08100005E"),
            ("PDG63M1600E5NN", "Power Defense PD6", "Power Defense PD6 1600A 3P 480V 65kAIC PXR25 Electronic LSIG Breaker", 1600.0, 65.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD6", "CA08100005E"),
            ("PDG63K2000E5NN", "Power Defense PD6", "Power Defense PD6 2000A 3P 480V 85kAIC PXR25 Electronic LSIG Breaker", 2000.0, 85.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD6", "CA08100005E"),
            ("PDG63P2500E5NN", "Power Defense PD6", "Power Defense PD6 2500A 3P 480V 100kAIC PXR25 Electronic LSIG Breaker", 2500.0, 100.0, "480V", "3PH", "3P", "PXR25 LSIG Electronic", "PD6", "CA08100005E"),
            # Magnum PXR Low-Voltage Power Circuit Breakers (magnum-pxr.html#models)
            ("MWI-808-3P-65K", "Magnum PXR", "Magnum PXR 800A Low-Voltage Power Circuit Breaker Drawout 65kAIC PXR20 LSI", 800.0, 65.0, "600V", "3PH", "3P", "PXR20 LSI Electronic", "Magnum PXR 800A", "Magnum-PXR-Portal"),
            ("MWI-816-3P-65K", "Magnum PXR", "Magnum PXR 1600A Low-Voltage Power Circuit Breaker Drawout 65kAIC PXR25 LSIG", 1600.0, 65.0, "600V", "3PH", "3P", "PXR25 LSIG Electronic", "Magnum PXR 1600A", "Magnum-PXR-Portal"),
            ("MWI-820-3P-65K", "Magnum PXR", "Magnum PXR 2000A Low-Voltage Power Circuit Breaker Drawout 65kAIC PXR25 LSIG", 2000.0, 65.0, "600V", "3PH", "3P", "PXR25 LSIG Electronic", "Magnum PXR 2000A", "Magnum-PXR-Portal"),
            ("MWI-832-3P-85K", "Magnum PXR", "Magnum PXR 3200A Low-Voltage Power Circuit Breaker Drawout 85kAIC PXR25 LSIG", 3200.0, 85.0, "600V", "3PH", "3P", "PXR25 LSIG Electronic", "Magnum PXR 3200A", "Magnum-PXR-Portal"),
            ("MWI-C40-3P-100K", "Magnum PXR", "Magnum PXR 4000A Low-Voltage Power Circuit Breaker Drawout 100kAIC PXR25 LSIG", 4000.0, 100.0, "600V", "3PH", "3P", "PXR25 LSIG Electronic", "Magnum PXR 4000A", "Magnum-PXR-Portal"),
            ("MWI-C50-3P-100K", "Magnum PXR", "Magnum PXR 5000A Low-Voltage Power Circuit Breaker Drawout 100kAIC PXR25 LSIG", 5000.0, 100.0, "600V", "3PH", "3P", "PXR25 LSIG Electronic", "Magnum PXR 5000A", "Magnum-PXR-Portal"),
            ("MWI-816-4P-65K", "Magnum PXR", "Magnum PXR 1600A 4-Pole Low-Voltage Power Circuit Breaker Drawout 65kAIC PXR25 LSIG", 1600.0, 65.0, "600V", "3PH", "4P4W", "PXR25 LSIG Electronic", "Magnum PXR 1600A 4P", "Magnum-PXR-Portal"),
            ("MWI-832-4P-85K", "Magnum PXR", "Magnum PXR 3200A 4-Pole Low-Voltage Power Circuit Breaker Drawout 85kAIC PXR25 LSIG", 3200.0, 85.0, "600V", "3PH", "4P4W", "PXR25 LSIG Electronic", "Magnum PXR 3200A 4P", "Magnum-PXR-Portal"),
            # Magnum DS Legacy Power Breakers
            ("MDS-808-3P-65K", "Magnum DS", "Magnum DS 800A Low-Voltage Power Circuit Breaker Drawout 65kAIC", 800.0, 65.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 800A", "CA08100005E"),
            ("MDS-816-3P-65K", "Magnum DS", "Magnum DS 1600A Low-Voltage Power Circuit Breaker Drawout 65kAIC", 1600.0, 65.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 1600A", "CA08100005E"),
            ("MDS-820-3P-65K", "Magnum DS", "Magnum DS 2000A Low-Voltage Power Circuit Breaker Drawout 65kAIC", 2000.0, 65.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 2000A", "CA08100005E"),
            ("MDS-832-3P-85K", "Magnum DS", "Magnum DS 3200A Low-Voltage Power Circuit Breaker Drawout 85kAIC", 3200.0, 85.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 3200A", "CA08100005E"),
            ("MDS-C40-3P-100K", "Magnum DS", "Magnum DS 4000A Low-Voltage Power Circuit Breaker Drawout 100kAIC", 4000.0, 100.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 4000A", "CA08100005E"),
            ("MDS-C50-3P-100K", "Magnum DS", "Magnum DS 5000A Low-Voltage Power Circuit Breaker Drawout 100kAIC", 5000.0, 100.0, "600V", "3PH", "3P", "Digitrip 1150+ LSIG", "Magnum 5000A", "CA08100005E"),
            # Medium Voltage Vacuum Circuit Breakers
            ("50VCP-W-1200A", "VacClad-W", "5kV 1200A VacClad Vacuum Circuit Breaker 50kAIC Drawout", 1200.0, 50.0, "5 kV", "3PH", "3P", "Vacuum Interrupter", "VCP-W 5kV", "CA08100005E"),
            ("150VCP-W-2000A", "VacClad-W", "15kV 2000A VacClad Vacuum Circuit Breaker 50kAIC Drawout", 2000.0, 50.0, "15 kV", "3PH", "3P", "Vacuum Interrupter", "VCP-W 15kV", "CA08100005E"),
            # Classified UL Replacement Breakers (Bulletin 5651B63)
            ("CL120", "Classified Replacement", "Classified 1-Pole 20A 120/240V 10kAIC Replacement Circuit Breaker", 20.0, 10.0, "120/240V", "1PH", "1P", "Thermal-Magnetic", "Classified 1-Pole", "5651B63"),
            ("CL230", "Classified Replacement", "Classified 2-Pole 30A 120/240V 10kAIC Replacement Circuit Breaker", 30.0, 10.0, "120/240V", "1PH", "2P", "Thermal-Magnetic", "Classified 2-Pole", "5651B63"),
            ("CL250", "Classified Replacement", "Classified 2-Pole 50A 120/240V 10kAIC Replacement Circuit Breaker", 50.0, 10.0, "120/240V", "1PH", "2P", "Thermal-Magnetic", "Classified 2-Pole", "5651B63"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, trip_unit, frame, doc_code in breakers_data:
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
                cut_sheet_url="https://www.eaton.com/us/en-us/catalog/electrical-circuit-protection/magnum-pxr.html#models" if "MWI" in pn else "https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/circuit-breakers/power-defense-mccb/power-defense-catalog-ca08100005e.pdf",
                specs={
                    "frame_size": frame,
                    "trip_unit": trip_unit,
                    "catalog_reference": doc_code
                },
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 3. LOAD CENTERS (CA08100002E, Type CH, Type BR, Enclosed Breakers)
        # -------------------------------------------------------------------------
        load_centers = [
            ("CH12L125R-COM", "CH Series Commercial", "CH Commercial 125A 3PH 208Y/120V 12-Circuit Main Lug Load Center NEMA 3R", 125.0, 10.0, "208Y/120V", "3PH", "3P4W", 12, "NEMA 3R Rainproof", "Copper"),
            ("CH24L125C-COM", "CH Series Commercial", "CH Commercial 125A 3PH 208Y/120V 24-Circuit Main Lug Load Center NEMA 1", 125.0, 10.0, "208Y/120V", "3PH", "3P4W", 24, "NEMA 1 Indoor", "Copper"),
            ("CH24B200C-COM", "CH Series Commercial", "CH Commercial 200A 3PH 208Y/120V 24-Circuit Main Breaker Load Center NEMA 1", 200.0, 22.0, "208Y/120V", "3PH", "3P4W", 24, "NEMA 1 Indoor", "Copper"),
            ("CH30L125R-COM", "CH Series Commercial", "CH Commercial 125A 3PH 208Y/120V 30-Circuit Main Lug Load Center NEMA 3R", 125.0, 10.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 3R Rainproof", "Copper"),
            ("CH30B225R-COM", "CH Series Commercial", "CH Commercial 225A 3PH 208Y/120V 30-Circuit Main Breaker Load Center NEMA 3R", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 3R Rainproof", "Copper"),
            ("CH42L225G-COM", "CH Series Commercial", "CH Commercial 225A 3PH 208Y/120V 42-Circuit Main Lug Load Center NEMA 1", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper"),
            ("CH42B200C-COM", "CH Series Commercial", "CH Commercial 200A 3PH 208Y/120V 42-Circuit Main Breaker Load Center NEMA 1", 200.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper"),
            ("CH42B225R-COM", "CH Series Commercial", "CH Commercial 225A 3PH 208Y/120V 42-Circuit Main Breaker Load Center NEMA 3R", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 3R Rainproof", "Copper"),
            ("CH42L225R-COM", "CH Series Commercial", "CH Commercial 225A 3PH 208Y/120V 42-Circuit Main Lug Load Center NEMA 3R", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 3R Rainproof", "Copper"),
            ("BR1224L125R-COM", "BR Series Commercial", "BR Commercial 125A 1PH 120/240V 12-Circuit Main Lug Load Center NEMA 3R", 125.0, 10.0, "120/240V", "1PH", "1P3W", 12, "NEMA 3R Rainproof", "Aluminum"),
            ("BR2442B150R-COM", "BR Series Commercial", "BR Commercial 150A 1PH 120/240V 24-Circuit Main Breaker Load Center NEMA 3R", 150.0, 22.0, "120/240V", "1PH", "1P3W", 24, "NEMA 3R Rainproof", "Aluminum"),
            ("BR3040B200R-COM", "BR Series Commercial", "BR Commercial 200A 1PH 120/240V 30-Circuit Main Breaker Load Center NEMA 3R", 200.0, 22.0, "120/240V", "1PH", "1P3W", 30, "NEMA 3R Rainproof", "Aluminum"),
            ("BR4242B225C-COM", "BR Series Commercial", "BR Commercial 225A 1PH 120/240V 42-Circuit Main Breaker Load Center NEMA 1", 225.0, 22.0, "120/240V", "1PH", "1P3W", 42, "NEMA 1 Indoor", "Copper"),
            ("BR4242B225R-COM", "BR Series Commercial", "BR Commercial 225A 1PH 120/240V 42-Circuit Main Breaker Load Center NEMA 3R", 225.0, 22.0, "120/240V", "1PH", "1P3W", 42, "NEMA 3R Rainproof", "Aluminum"),
            # Enclosed Circuit Breakers
            ("ECCB-100A-N1", "Enclosed Breakers", "Eaton Enclosed Circuit Breaker 100A 3P 480V NEMA 1 Indoor", 100.0, 35.0, "480V", "3PH", "3P", 0, "NEMA 1 Indoor", "Copper"),
            ("ECCB-225A-N3R", "Enclosed Breakers", "Eaton Enclosed Circuit Breaker 225A 3P 480V NEMA 3R Rainproof", 225.0, 65.0, "480V", "3PH", "3P", 0, "NEMA 3R Rainproof", "Copper"),
            ("ECCB-400A-N3R", "Enclosed Breakers", "Eaton Enclosed Circuit Breaker 400A 3P 480V NEMA 3R Rainproof", 400.0, 65.0, "480V", "3PH", "3P", 0, "NEMA 3R Rainproof", "Copper"),
            ("ECCB-600A-N4X", "Enclosed Breakers", "Eaton Enclosed Circuit Breaker 600A 3P 480V NEMA 4X Stainless Steel", 600.0, 65.0, "480V", "3PH", "3P", 0, "NEMA 4X Stainless", "Copper"),
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-controls-systems/loadcenter-and-circuit-breaker-catalog/eaton-loadcenters-and-circuit-breakers-typech-ca08100002e.pdf",
                specs={"bus_material": bus_mat, "catalog_volume": "Volume 1: Residential and Light Commercial (CA08100002E)"},
                docs={"catalog_volume": "CA08100002E"}
            ))

        # -------------------------------------------------------------------------
        # 4. MOTOR CONTROL CENTERS (MCC) (CA08100004E & DG043001EN)
        # -------------------------------------------------------------------------
        mcc_data = [
            ("F2100-600A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 600A 480V 3PH 65kAIC", 600.0, 65.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-800A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 800A 480V 3PH 65kAIC", 800.0, 65.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-1200A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 1200A 480V 3PH 65kAIC", 1200.0, 65.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-1600A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 1600A 480V 3PH 100kAIC", 1600.0, 100.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-2000A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 2000A 480V 3PH 100kAIC", 2000.0, 100.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-2500A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 2500A 480V 3PH 100kAIC", 2500.0, 100.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("F2100-3200A-480V", "Freedom 2100", "Freedom 2100 Motor Control Center 3200A 480V 3PH 100kAIC High-Amp Bus", 3200.0, 100.0, "480V", "3PH", "3P", "NEMA 1A Gasketed", "Copper", False),
            ("FG2100-0800A-480V", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center 800A 480V 65kAIC", 800.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
            ("FG2100-1200A-480V", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center 1200A 480V 65kAIC", 1200.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
            ("FG2100-1600A-480V", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center 1600A 480V 65kAIC", 1600.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
            ("FG2100-2000A-480V", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center 2000A 480V 100kAIC", 2000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
            ("FG2100-2500A-480V", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center 2500A 480V 100kAIC", 2500.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
            ("FG2100-VFD-100HP", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center Section with 100HP VFD Bucket 480V", 140.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
            ("FG2100-VFD-200HP", "FlashGard Arc-Resistant", "FlashGard Arc-Resistant Motor Control Center Section with 200HP VFD Bucket 480V", 260.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", True),
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-low-voltage-mcc-design-guide-dg043001en.pdf",
                specs={
                    "bus_material": bus_mat,
                    "arc_resistant": arc_res,
                    "starter_sizes": "NEMA Size 1 through Size 6",
                    "design_guide": "DG043001EN"
                },
                docs={"document_code": "DG043001EN"}
            ))

        # -------------------------------------------------------------------------
        # 5. PANELBOARDS (Pow-R-Line 1X, 2X, 3X, 4X, 13E, Fusible, Elevator, Column)
        # -------------------------------------------------------------------------
        panels = [
            # Pow-R-Line 1X (DG014001EN)
            ("PRL1X-18-100A", "Pow-R-Line 1X", "Pow-R-Line 1X 100A 208Y/120V 18-Circuit Branch Lighting Panel NEMA 1", 100.0, 10.0, "208Y/120V", "3PH", "3P4W", 18, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL1X-30-225A", "Pow-R-Line 1X", "Pow-R-Line 1X 225A 208Y/120V 30-Circuit Branch Lighting Panelboard NEMA 1", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL1X-42-225A", "Pow-R-Line 1X", "Pow-R-Line 1X 225A 208Y/120V 42-Circuit Branch Lighting Panelboard NEMA 1", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL1X-42-225R", "Pow-R-Line 1X", "Pow-R-Line 1X 225A 208Y/120V 42-Circuit Lighting Panelboard NEMA 3R Outdoor", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 3R Rainproof", "Copper", "DG014001EN"),
            ("PRL1X-42-400A", "Pow-R-Line 1X", "Pow-R-Line 1X 400A 208Y/120V 42-Circuit Heavy Lighting Panelboard NEMA 1", 400.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL1X-54-400A", "Pow-R-Line 1X", "Pow-R-Line 1X 400A 208Y/120V 54-Circuit High-Density Commercial Panel NEMA 1", 400.0, 22.0, "208Y/120V", "3PH", "3P4W", 54, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            # Pow-R-Line 2X (DG014001EN)
            ("PRL2X-30-100A", "Pow-R-Line 2X", "Pow-R-Line 2X 100A 480Y/277V 30-Circuit Commercial Panelboard NEMA 1", 100.0, 14.0, "480Y/277V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL2X-42-225A", "Pow-R-Line 2X", "Pow-R-Line 2X 225A 480Y/277V 42-Circuit Commercial Panelboard NEMA 1", 225.0, 22.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL2X-42-400A", "Pow-R-Line 2X", "Pow-R-Line 2X 400A 480Y/277V 42-Circuit Commercial Panelboard 65kAIC NEMA 1", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL2X-42-400R", "Pow-R-Line 2X", "Pow-R-Line 2X 400A 480Y/277V 42-Circuit Commercial Panelboard 65kAIC NEMA 3R", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 3R Rainproof", "Copper", "DG014001EN"),
            ("PRL2X-54-400A", "Pow-R-Line 2X", "Pow-R-Line 2X 400A 480Y/277V 54-Circuit High-Density Commercial Panel 65kAIC", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 54, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            # Pow-R-Line 3X (DG014001EN)
            ("PRL3X-42-400A", "Pow-R-Line 3X", "Pow-R-Line 3X 400A 480V 3PH 42-Space Power Distribution Panelboard 65kAIC", 400.0, 65.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL3X-42-600A", "Pow-R-Line 3X", "Pow-R-Line 3X 600A 480V 3PH 42-Space Power Distribution Panelboard 65kAIC", 600.0, 65.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL3X-42-800A", "Pow-R-Line 3X", "Pow-R-Line 3X 800A 480V 3PH 42-Space Power Distribution Panelboard 100kAIC", 800.0, 100.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            ("PRL3X-54-800A", "Pow-R-Line 3X", "Pow-R-Line 3X 800A 480V 3PH 54-Space Power Distribution Panelboard 100kAIC", 800.0, 100.0, "480V", "3PH", "3P3W", 54, "NEMA 1 Indoor", "Copper", "DG014001EN"),
            # Pow-R-Line 4X (DG014003EN)
            ("PRL4X-800A-480V", "Pow-R-Line 4X", "Pow-R-Line 4X 800A 480V Heavy Industrial Power Distribution Panelboard 100kAIC", 800.0, 100.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "DG014003EN"),
            ("PRL4X-1200A-480V", "Pow-R-Line 4X", "Pow-R-Line 4X 1200A 480V Heavy Industrial Power Distribution Panelboard 200kAIC", 1200.0, 200.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "DG014003EN"),
            # Pow-R-Line 13E (DG014002EN)
            ("PRL13E-30-225A", "Pow-R-Line 13E", "Pow-R-Line 13E High-Density Commercial Panelboard 225A 208Y/120V 30-Circuit", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper", "DG014002EN"),
            ("PRL13E-42-400A", "Pow-R-Line 13E", "Pow-R-Line 13E High-Density Commercial Panelboard 400A 480Y/277V 42-Circuit", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "DG014002EN"),
            # Fusible Panelboards (DG014004EN & DG014008EN)
            ("PRL4F-400A-600V", "Pow-R-Line 4F", "Pow-R-Line 4F Fusible Switch Distribution Panelboard 400A 600V Class R/J 200kAIC", 400.0, 200.0, "600V", "3PH", "3P3W", 30, "NEMA 1 Indoor", "Copper", "DG014004EN"),
            ("PRL4F-800A-600V", "Pow-R-Line 4F", "Pow-R-Line 4F Fusible Switch Distribution Panelboard 800A 600V Class R/J 200kAIC", 800.0, 200.0, "600V", "3PH", "3P3W", 30, "NEMA 1 Indoor", "Copper", "DG014004EN"),
            ("PRL4F-1200A-600V", "Pow-R-Line 4F", "Pow-R-Line 4F Fusible Switch Distribution Panelboard 1200A 600V Class R/J 200kAIC", 1200.0, 200.0, "600V", "3PH", "3P3W", 30, "NEMA 1 Indoor", "Copper", "DG014004EN"),
            ("PRL3FQS-225A-600V", "Pow-R-Line 3FQS", "Pow-R-Line 3FQS Quick-Switch Fusible Panelboard 225A 600V 200kAIC", 225.0, 200.0, "600V", "3PH", "3P3W", 30, "NEMA 1 Indoor", "Copper", "DG014008EN"),
            ("PRL3FQS-400A-600V", "Pow-R-Line 3FQS", "Pow-R-Line 3FQS Quick-Switch Fusible Panelboard 400A 600V 200kAIC", 400.0, 200.0, "600V", "3PH", "3P3W", 30, "NEMA 1 Indoor", "Copper", "DG014008EN"),
            # Elevator Control Panelboards (DG014005EN)
            ("PRL-ELEV-100A", "Elevator Control Panel", "Elevator Control Power Panelboard 100A 480V with Integrated Shunt-Trip & CPT", 100.0, 65.0, "480V", "3PH", "3P", 12, "NEMA 1 Indoor", "Copper", "DG014005EN"),
            ("PRL-ELEV-200A", "Elevator Control Panel", "Elevator Control Power Panelboard 200A 480V with Integrated Shunt-Trip & CPT", 200.0, 65.0, "480V", "3PH", "3P", 12, "NEMA 1 Indoor", "Copper", "DG014005EN"),
            ("PRL-ELEV-400A", "Elevator Control Panel", "Elevator Control Power Panelboard 400A 480V with Integrated Shunt-Trip & CPT", 400.0, 65.0, "480V", "3PH", "3P", 12, "NEMA 1 Indoor", "Copper", "DG014005EN"),
            # Column-Width Panelboards (DG014007EN)
            ("PRL-COL-100A", "Column-Width Panel", "Column-Width Narrow Panelboard 100A 208Y/120V 8.6-Inch Width for I-Beam Mounting", 100.0, 10.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper", "DG014007EN"),
            ("PRL-COL-225A", "Column-Width Panel", "Column-Width Narrow Panelboard 225A 480Y/277V 8.6-Inch Width for I-Beam Mounting", 225.0, 22.0, "480Y/277V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper", "DG014007EN"),
            # Retrofit Ez-Box Panelboard Interiors (DG014006EN)
            ("PRL-RETRO-225A", "Retrofit Panelboard", "Retrofit Chassis Replacement Interior 225A 480Y/277V for Existing Enclosures", 225.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Chassis Replacement", "Copper", "DG014006EN"),
            ("PRL-RETRO-400A", "Retrofit Panelboard", "Retrofit Chassis Replacement Interior 400A 480Y/277V for Existing Enclosures", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "Chassis Replacement", "Copper", "DG014006EN"),
            # Legacy Pow-R-Line Series (Preserved)
            ("PRL1A-18-100A", "Pow-R-Line 1a", "Pow-R-Line 1a 100A 208Y/120V 18-Circuit Branch Lighting Panel", 100.0, 10.0, "208Y/120V", "3PH", "3P4W", 18, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL1A-30-225A", "Pow-R-Line 1a", "Pow-R-Line 1a 225A 208Y/120V 30-Circuit Lighting Panelboard", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL1A-42-225A", "Pow-R-Line 1a", "Pow-R-Line 1a 225A 208Y/120V 42-Circuit Lighting Panelboard", 225.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL1A-42-400A", "Pow-R-Line 1a", "Pow-R-Line 1a 400A 208Y/120V 42-Circuit Heavy Lighting Panelboard", 400.0, 22.0, "208Y/120V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL2A-30-100A", "Pow-R-Line 2a", "Pow-R-Line 2a 100A 480Y/277V 30-Circuit Commercial Panelboard", 100.0, 14.0, "480Y/277V", "3PH", "3P4W", 30, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL2A-42-225A", "Pow-R-Line 2a", "Pow-R-Line 2a 225A 480Y/277V 42-Circuit Commercial Panelboard", 225.0, 22.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL2A-42-400A", "Pow-R-Line 2a", "Pow-R-Line 2a 400A 480Y/277V 42-Circuit Commercial Panelboard 65kAIC", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL2A-54-400A", "Pow-R-Line 2a", "Pow-R-Line 2a 400A 480Y/277V 54-Circuit High-Density Commercial Panel", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", 54, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL3A-42-400A", "Pow-R-Line 3a", "Pow-R-Line 3a 400A 480V 3PH 42-Space Power Distribution Panelboard", 400.0, 65.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL3A-42-600A", "Pow-R-Line 3a", "Pow-R-Line 3a 600A 480V 3PH 42-Space Power Distribution Panelboard", 600.0, 65.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL3A-42-800A", "Pow-R-Line 3a", "Pow-R-Line 3a 800A 480V 3PH 42-Space Power Distribution Panelboard 100kAIC", 800.0, 100.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL4B-800A-480V", "Pow-R-Line 4b", "Pow-R-Line 4b 800A 480V Heavy Industrial Distribution Panelboard", 800.0, 100.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL4B-1200A-480V", "Pow-R-Line 4b", "Pow-R-Line 4b 1200A 480V Heavy Industrial Distribution Panelboard 200kAIC", 1200.0, 200.0, "480V", "3PH", "3P3W", 42, "NEMA 1 Indoor", "Copper", "CA08100003E"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, slots, nema, bus_mat, doc_code in panels:
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
                cut_sheet_url=f"https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-panelboard-{series.lower().replace(' ', '-')}-design-guide.pdf",
                specs={"bus_material": bus_mat, "design_guide": doc_code},
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 6. SOFTSTARTERS & DRIVES (S811+, S801+, S611 & PowerXL DG1 VFDs)
        # -------------------------------------------------------------------------
        softstarters = [
            # Solid-State Reduced Voltage Soft Starters (CA08100007E)
            ("S811+N37P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 37A 480V 25HP Integral Bypass", 37.0, 65.0, "480V", "3PH", "3P", 25.0, "Open / Chassis", "CA08100007E"),
            ("S811+R65P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 65A 480V 50HP Integral Bypass", 65.0, 65.0, "480V", "3PH", "3P", 50.0, "Open / Chassis", "CA08100007E"),
            ("S811+T18P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 180A 480V 150HP Integral Bypass", 180.0, 65.0, "480V", "3PH", "3P", 150.0, "Open / Chassis", "CA08100007E"),
            ("S811+T30P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 304A 480V 250HP Integral Bypass", 304.0, 65.0, "480V", "3PH", "3P", 250.0, "Open / Chassis", "CA08100007E"),
            ("S811+U50P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 500A 480V 400HP Integral Bypass", 500.0, 65.0, "480V", "3PH", "3P", 400.0, "Open / Chassis", "CA08100007E"),
            ("S811+V10P3S", "S811+ Series", "S811+ Reduced Voltage Soft Starter 1000A 480V 900HP Integral Bypass", 1000.0, 65.0, "480V", "3PH", "3P", 900.0, "Open / Chassis", "CA08100007E"),
            ("S801+V10N3S", "S801+ Compact", "S801+ Compact Reduced Voltage Soft Starter 1000A 480V 900HP", 1000.0, 50.0, "480V", "3PH", "3P", 900.0, "Open / Chassis", "CA08100007E"),
            ("S611-100HP-480V", "S611 Enclosed", "S611 Enclosed Industrial Soft Starter 125A 480V 100HP NEMA 12", 125.0, 65.0, "480V", "3PH", "3P", 100.0, "NEMA 12 Dust-Tight", "CA08100007E"),
            ("S611-250HP-480V", "S611 Enclosed", "S611 Enclosed Industrial Soft Starter 300A 480V 250HP NEMA 3R", 300.0, 65.0, "480V", "3PH", "3P", 250.0, "NEMA 3R Rainproof", "CA08100007E"),
            # PowerXL DG1 General Purpose Variable Frequency Drives (DG040001EB)
            ("DG1-34016FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 16A 480V 10HP IP21 EMC Filter", 16.0, 100.0, "480V", "3PH", "3P", 10.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-34031FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 31A 480V 20HP IP21 EMC Filter", 31.0, 100.0, "480V", "3PH", "3P", 20.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-34061FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 61A 480V 40HP IP21 EMC Filter", 61.0, 100.0, "480V", "3PH", "3P", 40.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-34105FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 105A 480V 75HP IP21 EMC Filter", 105.0, 100.0, "480V", "3PH", "3P", 75.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-34140FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 140A 480V 100HP IP21 EMC Filter", 140.0, 100.0, "480V", "3PH", "3P", 100.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-34205FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 205A 480V 150HP IP21 EMC Filter", 205.0, 100.0, "480V", "3PH", "3P", 150.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-34261FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 261A 480V 200HP IP21 EMC Filter", 261.0, 100.0, "480V", "3PH", "3P", 200.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-34310FB-C21C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 310A 480V 250HP IP21 EMC Filter", 310.0, 100.0, "480V", "3PH", "3P", 250.0, "IP21 / NEMA 1", "DG040001EB"),
            ("DG1-32048FB-C54C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 48A 208V 15HP IP54 Washdown", 48.0, 100.0, "208V", "3PH", "3P", 15.0, "IP54 / NEMA 12", "DG040001EB"),
            ("DG1-32088FB-C54C", "PowerXL DG1 VFD", "PowerXL DG1 General Purpose VFD 88A 208V 30HP IP54 Washdown", 88.0, 100.0, "208V", "3PH", "3P", 30.0, "IP54 / NEMA 12", "DG040001EB"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, hp, nema, doc_code in softstarters:
            items.append(CatalogItem(
                part_number=pn,
                manufacturer=self.vendor_name,
                series=series,
                domain="motor_control",
                type_tag="SOFTSTART",
                type_name="Solid-State Soft Starter / VFD",
                description=desc,
                voltage=volt,
                amps=amps,
                aic=aic,
                poles=poles,
                phase=phase,
                nema_rating=nema,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/industrialcontrols-drives-automation-sensors/variable-frequency-drives/powerxl-dg1-variable-frequency-drives/powerxl-dg1-design-guide-dg040001eb.pdf" if "DG1" in pn else "https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/motor-control-contactors-starters/s811-soft-starters/s811-soft-starter-catalog-ca08100007e.pdf",
                specs={
                    "horsepower": hp,
                    "drive_type": "Variable Frequency Drive" if "DG1" in pn else "Solid-State Soft Starter",
                    "design_guide": doc_code
                },
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 7. SWITCHBOARDS (Pow-R-Line C, Pow-R-Line Xpert, Quick Connect, XD, IFS)
        # -------------------------------------------------------------------------
        swbds = [
            # Pow-R-Line Xpert Switchboards (DG015001EN)
            ("PRLX-2000A-480V", "Pow-R-Line Xpert", "Pow-R-Line Xpert Switchboard 2000A 480Y/277V 3PH 4W 65kAIC Front-Accessible", 2000.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015001EN"),
            ("PRLX-3000A-480V", "Pow-R-Line Xpert", "Pow-R-Line Xpert Switchboard 3000A 480Y/277V 3PH 4W 100kAIC Main Breaker", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015001EN"),
            ("PRLX-4000A-480V", "Pow-R-Line Xpert", "Pow-R-Line Xpert Switchboard 4000A 480Y/277V 3PH 4W 100kAIC Main Breaker", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015001EN"),
            ("PRLX-5000A-480V", "Pow-R-Line Xpert", "Pow-R-Line Xpert Switchboard 5000A 480Y/277V 3PH 4W 100kAIC High-Amp Bus", 5000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015001EN"),
            ("PRLX-6000A-480V", "Pow-R-Line Xpert", "Pow-R-Line Xpert Switchboard 6000A 480Y/277V 3PH 4W 100kAIC Main Service Lineup", 6000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015001EN"),
            # Quick Connect Switchboards with Cam-Lock Generator Tap Box (DG015007EN)
            ("PRL-QC-1200A-480V", "Quick Connect Switchboard", "Quick Connect Switchboard 1200A 480V with Integrated Cam-Lock Generator Docking Station", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 3R Rainproof", "Copper", "DG015007EN"),
            ("PRL-QC-2000A-480V", "Quick Connect Switchboard", "Quick Connect Switchboard 2000A 480V with Integrated Cam-Lock Generator Docking Station", 2000.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 3R Rainproof", "Copper", "DG015007EN"),
            ("PRL-QC-3000A-480V", "Quick Connect Switchboard", "Quick Connect Switchboard 3000A 480V with Integrated Cam-Lock Generator Docking Station", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 3R Rainproof", "Copper", "DG015007EN"),
            ("PRL-QC-4000A-480V", "Quick Connect Switchboard", "Quick Connect Switchboard 4000A 480V with Integrated Cam-Lock Generator Docking Station", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 3R Rainproof", "Copper", "DG015007EN"),
            # Pow-R-Line XD Drawout Switchboards (DG015003EN)
            ("PRL-XD-2000A-480V", "Pow-R-Line XD", "Pow-R-Line XD Drawout Breaker Switchboard 2000A 480V 65kAIC", 2000.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015003EN"),
            ("PRL-XD-3000A-480V", "Pow-R-Line XD", "Pow-R-Line XD Drawout Breaker Switchboard 3000A 480V 100kAIC", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015003EN"),
            # Integrated Facility Systems (IFS) (DG015005EN)
            ("IFS-1600A-480V", "Integrated Facility Systems", "IFS Switchboard 1600A 480V Integrated Transformer & Sub-Panels", 1600.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015005EN"),
            ("IFS-2000A-480V", "Integrated Facility Systems", "IFS Switchboard 2000A 480V Integrated 150kVA Dry-Type Transformer & Panels", 2000.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015005EN"),
            ("IFS-3000A-480V", "Integrated Facility Systems", "IFS Switchboard 3000A 480V Integrated 300kVA Dry-Type Transformer & Panels", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015005EN"),
            # Instant Stock Switchboards (DG015008EN)
            ("PRL-INST-0400A", "Instant Switchboard", "Instant Pre-Engineered Stock Switchboard 400A 480Y/277V 65kAIC NEMA 1", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015008EN"),
            ("PRL-INST-0800A", "Instant Switchboard", "Instant Pre-Engineered Stock Switchboard 800A 480Y/277V 65kAIC NEMA 1", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015008EN"),
            ("PRL-INST-1200A", "Instant Switchboard", "Instant Pre-Engineered Stock Switchboard 1200A 480Y/277V 65kAIC NEMA 1", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "DG015008EN"),
            # Pow-R-Line C Standard
            ("PRL-C-1200A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 1200A 480Y/277V 3PH 4W 65kAIC Front-Accessible", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL-C-2000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 2000A 480Y/277V 3PH 4W 65kAIC Front-Accessible", 2000.0, 65.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL-C-3000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 3000A 480Y/277V 3PH 4W 100kAIC Main Breaker", 3000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL-C-4000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 4000A 480Y/277V 3PH 4W 100kAIC Main Breaker", 4000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL-C-5000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 5000A 480Y/277V 3PH 4W 100kAIC High-Amp Bus", 5000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "CA08100003E"),
            ("PRL-C-6000A-480V", "Pow-R-Line C", "Pow-R-Line C Switchboard 6000A 480Y/277V 3PH 4W 100kAIC Main Service", 6000.0, 100.0, "480Y/277V", "3PH", "3P4W", "NEMA 1 Indoor", "Copper", "CA08100003E"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, bus_mat, doc_code in swbds:
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-swbd-prlxpert-design-guide-dg015001en.pdf",
                specs={"bus_material": bus_mat, "accessibility": "Front-Accessible", "design_guide": doc_code},
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 8. SWITCHES & DISCONNECTS (Heavy-Duty, Double-Throw, Enviroline 316, ST, Solar)
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
            # Enviroline NEMA 4X Grade 316 Stainless Steel (DG008002EN)
            ("DH361UWK-316", "Enviroline 316 Stainless", "Enviroline Heavy Duty Safety Switch 30A 3P 600V Non-Fusible NEMA 4X Grade 316 Stainless", 30.0, 10.0, "600V", "3PH", "3P", "NEMA 4X 316SS", False, 10.0),
            ("DH362UWK-316", "Enviroline 316 Stainless", "Enviroline Heavy Duty Safety Switch 60A 3P 600V Non-Fusible NEMA 4X Grade 316 Stainless", 60.0, 10.0, "600V", "3PH", "3P", "NEMA 4X 316SS", False, 10.0),
            ("DH363UWK-316", "Enviroline 316 Stainless", "Enviroline Heavy Duty Safety Switch 100A 3P 600V Non-Fusible NEMA 4X Grade 316 Stainless", 100.0, 10.0, "600V", "3PH", "3P", "NEMA 4X 316SS", False, 10.0),
            ("DH364UWK-316", "Enviroline 316 Stainless", "Enviroline Heavy Duty Safety Switch 200A 3P 600V Non-Fusible NEMA 4X Grade 316 Stainless", 200.0, 10.0, "600V", "3PH", "3P", "NEMA 4X 316SS", False, 10.0),
            ("DH365UWK-316", "Enviroline 316 Stainless", "Enviroline Heavy Duty Safety Switch 400A 3P 600V Non-Fusible NEMA 4X Grade 316 Stainless", 400.0, 10.0, "600V", "3PH", "3P", "NEMA 4X 316SS", False, 10.0),
            ("DH366UWK-316", "Enviroline 316 Stainless", "Enviroline Heavy Duty Safety Switch 600A 3P 600V Non-Fusible NEMA 4X Grade 316 Stainless", 600.0, 10.0, "600V", "3PH", "3P", "NEMA 4X 316SS", False, 10.0),
            # Shunt-Trip Safety Switches (DG008002EN)
            ("DH362UGK-ST", "Shunt-Trip Safety Switch", "Shunt-Trip Heavy Duty Safety Switch 60A 3P 600V with 120VAC Shunt-Trip Mechanism", 60.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH363UGK-ST", "Shunt-Trip Safety Switch", "Shunt-Trip Heavy Duty Safety Switch 100A 3P 600V with 120VAC Shunt-Trip Mechanism", 100.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH364UGK-ST", "Shunt-Trip Safety Switch", "Shunt-Trip Heavy Duty Safety Switch 200A 3P 600V with 120VAC Shunt-Trip Mechanism", 200.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DH365UGK-ST", "Shunt-Trip Safety Switch", "Shunt-Trip Heavy Duty Safety Switch 400A 3P 600V with 120VAC Shunt-Trip Mechanism", 400.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            # Solar Photovoltaic DC Disconnects (DG008002EN)
            ("DC600V-030A-3R", "Solar PV Disconnect", "Solar Photovoltaic Heavy Duty DC Disconnect 30A 600VDC NEMA 3R", 30.0, 10.0, "600VDC", "DC", "2P", "NEMA 3R Rainproof", False, 10.0),
            ("DC600V-060A-3R", "Solar PV Disconnect", "Solar Photovoltaic Heavy Duty DC Disconnect 60A 600VDC NEMA 3R", 60.0, 10.0, "600VDC", "DC", "2P", "NEMA 3R Rainproof", False, 10.0),
            ("DC600V-100A-3R", "Solar PV Disconnect", "Solar Photovoltaic Heavy Duty DC Disconnect 100A 600VDC NEMA 3R", 100.0, 10.0, "600VDC", "DC", "2P", "NEMA 3R Rainproof", False, 10.0),
            ("DC1000V-200A-3R", "Solar PV Disconnect", "Solar Photovoltaic Heavy Duty High-Voltage DC Disconnect 200A 1000VDC NEMA 3R", 200.0, 10.0, "1000VDC", "DC", "2P", "NEMA 3R Rainproof", False, 10.0),
            # Double Throw Manual Transfer (DG008002EN)
            ("DT361UGK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 30A 3P 600V Non-Fusible NEMA 1", 30.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DT362UGK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 60A 3P 600V Non-Fusible NEMA 1", 60.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DT363UGK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 100A 3P 600V Non-Fusible NEMA 1", 100.0, 10.0, "600V", "3PH", "3P", "NEMA 1 Indoor", False, 10.0),
            ("DT363URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 100A 3P 600V Non-Fusible NEMA 3R", 100.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            ("DT364URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 200A 3P 600V Non-Fusible NEMA 3R", 200.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            ("DT364UWK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 200A 3P 600V Non-Fusible NEMA 4X Stainless", 200.0, 10.0, "600V", "3PH", "3P", "NEMA 4X Stainless", False, 10.0),
            ("DT365URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 400A 3P 600V Non-Fusible NEMA 3R", 400.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            ("DT366URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 600A 3P 600V Non-Fusible NEMA 3R", 600.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            ("DT367URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 800A 3P 600V Non-Fusible NEMA 3R", 800.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
            ("DT368URK", "Double Throw Safety Switch", "Eaton Double Throw Safety Switch 1200A 3P 600V Non-Fusible NEMA 3R", 1200.0, 10.0, "600V", "3PH", "3P", "NEMA 3R Rainproof", False, 10.0),
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-safety-switch-general-design-guide-dg008001en.pdf",
                specs={"fusible": fusible, "sccr_kaic": sccr, "catalog_volume": "Volume 2: Commercial Distribution (CA08100003E)"},
                docs={"catalog_volume": "CA08100003E"}
            ))

        # -------------------------------------------------------------------------
        # 9. SWITCHGEAR (Magnum PXR, Arc-Resistant Type 2B, Arc-Quenching AQD, VacClad)
        # -------------------------------------------------------------------------
        switchgear = [
            # Magnum PXR Switchgear (DG019007EN, DG019008EN, DG019009EN, DG019010, DG019011)
            ("MPXR-FA-2000A", "Magnum PXR Switchgear", "Magnum PXR Front-Access Low-Voltage Switchgear 2000A 480V 65kAIC Drawout", 2000.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 65.0, "DG019007EN"),
            ("MPXR-FA-3200A", "Magnum PXR Switchgear", "Magnum PXR Front-Access Low-Voltage Switchgear 3200A 480V 85kAIC Drawout", 3200.0, 85.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 85.0, "DG019007EN"),
            ("MPXR-RA-4000A", "Magnum PXR Switchgear", "Magnum PXR Rear-Access Low-Voltage Switchgear 4000A 480V 100kAIC Drawout", 4000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 100.0, "DG019008EN"),
            ("MPXR-RA-5000A", "Magnum PXR Switchgear", "Magnum PXR Rear-Access Low-Voltage Switchgear 5000A 480V 100kAIC Drawout", 5000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 100.0, "DG019008EN"),
            ("MPXR-AR-2000A", "Magnum PXR Arc-Resistant", "Magnum PXR Arc-Resistant Type 2B Low-Voltage Switchgear 2000A 480V 65kAIC", 2000.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", 65.0, "DG019011-EN-US"),
            ("MPXR-AR-4000A", "Magnum PXR Arc-Resistant", "Magnum PXR Arc-Resistant Type 2B Low-Voltage Switchgear 4000A 480V 100kAIC", 4000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Arc-Resistant", "Copper", 100.0, "DG019011-EN-US"),
            ("MPXR-AQ-3200A", "Magnum PXR Arc-Quenching", "Magnum PXR Arc-Quenching Switchgear with AQD Arc-Quenching Device 3200A 85kAIC", 3200.0, 85.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 85.0, "DG019009EN"),
            ("MPXR-AQ-5000A", "Magnum PXR Arc-Quenching", "Magnum PXR Arc-Quenching Switchgear with AQD Arc-Quenching Device 5000A 100kAIC", 5000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 100.0, "DG019009EN"),
            # Magnum DS Legacy Switchgear
            ("MDS-LV-2000A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 2000A 480V 65kAIC Drawout", 2000.0, 65.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 65.0, "CA08100004E"),
            ("MDS-LV-3200A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 3200A 480V 85kAIC Drawout", 3200.0, 85.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 85.0, "CA08100004E"),
            ("MDS-LV-4000A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 4000A 480V 100kAIC Drawout", 4000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 100.0, "CA08100004E"),
            ("MDS-LV-5000A", "Magnum DS Low-Voltage Switchgear", "Magnum DS Low-Voltage Metal-Enclosed Switchgear 5000A 480V 100kAIC Drawout", 5000.0, 100.0, "480V", "3PH", "3P", "NEMA 1 Indoor", "Copper", 100.0, "CA08100004E"),
            # Medium Voltage VacClad-W
            ("VCW-5KV-1200A", "VacClad-W Medium Voltage", "VacClad-W 5kV 1200A Metal-Clad Vacuum Switchgear 50kAIC Drawout", 1200.0, 50.0, "5 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0, "CA08100004E"),
            ("VCW-15KV-1200A", "VacClad-W Medium Voltage", "VacClad-W 15kV 1200A Metal-Clad Vacuum Switchgear 50kAIC Drawout 95kV BIL", 1200.0, 50.0, "15 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0, "CA08100004E"),
            ("VCW-15KV-2000A", "VacClad-W Medium Voltage", "VacClad-W 15kV 2000A Metal-Clad Vacuum Switchgear 50kAIC Drawout 95kV BIL", 2000.0, 50.0, "15 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0, "CA08100004E"),
            ("VCW-15KV-3000A", "VacClad-W Medium Voltage", "VacClad-W 15kV 3000A Metal-Clad Vacuum Switchgear 50kAIC Drawout 95kV BIL", 3000.0, 50.0, "15 kV", "3PH", "3P", "NEMA 1 Indoor", "Copper", 50.0, "CA08100004E"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, nema, bus_mat, withstand, doc_code in switchgear:
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/low-voltage-power-distribution-controls-systems/switchgear/low-voltage-switchgear-documents/magnum-pxr/design-guides/eaton-magnum-pxr-low-voltage-switchgear-dg019008en.pdf",
                specs={
                    "bus_material": bus_mat,
                    "short_time_withstand_ka": withstand,
                    "standard": "UL 1558 / IEEE C37.20.2",
                    "design_guide": doc_code
                },
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 10. TRANSFORMERS (DT-3 DOE 2016, K-Factor, Mini-Power Centers, Buck-Boost, Encapsulated)
        # -------------------------------------------------------------------------
        xfmrs = [
            ("V48M28T1516CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 15kVA 480V-208Y/120V Copper", 15.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T3016CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 30kVA 480V-208Y/120V Copper", 30.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T4516CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 45kVA 480V-208Y/120V Copper", 45.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T7516CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 75kVA 480V-208Y/120V Copper", 75.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T1216CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 112.5kVA 480V-208Y/120V Copper", 112.5, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T1516CU-HD", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 150kVA 480V-208Y/120V Copper", 150.0, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T2216CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 225kVA 480V-208Y/120V Copper", 225.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T3316CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 300kVA 480V-208Y/120V Copper", 300.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T5016CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 500kVA 480V-208Y/120V Copper", 500.0, "480V", "208Y/120V", "3PH", 5.75, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T7516CU-LG", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 750kVA 480V-208Y/120V Copper", 750.0, "480V", "208Y/120V", "3PH", 5.75, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            ("V48M28T1016CU", "Type DT-3 Dry-Type", "Eaton DT-3 DOE 2016 Dry-Type Transformer 1000kVA 480V-208Y/120V Copper", 1000.0, "480V", "208Y/120V", "3PH", 5.75, "Copper", 150.0, "NEMA 2/3R", "DG009001EN"),
            # K-Factor Harmonic Mitigating (DG009002EN)
            ("V48M28K4-045K", "K-Factor 4 Harmonic", "Eaton K-Factor 4 Harmonic Mitigating Transformer 45kVA 480V-208Y/120V", 45.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K4-112K", "K-Factor 4 Harmonic", "Eaton K-Factor 4 Harmonic Mitigating Transformer 112.5kVA 480V-208Y/120V", 112.5, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K4-225K", "K-Factor 4 Harmonic", "Eaton K-Factor 4 Harmonic Mitigating Transformer 225kVA 480V-208Y/120V", 225.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K13-75K", "K-Factor 13 Harmonic", "Eaton K-Factor 13 Harmonic Mitigating Transformer 75kVA 480V-208Y/120V", 75.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K13-150K", "K-Factor 13 Harmonic", "Eaton K-Factor 13 Harmonic Mitigating Transformer 150kVA 480V-208Y/120V", 150.0, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K13-300K", "K-Factor 13 Harmonic", "Eaton K-Factor 13 Harmonic Mitigating Transformer 300kVA 480V-208Y/120V", 300.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K20-075K", "K-Factor 20 Harmonic", "Eaton K-Factor 20 High-Harmonic Transformer 75kVA 480V-208Y/120V", 75.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K20-150K", "K-Factor 20 Harmonic", "Eaton K-Factor 20 High-Harmonic Transformer 150kVA 480V-208Y/120V", 150.0, "480V", "208Y/120V", "3PH", 5.0, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            ("V48M28K20-300K", "K-Factor 20 Harmonic", "Eaton K-Factor 20 High-Harmonic Transformer 300kVA 480V-208Y/120V", 300.0, "480V", "208Y/120V", "3PH", 5.5, "Copper", 150.0, "NEMA 2/3R", "DG009002EN"),
            # Mini-Power Centers (MPC) (DG009003EN)
            ("MPC-05KVA-480-208", "Mini-Power Center", "Eaton Mini-Power Center 5kVA 480V-208Y/120V Integrated Breaker & Panel NEMA 3R", 5.0, "480V", "208Y/120V", "3PH", 4.0, "Copper", 115.0, "NEMA 3R Rainproof", "DG009003EN"),
            ("MPC-10KVA-480-208", "Mini-Power Center", "Eaton Mini-Power Center 10kVA 480V-208Y/120V Integrated Breaker & Panel NEMA 3R", 10.0, "480V", "208Y/120V", "3PH", 4.0, "Copper", 115.0, "NEMA 3R Rainproof", "DG009003EN"),
            ("MPC-15KVA-480-208", "Mini-Power Center", "Eaton Mini-Power Center 15kVA 480V-208Y/120V Integrated Breaker & Panel NEMA 3R", 15.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 115.0, "NEMA 3R Rainproof", "DG009003EN"),
            ("MPC-25KVA-480-208", "Mini-Power Center", "Eaton Mini-Power Center 25kVA 480V-208Y/120V Integrated Breaker & Panel NEMA 3R", 25.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 115.0, "NEMA 3R Rainproof", "DG009003EN"),
            ("MPC-30KVA-480-208", "Mini-Power Center", "Eaton Mini-Power Center 30kVA 480V-208Y/120V Integrated Breaker & Panel NEMA 3R", 30.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 115.0, "NEMA 3R Rainproof", "DG009003EN"),
            # Buck-Boost Transformers (DG009004EN)
            ("S20N11S01N", "Buck-Boost Transformer", "Eaton Single-Phase Buck-Boost Transformer 1kVA 120/240V to 12/24V NEMA 3R", 1.0, "120/240V", "12/24V", "1PH", 3.0, "Copper", 115.0, "NEMA 3R Rainproof", "DG009004EN"),
            ("S20N11S02N", "Buck-Boost Transformer", "Eaton Single-Phase Buck-Boost Transformer 2kVA 120/240V to 12/24V NEMA 3R", 2.0, "120/240V", "12/24V", "1PH", 3.0, "Copper", 115.0, "NEMA 3R Rainproof", "DG009004EN"),
            ("S20N11S05N", "Buck-Boost Transformer", "Eaton Single-Phase Buck-Boost Transformer 5kVA 120/240V to 12/24V NEMA 3R", 5.0, "120/240V", "12/24V", "1PH", 3.5, "Copper", 115.0, "NEMA 3R Rainproof", "DG009004EN"),
            ("S20N11S07N", "Buck-Boost Transformer", "Eaton Single-Phase Buck-Boost Transformer 7.5kVA 120/240V to 12/24V NEMA 3R", 7.5, "120/240V", "12/24V", "1PH", 3.5, "Copper", 115.0, "NEMA 3R Rainproof", "DG009004EN"),
            # Harsh Environment Encapsulated 316 Stainless (DG009005EN)
            ("EP-SS-15KVA-480-208", "Harsh Environment Encapsulated", "Harsh Environment Transformer 15kVA 480V-208Y/120V NEMA 4X Grade 316 Stainless Encapsulated", 15.0, "480V", "208Y/120V", "3PH", 4.0, "Copper", 115.0, "NEMA 4X 316SS", "DG009005EN"),
            ("EP-SS-30KVA-480-208", "Harsh Environment Encapsulated", "Harsh Environment Transformer 30kVA 480V-208Y/120V NEMA 4X Grade 316 Stainless Encapsulated", 30.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 115.0, "NEMA 4X 316SS", "DG009005EN"),
            ("EP-SS-45KVA-480-208", "Harsh Environment Encapsulated", "Harsh Environment Transformer 45kVA 480V-208Y/120V NEMA 4X Grade 316 Stainless Encapsulated", 45.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 115.0, "NEMA 4X 316SS", "DG009005EN"),
            ("EP-SS-75KVA-480-208", "Harsh Environment Encapsulated", "Harsh Environment Transformer 75kVA 480V-208Y/120V NEMA 4X Grade 316 Stainless Encapsulated", 75.0, "480V", "208Y/120V", "3PH", 4.5, "Copper", 115.0, "NEMA 4X 316SS", "DG009005EN"),
            # Medium Voltage Liquid Substation Transformers
            ("SUB-1500KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 1500kVA 13.8kV-480Y/277V FR3", 1500.0, "13.8 kV", "480Y/277V", "3PH", 5.75, "Copper", 65.0, "NEMA 3R Outdoor", "CA08100003E"),
            ("SUB-2500KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 2500kVA 13.8kV-480Y/277V FR3", 2500.0, "13.8 kV", "480Y/277V", "3PH", 5.75, "Copper", 65.0, "NEMA 3R Outdoor", "CA08100003E"),
            ("SUB-3500KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 3500kVA 13.8kV-480Y/277V FR3", 3500.0, "13.8 kV", "480Y/277V", "3PH", 5.75, "Copper", 65.0, "NEMA 3R Outdoor", "CA08100003E"),
            ("SUB-5000KVA-13.8KV", "Liquid Substation Transformer", "Eaton Liquid-Filled Substation Transformer 5000kVA 13.8kV-480Y/277V FR3", 5000.0, "13.8 kV", "480Y/277V", "3PH", 6.0, "Copper", 65.0, "NEMA 3R Outdoor", "CA08100003E"),
        ]
        for pn, series, desc, kva, v_pri, v_sec, phase, z, winding, temp_rise, nema, doc_code in xfmrs:
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
                poles="3P" if "3PH" in phase else "1P",
                nema_rating=nema,
                impedance_z=z,
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-dtdt-general-purpose-design-guide-dg009001en.pdf",
                specs={
                    "primary_voltage": v_pri,
                    "secondary_voltage": v_sec,
                    "winding_material": winding,
                    "temperature_rise_c": temp_rise,
                    "efficiency_standard": "DOE 2016 Compliant",
                    "design_guide": doc_code
                },
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 11. AUTOMATIC TRANSFER SWITCHES (ATS) (Power Frame, Breaker, Contactor)
        # -------------------------------------------------------------------------
        ats_data = [
            # Contactor-Based ATS with ATC-300+ (DG140001EN)
            ("AT300-100A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 100A 480V 3PH Open Transition NEMA 1", 100.0, 42.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Contactor", "NEMA 1 Indoor", "DG140001EN"),
            ("AT300-200A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 200A 480V 3PH Open Transition NEMA 3R", 200.0, 42.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Contactor", "NEMA 3R Rainproof", "DG140001EN"),
            ("AT300-400A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 400A 480V 3PH Delayed Transition NEMA 3R", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", "Delayed Transition", "Contactor", "NEMA 3R Rainproof", "DG140001EN"),
            ("ATC300-0600A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 600A 480V 3PH Open Transition NEMA 1", 600.0, 65.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Contactor", "NEMA 1 Indoor", "DG140001EN"),
            ("ATC300-0800A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 800A 480V 3PH Delayed Transition NEMA 3R", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "Delayed Transition", "Contactor", "NEMA 3R Rainproof", "DG140001EN"),
            ("ATC300-1000A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 1000A 480V 3PH Open Transition NEMA 1", 1000.0, 65.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Contactor", "NEMA 1 Indoor", "DG140001EN"),
            ("ATC300-1200A-480V", "ATC-300+ Series", "Eaton ATC-300+ Contactor ATS 1200A 480V 3PH Delayed Transition NEMA 3R", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "Delayed Transition", "Contactor", "NEMA 3R Rainproof", "DG140001EN"),
            # Molded Case Breaker-Based ATS with ATC-900 (DG140002EN)
            ("ATB-PD-0225A", "Power Defense ATS", "Power Defense Molded Case Breaker ATS 225A 480V 3PH with ATC-900", 225.0, 65.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Molded Case Breaker", "NEMA 1 Indoor", "DG140002EN"),
            ("ATB-PD-0400A", "Power Defense ATS", "Power Defense Molded Case Breaker ATS 400A 480V 3PH with ATC-900", 400.0, 65.0, "480Y/277V", "3PH", "3P4W", "Open Transition", "Molded Case Breaker", "NEMA 1 Indoor", "DG140002EN"),
            ("ATB-PD-0800A", "Power Defense ATS", "Power Defense Molded Case Breaker ATS 800A 480V 3PH with ATC-900", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Molded Case Breaker", "NEMA 1 Indoor", "DG140002EN"),
            ("ATB-PD-1200A", "Power Defense ATS", "Power Defense Molded Case Breaker ATS 1200A 480V 3PH with ATC-900", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Molded Case Breaker", "NEMA 1 Indoor", "DG140002EN"),
            # Power Frame ATS (Magnum PXR Based) (DG140003EN)
            ("ATV-PXR-0800A", "Magnum PXR Power Frame ATS", "Magnum PXR Power Frame ATS 800A 480V 65kAIC Drawout with ATC-900", 800.0, 65.0, "480V", "3PH", "3P", "Closed Transition", "Drawout Power Frame", "NEMA 1 Indoor", "DG140003EN"),
            ("ATV-PXR-1600A", "Magnum PXR Power Frame ATS", "Magnum PXR Power Frame ATS 1600A 480V 65kAIC Drawout with ATC-900", 1600.0, 65.0, "480V", "3PH", "3P", "Closed Transition", "Drawout Power Frame", "NEMA 1 Indoor", "DG140003EN"),
            ("ATV-PXR-2000A", "Magnum PXR Power Frame ATS", "Magnum PXR Power Frame ATS 2000A 480V 65kAIC Drawout with ATC-900", 2000.0, 65.0, "480V", "3PH", "3P", "Closed Transition", "Drawout Power Frame", "NEMA 1 Indoor", "DG140003EN"),
            ("ATV-PXR-3000A", "Magnum PXR Power Frame ATS", "Magnum PXR Power Frame ATS 3000A 480V 100kAIC Drawout with ATC-900", 3000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "Drawout Power Frame", "NEMA 1 Indoor", "DG140003EN"),
            ("ATV-PXR-4000A", "Magnum PXR Power Frame ATS", "Magnum PXR Power Frame ATS 4000A 480V 100kAIC Drawout with ATC-900", 4000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "Drawout Power Frame", "NEMA 1 Indoor", "DG140003EN"),
            ("ATV-PXR-5000A", "Magnum PXR Power Frame ATS", "Magnum PXR Power Frame ATS 5000A 480V 100kAIC Drawout with ATC-900", 5000.0, 100.0, "480V", "3PH", "3P", "Closed Transition", "Drawout Power Frame", "NEMA 1 Indoor", "DG140003EN"),
            # ATC-900 Bypass Isolation
            ("AT900-600A-480V", "ATC-900 Series", "Eaton ATC-900 Advanced ATS 600A 480V Closed Transition Bypass Isolation", 600.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Bypass Isolation", "NEMA 1 Indoor", "DG140004EN"),
            ("AT900-800A-480V", "ATC-900 Series", "Eaton ATC-900 Advanced ATS 800A 480V Closed Transition Bypass Isolation", 800.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Bypass Isolation", "NEMA 1 Indoor", "DG140004EN"),
            ("AT900-1200A-480V", "ATC-900 Series", "Eaton ATC-900 Advanced ATS 1200A 480V Closed Transition Bypass Isolation", 1200.0, 65.0, "480Y/277V", "3PH", "3P4W", "Closed Transition", "Bypass Isolation", "NEMA 1 Indoor", "DG140004EN"),
            # Magnum DS Legacy ATS
            ("ATV-MDS-1600A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 1600A 480V Drawout 65kAIC", 1600.0, 65.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor", "CA08100004E"),
            ("ATV-MDS-2000A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 2000A 480V Drawout 65kAIC", 2000.0, 65.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor", "CA08100004E"),
            ("ATV-MDS-3000A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 3000A 480V Drawout 100kAIC", 3000.0, 100.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor", "CA08100004E"),
            ("ATV-MDS-4000A", "Magnum Breaker ATS", "Eaton Magnum DS Breaker-Based ATS 4000A 480V Drawout 100kAIC", 4000.0, 100.0, "480V", "3PH", "3P", "Open/Delayed Transition", "Drawout Power Breaker", "NEMA 1 Indoor", "CA08100004E"),
        ]
        for pn, series, desc, amps, aic, volt, phase, poles, trans_type, mechanism, nema, doc_code in ats_data:
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-ats-breaker-design-guide-dg140002en.pdf",
                specs={
                    "transition_type": trans_type,
                    "switching_mechanism": mechanism,
                    "design_guide": doc_code
                },
                docs={"document_code": doc_code}
            ))

        # -------------------------------------------------------------------------
        # 12. PARALLELING SWITCHGEAR (PSG) (Multi-Gen Prime & Standby Paralleling)
        # -------------------------------------------------------------------------
        psg_data = [
            ("PSG-480V-2GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 2-Generator Master Sync 65kAIC", 4000.0, 65.0, "480V", "3PH", "3P", 2, "Emergency / Standby Paralleling"),
            ("PSG-480V-3GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 3-Generator Priority Shed 100kAIC", 6000.0, 100.0, "480V", "3PH", "3P", 3, "Prime Power / Multi-Source"),
            ("PSG-480V-4GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 4-Generator Utility Paralleling 100kAIC", 8000.0, 100.0, "480V", "3PH", "3P", 4, "Utility Co-generation & Peak Shaving"),
            ("PSG-480V-5GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 5-Generator Prime Power Lineup 10000A 100kAIC", 10000.0, 100.0, "480V", "3PH", "3P", 5, "Prime Power Data Center Paralleling"),
            ("PSG-480V-6GEN", "Power Xpert PSG", "Power Xpert Paralleling Switchgear 480V 6-Generator Mission-Critical Lineup 12000A 100kAIC", 12000.0, 100.0, "480V", "3PH", "3P", 6, "Mission-Critical N+2 Paralleling"),
            ("PSG-13.8KV-2GEN", "Power Xpert MV-PSG", "Power Xpert 13.8kV Medium Voltage Paralleling Switchgear VacClad 50kAIC", 2000.0, 50.0, "13.8 kV", "3PH", "3P", 2, "Medium Voltage Turbine/Recip Paralleling"),
            ("PSG-13.8KV-3GEN", "Power Xpert MV-PSG", "Power Xpert 13.8kV Medium Voltage Paralleling Switchgear VacClad 3000A 50kAIC", 3000.0, 50.0, "13.8 kV", "3PH", "3P", 3, "Campus Primary Generation Paralleling"),
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/services/eess/eess-documents/eaton-paralleling-switchgear-design-guide-letter-january-en-us.pdf",
                specs={
                    "generators_supported": gens,
                    "application": app,
                    "synchronization_control": "Woodward / PLC Master Synchronization"
                },
                docs={"document_code": "PSG-Design-Guide"}
            ))

        # -------------------------------------------------------------------------
        # 13. POWER CONDITIONING (AVC Sag Compensators, EVR Regulators, MHF Filters)
        # -------------------------------------------------------------------------
        pwr_cond = [
            ("AVC-480V-150KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 150kVA 480V 90% Sag Ride-Through", 180.0, 65.0, 150.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("AVC-480V-300KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 300kVA 480V 90% Sag Ride-Through", 360.0, 65.0, 300.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("AVC-480V-600KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 600kVA 480V 90% Sag Ride-Through", 720.0, 65.0, 600.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("AVC-480V-900KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 900kVA 480V Industrial Ride-Through", 1080.0, 65.0, 900.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            ("AVC-480V-1500KVA", "Active Voltage Conditioner", "Eaton AVC Active Voltage Conditioner 1500kVA 480V Industrial Process", 1800.0, 65.0, 1500.0, "480V", "3PH", "Voltage Sag Correction to 90% Depth", "2 ms"),
            # Electronic Voltage Regulators (EVR) (DG158006EN)
            ("EVR-480V-100KVA", "Electronic Voltage Regulator", "Eaton EVR Electronic Voltage Regulator 100kVA 480V ±1% Voltage Regulation", 120.0, 65.0, 100.0, "480V", "3PH", "Precision Voltage Regulation ±1%", "< 1 cycle"),
            ("EVR-480V-250KVA", "Electronic Voltage Regulator", "Eaton EVR Electronic Voltage Regulator 250kVA 480V ±1% Voltage Regulation", 300.0, 65.0, 250.0, "480V", "3PH", "Precision Voltage Regulation ±1%", "< 1 cycle"),
            ("EVR-480V-500KVA", "Electronic Voltage Regulator", "Eaton EVR Electronic Voltage Regulator 500kVA 480V ±1% Voltage Regulation", 600.0, 65.0, 500.0, "480V", "3PH", "Precision Voltage Regulation ±1%", "< 1 cycle"),
            # Multi-Harmonic Filters (MHF)
            ("MHF-480V-100A", "Power Xpert MHF", "Power Xpert Multi-Harmonic Filter 100A 480V Active Harmonic Compensation", 100.0, 65.0, None, "480V", "3PH", "Active Harmonic Cancellation 2nd-51st", "< 1 ms"),
            ("MHF-480V-200A", "Power Xpert MHF", "Power Xpert Multi-Harmonic Filter 200A 480V Active Harmonic Compensation", 200.0, 65.0, None, "480V", "3PH", "Active Harmonic Cancellation 2nd-51st", "< 1 ms"),
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-power-conditioning-design-guide-34.4-DG158006EN.pdf",
                specs={"capability": cap, "response_time": resp, "design_guide": "DG158006EN"},
                docs={"document_code": "DG158006EN"}
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
        # 16. SURGE PROTECTIVE DEVICES (SPD) (Aegis, Integrated, Side-Mounted)
        # -------------------------------------------------------------------------
        spds = [
            # Aegis Hybrid Filter Series (DG158005EN)
            ("AG-050-480Y", "Aegis Series SPD", "Aegis Series Hybrid Filter / Surge Suppressor 50kA/Phase 480Y/277V Type 2 NEMA 4X", 50.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 2", "DG158005EN"),
            ("AG-100-480Y", "Aegis Series SPD", "Aegis Series Hybrid Filter / Surge Suppressor 100kA/Phase 480Y/277V Type 2 NEMA 4X", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 2", "DG158005EN"),
            ("AG-160-480Y", "Aegis Series SPD", "Aegis Series Hybrid Filter / Surge Suppressor 160kA/Phase 480Y/277V Type 2 NEMA 4X", 160.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 2", "DG158005EN"),
            ("AG-100-208Y", "Aegis Series SPD", "Aegis Series Hybrid Filter / Surge Suppressor 100kA/Phase 208Y/120V Type 2 NEMA 4X", 100.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 4X", "Type 2", "DG158005EN"),
            # Integrated Switchboard / Panelboard SPDs (DG158003EN)
            ("SPD-INT-100K-480Y", "Integrated SPD", "Eaton Factory-Integrated Panelboard/Switchboard SPD 100kA/Phase 480Y/277V", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "Internal Mount", "Type 1 / Type 2", "DG158003EN"),
            ("SPD-INT-160K-480Y", "Integrated SPD", "Eaton Factory-Integrated Panelboard/Switchboard SPD 160kA/Phase 480Y/277V", 160.0, 200.0, "480Y/277V", "3PH", "3P4W", "Internal Mount", "Type 1 / Type 2", "DG158003EN"),
            ("SPD-INT-250K-480Y", "Integrated SPD", "Eaton Factory-Integrated Panelboard/Switchboard SPD 250kA/Phase 480Y/277V", 250.0, 200.0, "480Y/277V", "3PH", "3P4W", "Internal Mount", "Type 1 / Type 2", "DG158003EN"),
            # Side-Mounted External Heavy Industrial SPDs (DG158004EN)
            ("SPD-EXT-100K-480Y", "Side-Mounted SPD", "Eaton Side-Mounted External Surge Protective Device 100kA/Phase 480Y/277V NEMA 4X", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "DG158004EN"),
            ("SPD-EXT-200K-480Y", "Side-Mounted SPD", "Eaton Side-Mounted External Surge Protective Device 200kA/Phase 480Y/277V NEMA 4X", 200.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "DG158004EN"),
            ("SPD-EXT-300K-480Y", "Side-Mounted SPD", "Eaton Side-Mounted External Surge Protective Device 300kA/Phase 480Y/277V NEMA 4X", 300.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "DG158004EN"),
            ("SPD-EXT-400K-480Y", "Side-Mounted SPD", "Eaton Side-Mounted External Surge Protective Device 400kA/Phase 480Y/277V NEMA 4X", 400.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "DG158004EN"),
            # Power Xpert Standard
            ("SPD-PX-100K-480Y", "Power Xpert SPD", "Power Xpert SPD 100kA/Phase 480Y/277V Type 1/Type 2 NEMA 4X", 100.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("SPD-PX-160K-480Y", "Power Xpert SPD", "Power Xpert SPD 160kA/Phase 480Y/277V Type 1/Type 2 NEMA 4X", 160.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("SPD-PX-200K-480Y", "Power Xpert SPD", "Power Xpert SPD 200kA/Phase 480Y/277V Type 1/Type 2 NEMA 4X", 200.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("SPD-PX-250K-480Y", "Power Xpert SPD", "Power Xpert SPD 250kA/Phase 480Y/277V Service Entrance Rated", 250.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("SPD-PX-300K-480Y", "Power Xpert SPD", "Power Xpert SPD 300kA/Phase 480Y/277V Heavy Industrial Main", 300.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("SPD-PX-400K-480Y", "Power Xpert SPD", "Power Xpert SPD 400kA/Phase 480Y/277V Substation/Main Switchgear", 400.0, 200.0, "480Y/277V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("SPD-PX-160K-208Y", "Power Xpert SPD", "Power Xpert SPD 160kA/Phase 208Y/120V Type 1/Type 2 NEMA 4X", 160.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("SPD-PX-250K-208Y", "Power Xpert SPD", "Power Xpert SPD 250kA/Phase 208Y/120V Service Entrance Rated", 250.0, 200.0, "208Y/120V", "3PH", "3P4W", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
            ("PTX-160-480V", "Innovative Technology IT", "Innovative Technology Severe Industrial Surge Protector 160kA 480V", 160.0, 200.0, "480V", "3PH", "3P", "NEMA 4X", "Type 1 / Type 2", "PX-SPD"),
        ]
        for pn, series, desc, surge_ka, sccr, volt, phase, poles, nema, ul_type, doc_code in spds:
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
                cut_sheet_url="https://www.eaton.com/content/dam/eaton/products/design-guides---consultant-audience/eaton-spd-aegis-design-guide-34.3-DG158005EN.pdf" if "AG-" in pn else "https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/surge-suppression/power-xpert-spd-catalog.pdf",
                specs={"surge_current_per_phase_ka": surge_ka, "sccr_kaic": sccr, "ul_1449_type": ul_type, "design_guide": doc_code},
                docs={"document_code": doc_code}
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
