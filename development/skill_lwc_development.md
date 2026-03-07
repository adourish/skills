# Lightning Web Component (LWC) Development

## Overview
Patterns and best practices for developing Lightning Web Components in Salesforce, including component communication, data access, event handling, and deployment.

## Core LWC Patterns

### 1. Basic Component Structure

```javascript
// myComponent.js
import { LightningElement, api, track, wire } from 'lwc';

export default class MyComponent extends LightningElement {
    // Public properties (accessible from parent)
    @api recordId;
    @api objectApiName;
    
    // Tracked properties (reactive)
    @track items = [];
    
    // Private properties (not reactive)
    isLoading = false;
    error;
    
    // Lifecycle hooks
    connectedCallback() {
        // Component inserted into DOM
        this.loadData();
    }
    
    disconnectedCallback() {
        // Component removed from DOM
    }
    
    renderedCallback() {
        // After component renders
    }
    
    // Event handlers
    handleClick(event) {
        // Handle user interaction
    }
}
```

```html
<!-- myComponent.html -->
<template>
    <lightning-card title="My Component">
        <template if:true={isLoading}>
            <lightning-spinner></lightning-spinner>
        </template>
        
        <template if:false={isLoading}>
            <template if:true={items}>
                <template for:each={items} for:item="item">
                    <div key={item.id}>{item.name}</div>
                </template>
            </template>
        </template>
        
        <template if:true={error}>
            <div class="slds-text-color_error">{error}</div>
        </template>
    </lightning-card>
</template>
```

### 2. Data Access with Wire Service

```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import getProjects from '@salesforce/apex/ProjectController.getProjects';

export default class MyComponent extends LightningElement {
    @api recordId;
    
    // Wire to Apex method
    @wire(getProjects, { lifecycleId: '$recordId' })
    wiredProjects({ error, data }) {
        if (data) {
            this.projects = data;
            this.error = undefined;
        } else if (error) {
            this.error = error;
            this.projects = undefined;
        }
    }
    
    // Wire to UI API
    @wire(getRecord, { recordId: '$recordId', fields: ['Account.Name', 'Account.Industry'] })
    account;
    
    get accountName() {
        return this.account.data?.fields.Name.value;
    }
}
```

### 3. Imperative Apex Calls

```javascript
import { LightningElement } from 'lwc';
import saveProject from '@salesforce/apex/ProjectController.saveProject';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class MyComponent extends LightningElement {
    async handleSave() {
        try {
            const result = await saveProject({ 
                projectId: this.projectId,
                data: this.formData 
            });
            
            this.showToast('Success', 'Project saved successfully', 'success');
            this.dispatchEvent(new CustomEvent('save', { detail: result }));
            
        } catch (error) {
            this.showToast('Error', error.body.message, 'error');
        }
    }
    
    showToast(title, message, variant) {
        this.dispatchEvent(new ShowToastEvent({ title, message, variant }));
    }
}
```

## Component Communication

### Pattern 1: Parent to Child (@api)

```javascript
// Parent component
<template>
    <c-child-component 
        record-id={recordId}
        title="My Title"
        onaction={handleChildAction}>
    </c-child-component>
</template>

// Child component
import { LightningElement, api } from 'lwc';

export default class ChildComponent extends LightningElement {
    @api recordId;
    @api title;
    
    handleClick() {
        // Fire event to parent
        this.dispatchEvent(new CustomEvent('action', {
            detail: { id: this.recordId }
        }));
    }
}
```

### Pattern 2: Child to Parent (Custom Events)

```javascript
// Child fires event
handleSave() {
    const event = new CustomEvent('save', {
        detail: {
            recordId: this.recordId,
            data: this.formData
        },
        bubbles: true,
        composed: true  // Cross shadow DOM boundary
    });
    this.dispatchEvent(event);
}

// Parent handles event
<template>
    <c-child-component onsave={handleSave}></c-child-component>
</template>

handleSave(event) {
    const { recordId, data } = event.detail;
    // Process save
}
```

### Pattern 3: Sibling Communication (PubSub or LMS)

