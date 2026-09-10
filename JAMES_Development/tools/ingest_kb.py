#!/usr/bin/env python3
"""
CLI Ingestion Tool for Build Aware Knowledge Base
Scans documentation, specs, PDF manuals, and guides, chunking and indexing them into SQLite FTS5.

Usage:
    python -m tools.ingest_kb
    python -m tools.ingest_kb --path docs/
    python -m tools.ingest_kb --file docs/PANEL_RULES_AND_LAYOUT_SPEC.md --category specs
    python -m tools.ingest_kb --stats
    python -m tools.ingest_kb --search "breaker sizing 125%"
"""

import sys
import os
import argparse
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from james_app.knowledge_base import KnowledgeBaseManager


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into Build Aware SQLite FTS5 Knowledge Base")
    parser.add_argument("--path", "-p", type=str, help="Directory path to scan and ingest recursively")
    parser.add_argument("--file", "-f", type=str, help="Single file to ingest (.md, .pdf, .html, .txt)")
    parser.add_argument("--category", "-c", type=str, help="Category override (specs, workflow, nec_code, objects, manuals)")
    parser.add_argument("--clear", action="store_true", help="Clear Knowledge Base before ingestion")
    parser.add_argument("--stats", "-s", action="store_true", help="Show Knowledge Base statistics")
    parser.add_argument("--search", "-q", type=str, help="Test search query against FTS5 Knowledge Base")
    
    args = parser.parse_args()
    kb = KnowledgeBaseManager()

    if args.clear:
        print("Clearing Knowledge Base...")
        kb.clear()
        print("Knowledge Base cleared.")

    if args.stats:
        stats = kb.get_stats()
        print("\n=======================================================")
        print("  Build Aware Knowledge Base Statistics")
        print("=======================================================")
        print(f"Total Chunks Indexed: {stats['total_chunks']}")
        print(f"Distinct Files:       {stats['distinct_files']}")
        print(f"Categories:           {', '.join(stats['categories']) or 'None'}")
        print("\nFiles Indexed:")
        for f in stats["files"]:
            print(f"  • {f['file']:<40} [{f['type'].upper():<4}] [{f['category']:<10}] {f['chunks']} chunks")
        print("=======================================================\n")
        return

    if args.search:
        results = kb.search(args.search, category=args.category, limit=5)
        print(f"\nSearch results for '{args.search}' ({len(results)} matches):")
        print("-------------------------------------------------------")
        for idx, r in enumerate(results, 1):
            print(f"[{idx}] {r['title']} > {r['section_heading']}")
            print(f"    Source: {r['source_file']} (Category: {r['category']}, Rank: {r['rank']})")
            print(f"    Snippet: {r['snippet']}")
            print("-------------------------------------------------------")
        return

    # Ingestion Mode
    project_root = Path(__file__).resolve().parent.parent
    
    if args.file:
        count = kb.ingest_file(args.file, category=args.category)
        print(f"✓ Ingested {args.file} -> {count} chunks indexed.")
    elif args.path:
        results = kb.ingest_directory(args.path, recursive=True, category=args.category)
        total = sum(results.values())
        print(f"✓ Ingested directory {args.path} -> {len(results)} files, {total} total chunks indexed.")
    else:
        # Default: Ingest faq/ directories, docs/ directory, data/knowledge_base, and root PDF/doc files
        faq_dir = project_root / "faq"
        data_faq_dir = project_root / "data" / "faq"
        docs_dir = project_root / "docs"
        kb_dir = project_root / "data" / "knowledge_base"
        
        faq_dir.mkdir(parents=True, exist_ok=True)
        data_faq_dir.mkdir(parents=True, exist_ok=True)
        kb_dir.mkdir(parents=True, exist_ok=True)
        
        scan_targets = [faq_dir, data_faq_dir, docs_dir, kb_dir]
        total_indexed = 0
        total_files = 0
        
        for target in scan_targets:
            if target.exists():
                print(f"Scanning directory: {target}")
                results = kb.ingest_directory(str(target), recursive=True)
                total_indexed += sum(results.values())
                total_files += len(results)

        print(f"\n✓ Completed default ingestion -> {total_files} files, {total_indexed} total chunks indexed into SQLite FTS5.")

    stats = kb.get_stats()
    print(f"\nKnowledge Base Ready: {stats['total_chunks']} chunks from {stats['distinct_files']} files.")


if __name__ == "__main__":
    main()
