# Skills Organization Diagram

Complete visual map of all 63 AI skills organized by category.

---

## Skills Overview Diagram

```mermaid
flowchart TB
    Root[06_Skills - 63 AI Skills - 6 Categories]
    
    Root --> Automation[AUTOMATION - 7 Skills - Daily Workflows]
    Root --> Integrations[INTEGRATIONS - 5 Skills - API & Services]
    Root --> Development[DEVELOPMENT - 15 Skills - Dev Tools]
    Root --> Documentation[DOCUMENTATION - 8 Skills - Templates & Diagrams]
    Root --> System[SYSTEM - 7 Skills - Core Configuration]
    
    %% Automation Skills
    Automation --> A1[daily_planning - Kanban board generation]
    Automation --> A2[email_processing - Automated email handling]
    Automation --> A3[file_organization - PARA method filing]
    Automation --> A4[browser_automation - Playwright web automation]
    Automation --> A5[powershell_automation - PowerShell scripting]
    Automation --> A6[torrent_downloads - Torrent management]
    Automation --> A7[archive_parts_recovery - Archive recovery]
    
    %% Integration Skills
    Integrations --> I1[amplenote_api - Amplenote integration]
    Integrations --> I2[amplenote_relay_systems - Advanced relay configs]
    Integrations --> I3[gmail_automation - Gmail API setup]
    Integrations --> I4[todoist_api - Task management API]
    Integrations --> I5[keepass_integration - Password manager]
    
    %% Development Skills
    Development --> D1[salesforce_development - Apex & LWC]
    Development --> D2[salesforce_fls_automation - Field-level security]
    Development --> D3[salesforce_developer_activity_report - Activity tracking]
    Development --> D4[git_version_control - Git workflows]
    Development --> D5[azure_devops_automation - ADO work items]
    Development --> D6[mcp_builder - Build MCP servers]
    Development --> D7[github_pull_requests - PR workflow]
    Development --> D8[gitflow_workflow - GitFlow branching]
    Development --> D9[splunk_monitoring - Splunk queries]
    Development --> D10[soql_sosl - SOQL/SOSL queries]
    Development --> D11[apex_testing - Test patterns]
    Development --> D12[salesforce_deployment - Deployment & cache]
    Development --> D13[lwc_development - LWC components]
    Development --> D14[salesforce_rest_api - OAuth & REST API]
    Development --> D15[sfsync_script - Deployment script]
    
    %% Documentation Skills
    Documentation --> Doc1[mermaid_diagrams - Diagram syntax]
    Documentation --> Doc2[visio_via_mermaid - Mermaid to Visio]
    Documentation --> Doc3[visio_section_508 - Accessible diagrams]
    Documentation --> Doc4[visio_grant_lifecycle_diagram - Grant diagrams]
    Documentation --> Doc5[teg_discussion_templates - TEG templates]
    Documentation --> Doc6[feature_documentation - Doc standards]
    Documentation --> Doc7[qif_dndd_fillable_forms_visio_spec - QIF forms]
    Documentation --> Doc8[teg_discussion_template_alt - Alt TEG template]
    
    %% System Skills
    System --> S1[routing_rules - System routing]
    System --> S2[environments_credentials - Credential management]
    System --> S3[cascade_workflow - AI workflow patterns]
    System --> S4[process_new - Process new items]
    System --> S5[agent_handoff - Agent protocols]
    System --> S6[mcp_server_setup - MCP configuration]
    System --> S7[organizing_skills - Skill organization]
    
    %% Styling
    style Root fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style Automation fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Integrations fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style Development fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style Documentation fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    style System fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    
    style A1 fill:#ffe0b2,stroke:#e65100
    style A2 fill:#ffe0b2,stroke:#e65100
    style A3 fill:#ffe0b2,stroke:#e65100
    style A4 fill:#ffe0b2,stroke:#e65100
    style A5 fill:#ffe0b2,stroke:#e65100
    style A6 fill:#ffe0b2,stroke:#e65100
    style A7 fill:#ffe0b2,stroke:#e65100
    
    style I1 fill:#f3e5f5,stroke:#6a1b9a
    style I2 fill:#f3e5f5,stroke:#6a1b9a
    style I3 fill:#f3e5f5,stroke:#6a1b9a
    style I4 fill:#f3e5f5,stroke:#6a1b9a
    style I5 fill:#f3e5f5,stroke:#6a1b9a
    
    style D1 fill:#c8e6c9,stroke:#1b5e20
    style D2 fill:#c8e6c9,stroke:#1b5e20
    style D3 fill:#c8e6c9,stroke:#1b5e20
    style D4 fill:#c8e6c9,stroke:#1b5e20
    style D5 fill:#c8e6c9,stroke:#1b5e20
    style D6 fill:#c8e6c9,stroke:#1b5e20
    style D7 fill:#c8e6c9,stroke:#1b5e20
    style D8 fill:#c8e6c9,stroke:#1b5e20
    style D9 fill:#c8e6c9,stroke:#1b5e20
    style D10 fill:#c8e6c9,stroke:#1b5e20
    style D11 fill:#c8e6c9,stroke:#1b5e20
    style D12 fill:#c8e6c9,stroke:#1b5e20
    style D13 fill:#c8e6c9,stroke:#1b5e20
    style D14 fill:#c8e6c9,stroke:#1b5e20
    style D15 fill:#c8e6c9,stroke:#1b5e20
    
    style Doc1 fill:#f8bbd0,stroke:#880e4f
    style Doc2 fill:#f8bbd0,stroke:#880e4f
    style Doc3 fill:#f8bbd0,stroke:#880e4f
    style Doc4 fill:#f8bbd0,stroke:#880e4f
    style Doc5 fill:#f8bbd0,stroke:#880e4f
    style Doc6 fill:#f8bbd0,stroke:#880e4f
    style Doc7 fill:#f8bbd0,stroke:#880e4f
    style Doc8 fill:#f8bbd0,stroke:#880e4f
    
    style S1 fill:#fff59d,stroke:#f57f17
    style S2 fill:#fff59d,stroke:#f57f17
    style S3 fill:#fff59d,stroke:#f57f17
    style S4 fill:#fff59d,stroke:#f57f17
    style S5 fill:#fff59d,stroke:#f57f17
    style S6 fill:#fff59d,stroke:#f57f17
    style S7 fill:#fff59d,stroke:#f57f17
```

