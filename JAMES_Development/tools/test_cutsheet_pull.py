#!/usr/bin/env python3
"""Polite test script to verify cut-sheet URLs for 5 sample items at 5-second intervals."""

import time
import urllib.request
import urllib.error
import re
import ssl

SAMPLE_PARTS = [
    {
        "part_number": "PDG23G0150TFAN",
        "manufacturer": "Eaton",
        "type": "Molded Case Circuit Breaker",
        "url": "https://www.eaton.com/us/en-us/skuPage.PDG23G0150TFAN.html"
    },
    {
        "part_number": "EE75T3H",
        "manufacturer": "Square D / Schneider Electric",
        "type": "75kVA Dry-Type Transformer",
        "url": "https://www.se.com/us/en/product/EE75T3H/"
    },
    {
        "part_number": "LPJ-100SP",
        "manufacturer": "Bussmann (Eaton)",
        "type": "Class J 100A Fuse",
        "url": "https://www.eaton.com/us/en-us/skuPage.LPJ-100SP.html"
    },
    {
        "part_number": "5362-W",
        "manufacturer": "Leviton",
        "type": "20A Spec Grade Receptacle",
        "url": "https://www.leviton.com/en/products/5362-w"
    },
    {
        "part_number": "DH363UGK",
        "manufacturer": "Eaton",
        "type": "100A Heavy Duty Safety Switch",
        "url": "https://www.eaton.com/us/en-us/skuPage.DH363UGK.html"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("================================================================================")
print("🔍 TESTING 5 CUT-SHEET URLS AT 5-SECOND INTERVALS")
print("================================================================================\n")

results = []

for idx, item in enumerate(SAMPLE_PARTS, 1):
    pn = item["part_number"]
    mfg = item["manufacturer"]
    url = item["url"]
    
    print(f"[{idx}/5] Requesting: {pn} ({mfg})")
    print(f"     URL: {url}")
    
    start_time = time.time()
    status_code = None
    title = None
    pdf_links = []
    error_msg = None
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            status_code = resp.getcode()
            html = resp.read().decode("utf-8", errors="ignore")
            
            # Extract <title>
            m_title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
            if m_title:
                title = m_title.group(1).strip()
                title = " ".join(title.split())
                
            # Extract PDF links on the page (cut sheets, specs)
            all_pdfs = re.findall(r'href=["\'](https?://[^"\']+\.pdf[^"\']*)["\']', html, re.I)
            pdf_links = list(set(all_pdfs))[:3]
            
    except urllib.error.HTTPError as e:
        status_code = e.code
        error_msg = f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        error_msg = f"URL Error: {e.reason}"
    except Exception as e:
        error_msg = f"Exception: {e}"
        
    duration = time.time() - start_time
    
    result_entry = {
        "part_number": pn,
        "manufacturer": mfg,
        "status": status_code,
        "duration_sec": round(duration, 2),
        "title": title,
        "pdf_count": len(pdf_links),
        "sample_pdfs": pdf_links,
        "error": error_msg
    }
    results.append(result_entry)
    
    if status_code == 200:
        print(f"     ✅ Status: {status_code} OK (Response in {duration:.2f}s)")
        if title:
            print(f"     📄 Page Title: {title[:75]}...")
        if pdf_links:
            print(f"     📎 Direct PDF Links Found ({len(pdf_links)}):")
            for pdf in pdf_links:
                print(f"        -> {pdf}")
    else:
        print(f"     ⚠️ Status: {status_code or 'Failed'} ({error_msg}) (in {duration:.2f}s)")
        
    if idx < len(SAMPLE_PARTS):
        print(f"     ⏳ Sleeping 5.0 seconds (polite interval)...\n")
        time.sleep(5.0)

print("\n================================================================================")
print("📊 SUMMARY OF CUT-SHEET URL TEST RESULTS")
print("================================================================================")
for r in results:
    status_sym = "✅ 200 OK" if r["status"] == 200 else f"❌ {r['status'] or r['error']}"
    print(f"• {r['part_number']} ({r['manufacturer']}): {status_sym} - {r['duration_sec']}s")
