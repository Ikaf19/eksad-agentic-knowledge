---
name: docx-extractor
description: "Use when the user asks to extract, read, parse, convert, OR GENERATE a .docx file. Triggers on: 'baca file docx', 'extract docx', 'konversi docx ke markdown', 'buat style guide dari docx', 'generate docx', 'buat dokumen word', 'generate BRD docx', 'generate FSD docx', 'buat dokumen dari template EKSAD', 'generate document with style from', 'pakai style dari docx ini untuk generate'. Extracts text/tables/headers/footers/styling from existing .docx AND generates new styled .docx documents based on a baseline style file and EKSAD document templates."
version: 1.1.0
author: EKSAD Platform Team (Hermes-native)
license: MIT
metadata:
  hermes:
    tags: [docx, word, extract, convert, generate, markdown, styling, document, parser, brd, fsd, tsd]
---

# DOCX Extractor & Generator Skill

Extracts text, structure, tables, and styling metadata from any `.docx` file,
AND generates new styled `.docx` documents using a baseline style file + EKSAD templates.
Works on any Hermes surface (CLI, Telegram, WebUI) on Windows or Linux.

## When to Use

**Extract / Read:**
- User provides a `.docx` path and wants its content read
- User wants to extract styling/formatting rules from an approved document
- User wants to convert a Word document to Markdown
- User wants to build a style guide from an existing approved `.docx`

**Generate / Write:**
- User asks to generate a `.docx` from a baseline style file (`pakai style dari X.docx`)
- User asks to generate a BRD/FSD/TSD/document dummy following EKSAD template
- User provides a style reference DOCX + content to produce a new Word document

## When NOT to Use

- File is `.doc` (old binary format) → inform user to re-save as `.docx`
- File is password-protected → inform user to remove protection first
- User wants to edit an existing `.docx` in-place with tracked changes → not supported

---

## Detection: Which Method to Use

Before running, check what is available:

```python
# Check python-docx availability
import importlib.util
has_docx = importlib.util.find_spec("docx") is not None
```

| Condition | Method to use |
|---|---|
| `python-docx` available | **Method A** — Full extraction (text + styling) |
| Only Python stdlib | **Method B** — ZIP/XML extraction (text + raw style tags) |
| Only PowerShell available | **Method C** — PowerShell ZIP extraction |

---

## Method A — python-docx (Recommended)

Use when `python-docx` is installed. Gives cleanest output.

```python
#!/usr/bin/env python3
"""EKSAD DOCX Extractor — Method A (python-docx)"""
import sys
from docx import Document

def extract_docx(path: str) -> dict:
    doc = Document(path)
    result = {
        "paragraphs": [],
        "tables": [],
        "styles_used": set(),
        "default_style": None,
        "headers": [],
        "footers": [],
        "sections": [],
    }

    # Extract paragraphs with style info
    for para in doc.paragraphs:
        if not para.text.strip():
            continue
        entry = {
            "text": para.text,
            "style": para.style.name,
            "alignment": str(para.alignment),
        }
        result["styles_used"].add(para.style.name)
        result["paragraphs"].append(entry)

    # Extract tables
    for i, table in enumerate(doc.tables):
        rows = []
        for row in table.rows:
            rows.append([cell.text.strip() for cell in row.cells])
        result["tables"].append({"table_index": i, "rows": rows})

    # Extract headers, footers, and section page layout per section
    for i, section in enumerate(doc.sections):
        has_different_first = section.different_first_page_header_footer

        def _extract_hf_paras(hf_obj):
            """Extract non-empty paragraphs from a header/footer object."""
            if hf_obj.is_linked_to_previous:
                return []
            return [
                {
                    "text": p.text,
                    "style": p.style.name,
                    "alignment": str(p.alignment),
                }
                for p in hf_obj.paragraphs if p.text.strip()
            ]

        header_entry = {
            "section": i,
            "default": _extract_hf_paras(section.header),
            "first_page": _extract_hf_paras(section.first_page_header) if has_different_first else None,
            "even_page": _extract_hf_paras(section.even_page_header),
        }
        result["headers"].append(header_entry)

        footer_entry = {
            "section": i,
            "default": _extract_hf_paras(section.footer),
            "first_page": _extract_hf_paras(section.first_page_footer) if has_different_first else None,
            "even_page": _extract_hf_paras(section.even_page_footer),
        }
        result["footers"].append(footer_entry)

        # Page layout (margins, size)
        try:
            from docx.shared import Cm
            result["sections"].append({
                "section": i,
                "page_width_cm": round(section.page_width.cm, 2) if section.page_width else None,
                "page_height_cm": round(section.page_height.cm, 2) if section.page_height else None,
                "left_margin_cm": round(section.left_margin.cm, 2) if section.left_margin else None,
                "right_margin_cm": round(section.right_margin.cm, 2) if section.right_margin else None,
                "top_margin_cm": round(section.top_margin.cm, 2) if section.top_margin else None,
                "bottom_margin_cm": round(section.bottom_margin.cm, 2) if section.bottom_margin else None,
                "header_distance_cm": round(section.header_distance.cm, 2) if section.header_distance else None,
                "footer_distance_cm": round(section.footer_distance.cm, 2) if section.footer_distance else None,
            })
        except Exception:
            result["sections"].append({"section": i, "page_layout": "unavailable"})

    # Extract default document style
    try:
        normal = doc.styles["Normal"]
        font = normal.font
        result["default_style"] = {
            "font_name": font.name,
            "font_size_pt": font.size.pt if font.size else None,
            "bold": font.bold,
            "italic": font.italic,
        }
    except Exception:
        pass

    result["styles_used"] = sorted(result["styles_used"])
    return result


def to_markdown(extracted: dict) -> str:
    lines = []
    style_map = {
        "Heading 1": "# ",
        "Heading 2": "## ",
        "Heading 3": "### ",
        "Heading 4": "#### ",
        "Heading 5": "##### ",
        "Title": "# ",
        "Subtitle": "## ",
    }

    for para in extracted["paragraphs"]:
        prefix = style_map.get(para["style"], "")
        if prefix:
            lines.append(f"{prefix}{para['text']}")
        else:
            lines.append(para["text"])
        lines.append("")

    for table in extracted["tables"]:
        rows = table["rows"]
        if not rows:
            continue
        lines.append("| " + " | ".join(rows[0]) + " |")
        lines.append("| " + " | ".join(["---"] * len(rows[0])) + " |")
        for row in rows[1:]:
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <path_to_file.docx> [--markdown]")
        sys.exit(1)

    path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else ""
    extracted = extract_docx(path)

    if mode == "--markdown":
        print(to_markdown(extracted))
    else:
        import json
        print(json.dumps(extracted, indent=2, default=str))
```