---

## Skill Relationships Diagram

```mermaid
flowchart LR
    %% Core Daily Workflow
    DP[daily_planning]
    EP[email_processing]
    FO[file_organization]
    
    %% Integrations Used
    AMP[amplenote_api]
    TODO[todoist_api]
    GMAIL[gmail_automation]
    
    %% System Skills
    RR[routing_rules]
    EC[environments_credentials]
    PN[process_new]
    
    %% Workflow Connections
    PN --> DP
    PN --> EP
    PN --> FO
    
    DP --> AMP
    DP --> TODO
    EP --> GMAIL
    EP --> AMP
    EP --> TODO
    
    RR --> FO
    EC --> AMP
    EC --> TODO
    EC --> GMAIL
    
    %% Styling
    style DP fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style EP fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style FO fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style PN fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#fff
    
    style AMP fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style TODO fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style GMAIL fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    
    style RR fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style EC fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
```

---

## Development Skills Workflow

```mermaid
flowchart TD
    %% Development Workflow
    SF[salesforce_development]
    GIT[git_version_control]
    ADO[azure_devops_automation]
    FLS[salesforce_fls_automation]
    ACT[salesforce_developer_activity_report]
    
    %% Workflow
    ADO --> SF
    SF --> GIT
    GIT --> SF
    SF --> FLS
    SF --> ACT
    
    %% Supporting
    EC[environments_credentials]
    EC --> SF
    EC --> ADO
    
    %% Styling
    style SF fill:#c8e6c9,stroke:#1b5e20,stroke-width:3px
    style GIT fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style ADO fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style FLS fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style ACT fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style EC fill:#fff59d,stroke:#f57f17,stroke-width:2px
```

---

## Documentation Skills Workflow

```mermaid
flowchart LR
    %% Documentation Creation Flow
    MD[mermaid_diagrams]
    VVM[visio_via_mermaid]
    V508[visio_section_508]
    
    %% Templates
    TEG[teg_discussion_templates]
    FD[feature_documentation]
    
    %% Workflow
    MD --> VVM
    VVM --> V508
    
    TEG --> FD
    MD --> FD
    
    %% Styling
    style MD fill:#f48fb1,stroke:#880e4f,stroke-width:3px
    style VVM fill:#f48fb1,stroke:#880e4f,stroke-width:3px
    style V508 fill:#f48fb1,stroke:#880e4f,stroke-width:2px
    style TEG fill:#f8bbd0,stroke:#880e4f,stroke-width:2px
    style FD fill:#f8bbd0,stroke:#880e4f,stroke-width:2px
```

---

## System Configuration Flow

