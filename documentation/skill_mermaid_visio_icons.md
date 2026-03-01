# SKILL: Using Visio Template Icons in Mermaid Diagrams

**Actionable workflow for incorporating Visio Template Visio icons into Mermaid diagrams with Section 508 compliance.**

**Last Updated:** March 1, 2026  
**Version:** 1.0.0  
**Category:** Documentation

---

## What This Skill Does

Provides workflows and techniques for:
- Embedding Visio Template icon images in Mermaid diagrams
- Maintaining Section 508 accessibility compliance
- Using exported PNG icons from Visio Template template
- Creating professional diagrams with standardized iconography

## When to Use This Skill

- **User says:** "Add Visio Template icons to my Mermaid diagram"
- **User says:** "Show me available icons for diagrams"
- **User says:** "Make my diagram use official Visio Template icons"
- **User creates:** Mermaid diagrams requiring Visio Template branding
- **Trigger:** Need to enhance Mermaid diagrams with visual icons

## What You'll Need

- Exported Visio Template icon PNG files in `${SKILLS_ROOT}/documentation/Visio Template_icons/`
- Mermaid diagram syntax knowledge
- Section 508 color palette compliance
- Markdown rendering environment that supports images

---

## Workflow: Add Visio Template Icons to Mermaid Diagrams

### Step 1: Choose Icons from Library

**Browse available icons:**

