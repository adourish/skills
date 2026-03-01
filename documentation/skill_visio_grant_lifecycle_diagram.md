# Visio + Section 508 Master Guide: Grant Lifecycle Domain Object Capture Crosswalk

**Last Updated:** 2026-01-29  
**Purpose:** Create a Section 508-friendly Visio diagram that shows *where post-award domain objects are captured/updated* across the grant lifecycle.

---

## 1. Inputs

### 1.1 Grant lifecycle phases (post-award)

Use the phases as the **timeline columns** (left-to-right):

1. Program Specific Data Capture (GAAM)
2. Progress Report 1
3. Grantee Modification Request 1
4. HRSA Staff Data Correction 1
5. Progress Report 2
6. Non-Competitive Continuation (NCC) 1
7. Progress Report 3
8. Progress Report 4
9. Grantee Modification Request 2

### 1.2 Domain objects

Use the domain objects as the **row headers** (top-to-bottom):

- Activity & Project
- Objective & Goal
- Financial Management
- Key Factor & Risk
- Performance & Workforce
- Site & Service
- Construction & Facility
- Change Management
- Clinical Services
- Equipment Management
- Board Management
- Documentation

### 1.3 Capture markers (text-first, not color-only)

Inside each matrix cell, use one of:

- `C` = Capture (new)
- `U` = Update (modify existing)
- `R` = Review/Validate (no new entry)
- `N/A` = not collected

---

## 2. Recommended diagram type (Visio)

### 2.1 Page type

- **Diagram pattern:** Matrix / crosswalk
- **Orientation:** Landscape
- **Page size:** Start with 11x17 if you need legible text; otherwise 8.5x11 landscape

### 2.2 Structure

- **Top header row:** the phases (timeline)
- **Left header column:** the domain objects
- **Cell content:** `C/U/R/N/A` markers (optionally with short notes)
- **Legend:** one small legend box explaining the markers and any icons

### 2.3 Emphasizing “captured at multiple phases” (without color-only meaning)

Use one of these (preferably only one):

- **Icon** (e.g., a solid dot) next to the row header when a domain object has 2+ `C`/`U` marks
- **Bold row header text** for multi-phase objects
- **Thicker row separator line** for multi-phase rows

---

## 3. Section 508 / Accessibility requirements (practical)

### 3.1 Color and contrast

Follow the repo palette:

- `c:\projects\POCs\src\dmedev5\docs\Section_508_Color_Palette_Style_Guide.md`

Rules:

- **Black text** on light fills (e.g., Cream `#F5F3D5`, Aqua `#B3E3EC`, Periwinkle `#B3C7F7`)
- **White text** on dark fills (e.g., Navy `#3E4367`, Forest Green `#36513F`)
- Ensure **minimum contrast 4.5:1** for normal text

### 3.2 No color-only meaning

- The cell marker letters `C/U/R/N/A` must fully convey meaning even if printed in grayscale.

### 3.3 Typography

Follow the repo diagram style:

- `c:\projects\POCs\src\dmedev5\docs\Modern_Diagram_Design_Guide.md`

Minimums:

- Body text: **11–12pt**
- Headers: **14–16pt**

### 3.4 Reading order (screen readers)

- Make sure the title is first.
- Then the header timeline row.
- Then rows **top-to-bottom**.

If you group shapes, ensure groups don’t break the logical reading flow.

### 3.5 Alt text

Add alt text to:

- The overall diagram container/title shape (summary)
- The legend
- Any non-text icons

Alt text should describe meaning, not style.

---

## 4. Build steps in Visio (repeatable)

### 4.1 Start from an existing PRM diagram (optional)

If you want consistent visual branding, open an existing diagram in this repo and reuse styles/themes:

- `c:\projects\POCs\src\dmedev5\docs\PRM_Solution_Architecture.vsdx`

### 4.2 Create the matrix

1. Create a header row for the phases.
2. Create a left column for domain objects.
3. Create the grid cells.
4. Fill each cell with `C/U/R/N/A`.
5. Add a small legend box.

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

- `G:\My Drive\06_Master_Guides\Visio_Section_508_Grant_Lifecycle_Diagram_Master_Guide.md`
