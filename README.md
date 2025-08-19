# $MOD Network Documentation
This repo is intended to serve as a cohesive design and architecture document for the $MOD Network. This documentation should serve as the central source of truth for the entire chain, offchain module architecture and SDK, and official frontend services.

## How to Use This Repo
1. Clone this repository to your computer
2. Download [Obsidian](https://obsidian.md/) and open the repository folder as a Vault
3. Begin reading the documentation with the [[Overview]] (if this link doesn't work, you're not using Obsidian)

*Note: If you choose to only browse through the GitHub website or another editor, you will lose out on some of the rendering features that Obsidian provides. However, the documentation is structured into folders that resemble the outline of the document to assist with finding the information in a coherent manner.*

---

## CLI Utilities (Docs Tooling)

Utilities live in `main.py` and `utils/`:
- `docx-to-md`: Convert `.docx` to Markdown
- `md-to-pdf`: Convert Markdown to PDF (WeasyPrint)

### Install dependencies
- Using uv (recommended):
  ```bash
  uv add -r utils/requirements.txt
  ```
- Using pip:
  ```bash
  pip install -r utils/requirements.txt
  ```

WeasyPrint requires some system libraries:
- Debian/Ubuntu:
  ```bash
  sudo apt-get update && sudo apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libffi-dev libgdk-pixbuf-2.0-0
  ```
- Fedora:
  ```bash
  sudo dnf install -y pango cairo gdk-pixbuf2 libffi
  ```
- Arch:
  ```bash
  sudo pacman -S --needed pango cairo gdk-pixbuf2 libffi
  ```

### Usage
- DOCX → Markdown:
  ```bash
  python main.py docx-to-md /path/to/input.docx --out /path/to/output.md
  ```
  Backward compatible: `python main.py /path/to/input.docx --out /path/to/output.md`

- Markdown → PDF:
  ```bash
  python main.py md-to-pdf /path/to/input.md --out /path/to/output.pdf
  ```
  Optional CSS styling:
  ```bash
  python main.py md-to-pdf /path/to/input.md --css utils/print.css
  ```

Notes:
- If `--out` is omitted, output files are created next to the input with the appropriate extension.
- Markdown conversion enables common extensions: extra, codehilite, toc, sane_lists, smarty.