```javascript
// Using Lightning Message Service
import { LightningElement, wire } from 'lwc';
import { publish, subscribe, MessageContext } from 'lightning/messageService';
import MY_CHANNEL from '@salesforce/messageChannel/MyChannel__c';

export default class Publisher extends LightningElement {
    @wire(MessageContext)
    messageContext;
    
    publishMessage() {
        const message = { recordId: this.recordId };
        publish(this.messageContext, MY_CHANNEL, message);
    }
}

export default class Subscriber extends LightningElement {
    @wire(MessageContext)
    messageContext;
    
    subscription = null;
    
    connectedCallback() {
        this.subscription = subscribe(
            this.messageContext,
            MY_CHANNEL,
            (message) => this.handleMessage(message)
        );
    }
    
    handleMessage(message) {
        this.recordId = message.recordId;
    }
}
```

## Common Patterns

### Pattern 1: Table with Modal (Triad Pattern)

```javascript
// Table Component
import { LightningElement, api } from 'lwc';

export default class ProjectsTable extends LightningElement {
    @api projects;
    
    columns = [
        { label: 'Title', fieldName: 'title' },
        { label: 'Status', fieldName: 'status' },
        { type: 'action', typeAttributes: { rowActions: this.getRowActions } }
    ];
    
    handleRowAction(event) {
        const action = event.detail.action;
        const row = event.detail.row;
        
        if (action.name === 'edit') {
            this.dispatchEvent(new CustomEvent('edit', { 
                detail: { record: row } 
            }));
        }
    }
    
    getRowActions(row, doneCallback) {
        const actions = [
            { label: 'Edit', name: 'edit' },
            { label: 'Delete', name: 'delete' }
        ];
        doneCallback(actions);
    }
}

// Modal Component
import { LightningElement, api } from 'lwc';

export default class ProjectsModal extends LightningElement {
    @api record;
    @api isOpen = false;
    
    handleClose() {
        this.dispatchEvent(new CustomEvent('close'));
    }
    
    handleSave() {
        // Save logic
        this.dispatchEvent(new CustomEvent('save', { 
            detail: this.formData 
        }));
    }
}

// Container Component
<template>
    <c-projects-table 
        projects={projects}
        onedit={handleEdit}>
    </c-projects-table>
    
    <c-projects-modal
        record={selectedRecord}
        is-open={isModalOpen}
        onclose={handleModalClose}
        onsave={handleSave}>
    </c-projects-modal>
</template>
```

### Pattern 2: Form Handling

```javascript
import { LightningElement, api } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class ProjectForm extends LightningElement {
    @api recordId;
    formData = {};
    
    handleFieldChange(event) {
        const field = event.target.name;
        const value = event.target.value;
        this.formData[field] = value;
    }
    
    async handleSubmit(event) {
        event.preventDefault();
        
        // Validate
        if (!this.validateForm()) {
            return;
        }
        
        // Submit
        try {
            const result = await saveRecord({ data: this.formData });
            this.showToast('Success', 'Record saved', 'success');
            this.dispatchEvent(new CustomEvent('success', { detail: result }));
        } catch (error) {
            this.showToast('Error', error.body.message, 'error');
        }
    }
    
    validateForm() {
        const inputs = this.template.querySelectorAll('lightning-input');
        return Array.from(inputs).every(input => input.reportValidity());
    }
}
```

### Pattern 3: Conditional Rendering

```html
<template>
    <!-- if:true / if:false -->
    <template if:true={isLoading}>
        <lightning-spinner></lightning-spinner>
    </template>
    
    <template if:false={isLoading}>
        <div>Content loaded</div>
    </template>
    
    <!-- for:each -->
    <template for:each={items} for:item="item">
        <div key={item.id}>{item.name}</div>
    </template>
    
    <!-- iterator -->
    <template iterator:it={items}>
        <div key={it.value.id}>
            <template if:true={it.first}>First item</template>
            {it.value.name}
            <template if:true={it.last}>Last item</template>
        </div>
    </template>
</template>
```

### Pattern 4: Getters for Computed Properties

```javascript
export default class MyComponent extends LightningElement {
    firstName = 'John';
    lastName = 'Doe';
    
    // Computed property
    get fullName() {
        return `${this.firstName} ${this.lastName}`;
    }
    
    // Conditional class
    get cardClass() {
        return this.isActive ? 'slds-card active' : 'slds-card';
    }
    
    // Formatted data
    get formattedDate() {
        return this.date ? new Date(this.date).toLocaleDateString() : '';
    }
}
```

