from utils.docx_to_md import docx_to_markdown
import argparse
import pathlib
import sys


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Convert DOCX to Markdown")
    parser.add_argument("input", type=str, help="Path to .docx file")
    parser.add_argument("--out", type=str, default=None, help="Output .md path (optional)")
    args = parser.parse_args(argv)

    in_path = pathlib.Path(args.input).expanduser().resolve()
    out_path = pathlib.Path(args.out).expanduser().resolve() if args.out else None

    try:
        result_path = docx_to_markdown(in_path, out_path)
        print(str(result_path))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
