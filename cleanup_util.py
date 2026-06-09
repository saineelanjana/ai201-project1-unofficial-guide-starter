#!/usr/bin/env python3
"""
OMSCS Reviews Cleanup Utility
Extract and process Reddit API JSON files for RAG model ingestion
"""

import json
import re
import html
import argparse
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

class OmscsReviewCleaner:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def clean_html(self, text: str) -> str:
        """Remove HTML entities and tags."""
        if not text:
            return ""
        text = html.unescape(text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&[a-z]+;', '', text)
        return text

    def load_json(self, filename: str) -> Any:
        """Load JSON file with error handling."""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def extract_reddit_content(self, data: Any, max_depth: int = 10, depth: int = 0) -> List[Dict]:
        """Recursively extract content from Reddit API JSON."""
        if depth > max_depth or data is None:
            return []

        content = []

        if isinstance(data, dict):
            kind = data.get("kind")
            
            # Handle Listing wrapper - check for data.data structure
            if kind == "Listing" and "data" in data:
                return self.extract_reddit_content(data["data"], max_depth, depth)
            
            # Posts (kind: t3)
            if kind == "t3":
                post_data = data.get("data", data)
                text = post_data.get("selftext", "").strip()
                if len(text) > 50:
                    content.append({
                        "type": "post",
                        "title": post_data.get("title", "").strip(),
                        "body": self.clean_html(text),
                        "score": post_data.get("score", 0),
                        "author": post_data.get("author", "[deleted]"),
                        "created": post_data.get("created_utc", None),
                    })

            # Comments (kind: t1)
            elif kind == "t1":
                comment_data = data.get("data", data)
                body = comment_data.get("body", "").strip()
                if body not in ["[deleted]", "[removed]"] and len(body) > 20:
                    content.append({
                        "type": "comment",
                        "title": "",
                        "body": self.clean_html(body),
                        "score": comment_data.get("score", 0),
                        "author": comment_data.get("author", "[deleted]"),
                        "created": comment_data.get("created_utc", None),
                    })

            # Wiki pages
            if "content_md" in data:
                text = data.get("content_md", "").strip()
                if len(text) > 50:
                    content.append({
                        "type": "wiki",
                        "title": "FAQ",
                        "body": self.clean_html(text),
                        "score": 0,
                        "author": "wiki",
                        "created": None,
                    })

            # Traverse children (common in Listing.data)
            if "children" in data and isinstance(data["children"], list):
                for child in data["children"][:100]:  # Limit to 100 per level
                    content.extend(self.extract_reddit_content(child, max_depth, depth + 1))

            # Traverse replies (common in comment objects)
            if "replies" in data and isinstance(data["replies"], dict):
                content.extend(self.extract_reddit_content(data["replies"], max_depth, depth + 1))

            # Traverse other dict values (excluding certain keys)
            skip_keys = {"kind", "data", "children", "replies", "body", "selftext", "content_md"}
            for key, value in list(data.items()):
                if key not in skip_keys and isinstance(value, (dict, list)) and depth < max_depth - 1:
                    content.extend(self.extract_reddit_content(value, max_depth, depth + 1))

        elif isinstance(data, list):
            for item in data[:50]:
                content.extend(self.extract_reddit_content(item, max_depth, depth + 1))

        return content

    def deduplicate(self, items: List[Dict]) -> List[Dict]:
        """Remove duplicate content."""
        seen = {}
        result = []

        for item in items:
            # Create normalized key
            text = item["body"].lower()
            key = re.sub(r'\s+', '', text)[:300]

            if key not in seen and len(item["body"]) > 30:
                seen[key] = True
                result.append(item)

        return result

    def categorize(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize content by topic."""
        categories = defaultdict(list)
        keywords = {
            "course-selection": ["course", "take", "recommend", "first", "pairing"],
            "difficulty": ["difficult", "hard", "easy", "workload", "hours"],
            "admissions": ["admitted", "admission", "gpa", "accepted"],
            "registration": ["register", "phase", "waitlist"],
            "ml-ai": ["machine learning", "deep learning", "ml", "ai"],
            "systems": ["systems", "gios", "hpc", "cloud"],
        }

        for item in items:
            text = (item["title"] + " " + item["body"][:300]).lower()
            found = False
            for cat, kws in keywords.items():
                if any(kw in text for kw in kws):
                    categories[cat].append(item)
                    found = True
                    break
            if not found:
                categories["general"].append(item)

        return categories

    def format_markdown(self, filename: str, items: List[Dict]) -> str:
        """Format items as markdown."""
        lines = [
            f"# {filename.replace('_', ' ').replace('-', ' ').title()}",
            "",
            "*Compiled from OMSCS community discussions*",
            "=" * 60,
            ""
        ]

        # Sort by score
        sorted_items = sorted(items, key=lambda x: x.get("score", 0), reverse=True)

        for item in sorted_items[:300]:  # Limit to 300 items
            if item["title"]:
                lines.append(f"## {item['title']}")
                lines.append("")

            lines.append(item["body"])
            lines.append("")

            if item["score"]:
                lines.append(f"*Score: {item['score']} · Author: {item['author']}*")
                lines.append("")

            lines.append("-" * 40)
            lines.append("")

        return "\n".join(lines)

    def process_file(self, filepath: Path, min_items: int = 10) -> bool:
        """Process a single file."""
        filename = filepath.name
        outname = filename.replace('-', '_') + '.md'
        outpath = self.output_dir / outname

        print(f"  Processing {filename}...", end=" ", flush=True)

        if filepath.stat().st_size == 0:
            print("SKIP (empty)")
            return False

        data = self.load_json(str(filepath))
        if data is None:
            print("SKIP (invalid)")
            return False

        items = self.extract_reddit_content(data)
        print(f"({len(items)} items) ", end="", flush=True)

        if len(items) < min_items:
            print(f"SKIP (<{min_items} items)")
            return False

        items = self.deduplicate(items)
        print(f"({len(items)} unique) ", end="", flush=True)

        markdown = self.format_markdown(filename, items)

        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print("✓")
        return True

    def run(self, min_items: int = 10) -> None:
        """Process all files."""
        files = sorted([
            f for f in self.input_dir.iterdir()
            if f.is_file() and not f.name.startswith('.')
        ])

        print("=" * 60)
        print("OMSCS Reviews Cleanup for RAG")
        print("=" * 60)
        print(f"Input:  {self.input_dir}")
        print(f"Output: {self.output_dir}")
        print(f"Min items threshold: {min_items}\n")

        processed = 0
        for filepath in files:
            if self.process_file(filepath, min_items=min_items):
                processed += 1

        print("\n" + "=" * 60)
        print(f"✅ Complete! {processed} files processed")
        print("=" * 60)

    def process_files(self, min_items: int = 10) -> None:
        """Alias for run() to maintain backward compatibility."""
        self.run(min_items=min_items)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OMSCS Reviews Cleanup Utility for RAG model ingestion")
    parser.add_argument(
        "--input-dir",
        type=str,
        default="documents/reviews",
        help="Input directory containing review files (default: documents/reviews)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="documents/reviews_cleaned",
        help="Output directory for cleaned markdown files (default: documents/reviews_cleaned)"
    )
    parser.add_argument(
        "--min-items",
        type=int,
        default=1,
        help="Minimum number of items required to process a file (default: 1)"
    )

    args = parser.parse_args()

    INPUT = args.input_dir
    OUTPUT = args.output_dir
    MIN_ITEMS = args.min_items

    cleaner = OmscsReviewCleaner(INPUT, OUTPUT)
    cleaner.process_files(min_items=MIN_ITEMS)

