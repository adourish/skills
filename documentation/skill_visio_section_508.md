# Visio + Section 508 Master Guide: Creating Accessible Visio Diagrams

**Last Updated:** 2026-01-29  
**Purpose:** Create Section 508-friendly Visio diagrams that are readable, export cleanly to accessible PDFs, and do not rely on color-only meaning.

---

## 1. References

Use these repo guides as the authoritative sources for colors and visual style:

- `c:\projects\POCs\src\dmedev5\docs\Section_508_Color_Palette_Style_Guide.md`
- `c:\projects\POCs\src\dmedev5\docs\Modern_Diagram_Design_Guide.md`

---

## 2. Visio accessibility rules (Section 508 oriented)

### 2.1 No color-only meaning

- Use **text labels** and/or **icons** to convey meaning.
- Any meaning conveyed by color must also be conveyed by text.

### 2.2 Contrast and legibility

- Use the approved palette; ensure readable text:
  - **Black text** on light fills
  - **White text** on dark fills
- Aim for **minimum 4.5:1** contrast for normal text.

### 2.3 Typography

- Use a clean sans-serif (Segoe UI / Calibri / Arial).
- Minimum recommended sizes:
  - Body: **11–12pt**
  - Headers: **14–16pt**

### 2.4 Reading order and grouping

- Maintain a logical reading order (title first, then primary content).
- Be careful with grouping; groups can break reading order if used heavily.

### 2.5 Alt text

- Add alt text to:
  - The main diagram container/title shape (summary)
  - Legends
  - Non-text icons
- Alt text should describe **meaning**, not styling.

---

## 3. Recommended Visio styling (modern + consistent)

- Prefer **flat, borderless boxes** with rounded corners.
- Use consistent spacing, alignment, and connector styling.
- Keep color count low (3–4 primary colors per diagram).

---

## 4. Build steps in Visio (repeatable)

### 4.1 Start from an existing PRM diagram (optional)

If you want consistent visual branding, open an existing diagram in this repo and reuse styles/themes:

- `c:\projects\POCs\src\dmedev5\docs\PRM_Solution_Architecture.vsdx`

### 4.2 Create the diagram

1. Decide the diagram pattern (matrix, flow, architecture layers, etc.).
2. Apply the approved palette + modern styling.
3. Ensure meaning is conveyed by text (not just color).
4. Add a legend if any markers/icons are used.
5. Add alt text for the title container, legend, and any icons.

### 4.3 Validation pass

- Confirm text sizes are readable at 100% zoom.
- Confirm contrast for any colored fills.
- Confirm no phase names are truncated.

---

## 5. Export steps (accessible deliverable)

1. Export as **PDF** (prefer selectable text, not an image-only PDF).
2. Run **Accessibility Checker** in your PDF tool (Acrobat if available).
3. Verify:
   - Title is present
   - Text is selectable
   - Reading order is logical
   - Legend is included

---

## 6. Where to store this Master Guide

Per standard practice, this guide should be placed at:

- `G:\My Drive\06_Master_Guides\Visio_Section_508_Master_Guide.md`