See the [Icon Preview Gallery](#icon-preview-gallery) below for all 95 available icons.

**Categories:**
- Status & Indicators (9 icons)
- Cloud & Network (8 icons)
- Database & Storage (8 icons)
- People & Roles (5 icons)
- Security (3 icons)
- Communication (4 icons)
- Favorites (6 icons)
- Shapes (14 icons)
- Flowchart (9 icons)
- Arrows (10 icons)
- Containers (6 icons)
- Diagrams (2 icons)
- Reference (3 icons)
- ER Diagram (2 icons)
- Other (5 icons)

### Step 2: Reference Icons in Mermaid

**Technique 1: Use HTML img tags in node labels**

```mermaid
graph LR
    A["<img src='Visio Template_icons/Cloud.png' width='30'/><br/>Cloud Storage"]
    B["<img src='Visio Template_icons/Database.png' width='30'/><br/>Database"]
    C["<img src='Visio Template_icons/Users.png' width='30'/><br/>Users"]
    
    A --> B
    B --> C
```

**Technique 2: Use emoji approximations (fallback)**

```mermaid
graph LR
    A["☁️ Cloud Storage"]
    B["🗄️ Database"]
    C["👥 Users"]
    
    A --> B
    B --> C
```

**Technique 3: Combine icons with Section 508 colors**

```mermaid
graph TB
    Cloud["<img src='Visio Template_icons/Cloud.png' width='40'/><br/>Cloud Services"]
    DB["<img src='Visio Template_icons/Database.png' width='40'/><br/>Database"]
    API["<img src='Visio Template_icons/API.png' width='40'/><br/>API Gateway"]
    
    Cloud --> API
    API --> DB
    
    style Cloud fill:#e1f5fe,stroke:#0d47a1,stroke-width:2px,color:#000
    style DB fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000
    style API fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
```

### Step 3: Ensure Section 508 Compliance

**Always include:**

1. **Text labels** - Don't rely on icons alone
2. **Color contrast** - Use approved color palette
3. **Alt text** - Add descriptive labels
4. **Icon + text** - Combine for clarity

**Example with full compliance:**

```mermaid
flowchart LR
    Start["<img src='Visio Template_icons/Personnel_Staff.png' width='35'/><br/>User Request"]
    Process["<img src='Visio Template_icons/Gear.png' width='35'/><br/>Process"]
    Success["<img src='Visio Template_icons/Information.png' width='35'/><br/>Success"]
    Error["<img src='Visio Template_icons/Error_icon.png' width='35'/><br/>Error"]
    
    Start --> Process
    Process -->|Valid| Success
    Process -->|Invalid| Error
    
    style Start fill:#e1f5fe,stroke:#0d47a1,stroke-width:2px,color:#000
    style Process fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style Success fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    style Error fill:#f8bbd0,stroke:#880e4f,stroke-width:2px,color:#000
```

### Step 4: Test Rendering

**Verify in your environment:**

1. Check that images render correctly
2. Verify icon paths are accessible
3. Test on different screen sizes
4. Validate color contrast ratios

---

## Icon Preview Gallery

**All 95 exported Visio Template icons with visual previews:**

### Status and Indicators (9)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Error](Visio Template_icons/Error_icon.png) | `Error_icon.png` | Error states, failures |
| ![Question](Visio Template_icons/Question_icon.png) | `Question_icon.png` | Questions, help needed |
| ![Info](Visio Template_icons/Information_icon.png) | `Information_icon.png` | Information, notes |
| ![Status](Visio Template_icons/Status_icons.png) | `Status_icons.png` | Multiple status indicators |
| ![Flags](Visio Template_icons/Flags.png) | `Flags.png` | Priority, markers |
| ![NO](Visio Template_icons/NO_sign.png) | `NO_sign.png` | Prohibited, not allowed |
| ![Help](Visio Template_icons/Help.png) | `Help.png` | Help, assistance |
| ![Information](Visio Template_icons/Information.png) | `Information.png` | Info indicator |
| ![Best Practices](Visio Template_icons/Best_Practices.png) | `Best_Practices.png` | Best practices, excellence |

### Cloud and Network (8)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Cloud](Visio Template_icons/Cloud.png) | `Cloud.png` | Cloud services, storage |
| ![Cloud Alt](Visio Template_icons/Cloud.1070.png) | `Cloud.1070.png` | Cloud variant |
| ![Cloud Upload](Visio Template_icons/Cloud_Upload.png) | `Cloud_Upload.png` | Upload to cloud |
| ![Cloud Download](Visio Template_icons/Cloud_Download.png) | `Cloud_Download.png` | Download from cloud |
| ![Network](Visio Template_icons/Network.png) | `Network.png` | Network infrastructure |
| ![Globe](Visio Template_icons/Globe_Internet.png) | `Globe_Internet.png` | Internet, web |
| ![API](Visio Template_icons/API.png) | `API.png` | API endpoints, services |

### Database and Storage (8)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Database](Visio Template_icons/Database.png) | `Database.png` | Database systems |
| ![Database Alt](Visio Template_icons/Database.1075.png) | `Database.1075.png` | Database variant |
| ![DB Group](Visio Template_icons/Database_Availability_Group.png) | `Database_Availability_Group.png` | HA databases |
| ![DB Mini](Visio Template_icons/Database_Mini_2.png) | `Database_Mini_2.png` | Small database |
| ![DB Orange](Visio Template_icons/Database_mini_2_-_orange.png) | `Database_mini_2_-_orange.png` | Orange database |
| ![DB Server](Visio Template_icons/Database_Server_-_orange.png) | `Database_Server_-_orange.png` | Database server |
| ![Data](Visio Template_icons/Data.png) | `Data.png` | Data storage |

### People and Roles (5)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Personnel](Visio Template_icons/Personnel_Staff.png) | `Personnel_Staff.png` | Staff, employees |
| ![Users](Visio Template_icons/Users.png) | `Users.png` | User accounts |
| ![Admin](Visio Template_icons/Administrator.png) | `Administrator.png` | Admin roles |
| ![Approver](Visio Template_icons/Approver.png) | `Approver.png` | Approval roles |
| ![Role Group](Visio Template_icons/Role_Group.png) | `Role_Group.png` | User groups |

### Security and Access (3)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Key](Visio Template_icons/Key_Permissions_-_green.png) | `Key_Permissions_-_green.png` | Access, permissions |
| ![Token](Visio Template_icons/Token.png) | `Token.png` | Authentication tokens |
| ![Credentials](Visio Template_icons/Credentials.png) | `Credentials.png` | Login credentials |

### Communication (4)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Chat](Visio Template_icons/Chat.png) | `Chat.png` | Messaging, communication |
| ![Chat Alt](Visio Template_icons/Chat.1099.png) | `Chat.1099.png` | Chat variant |
| ![Post](Visio Template_icons/Post.png) | `Post.png` | Posts, messages |
| ![Document](Visio Template_icons/Document.png) | `Document.png` | Documents, files |

### Favorites and Highlights (6)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Favorite](Visio Template_icons/Favorite.png) | `Favorite.png` | Favorites, bookmarks |
| ![Favorite Alt](Visio Template_icons/Favorite.1095.png) | `Favorite.1095.png` | Favorite variant |
| ![Star](Visio Template_icons/Star.png) | `Star.png` | Ratings, important |
| ![Star Label](Visio Template_icons/Star_label.png) | `Star_label.png` | Tagged favorites |
| ![Pin](Visio Template_icons/Pin.png) | `Pin.png` | Pinned items |
| ![Pin Alt](Visio Template_icons/Pin.1101.png) | `Pin.1101.png` | Location pin |

### Shapes and Symbols (7)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Heart](Visio Template_icons/Heart.png) | `Heart.png` | Favorites, health |
| ![Smile](Visio Template_icons/Smiling_Face.png) | `Smiling_Face.png` | Positive feedback |
| ![Lightning](Visio Template_icons/Lightning_Bolt.png) | `Lightning_Bolt.png` | Power, energy, fast |
| ![Gear](Visio Template_icons/Gear.png) | `Gear.png` | Settings, configuration |
| ![Drop](Visio Template_icons/Drop.png) | `Drop.png` | Water, liquid |

### Geometric Shapes (14)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Circle](Visio Template_icons/Circle.png) | `Circle.png` | Circle outline |
| ![Circle Alt1](Visio Template_icons/Circle.1012.png) | `Circle.1012.png` | Circle variant |
| ![Circle Alt2](Visio Template_icons/Circle.1110.png) | `Circle.1110.png` | Circle variant |
| ![Ellipse](Visio Template_icons/Ellipse.png) | `Ellipse.png` | Oval shape |
| ![Rectangle](Visio Template_icons/Rectangle.png) | `Rectangle.png` | Rectangle |
| ![Rectangle Alt](Visio Template_icons/Rectangle.1107.png) | `Rectangle.1107.png` | Rectangle variant |
| ![Triangle](Visio Template_icons/Triangle.png) | `Triangle.png` | Triangle |
| ![Diamond](Visio Template_icons/Diamond.png) | `Diamond.png` | Diamond/rhombus |
| ![Pentagon](Visio Template_icons/Pentagon.png) | `Pentagon.png` | Pentagon |
| ![Semi Circle](Visio Template_icons/Semi_Circle.png) | `Semi_Circle.png` | Half circle |
| ![Cone](Visio Template_icons/Cone.png) | `Cone.png` | Cone shape |
| ![6-Point Star](Visio Template_icons/6-Point_Star.png) | `6-Point_Star.png` | Star of David |
| ![16-Point Star](Visio Template_icons/16-Point_Star.png) | `16-Point_Star.png` | Multi-point star |

### Flowchart Shapes (9)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Start/End](Visio Template_icons/StartEnd.png) | `StartEnd.png` | Flow start/end |
| ![Start/End Alt1](Visio Template_icons/StartEnd.1003.png) | `StartEnd.1003.png` | Start/End variant |
| ![Process](Visio Template_icons/Process.png) | `Process.png` | Process steps |
| ![Process Box](Visio Template_icons/Process_or_Simple_Box.png) | `Process_or_Simple_Box.png` | Basic process |
| ![Subprocess](Visio Template_icons/Subprocess.png) | `Subprocess.png` | Sub-routine |
| ![On-page Ref](Visio Template_icons/On-page_reference.png) | `On-page_reference.png` | Page reference |
| ![Plain](Visio Template_icons/Plain.png) | `Plain.png` | Plain shape |

### Arrows and Connectors (10)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Simple Arrow](Visio Template_icons/Simple_Arrow.png) | `Simple_Arrow.png` | Basic arrow |
| ![Modern Arrow](Visio Template_icons/Modern_Arrow.png) | `Modern_Arrow.png` | Stylized arrow |
| ![Modern Arrow Alt](Visio Template_icons/Modern_Arrow.1012.png) | `Modern_Arrow.1012.png` | Arrow variant |
| ![Double Arrow](Visio Template_icons/Simple_Double_Arrow.png) | `Simple_Double_Arrow.png` | Bidirectional |
| ![Block Arrow](Visio Template_icons/Block_Arrow.png) | `Block_Arrow.png` | Thick arrow |
| ![Line Arrow](Visio Template_icons/Line_Arrow.png) | `Line_Arrow.png` | Line with arrow |
| ![Line Double](Visio Template_icons/Line_Double_Arrow.png) | `Line_Double_Arrow.png` | Line both arrows |
| ![Straight Line](Visio Template_icons/Straight_Line.png) | `Straight_Line.png` | Simple line |
| ![Arrow Box](Visio Template_icons/Arrow_box.png) | `Arrow_box.png` | Box with arrow |

### Containers and Layouts (6)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Swimlane](Visio Template_icons/Swimlane.png) | `Swimlane.png` | Process swimlanes |
| ![Container](Visio Template_icons/CFF_Container.png) | `CFF_Container.png` | Grouping container |
| ![Swimlane List](Visio Template_icons/Swimlane_List.png) | `Swimlane_List.png` | Multiple lanes |
| ![Phase List](Visio Template_icons/Phase_List.png) | `Phase_List.png` | Project phases |
| ![Layered Box](Visio Template_icons/Layered_Box.png) | `Layered_Box.png` | Stacked boxes |

### Diagrams and Charts (2)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![4-Phase](Visio Template_icons/4-Phase_Circular_Motion.png) | `4-Phase_Circular_Motion.png` | 4-part cycle |
| ![Pyramid](Visio Template_icons/Inverted_Pyramid.png) | `Inverted_Pyramid.png` | Hierarchy, funnel |

### Reference and Notes (3)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Ref Oval](Visio Template_icons/Reference_oval.png) | `Reference_oval.png` | Reference marker |
| ![Ref Rectangle](Visio Template_icons/Reference_rectangle.png) | `Reference_rectangle.png` | Reference box |
| ![Yellow Note](Visio Template_icons/Yellow_note.png) | `Yellow_note.png` | Notes, annotations |

### Entity Relationship (2)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Entity](Visio Template_icons/Entity_With_Attributes.png) | `Entity_With_Attributes.png` | ER entity |
| ![PK Separator](Visio Template_icons/Primary_Key_Separator.png) | `Primary_Key_Separator.png` | Attribute divider |

### Other Specialized (5)

| Icon | Filename | Use Case |
|------|----------|----------|
| ![Component](Visio Template_icons/Component.png) | `Component.png` | System component |
| ![Enterprise](Visio Template_icons/Enterprise_area.png) | `Enterprise_area.png` | Enterprise boundary |
| ![Process Path](Visio Template_icons/Process_path.png) | `Process_path.png` | Process pathway |
| ![Topic](Visio Template_icons/Topic.png) | `Topic.png` | Discussion topic |
| ![Delete](Visio Template_icons/Delete.png) | `Delete.png` | Delete action |

---

## Example Diagrams

### Example 1: Cloud Architecture

```mermaid
graph TB
    User["<img src='Visio Template_icons/Users.png' width='40'/><br/>Users"]
    Web["<img src='Visio Template_icons/Globe_Internet.png' width='40'/><br/>Web App"]
    API["<img src='Visio Template_icons/API.png' width='40'/><br/>API Gateway"]
    Cloud["<img src='Visio Template_icons/Cloud.png' width='40'/><br/>Cloud Services"]
    DB["<img src='Visio Template_icons/Database.png' width='40'/><br/>Database"]
    
    User --> Web
    Web --> API
    API --> Cloud
    Cloud --> DB
    
    style User fill:#e1f5fe,stroke:#0d47a1,stroke-width:2px,color:#000
    style Web fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style API fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
    style Cloud fill:#e0f2f1,stroke:#00695c,stroke-width:2px,color:#000
    style DB fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
```

### Example 2: Security Flow

```mermaid
flowchart LR
    Login["<img src='Visio Template_icons/Personnel_Staff.png' width='35'/><br/>User Login"]
    Creds["<img src='Visio Template_icons/Credentials.png' width='35'/><br/>Credentials"]
    Token["<img src='Visio Template_icons/Token.png' width='35'/><br/>Auth Token"]
    Access["<img src='Visio Template_icons/Key_Permissions_-_green.png' width='35'/><br/>Access Granted"]
    
    Login --> Creds
    Creds --> Token
    Token --> Access
    
    style Login fill:#e1f5fe,stroke:#0d47a1,stroke-width:2px,color:#000
    style Creds fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style Token fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
    style Access fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
```

### Example 3: Data Processing

```mermaid
graph LR
    Start["<img src='Visio Template_icons/StartEnd.png' width='35'/><br/>Start"]
    Process["<img src='Visio Template_icons/Gear.png' width='35'/><br/>Process Data"]
    DB["<img src='Visio Template_icons/Database.png' width='35'/><br/>Store"]
    Success["<img src='Visio Template_icons/Information.png' width='35'/><br/>Success"]
    Error["<img src='Visio Template_icons/Error_icon.png' width='35'/><br/>Error"]
    
    Start --> Process
    Process -->|Valid| DB
    Process -->|Invalid| Error
    DB --> Success
    
    style Start fill:#e1f5fe,stroke:#0d47a1,stroke-width:2px,color:#000
    style Process fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style DB fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    style Success fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    style Error fill:#f8bbd0,stroke:#880e4f,stroke-width:2px,color:#000
```

---

## Best Practices

### Icon Usage

✅ **Do:**
- Use icons to supplement text labels
- Keep icon sizes consistent (30-40px recommended)
- Combine icons with Section 508 colors
- Test rendering in target environment
- Provide text alternatives

❌ **Don't:**
- Rely on icons alone for meaning
- Use icons without text labels
- Mix icon sizes inconsistently
- Use non-Visio Template icons in official diagrams
- Forget color contrast requirements

### Section 508 Compliance

**Always ensure:**
1. Text labels accompany all icons
2. Color contrast meets 4.5:1 minimum
3. Icons are decorative, not informational alone
4. Diagrams work in black and white
5. Alt text is provided for images

---

## AI Agent Instructions

**When user requests Visio Template icons in Mermaid:**

1. **Show icon gallery** - Reference this skill's preview section
2. **Provide syntax** - Use HTML img tag technique
3. **Add Section 508 colors** - Include approved color styling
4. **Test accessibility** - Verify text labels and contrast
5. **Provide examples** - Show complete working diagrams

**Output format:**
```
📊 Icon: Visio Template_icons/{icon_name}.png
🎨 Section 508 Color: fill:#{color},stroke:#{stroke}
📝 Label: Always include text with icon
✅ Accessible: Icon + Text + Color contrast
```

---

## Related Skills

- **skill_Visio Template_visio_icons.md** - Visio Template icon library and extraction
- **Visio Template_ICON_GALLERY.md** - Complete icon reference
- **skill_mermaid_diagrams.md** - Mermaid diagram syntax
- **skill_mermaid_section_508.md** - Section 508 Mermaid compliance
- **skill_section_508_color_palette.md** - Approved color palette
- **skill_diagram_icons.md** - Unicode emoji alternatives

---

## Troubleshooting

### Icons Not Rendering

**Problem:** Images don't show in diagram  
**Solution:** 
- Verify path: `Visio Template_icons/{icon_name}.png`
- Check file exists in documentation folder
- Use relative path from markdown file location
- Test in different markdown renderer

### Icons Too Large/Small

**Problem:** Icon size inconsistent  
**Solution:**
- Use `width='30'` to `width='40'` for consistency
- Adjust based on diagram complexity
- Keep all icons same size within diagram

### Poor Contrast

**Problem:** Icons hard to see on colored backgrounds  
**Solution:**
- Use Section 508 approved light backgrounds
- Ensure 4.5:1 contrast ratio minimum
- Test with color blindness simulators
- Add stroke/border to icons if needed

---

## Changelog

- **2026-03-01:** Created skill for using Visio Template icons in Mermaid diagrams
- **2026-03-01:** Added visual preview gallery of all 95 exported icons
- **2026-03-01:** Included example diagrams with Section 508 compliance
- **2026-03-01:** Added AI agent instructions and best practices

---

**Location:** `${SKILLS_ROOT}/documentation/skill_mermaid_Visio Template_icons.md`  
**Category:** Documentation  
**Icons Available:** 95 PNG files  
**Section 508:** Compliant when used with approved colors  
**Requires:** Exported Visio Template icons in Visio Template_icons/ directory