---

## Method B — Python stdlib only (ZIP/XML)

Use when `python-docx` is NOT installed. Extracts raw text from the ZIP structure.

```python
#!/usr/bin/env python3
"""EKSAD DOCX Extractor — Method B (stdlib only, no pip required)"""
import sys
import zipfile
import xml.etree.ElementTree as ET

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def _extract_paragraphs_from_xml(root) -> list:
    """Extract non-empty paragraph texts from a parsed XML root."""
    paragraphs = []
    for para in root.iter(f"{{{WORD_NS}}}p"):
        texts = []
        for t in para.iter(f"{{{WORD_NS}}}t"):
            if t.text:
                texts.append(t.text)
        line = "".join(texts).strip()
        if line:
            paragraphs.append(line)
    return paragraphs


def extract_text_from_docx(path: str) -> str:
    with zipfile.ZipFile(path, "r") as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
            root = tree.getroot()

    return "\n\n".join(_extract_paragraphs_from_xml(root))


def extract_headers_footers_from_docx(path: str) -> dict:
    """Extract header and footer text from all header*.xml / footer*.xml entries."""
    result = {"headers": {}, "footers": {}}
    with zipfile.ZipFile(path, "r") as z:
        names = z.namelist()
        for name in names:
            if name.startswith("word/header") and name.endswith(".xml"):
                with z.open(name) as f:
                    root = ET.parse(f).getroot()
                texts = _extract_paragraphs_from_xml(root)
                result["headers"][name] = texts
            elif name.startswith("word/footer") and name.endswith(".xml"):
                with z.open(name) as f:
                    root = ET.parse(f).getroot()
                texts = _extract_paragraphs_from_xml(root)
                result["footers"][name] = texts
    return result


def extract_styles_from_docx(path: str) -> list:
    styles = []
    with zipfile.ZipFile(path, "r") as z:
        if "word/styles.xml" not in z.namelist():
            return styles
        with z.open("word/styles.xml") as f:
            tree = ET.parse(f)
            root = tree.getroot()

    for style in root.iter(f"{{{WORD_NS}}}style"):
        style_id = style.get(f"{{{WORD_NS}}}styleId", "")
        name_el = style.find(f"{{{WORD_NS}}}name")
        name = name_el.get(f"{{{WORD_NS}}}val", "") if name_el is not None else ""

        sz = style.find(f".//{{{WORD_NS}}}sz")
        sz_val = sz.get(f"{{{WORD_NS}}}val") if sz is not None else None
        size_pt = int(sz_val) / 2 if sz_val else None

        fonts = style.find(f".//{{{WORD_NS}}}rFonts")
        font_name = None
        if fonts is not None:
            font_name = (fonts.get(f"{{{WORD_NS}}}ascii") or
                         fonts.get(f"{{{WORD_NS}}}hAnsi"))

        bold = style.find(f".//{{{WORD_NS}}}b") is not None

        if name:
            styles.append({
                "id": style_id,
                "name": name,
                "font": font_name,
                "size_pt": size_pt,
                "bold": bold,
            })

    return styles


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx_stdlib.py <path.docx> [--styles|--headers-footers|--all]")
        sys.exit(1)

    path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else ""

    if mode == "--styles":
        import json
        styles = extract_styles_from_docx(path)
        print(json.dumps(styles, indent=2))
    elif mode == "--headers-footers":
        import json
        hf = extract_headers_footers_from_docx(path)
        print(json.dumps(hf, indent=2))
    elif mode == "--all":
        import json
        output = {
            "body": extract_text_from_docx(path),
            "styles": extract_styles_from_docx(path),
            "headers_footers": extract_headers_footers_from_docx(path),
        }
        print(json.dumps(output, indent=2))
    else:
        print(extract_text_from_docx(path))
```

