# Section 508 Compliance Guidelines

**Last Updated:** March 1, 2026  
**Purpose:** General Section 508 accessibility guidelines for all digital content including documents, diagrams, and web applications.

---

## Overview

Section 508 is a federal law requiring that electronic and information technology be accessible to people with disabilities. This skill provides comprehensive guidelines for creating accessible content across all formats.

**Applies to:**
- Documents (Word, PDF, Markdown)
- Diagrams (Visio, Mermaid, images)
- Web applications and interfaces
- Presentations and training materials
- Forms and data entry

---

## Core Section 508 Principles

### 1. Perceivable

**Information must be presentable to users in ways they can perceive.**

- Provide text alternatives for non-text content
- Provide captions and alternatives for multimedia
- Create content that can be presented in different ways
- Make it easier for users to see and hear content

### 2. Operable

**User interface components must be operable.**

- Make all functionality available from keyboard
- Give users enough time to read and use content
- Do not use content that causes seizures
- Help users navigate and find content

### 3. Understandable

**Information and operation must be understandable.**

- Make text readable and understandable
- Make content appear and operate in predictable ways
- Help users avoid and correct mistakes

### 4. Robust

**Content must be robust enough for assistive technologies.**

- Maximize compatibility with current and future tools
- Use standard formats and markup
- Ensure content works with screen readers

---

## Color and Contrast Requirements

### Contrast Ratios (WCAG 2.1)

**Level AA (Required):**
- Normal text: 4.5:1 minimum
- Large text (18pt+ or 14pt+ bold): 3:1 minimum
- UI components and graphics: 3:1 minimum

**Level AAA (Enhanced):**
- Normal text: 7:1 minimum
- Large text: 4.5:1 minimum

### No Color-Only Meaning

**❌ Bad - Color alone conveys status:**
- Red box = error
- Green box = success
- Yellow box = warning

**✅ Good - Color + text/icons:**
- Red box with "✗ Error" text
- Green box with "✓ Success" text
- Yellow box with "⚠ Warning" text

### Approved Color Palette

**High Contrast Colors:**

| Purpose | Light BG | Dark BG | Text Color |
|---------|----------|---------|------------|
| Primary | #e1f5fe | #0d47a1 | Black/White |
| Success | #e8f5e9 | #1b5e20 | Black/White |
| Warning | #fff3e0 | #e65100 | Black/White |
| Error | #fce4ec | #880e4f | Black/White |
| Info | #e0f2f1 | #00695c | Black/White |

---

## Document Accessibility

### Microsoft Word Documents

**Required elements:**
- Document title in properties
- Heading styles (Heading 1, 2, 3) for structure
- Alt text for all images and diagrams
- Meaningful hyperlink text (not "click here")
- Table headers identified
- Lists using list formatting (not manual bullets)

**Accessibility Checker:**
```
File > Info > Check for Issues > Check Accessibility
```

### PDF Documents

**Requirements:**
- Tagged PDF (not scanned image)
- Document title and language set
- Logical reading order
- Alt text for images
- Form fields labeled
- Bookmarks for navigation (long documents)

**Adobe Acrobat Checker:**
```
Tools > Accessibility > Full Check
```

### Markdown Documents