## Best Practices

### 1. Use @track Sparingly

```javascript
// ❌ BAD - Unnecessary @track
import { track } from 'lwc';
@track name = 'John';

// ✅ GOOD - Only track complex objects
@track formData = { name: '', email: '' };

// ✅ BETTER - Use reactive properties
name = 'John';  // Automatically reactive for primitives
```

### 2. Avoid DOM Manipulation

```javascript
// ❌ BAD - Direct DOM manipulation
this.template.querySelector('.my-div').style.display = 'none';

// ✅ GOOD - Use conditional rendering
<template if:true={isVisible}>
    <div class="my-div"></div>
</template>
```

### 3. Use Lightning Base Components

```html
<!-- ✅ GOOD - Use base components -->
<lightning-input label="Name" value={name}></lightning-input>
<lightning-button label="Save" onclick={handleSave}></lightning-button>
<lightning-datatable data={data} columns={columns}></lightning-datatable>

<!-- ❌ BAD - Custom HTML inputs -->
<input type="text" value={name} />
<button onclick={handleSave}>Save</button>
```

### 4. Handle Errors Properly

```javascript
async loadData() {
    try {
        this.isLoading = true;
        this.data = await getData();
        this.error = undefined;
    } catch (error) {
        this.error = this.reduceErrors(error);
        this.data = undefined;
    } finally {
        this.isLoading = false;
    }
}

reduceErrors(error) {
    if (Array.isArray(error.body)) {
        return error.body.map(e => e.message).join(', ');
    } else if (error.body?.message) {
        return error.body.message;
    }
    return 'Unknown error';
}
```

## Deployment Considerations

### 1. Always Deploy Parent Components

```powershell
# ❌ WRONG - Only child
.\sfsync.ps1 -type lwc -pattern "childComponent" -action push -org myorg

# ✅ CORRECT - Child and parents
.\sfsync.ps1 -type lwc -pattern "*Component" -action push -org myorg
```

### 2. Component Dependencies

When deploying LWC that uses:
- Apex classes → Deploy Apex first
- Custom objects → Deploy objects first
- Other LWC → Deploy all related components

### 3. Cache Invalidation

Deploy parent components to invalidate Salesforce cache:

```powershell
# Component hierarchy:
# containerComponent
#   └─> parentComponent
#       └─> childComponent

# Modified childComponent, deploy all three:
.\sfsync.ps1 -type lwc -pattern "*Component" -action push -org myorg
```

## Testing LWC

### 1. Jest Unit Tests

```javascript
// myComponent.test.js
import { createElement } from 'lwc';
import MyComponent from 'c/myComponent';

describe('c-my-component', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
    });
    
    it('displays title', () => {
        const element = createElement('c-my-component', {
            is: MyComponent
        });
        element.title = 'Test Title';
        document.body.appendChild(element);
        
        const title = element.shadowRoot.querySelector('h1');
        expect(title.textContent).toBe('Test Title');
    });
    
    it('handles button click', () => {
        const element = createElement('c-my-component', {
            is: MyComponent
        });
        document.body.appendChild(element);
        
        const handler = jest.fn();
        element.addEventListener('action', handler);
        
        const button = element.shadowRoot.querySelector('button');
        button.click();
        
        expect(handler).toHaveBeenCalled();
    });
});
```

## Quick Reference

### Component Decorators
- `@api` - Public property/method
- `@track` - Track complex object changes
- `@wire` - Wire to data service

### Lifecycle Hooks
- `constructor()` - Component created
- `connectedCallback()` - Inserted into DOM
- `renderedCallback()` - After render
- `disconnectedCallback()` - Removed from DOM
- `errorCallback()` - Error in component

### Common Imports
```javascript
import { LightningElement, api, track, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { NavigationMixin } from 'lightning/navigation';
import { refreshApex } from '@salesforce/apex';
```

## Related Skills
- `skill_salesforce_deployment.md` - LWC deployment patterns
- `skill_salesforce_development.md` - General Salesforce patterns
- `skill_apex_testing.md` - Testing Apex called by LWC
