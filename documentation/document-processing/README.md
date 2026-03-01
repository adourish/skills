# Document Processing Skills

Comprehensive guides for creating, editing, and analyzing Microsoft Office and PDF documents.

---

## Overview

This folder contains skills for working with common document formats:
- **DOCX** - Microsoft Word documents
- **PPTX** - Microsoft PowerPoint presentations
- **PDF** - Portable Document Format files
- **XLSX** - Microsoft Excel spreadsheets

These skills are adapted from [Anthropic's Skills Repository](https://github.com/anthropics/skills) and customized for our workflow.

---

## Skills Reference

| Skill | File | Purpose |
|-------|------|---------|
| **Word Documents** | `skill_docx.md` | Create, edit, and analyze .docx files |
| **PowerPoint** | `skill_pptx.md` | Create, edit, and analyze .pptx presentations |
| **PDF Processing** | `skill_pdf.md` | Extract, manipulate, and create PDF files |
| **Excel Spreadsheets** | `skill_xlsx.md` | Create, edit, and analyze .xlsx files with formulas |

---

## Quick Reference

### DOCX (Word)
```bash
# Read content
pandoc document.docx -t markdown

# Create new document
# Use docx-js library (see skill_docx.md)

# Edit existing document
# Unpack → edit XML → repack (see skill_docx.md)
```

### PPTX (PowerPoint)
```bash
# Read content
python -m markitdown presentation.pptx

# Create from scratch
# Use pptxgenjs library (see skill_pptx.md)

# Edit existing
# Unpack → edit slides → repack (see skill_pptx.md)
```

### PDF
```bash
# Extract text
python -c "from pypdf import PdfReader; print(PdfReader('file.pdf').pages[0].extract_text())"

# Merge PDFs
# See skill_pdf.md for pypdf examples

# Extract images
# See skill_pdf.md for pdfplumber examples
```

### XLSX (Excel)
```bash
# Read data
python -c "import pandas as pd; print(pd.read_excel('file.xlsx'))"

# Create with formulas
# Use openpyxl library (see skill_xlsx.md)

# Recalculate formulas
# Use LibreOffice (see skill_xlsx.md)
```

---

## Integration with Skills Folder

These document processing skills are located in:
```
G:\My Drive\06_Skills\documentation\document-processing\
```

They complement existing skills:
- **Diagram Tools** (`documentation/diagram-tools/`) - Mermaid to Visio conversion
- **File Organization** (`automation/skill_file_organization.md`) - PARA filing system
- **Media Filing** (`G:\My Drive\04_Resources\Media\HOW_TO_FILE_MEDIA.md`) - Media organization

---

## Common Use Cases

### 1. Generate Reports
- Create Word documents with tables, charts, and formatting
- Export data to Excel with formulas and styling
- Convert to PDF for distribution

### 2. Presentation Creation
- Build PowerPoint decks from templates
- Apply consistent branding and design
- Export slides as images

### 3. Data Processing
- Extract text from PDFs for analysis
- Parse Excel files for data transformation
- Merge and split documents

### 4. Document Automation
- Batch process multiple files
- Fill forms programmatically
- Generate documents from templates

---

## Dependencies

### Python Libraries

**DOCX:**
- `docx-js` (Node.js) - Creating new documents
- `pandoc` - Reading and converting
- `python-docx` - Python alternative

**PPTX:**
- `pptxgenjs` (Node.js) - Creating presentations
- `markitdown` - Reading content
- `python-pptx` - Python alternative

**PDF:**
- `pypdf` - Basic PDF operations
- `pdfplumber` - Text and table extraction
- `reportlab` - PDF creation
- `poppler-utils` - Command-line tools

**XLSX:**
- `openpyxl` - Excel file manipulation
- `pandas` - Data analysis
- `xlsxwriter` - Excel creation
- LibreOffice - Formula recalculation

### Installation

```bash
# Python packages
pip install pypdf pdfplumber reportlab openpyxl pandas xlsxwriter python-docx python-pptx

# Node.js packages (if needed)
npm install docx pptxgenjs

# System tools
# Windows: Install LibreOffice from https://www.libreoffice.org/
# Linux: sudo apt-get install libreoffice poppler-utils
# macOS: brew install libreoffice poppler
```

---

## Best Practices

### 1. Always Validate Output
- Check formulas in Excel files
- Verify formatting in Word/PowerPoint
- Test PDF extraction accuracy

### 2. Use Templates When Possible
- Maintain consistent branding
- Reduce creation time
- Ensure professional appearance

### 3. Handle Errors Gracefully
- Check file existence before processing
- Validate input data
- Provide clear error messages

### 4. Optimize for Performance
- Process large files in chunks
- Cache frequently accessed data
- Use appropriate libraries for the task

---

## License

These skills are adapted from Anthropic's Skills Repository and are subject to their license terms.

Original source: https://github.com/anthropics/skills

---

## Changelog

- **2026-03-01:** Added DOCX, PPTX, PDF, and XLSX skills from Anthropic repository
- **2026-03-01:** Created document-processing folder in Skills/documentation

---

**Last Updated:** March 1, 2026  
**Location:** `G:\My Drive\06_Skills\documentation\document-processing\`