---

## Method C — PowerShell (Windows, no Python)

Use when only PowerShell is available on the machine.

```powershell
# EKSAD DOCX Extractor — Method C (PowerShell)
param(
    [Parameter(Mandatory=$true)][string]$DocxPath,
    [switch]$StylesOnly,
    [switch]$HeadersFooters,
    [switch]$All
)

$tempDir = Join-Path $env:TEMP ("docx_extract_" + [System.IO.Path]::GetRandomFileName())
New-Item -ItemType Directory -Path $tempDir | Out-Null
$ns = @{ w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main" }

function Extract-XmlParagraphs([xml]$xmlDoc) {
    $paragraphs = Select-Xml -Xml $xmlDoc -XPath "//w:p" -Namespace $ns
    foreach ($para in $paragraphs) {
        $texts = Select-Xml -Xml $para.Node -XPath ".//w:t" -Namespace $ns
        $line = ($texts | ForEach-Object { $_.Node.InnerText }) -join ""
        if ($line.Trim()) { Write-Output $line }
    }
}

try {
    Expand-Archive -Path $DocxPath -DestinationPath $tempDir -Force

    if ($StylesOnly) {
        $stylesPath = Join-Path $tempDir "word\styles.xml"
        if (Test-Path $stylesPath) {
            [xml]$styles = Get-Content $stylesPath -Encoding UTF8
            $styles.OuterXml
        } else { Write-Warning "styles.xml not found" }

    } elseif ($HeadersFooters -or $All) {
        # Extract headers
        Get-ChildItem (Join-Path $tempDir "word") -Filter "header*.xml" | ForEach-Object {
            Write-Output "=== HEADER: $($_.Name) ==="
            [xml]$hdr = Get-Content $_.FullName -Encoding UTF8
            Extract-XmlParagraphs $hdr
        }
        # Extract footers
        Get-ChildItem (Join-Path $tempDir "word") -Filter "footer*.xml" | ForEach-Object {
            Write-Output "=== FOOTER: $($_.Name) ==="
            [xml]$ftr = Get-Content $_.FullName -Encoding UTF8
            Extract-XmlParagraphs $ftr
        }
        # If --all, also extract body
        if ($All) {
            Write-Output "=== BODY ==="
            $docPath = Join-Path $tempDir "word\document.xml"
            [xml]$doc = Get-Content $docPath -Encoding UTF8
            Extract-XmlParagraphs $doc
        }
    } else {
        # Default: body only
        $docPath = Join-Path $tempDir "word\document.xml"
        [xml]$doc = Get-Content $docPath -Encoding UTF8
        Extract-XmlParagraphs $doc
    }
} finally {
    Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
}
```

---

## Workflow: Extract & Build Style Guide

When the user wants a **style guide** from an approved DOCX:

### Step 1 — Confirm file path

Ask user: "Share path lengkap file .docx-nya"

### Step 2 — Detect method & run extraction

Run Method A or B depending on environment. Extract:
- Paragraphs + their styles
- Tables
- Headers & footers per section
- Page layout (margins, page size, header/footer distance)
- Font/size/bold from `styles.xml`

### Step 3 — Build Markdown style guide

Output format:

```markdown
# EKSAD Document Style Guide
Source: <filename.docx> (approved by <team/atasan>)
Extracted: <date>

## Page Layout

| Property | Value |
|---|---|
| Page Size | A4 (21.0 x 29.7 cm) |
| Left Margin | ... cm |
| Right Margin | ... cm |
| Top Margin | ... cm |
| Bottom Margin | ... cm |
| Header Distance | ... cm |
| Footer Distance | ... cm |

## Header

> <teks header dari dokumen — misalnya nama perusahaan, judul dokumen>
> Alignment: center / left / right

## Footer

> <teks footer dari dokumen — misalnya nomor halaman, tanggal, confidentiality>
> Alignment: center / left / right

## Typography

| Style Name | Font | Size (pt) | Bold | Usage |
|---|---|---|---|---|
| Heading 1 | ... | ... | Yes | Chapter titles |
| Normal | ... | ... | No | Body text |

## Heading Hierarchy

# H1 — <example from doc>
## H2 — <example from doc>
### H3 — <example from doc>

## Tables
<example table structure from doc>

## Notes
- Language: Bahasa Indonesia / English
- Multi-section: yes/no
```

### Step 4 — Offer to save

Ask: "Simpan sebagai project artifact `{PROJECT_CODE}_DOCX_STYLE_GUIDE_v{VERSION}.md` di lokasi dokumen proyek yang sudah disetujui?"
Save only after user confirms. Never create or overwrite a canonical file under `EKSAD/gpt/_template/` from an extracted project document.

---

## Output Contract

| Output | Format | When |
|---|---|---|
| Full text extraction | Plain text / Markdown | Default |
| Style metadata | JSON or Markdown table | When `--styles` or user asks |
| Style guide doc | Project-owned `.md` artifact | After user confirmation; never auto-write canonical `_template/` source |
| Error message | Plain text | File not found / wrong format / protected |

---

## Forbidden

- Do not push `.docx` binary files to Git
- Do not write extracted output to `_template/` without explicit user confirmation
- Do not claim styling info is accurate if `styles.xml` is missing or corrupt
- Do not run on password-protected files — inform user to unlock first
- Do not leave temp directories behind after extraction (always clean up)

---

## Error Handling

| Error | Response |
|---|---|
| File not found | "File tidak ditemukan di path tersebut. Cek kembali path-nya." |
| Not a valid ZIP / corrupt | "File bukan .docx yang valid atau rusak. Coba buka di Word dan save ulang." |
| Password protected | "File dilindungi password. Hapus proteksi dulu di Word > Review > Restrict Editing." |
| `python-docx` not found | Fallback ke Method B (stdlib) atau Method C (PowerShell) |
| Old `.doc` format | "File adalah format .doc lama. Buka di Word dan Save As ke .docx" |
| Permission denied saat save | "File output mungkin sedang terbuka di Word. Tutup dulu lalu coba lagi." |

---

## Generate Workflow — New DOCX from Baseline Style

Use this workflow when the user wants to **create** a new `.docx` using styling from an approved baseline file.

### When triggered

- "generate BRD docx dengan style dari `BRD_BASELINE_STYLE.docx`"
- "buat FSD dummy pakai style dokumen yang sudah approved"
- "generate document word dari template EKSAD"

### Step 1 — Confirm inputs

Ask user:
- **Style source**: path ke `.docx` baseline (wajib)
- **Document type**: BRD / FSD / TSD / other (determines EKSAD template to follow)
- **Output path**: default ke direktori yang sama dengan source + suffix `_generated.docx`
- **Project name / placeholder values** jika diperlukan

### Step 2 — Extract available styles from baseline

```python
#!/usr/bin/env python3
"""EKSAD DOCX Generator — Step 2: Extract available styles from baseline"""
from docx import Document
from docx.enum.style import WD_STYLE_TYPE

def inspect_baseline(path: str) -> dict:
    doc = Document(path)
    return {
        "para_styles": [s.name for s in doc.styles if s.type == WD_STYLE_TYPE.PARAGRAPH],
        "table_styles": [s.name for s in doc.styles if s.type == WD_STYLE_TYPE.TABLE],
        "tables_used": list({t.style.name for t in doc.tables}),
        "page_layout": {
            "page_width_cm":   round(doc.sections[0].page_width.cm, 2),
            "page_height_cm":  round(doc.sections[0].page_height.cm, 2),
            "left_margin_cm":  round(doc.sections[0].left_margin.cm, 2),
            "right_margin_cm": round(doc.sections[0].right_margin.cm, 2),
            "top_margin_cm":   round(doc.sections[0].top_margin.cm, 2),
            "bottom_margin_cm":round(doc.sections[0].bottom_margin.cm, 2),
        }
    }
```

