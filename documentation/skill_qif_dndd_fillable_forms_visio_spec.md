# QIF-DNDD Fillable Forms Solution - Architecture Diagram Specification
**For Visio Diagram Creation with Section 508 Compliance**

**Document Version:** 1.0  
**Date:** February 24, 2026  
**Purpose:** Detailed specification for creating Section 508 compliant Visio architecture diagram  
**NOFO:** HRSA-26-062 QIF-DNDD

---

## Section 508 Compliance Requirements

**All diagram elements MUST include:**
1. **Alt Text:** Descriptive text for each shape/component
2. **High Contrast:** Use colors with sufficient contrast ratio (4.5:1 minimum)
3. **Text Labels:** All connections and flows must have readable text labels
4. **Logical Reading Order:** Left-to-right, top-to-bottom flow
5. **No Color-Only Information:** Use patterns/shapes in addition to colors
6. **Accessible Fonts:** Minimum 12pt, sans-serif (Arial, Calibri)

**Recommended Visio Stencils:**
- Azure (for cloud components)
- Basic Flowchart
- Cross-Functional Flowchart
- Network and Peripherals

---

## Architecture Overview

**Diagram Title:** AI-Powered Fillable Forms Solution Architecture  
**Subtitle:** QIF-DNDD NOFO Form Generation and Data Extraction Pipeline

