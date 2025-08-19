#!/usr/bin/env python3
"""
Convert a .docx document to Markdown (.md)

Dependencies:
  pip install -r utils/requirements.txt

Usage:
  python utils/docx_to_md.py /path/to/input.docx [--out /path/to/output.md]
  # If --out is omitted, writes alongside the input with .md extension

Notes:
- Uses mammoth to convert DOCX -> HTML, then html2text to convert HTML -> Markdown.
- Attempts to preserve headings, lists, links, images, and basic formatting.
"""
import argparse
import pathlib
import sys

from typing import Optional

try:
    import mammoth  # type: ignore
except ImportError as e:
    print("Missing dependency 'mammoth'. Run: pip install -r utils/requirements.txt", file=sys.stderr)
    raise

try:
    import html2text  # type: ignore
except ImportError as e:
    print("Missing dependency 'html2text'. Run: pip install -r utils/requirements.txt", file=sys.stderr)
    raise


def docx_to_markdown(input_path: pathlib.Path, output_path: Optional[pathlib.Path] = None) -> pathlib.Path:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.suffix.lower() != ".docx":
        raise ValueError("Input must be a .docx file")

    # Read DOCX and convert to HTML via mammoth
    with input_path.open("rb") as f:
        result = mammoth.convert_to_html(f)
        html = result.value  # The generated HTML
        messages = result.messages
        if messages:
            # Print conversion warnings to stderr but do not fail
            for m in messages:
                print(f"[mammoth] {m.type}: {m.message}", file=sys.stderr)

    # Convert HTML to Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.protect_links = True
    h.body_width = 0  # do not wrap lines
    markdown = h.handle(html)

    # Determine output path
    if output_path is None:
        output_path = input_path.with_suffix(".md")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(markdown, encoding="utf-8")
    return output_path

