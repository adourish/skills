# Mermaid to Visio Converter - Quick Start

Convert Mermaid diagrams from markdown files to Visio-compatible formats (SVG, PNG, PDF).

## Installation

```bash
# 1. Install Node.js from https://nodejs.org/

# 2. Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# 3. Verify installation
python mermaid_to_visio.py --check
```

## Basic Usage

```bash
# Convert single file to SVG
python mermaid_to_visio.py your_file.md

# Convert all markdown files in a directory
python mermaid_to_visio.py docs/ --recursive

# Convert to multiple formats
python mermaid_to_visio.py your_file.md --formats svg png pdf
```

## Import to Visio

1. Open Visio
2. **Insert** → **Pictures** → **From File**
3. Select the `.svg` file from `diagrams/` folder
4. Done! Editable vector graphics imported

## Output

Files are saved to `diagrams/` folder with naming:
- `{filename}_diagram_{number}_{type}.svg`
- Example: `architecture_diagram_1_graph.svg`

## Help

```bash
python mermaid_to_visio.py --help
```

See `README.md` for complete documentation.