**Diagram Dimensions:** 11" x 17" (Landscape)  
**Color Scheme:** 
- Primary: Blue (#0078D4) - Azure/Microsoft services
- Secondary: Green (#107C10) - Success/Data flow
- Accent: Orange (#D83B01) - AI/Intelligent services
- Neutral: Gray (#605E5C) - Infrastructure/Storage

---

## Layer 1: User Interface & Input (Top)

### Component 1.1: Admin Portal
- **Shape:** Rectangle with rounded corners
- **Color:** Light Blue (#E1F5FE)
- **Icon:** User/Admin icon
- **Label:** "Admin Portal / Super User Interface"
- **Alt Text:** "Administrative portal where super users create packages, upload RSD documents, and select grantee cohorts"
- **Sub-components:**
  - Package Creation
  - RSD Upload
  - Cohort Selection
  - Configuration Management

### Component 1.2: Input Documents
- **Shape:** Document icon (stacked papers)
- **Color:** White with blue border
- **Label:** "Input Documents"
- **Alt Text:** "Requirements Specification Documents (RSD) and static PDF/Word templates"
- **Items:**
  - RSD (Requirements Specification Document)
  - Static PDF Templates
  - Static Word Templates
  - Static Excel Templates

---

## Layer 2: MCP Server & Aspose Tools (Core Processing)

### Component 2.1: MCP Server
- **Shape:** Server rack icon
- **Color:** Dark Blue (#003366)
- **Label:** "MCP Server (Model Context Protocol)"
- **Alt Text:** "MCP Server hosting Aspose document manipulation tools and providing API endpoints for agentic AI integration"
- **Position:** Center-left of diagram
- **Specifications:**
  - Hosts Aspose tool libraries
  - Provides API endpoints
  - Manages tool registration
  - Handles authentication

### Component 2.2: Aspose Tools Suite (Inside MCP Server)
- **Shape:** Three connected rectangles within MCP Server boundary
- **Color:** Light Orange (#FFF4E5)
- **Labels:**
  1. **Aspose.PDF**
     - Alt Text: "Aspose.PDF library for PDF generation, manipulation, and field extraction"
     - Functions: Generate fillable PDFs, extract form fields, add digital signatures
  
  2. **Aspose.Words**
     - Alt Text: "Aspose.Words library for Word document generation and manipulation"
     - Functions: Generate fillable Word forms, extract content, convert formats
  
  3. **Aspose.Cells**
     - Alt Text: "Aspose.Cells library for Excel generation and manipulation"
     - Functions: Generate fillable Excel forms, extract data, validate formulas

### Component 2.3: Agentic AI Platform
- **Shape:** Brain/AI icon in rectangle
- **Color:** Orange (#D83B01)
- **Label:** "Agentic AI Platform (Devin/Windsurf)"
- **Alt Text:** "Agentic AI platform that orchestrates form generation by calling MCP Aspose tools based on RSD analysis"
- **Position:** Center of diagram
- **Functions:**
  - RSD Analysis
  - Field Detection
  - Schema Generation
  - Tool Orchestration
  - Code Generation

**Connection:** Bidirectional arrow between Agentic AI and MCP Server
- **Label:** "Tool Calls & Responses (JSON)"
- **Alt Text:** "Agentic AI calls Aspose tools via MCP API and receives JSON responses"

---

## Layer 3: Form Generation Pipeline (Middle-Left)

### Component 3.1: AI Field Detection
- **Shape:** Hexagon (processing step)
- **Color:** Light Orange (#FFF4E5)
- **Label:** "AI Field Detection & Analysis"
- **Alt Text:** "AI analyzes RSD and static documents to identify form fields, validation rules, and relationships"
- **Process:**
  - Document layout analysis
  - Field type identification
  - Validation rule extraction
  - Relationship mapping

### Component 3.2: JSON Schema Generation
- **Shape:** Cylinder (data)
- **Color:** Light Green (#E8F5E9)
- **Label:** "JSON Schema"
- **Alt Text:** "Standardized JSON schema defining field names, types, validations, and relationships"
- **Schema Elements:**
  - Field definitions
  - Data types
  - Validation rules
  - Dependencies
  - Default values

### Component 3.3: Pre-population Service
- **Shape:** Rectangle
- **Color:** Light Blue (#E3F2FD)
- **Label:** "Grantee Data Pre-population"
- **Alt Text:** "Service that retrieves existing grantee data and pre-populates form fields"
- **Data Sources:**
  - Organization info (name, address, EIN)
  - Active grant details (H80 award)
  - Historical submissions
  - NOFO-specific data

### Component 3.4: Fillable Form Generator
- **Shape:** Rectangle with gear icon
- **Color:** Blue (#0078D4)
- **Label:** "Fillable Form Generator (Aspose via MCP)"
- **Alt Text:** "Generator that creates fillable PDF/Word/Excel forms using Aspose tools through MCP server"
- **Outputs:**
  - Fillable PDF with digital signature
  - Fillable Word document
  - Fillable Excel workbook
  - Validation macros/JavaScript

### Component 3.5: Automated Test Suite
- **Shape:** Rectangle with checkmark
- **Color:** Green (#107C10)
- **Label:** "Automated Test Suite"
- **Alt Text:** "Automated tests validating form functionality, field validation, and data extraction"

---

## Layer 4: Azure Cloud Services (Middle)

### Component 4.1: Azure Blob Storage
- **Shape:** Azure Blob Storage icon
- **Color:** Azure Blue (#0078D4)
- **Label:** "Azure Blob Storage"
- **Alt Text:** "Azure Blob Storage for storing generated forms, submitted PDFs, and extraction artifacts"
- **Storage Containers:**
  - Generated Forms
  - Submitted PDFs
  - Extraction Artifacts
  - Audit Logs

### Component 4.2: Azure SQL Database / Cosmos DB
- **Shape:** Database cylinder
- **Color:** Azure Blue (#0078D4)
- **Label:** "Azure SQL / Cosmos DB"
- **Alt Text:** "Database storing JSON schemas, extracted data, metadata, and audit trails"
- **Data Stored:**
  - JSON schemas
  - Extracted form data
  - Metadata
  - Audit trails
  - Version history

### Component 4.3: Azure OpenAI Service
- **Shape:** AI brain icon
- **Color:** Orange (#D83B01)
- **Label:** "Azure OpenAI"
- **Alt Text:** "Azure OpenAI service for analyzing extracted data, detecting anomalies, and generating review summaries"
- **Functions:**
  - Anomaly detection
  - Risk scoring
  - Completeness analysis
  - Summary generation

### Component 4.4: Azure API Management
- **Shape:** API gateway icon
- **Color:** Azure Blue (#0078D4)
- **Label:** "Azure API Management"
- **Alt Text:** "API Management gateway for secure API endpoints, authentication, and rate limiting"

---

## Layer 5: Data Extraction Pipeline (Middle-Right)

### Component 5.1: PDF Submission Endpoint
- **Shape:** Rectangle
- **Color:** Light Blue (#E3F2FD)
- **Label:** "PDF Submission API"
- **Alt Text:** "API endpoint receiving submitted PDFs from Grants.gov"

### Component 5.2: Field Extraction Service
- **Shape:** Hexagon
- **Color:** Light Orange (#FFF4E5)
- **Label:** "Field Extraction (Aspose via MCP)"
- **Alt Text:** "Service using Aspose.PDF through MCP to extract form fields and values"

### Component 5.3: Schema Mapping
- **Shape:** Hexagon
- **Color:** Light Green (#E8F5E9)
- **Label:** "Schema Mapping & Transformation"
- **Alt Text:** "Converts extracted fields to standardized JSON schema"

### Component 5.4: Validation Engine
- **Shape:** Diamond (decision)
- **Color:** Yellow (#FFF9C4)
- **Label:** "Rule-based Validation"
- **Alt Text:** "Validates extracted data against business rules and requirements"

### Component 5.5: AI Review Service
- **Shape:** Rectangle with AI icon
- **Color:** Orange (#D83B01)
- **Label:** "AI Review & Analysis"
- **Alt Text:** "Azure OpenAI analyzes data for anomalies, risk indicators, and generates summaries"

---

## Layer 6: External Systems (Bottom)

### Component 6.1: Grants.gov
- **Shape:** Cloud with government building icon
- **Color:** Gray (#605E5C)
- **Label:** "Grants.gov"
- **Alt Text:** "Federal grants management system where fillable forms are submitted and retrieved"
- **Interactions:**
  - Form upload (outbound)
  - Submission retrieval (inbound)

### Component 6.2: EHBs Data Integration Hub
- **Shape:** Rectangle with database icon
- **Color:** Blue (#0078D4)
- **Label:** "EHBs Data Integration Hub"
- **Alt Text:** "Enterprise Health Benefits data integration hub receiving structured form data"
- **Data Received:**
  - Structured JSON data
  - Metadata
  - AI review results
  - Audit trails

### Component 6.3: Review Workflow Systems
- **Shape:** Rectangle
- **Color:** Light Blue (#E3F2FD)
- **Label:** "Review Workflow Systems"
- **Alt Text:** "Downstream systems for application review and decision-making"

---

## Data Flows & Connections

### Flow 1: Form Generation Flow (Left to Right, Top to Bottom)
1. **Admin Portal → Agentic AI**
   - Label: "RSD Upload & Configuration"
   - Alt Text: "Admin uploads RSD and configuration to Agentic AI platform"
   - Style: Solid blue arrow

2. **Agentic AI → MCP Server**
   - Label: "Tool Calls (Aspose API)"
   - Alt Text: "Agentic AI calls Aspose tools through MCP server API"
   - Style: Solid orange arrow (bidirectional)

3. **MCP Server → Aspose Tools**
   - Label: "Execute Tool Functions"
   - Alt Text: "MCP server executes Aspose tool functions"
   - Style: Solid orange arrow (internal)

4. **Agentic AI → JSON Schema**
   - Label: "Generate Schema"
   - Alt Text: "AI generates JSON schema from RSD analysis"
   - Style: Solid green arrow

5. **JSON Schema → Pre-population Service**
   - Label: "Schema + Grantee Data"
   - Alt Text: "Schema combined with grantee data for pre-population"
   - Style: Solid blue arrow

6. **Pre-population Service → Fillable Form Generator**
   - Label: "Pre-populated Schema"
   - Alt Text: "Pre-populated schema sent to form generator"
   - Style: Solid blue arrow

7. **Fillable Form Generator → MCP Server**
   - Label: "Generate Forms (Aspose)"
   - Alt Text: "Form generator calls Aspose tools via MCP to create fillable forms"
   - Style: Solid orange arrow

8. **Fillable Form Generator → Azure Blob Storage**
   - Label: "Store Generated Forms"
   - Alt Text: "Generated fillable forms stored in Azure Blob Storage"
   - Style: Solid blue arrow

9. **Fillable Form Generator → Automated Test Suite**
   - Label: "Test Forms"
   - Alt Text: "Generated forms sent to automated test suite for validation"
   - Style: Dashed green arrow

10. **Azure Blob Storage → Grants.gov**
    - Label: "Upload Fillable Forms"
    - Alt Text: "Fillable forms uploaded to Grants.gov for grantee access"
    - Style: Solid blue arrow

### Flow 2: Data Extraction Flow (Right to Left, Top to Bottom)
1. **Grants.gov → PDF Submission Endpoint**
   - Label: "Submitted PDFs"
   - Alt Text: "Submitted PDF forms retrieved from Grants.gov"
   - Style: Solid blue arrow

2. **PDF Submission Endpoint → Azure Blob Storage**
   - Label: "Store Submissions"
   - Alt Text: "Submitted PDFs stored in Azure Blob Storage"
   - Style: Solid blue arrow

3. **Azure Blob Storage → Field Extraction Service**
   - Label: "Retrieve PDF"
   - Alt Text: "PDF retrieved for field extraction"
   - Style: Solid blue arrow

4. **Field Extraction Service → MCP Server**
   - Label: "Extract Fields (Aspose)"
   - Alt Text: "Field extraction service calls Aspose.PDF via MCP to extract form data"
   - Style: Solid orange arrow

5. **Field Extraction Service → Schema Mapping**
   - Label: "Extracted Fields"
   - Alt Text: "Extracted fields sent to schema mapping service"
   - Style: Solid green arrow

6. **Schema Mapping → Validation Engine**
   - Label: "JSON Data"
   - Alt Text: "Mapped JSON data sent to validation engine"
   - Style: Solid green arrow

7. **Validation Engine → Azure SQL/Cosmos DB**
   - Label: "Store Valid Data"
   - Alt Text: "Validated data stored in database"
   - Style: Solid blue arrow (if valid)

8. **Validation Engine → Error Handling**
   - Label: "Validation Errors"
   - Alt Text: "Validation errors logged for review"
   - Style: Dashed red arrow (if errors)

9. **Azure SQL/Cosmos DB → AI Review Service**
   - Label: "Retrieve Data"
   - Alt Text: "Validated data retrieved for AI review"
   - Style: Solid blue arrow

10. **AI Review Service → Azure OpenAI**
    - Label: "Analyze Data"
    - Alt Text: "Data sent to Azure OpenAI for analysis"
    - Style: Solid orange arrow

11. **Azure OpenAI → Azure SQL/Cosmos DB**
    - Label: "Store AI Review Results"
    - Alt Text: "AI review results and summaries stored in database"
    - Style: Solid orange arrow

12. **Azure SQL/Cosmos DB → EHBs Data Integration Hub**
    - Label: "Structured Data + AI Insights"
    - Alt Text: "Structured data and AI insights sent to EHBs"
    - Style: Solid blue arrow

13. **Azure SQL/Cosmos DB → Review Workflow Systems**
    - Label: "Trigger Workflows"
    - Alt Text: "Workflow events triggered for downstream review systems"
    - Style: Solid blue arrow

### Flow 3: Audit & Logging (Throughout)
- **All Components → Azure SQL/Cosmos DB**
  - Label: "Audit Logs"
  - Alt Text: "All components log activities to database for audit trail"
  - Style: Dashed gray arrows

---

## Legend (Bottom Right Corner)

**Shape Legend:**
- Rectangle: Service/Component
- Hexagon: Processing Step
- Diamond: Decision Point
- Cylinder: Data Storage
- Cloud: External System
- Document: Input/Output Document

**Color Legend:**
- Blue: Azure Services / Core Components
- Orange: AI/Intelligent Services
- Green: Data/Success Flows
- Gray: External Systems
- Yellow: Validation/Decision Points

**Arrow Legend:**
- Solid Arrow: Primary data flow
- Dashed Arrow: Secondary/conditional flow
- Bidirectional Arrow: Two-way communication

---

## 9-Step Data Extraction Pipeline (Callout Box)

**Position:** Bottom center of diagram  
**Shape:** Rounded rectangle callout  
**Color:** Light yellow background (#FFFDE7)

**Steps:**
1. **PDF Submission** – API retrieval → Blob storage
2. **Field Extraction** – Aspose extracts form fields via MCP
3. **Schema Mapping** – Convert to JSON schema
4. **Validation** – Rule-based data checks
5. **Data Storage** – JSON + metadata to database
6. **AI Review** – Azure OpenAI analyzes for anomalies/risk
7. **Audit Trail** – Save AI review output
8. **Workflow Trigger** – Send events to downstream systems
9. **Error Handling** – Logging and audit trail

---

## Key Metrics Callout (Top Right Corner)

**Position:** Top right  
**Shape:** Rounded rectangle  
**Color:** Light green background (#E8F5E9)

**Content:**
- **Timeline:** 19 days to Feb 11 deadline
- **Volume:** 25 applications @ $2M each
- **Performance:** <5 minutes per form extraction
- **Accuracy:** 90% data extraction accuracy
- **Reusability:** 10+ NOFOs in FY26/FY27

---

## Security & Compliance Callout (Bottom Left Corner)

**Position:** Bottom left  
**Shape:** Shield icon with text  
**Color:** Light blue background (#E3F2FD)

**Content:**
- Document signing validation
- Macro/JavaScript execution controls
- API authentication (OAuth 2.0)
- Audit logging (all operations)
- OMB compliance maintained
- Grants.gov compatibility

---

## Visio Implementation Notes

### Layers to Use:
1. **Background Layer:** Grid, title, legend
2. **Infrastructure Layer:** Azure services, MCP server
3. **Application Layer:** Agentic AI, form generator, extraction services
4. **Data Flow Layer:** Arrows and connection labels
5. **Callout Layer:** Metrics, pipeline, security callouts

### Accessibility Checklist:
- [ ] All shapes have alt text
- [ ] All connectors have labels
- [ ] Color contrast ratio ≥ 4.5:1
- [ ] Font size ≥ 12pt
- [ ] Logical reading order (left-to-right, top-to-bottom)
- [ ] No information conveyed by color alone
- [ ] Document properties include title and description
- [ ] Diagram can be navigated with keyboard only

### Export Formats:
- Primary: .vsdx (Visio)
- Accessible: .pdf (with tags and alt text)
- Web: .svg (with ARIA labels)
- Print: High-resolution .png

---

## Document Metadata

**Title:** AI-Powered Fillable Forms Solution Architecture  
**Description:** Architecture diagram showing the complete flow from RSD upload through form generation, submission, and data extraction for the QIF-DNDD NOFO fillable forms solution. Includes MCP server hosting Aspose tools, Agentic AI orchestration, Azure cloud services, and integration with Grants.gov and EHBs.  
**Keywords:** Fillable Forms, Aspose, MCP Server, Agentic AI, Azure OpenAI, Grants.gov, EHBs, QIF-DNDD, NOFO, Data Extraction  
**Author:** DME/O&M Teams  
**Date:** February 24, 2026  
**Version:** 1.0

---

## End of Specification

This specification provides all necessary details to create a Section 508 compliant Visio architecture diagram. The diagram should clearly show the MCP server as the central hub hosting Aspose tools, with Agentic AI orchestrating the entire process through MCP API calls.
