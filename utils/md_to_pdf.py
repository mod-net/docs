#!/usr/bin/env python3
"""
Convert a Markdown (.md) document to PDF (.pdf)

Pipeline:
  Markdown (.md) -> HTML (python-markdown) -> PDF (WeasyPrint)

Dependencies:
  pip install -r utils/requirements.txt

Usage:
  python utils/md_to_pdf.py /path/to/input.md [--out /path/to/output.pdf] [--css /path/to/style.css]
  # If --out is omitted, writes alongside the input with .pdf extension

Notes:
- WeasyPrint renders HTML+CSS to high-quality PDFs with good Unicode support.
- You can pass a custom CSS file via --css for branding/typography.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Optional

try:
    import markdown  # type: ignore
except ImportError:
    print("Missing dependency 'markdown'. Run: pip install -r utils/requirements.txt", file=sys.stderr)
    raise

try:
    from weasyprint import HTML  # type: ignore
except ImportError:
    print("Missing dependency 'weasyprint'. Run: pip install -r utils/requirements.txt", file=sys.stderr)
    raise

# Compatibility shim: If running with older pydyf (PDF.__init__ takes only self),
# monkeypatch __init__ to accept extra args used by newer WeasyPrint versions.
try:
    import inspect  # type: ignore
    import pydyf  # type: ignore
    _sig = inspect.signature(pydyf.PDF.__init__)
    if len(_sig.parameters) == 1:  # only 'self'
        _orig_init = pydyf.PDF.__init__

        def _compat_init(self, *args, **kwargs):  # ignore extra args
            return _orig_init(self)

        pydyf.PDF.__init__ = _compat_init  # type: ignore
except Exception:
    # Best-effort patch; if anything goes wrong, let WeasyPrint raise normally
    pass


DEFAULT_CSS = """
@page { size: A4; margin: 24mm 18mm; }
html { font-size: 11pt; }
body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Noto Sans', 'Liberation Sans', sans-serif; line-height: 1.45; color: #111; }
h1, h2, h3, h4, h5, h6 { font-weight: 700; margin: 1.2em 0 0.4em; }
h1 { font-size: 1.8em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.25em; }
p { margin: 0.6em 0; }
ul, ol { margin: 0.6em 0 0.6em 1.4em; }
code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; }
pre { background: #f6f8fa; padding: 10px; border-radius: 6px; overflow-x: auto; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ddd; padding: 6px 8px; }
th { background: #f3f4f6; text-align: left; }
blockquote { border-left: 3px solid #e5e7eb; margin: 0.6em 0; padding: 0.2em 0.8em; color: #374151; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.2em 0; }
"""


def md_to_pdf(input_path: pathlib.Path, output_path: Optional[pathlib.Path] = None, css_path: Optional[pathlib.Path] = None) -> pathlib.Path:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("Input must be a .md or .markdown file")

    md_text = input_path.read_text(encoding="utf-8")

    # Convert Markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=[
            "extra",            # tables, fenced_code, etc.
            "codehilite",       # code highlighting (requires Pygments for full effect)
            "toc",              # table of contents ids
            "sane_lists",
            "smarty",
        ],
        output_format="html5",
    )

    # Read external CSS if provided, else use default
    if css_path is not None:
        if not css_path.exists():
            raise FileNotFoundError(f"CSS file not found: {css_path}")
        css_text = css_path.read_text(encoding="utf-8")
    else:
        css_text = DEFAULT_CSS

    # Wrap in a minimal HTML document (CSS inlined in <style>)
    html_doc = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{input_path.stem}</title>
  <style>
{css_text}
  </style>
</head>
<body>
{html_body}
</body>
</html>
"""

    # Output path
    if output_path is None:
        output_path = input_path.with_suffix(".pdf")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Render to PDF (styles already inlined)
    HTML(string=html_doc, base_url=str(input_path.parent)).write_pdf(str(output_path))
    return output_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument("input", type=str, help="Path to .md/.markdown file")
    parser.add_argument("--out", type=str, default=None, help="Output .pdf path (optional)")
    parser.add_argument("--css", type=str, default=None, help="Optional CSS path to style the PDF")
    args = parser.parse_args(argv)

    in_path = pathlib.Path(args.input).expanduser().resolve()
    out_path = pathlib.Path(args.out).expanduser().resolve() if args.out else None
    css = pathlib.Path(args.css).expanduser().resolve() if args.css else None

    try:
        out = md_to_pdf(in_path, out_path, css)
        print(str(out))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