> **Important:** Always inspect the baseline before generating — do not assume `Table Grid`,
> `List Bullet`, or other common styles exist. Use only styles confirmed present.

### Step 3 — Generate: Core template

```python
#!/usr/bin/env python3
"""EKSAD DOCX Generator — Step 3: Generate new DOCX inheriting baseline styles"""
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def create_from_baseline(src_path: str, out_path: str):
    """
    Load the baseline .docx as the style source.
    Clear all body content (keep sectPr = page layout + header/footer).
    Write new content using only styles confirmed in the baseline.
    """
    doc = Document(src_path)
    body = doc.element.body
    # Remove all existing content, preserve section properties (page layout, header, footer)
    for child in list(body):
        if child.tag != qn('w:sectPr'):
            body.remove(child)
    return doc


def add_border_to_table(table):
    """Add single-line borders to a table via XML (works with any table style)."""
    tbl = table._tbl
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    borders = OxmlElement('w:tblBorders')
    for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:color'), '000000')
        borders.append(el)
    tblPr.append(borders)


def make_table(doc, col_headers: list, data_rows: list,
               table_style: str = 'Normal Table', bold_header: bool = True):
    """Create a bordered table. Use table_style from inspect_baseline() output."""
    t = doc.add_table(rows=1 + len(data_rows), cols=len(col_headers))
    t.style = table_style
    add_border_to_table(t)
    for i, h in enumerate(col_headers):
        cell = t.rows[0].cells[i]
        cell.text = str(h)
        if bold_header:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.bold = True
    for ri, row in enumerate(data_rows, 1):
        for ci, v in enumerate(row):
            t.rows[ri].cells[ci].text = str(v)
    return t


def make_bullet(doc, text: str, list_style: str = 'List Paragraph', indent_pt: int = 18):
    """Add a bullet-style paragraph. Use list_style from inspect_baseline() output."""
    pp = doc.add_paragraph(text, style=list_style)
    pp.paragraph_format.left_indent = Pt(indent_pt)
    return pp


def cover_para(doc, text: str, bold: bool = False,
               size_pt: float = None, center: bool = False):
    """Add a cover page paragraph with optional bold/size/centering."""
    para = doc.add_paragraph()
    if center:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(text)
    if bold:
        run.bold = True
    if size_pt:
        run.font.size = Pt(size_pt)
    return para
```

### Step 4 — Document type routing

After inspecting baseline and creating the doc object, route to the correct content builder:

| Document Type | EKSAD Template Reference | Sections to Include |
|---|---|---|
| BRD | `EKSAD/gpt/_template/EKSAD_GENERIC_BRD_TEMPLATE.md` | Doc Control, Rev History, Approval, TOC, Sections 1–16, Appendix A–B |
| FSD | `EKSAD/gpt/_template/EKSAD_GENERIC_FSD_TEMPLATE.md` | Doc Control, Rev History, Approval, TOC, Feature Specs, NFRs, Gap Analysis |
| TSD | `EKSAD/gpt/_template/EKSAD_GENERIC_TSD_TEMPLATE.md` | Doc Control, Rev History, Approval, TOC, Architecture, API, Data Model |
| UR | `EKSAD/gpt/_template/EKSAD_GENERIC_UR_TEMPLATE.md` | Doc Control, Rev History, Stakeholders, UR list |
| Other | Derive from closest template | Adapt as needed |

> Always read the target template `.md` file first to get the exact section names and structure
> before generating content. Do not invent section names not in the template.

### Step 5 — Confirm output path & save

```python
doc.save(out_path)
print(f"Generated: {out_path}")
```

After saving:
- Report: filename, total tables, total sections
- Warn if any placeholder values (`[TBD]`, `{PROJECT_NAME}`) remain in the output
- Offer to open the file: `start <path>` (Windows) or `open <path>` (macOS)

---

## Generate Output Contract

| Output | Format | When |
|---|---|---|
| Inspected styles | JSON / Markdown table | Before generating, so AI knows which styles are safe to use |
| Generated `.docx` | Binary file saved to output path | After user confirms output path |
| Summary report | Plain text | After successful save: file path, table count, placeholders remaining |
| Error | Plain text | Permission denied / style missing / path invalid |

---

## Generate Forbidden

- Do not assume `Table Grid`, `List Bullet`, or other styles exist — always inspect baseline first
- Do not overwrite an existing file without user confirmation
- Do not load the baseline as read-only and write styles from scratch — inherit from baseline by loading it then clearing content
- Do not leave placeholder text like `{PROJECT_NAME}` in the final output unless user explicitly allows it
- Do not push generated `.docx` binary files to Git