```mermaid
flowchart TD
    %% System Setup
    EC[environments_credentials]
    RR[routing_rules]
    MCP[mcp_server_setup]
    CW[cascade_workflow]
    AH[agent_handoff]
    OS[organizing_skills]
    
    %% Dependencies
    EC --> MCP
    RR --> CW
    CW --> AH
    OS --> CW
    
    %% All depend on credentials
    EC --> RR
    EC --> CW
    
    %% Styling
    style EC fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style RR fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style MCP fill:#fff59d,stroke:#f57f17,stroke-width:2px
    style CW fill:#fff59d,stroke:#f57f17,stroke-width:2px
    style AH fill:#fff59d,stroke:#f57f17,stroke-width:2px
    style OS fill:#fff59d,stroke:#f57f17,stroke-width:2px
```

---

## Complete Skill Dependencies

```mermaid
graph TB
    %% Legend
    subgraph Legend
        L1[⭐ Most Used]
        L2[🔧 Setup Required]
        L3[📦 Supporting]
    end
    
    %% Core Skills
    subgraph "Core Daily Workflow"
        DP[daily_planning ⭐]
        EP[email_processing ⭐]
        FO[file_organization ⭐]
        PN[process_new ⭐]
    end
    
    %% Setup Skills
    subgraph "Setup & Configuration 🔧"
        EC[environments_credentials]
        RR[routing_rules]
        MCP[mcp_server_setup]
    end
    
    %% Integration Layer
    subgraph "Integration APIs"
        AMP[amplenote_api]
        TODO[todoist_api]
        GMAIL[gmail_automation]
        KEEP[keepass_integration]
    end
    
    %% Development Tools
    subgraph "Development Tools"
        SF[salesforce_development]
        GIT[git_version_control]
        ADO[azure_devops_automation]
    end
    
    %% Documentation Tools
    subgraph "Documentation & Diagrams"
        MD[mermaid_diagrams]
        VVM[visio_via_mermaid]
        V508[visio_section_508]
    end
    
    %% System Management
    subgraph "System Management"
        CW[cascade_workflow]
        AH[agent_handoff]
        OS[organizing_skills]
    end
    
    %% Dependencies
    EC --> AMP
    EC --> TODO
    EC --> GMAIL
    EC --> SF
    EC --> ADO
    
    RR --> FO
    RR --> PN
    
    MCP --> PN
    
    PN --> DP
    PN --> EP
    PN --> FO
    
    DP --> AMP
    DP --> TODO
    EP --> GMAIL
    EP --> AMP
    
    SF --> GIT
    ADO --> SF
    
    MD --> VVM
    VVM --> V508
    
    CW --> AH
    OS --> CW
    
    %% Styling
    style DP fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style EP fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style FO fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style PN fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#fff
    
    style EC fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#fff
    style RR fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#fff
    style MCP fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#fff
```

---

## Skills by Frequency of Use

```mermaid
flowchart LR
    subgraph "Daily Use"
        D1[daily_planning]
        D2[file_organization]
        D3[routing_rules]
    end
    
    subgraph "Weekly Use"
        W1[email_processing]
    end
    
    subgraph "As-Needed"
        AN1[salesforce_development]
        AN2[git_version_control]
        AN3[browser_automation]
        AN4[mermaid_diagrams]
        AN5[amplenote_api]
        AN6[todoist_api]
        AN7[And 22 more...]
    end
    
    style D1 fill:#2e7d32,stroke:#ffffff,stroke-width:3px,color:#fff
    style D2 fill:#2e7d32,stroke:#ffffff,stroke-width:3px,color:#fff
    style D3 fill:#2e7d32,stroke:#ffffff,stroke-width:3px,color:#fff
    
    style W1 fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#fff
    
    style AN1 fill:#757575,stroke:#ffffff,stroke-width:2px,color:#fff
    style AN2 fill:#757575,stroke:#ffffff,stroke-width:2px,color:#fff
    style AN3 fill:#757575,stroke:#ffffff,stroke-width:2px,color:#fff
    style AN4 fill:#757575,stroke:#ffffff,stroke-width:2px,color:#fff
    style AN5 fill:#757575,stroke:#ffffff,stroke-width:2px,color:#fff
    style AN6 fill:#757575,stroke:#ffffff,stroke-width:2px,color:#fff
    style AN7 fill:#757575,stroke:#ffffff,stroke-width:2px,color:#fff
```

---

**Last Updated:** March 2, 2026  
**Total Skills:** 63  
**Location:** `G:\My Drive\06_Skills\SKILLS_DIAGRAM.md`
