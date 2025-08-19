from utils.docx_to_md import docx_to_markdown
from utils.md_to_pdf import md_to_pdf
import argparse
import pathlib
import sys


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Docs utilities")
    subparsers = parser.add_subparsers(dest="cmd")

    # Subcommand: docx-to-md
    p_docx = subparsers.add_parser("docx-to-md", help="Convert DOCX to Markdown")
    p_docx.add_argument("input", type=str, help="Path to .docx file")
    p_docx.add_argument("--out", type=str, default=None, help="Output .md path (optional)")

    # Subcommand: md-to-pdf
    p_pdf = subparsers.add_parser("md-to-pdf", help="Convert Markdown to PDF")
    p_pdf.add_argument("input", type=str, help="Path to .md/.markdown file")
    p_pdf.add_argument("--out", type=str, default=None, help="Output .pdf path (optional)")
    p_pdf.add_argument("--css", type=str, default=None, help="Optional CSS path to style the PDF")

    args, extras = parser.parse_known_args(argv)

    # Backward compatibility: if no subcommand, assume docx-to-md signature
    if args.cmd is None:
        compat = argparse.ArgumentParser(add_help=False)
        compat.add_argument("input", type=str)
        compat.add_argument("--out", type=str, default=None)
        cargs = compat.parse_args(argv)
        in_path = pathlib.Path(cargs.input).expanduser().resolve()
        out_path = pathlib.Path(cargs.out).expanduser().resolve() if cargs.out else None
        try:
            result_path = docx_to_markdown(in_path, out_path)
            print(str(result_path))
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if args.cmd == "docx-to-md":
        in_path = pathlib.Path(args.input).expanduser().resolve()
        out_path = pathlib.Path(args.out).expanduser().resolve() if args.out else None
        try:
            result_path = docx_to_markdown(in_path, out_path)
            print(str(result_path))
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if args.cmd == "md-to-pdf":
        in_path = pathlib.Path(args.input).expanduser().resolve()
        out_path = pathlib.Path(args.out).expanduser().resolve() if args.out else None
        css_path = pathlib.Path(args.css).expanduser().resolve() if args.css else None
        try:
            result_path = md_to_pdf(in_path, out_path, css_path)
            print(str(result_path))
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