**Best practices:**
- Use proper heading hierarchy (#, ##, ###)
- Alt text for images: `![Description](image.png)`
- Descriptive link text: `[View report](url)` not `[Click here](url)`
- Tables with headers
- Lists using proper markdown syntax

---

## Diagram Accessibility

### General Requirements

**All diagrams must have:**
- Descriptive title
- Alt text or long description
- Text labels (not color-only coding)
- Sufficient contrast
- Readable font sizes (11pt minimum)

### Visio Diagrams

**See:** [skill_visio_section_508.md](../documentation/skill_visio_section_508.md)

**Key requirements:**
- Alt text on diagram and shapes
- Text labels for all meaning
- Approved color palette
- Export to tagged PDF

### Mermaid Diagrams

**See:** [skill_mermaid_section_508.md](../documentation/skill_mermaid_section_508.md)

**Key requirements:**
- Icons + text labels
- Section 508 color palette
- Text description in documentation
- Sufficient contrast

### Image Diagrams

**Requirements:**
- Provide alt text
- Include long description for complex diagrams
- Ensure text in image is readable
- Consider providing text alternative

**Example:**
```html
<img src="architecture.png" 
     alt="System architecture diagram" 
     longdesc="architecture-description.html">
```

---

## Web Application Accessibility

### Keyboard Navigation

**Requirements:**
- All functionality accessible via keyboard
- Visible focus indicators
- Logical tab order
- Skip navigation links
- Keyboard shortcuts documented

**Test:**
- Navigate entire application using only Tab, Enter, Arrow keys
- Ensure all interactive elements are reachable
- Verify focus is always visible

### Screen Reader Compatibility

**Requirements:**
- Semantic HTML (header, nav, main, footer)
- ARIA labels where needed
- Form labels associated with inputs
- Error messages announced
- Dynamic content updates announced

**Test with:**
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (Mac/iOS)
- TalkBack (Android)

### Forms

**Requirements:**
- Labels for all inputs
- Required fields indicated
- Error messages clear and specific
- Instructions provided before form
- Confirmation for destructive actions

**Example:**
```html
<label for="email">Email Address (required)</label>
<input type="email" id="email" required aria-required="true">
<span id="email-error" role="alert"></span>
```

---

## Typography and Readability

### Font Requirements

**Approved fonts:**
- Segoe UI
- Calibri
- Arial
- Helvetica
- Verdana

**Avoid:**
- Decorative fonts
- Script fonts
- All caps for long text
- Italics for long text

### Size Requirements

**Minimum sizes:**
- Body text: 11-12pt
- Headings: 14-18pt
- Captions: 10pt minimum
- Allow user to resize text to 200%

### Line Spacing

**Requirements:**
- Line height: 1.5x font size minimum
- Paragraph spacing: 1.5x line height
- Letter spacing: 0.12x font size
- Word spacing: 0.16x font size

---

## Multimedia Accessibility

### Video Requirements

**Must provide:**
- Captions for all speech and sounds
- Audio description for visual content
- Transcript of all content
- Media player keyboard accessible

### Audio Requirements

**Must provide:**
- Transcript of all content
- Visual indicators for sound cues
- Pause/stop controls
- Volume control

---

## Testing and Validation

### Automated Testing Tools

**Web content:**
- WAVE (Web Accessibility Evaluation Tool)
- axe DevTools (browser extension)
- Lighthouse (Chrome DevTools)
- Pa11y (command line)

**Documents:**
- Microsoft Accessibility Checker (Word, PowerPoint)
- Adobe Acrobat Accessibility Checker (PDF)
- CommonLook (PDF)

### Manual Testing

**Required tests:**
- Keyboard-only navigation
- Screen reader testing
- Color contrast verification
- Zoom to 200% and verify layout
- Test with browser extensions disabled

### User Testing

**Best practice:**
- Test with users who have disabilities
- Include variety of assistive technologies
- Document issues and fixes
- Iterate based on feedback

---

## Common Violations and Fixes

### Violation 1: Missing Alt Text

**Issue:** Images without alt text  
**Fix:** Add descriptive alt text to all images

```html
<!-- Bad -->
<img src="chart.png">

<!-- Good -->
<img src="chart.png" alt="Bar chart showing 25% increase in sales">
```

### Violation 2: Low Contrast

**Issue:** Text doesn't meet 4.5:1 contrast  
**Fix:** Use darker text or lighter background

```css
/* Bad - 2.5:1 contrast */
color: #999999;
background: #ffffff;

/* Good - 7:1 contrast */
color: #424242;
background: #ffffff;
```

### Violation 3: Unlabeled Form Fields

**Issue:** Input without associated label  
**Fix:** Add label element with for attribute

```html
<!-- Bad -->
<input type="text" placeholder="Name">

<!-- Good -->
<label for="name">Name</label>
<input type="text" id="name">
```

### Violation 4: Non-Semantic HTML

**Issue:** Using divs for everything  
**Fix:** Use semantic HTML elements

```html
<!-- Bad -->
<div class="header">
  <div class="nav">...</div>
</div>

<!-- Good -->
<header>
  <nav>...</nav>
</header>
```

---

## Compliance Checklist

### Document Checklist

- [ ] Document title set
- [ ] Headings use proper styles
- [ ] Images have alt text
- [ ] Links have descriptive text
- [ ] Tables have headers
- [ ] Lists use proper formatting
- [ ] Color not sole means of conveying information
- [ ] Contrast meets 4.5:1 minimum
- [ ] Font size 11pt or larger
- [ ] Accessibility checker run and issues resolved

### Diagram Checklist

- [ ] Diagram has title
- [ ] Alt text provided
- [ ] Text labels for all elements
- [ ] Icons supplement color coding
- [ ] Contrast meets 4.5:1 minimum
- [ ] Font size readable (11pt+)
- [ ] Approved color palette used
- [ ] Logical reading order
- [ ] Legend included if needed
- [ ] Text description provided

### Web Application Checklist

- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Screen reader compatible
- [ ] Form labels present
- [ ] Error messages clear
- [ ] Semantic HTML used
- [ ] ARIA labels where needed
- [ ] Color contrast sufficient
- [ ] Text resizable to 200%
- [ ] Automated tests pass

---

## Resources

### Official Guidelines

- **Section 508:** https://www.section508.gov/
- **WCAG 2.1:** https://www.w3.org/WAI/WCAG21/quickref/
- **ADA:** https://www.ada.gov/

### Testing Tools

- **WAVE:** https://wave.webaim.org/
- **axe DevTools:** https://www.deque.com/axe/devtools/
- **Contrast Checker:** https://webaim.org/resources/contrastchecker/
- **Color Blindness Simulator:** https://www.color-blindness.com/coblis-color-blindness-simulator/

### Training

- **WebAIM:** https://webaim.org/training/
- **Deque University:** https://dequeuniversity.com/
- **Section 508 Training:** https://www.section508.gov/training/

---

## Related Skills

- [skill_mermaid_section_508.md](../documentation/skill_mermaid_section_508.md) - Mermaid diagram accessibility
- [skill_visio_section_508.md](../documentation/skill_visio_section_508.md) - Visio diagram accessibility
- [skill_feature_documentation.md](../documentation/skill_feature_documentation.md) - Documentation standards

---

## Quick Reference

**Section 508 in 5 Rules:**

1. **No color-only meaning** - Use text + icons
2. **4.5:1 contrast minimum** - Dark text on light backgrounds
3. **Alt text for images** - Describe meaning, not appearance
4. **Keyboard accessible** - All functions work without mouse
5. **Semantic structure** - Use proper headings and markup

**When in doubt:**
- Add more text labels
- Increase contrast
- Test with keyboard only
- Run accessibility checker

---

**Last Updated:** March 1, 2026  
**Location:** `G:\My Drive\06_Skills\system\skill_section_508_compliance.md`
