# SOQL & SOSL Query Patterns

## Overview
Salesforce Object Query Language (SOQL) and Salesforce Object Search Language (SOSL) patterns, best practices, and common pitfalls to avoid governor limits and optimize performance.

## When to Use

- **SOQL**: Single object queries, relationship queries, precise filtering
- **SOSL**: Multi-object text searches, fuzzy matching, searching across multiple fields

## SOQL Best Practices

### 1. Always Use Selective Queries

```apex
// ✅ GOOD - Uses indexed fields in WHERE clause
List<Account> accounts = [
    SELECT Id, Name 
    FROM Account 
    WHERE Id = :accountId
    LIMIT 1
];

// ✅ GOOD - External ID fields are indexed
List<Project__c> projects = [
    SELECT Id, Name 
    FROM Project__c 
    WHERE External_ID__c = :externalId
];

// ❌ BAD - No WHERE clause, queries all records
List<Account> allAccounts = [SELECT Id FROM Account];
```

### 2. Use LIMIT to Prevent Governor Limit Issues

```apex
// ✅ GOOD - Always use LIMIT for testing/development
List<Project__c> projects = [
    SELECT Id, Name 
    FROM Project__c 
    WHERE Status__c = 'Active'
    LIMIT 200
];

// Governor Limits:
// - SOQL queries: 100 per transaction
// - Query rows: 50,000 per transaction
// - Heap size: 6 MB (synchronous), 12 MB (asynchronous)
```

### 3. Use Bind Variables for Dynamic Queries

```apex
// ✅ GOOD - Prevents SOQL injection
String status = 'Active';
List<Project__c> projects = [
    SELECT Id, Name 
    FROM Project__c 
    WHERE Status__c = :status
];

// ❌ BAD - SOQL injection vulnerability
String query = 'SELECT Id FROM Project__c WHERE Status__c = \'' + status + '\'';
List<Project__c> projects = Database.query(query);
```

### 4. Relationship Queries

```apex
// Parent-to-Child (1-to-Many)
List<Account> accounts = [
    SELECT Id, Name,
        (SELECT Id, Name FROM Contacts)
    FROM Account
    WHERE Id = :accountId
];

// Child-to-Parent (Many-to-1)
List<Contact> contacts = [
    SELECT Id, Name, Account.Name, Account.Industry
    FROM Contact
    WHERE AccountId = :accountId
];

// Multi-level relationships (up to 5 levels)
List<Contact> contacts = [
    SELECT Id, Name, 
           Account.Owner.Name,
           Account.Owner.Manager.Name
    FROM Contact
];
```

### 5. Aggregate Queries

```apex
// COUNT, SUM, AVG, MIN, MAX
AggregateResult[] results = [
    SELECT COUNT(Id) totalProjects,
           SUM(Budget__c) totalBudget,
           AVG(Budget__c) avgBudget,
           Status__c
    FROM Project__c
    GROUP BY Status__c
];

for (AggregateResult ar : results) {
    Integer count = (Integer)ar.get('totalProjects');
    Decimal total = (Decimal)ar.get('totalBudget');
    String status = (String)ar.get('Status__c');
}
```

### 6. Versioning Query Pattern

```apex
// Get latest version only
List<Project__c> latest = [
    SELECT Id, Name, Version__c
    FROM Project__c
    WHERE Lifecycle_Instance_Id__c = :lifecycleId
    AND Is_Latest__c = true
];

// Get all versions for comparison
List<Project__c> allVersions = [
    SELECT Id, Name, Version__c, Is_Draft__c, Is_Latest__c
    FROM Project__c
    WHERE Context_Instance_Id__c = :contextId
    ORDER BY Version__c DESC
];

// Get draft or create new
List<Project__c> drafts = [
    SELECT Id, Name, Version__c
    FROM Project__c
    WHERE Context_Instance_Id__c = :contextId
    AND Is_Draft__c = true
    LIMIT 1
];
```

### 7. Date Filtering

```apex
// Date literals
List<Project__c> recent = [
    SELECT Id, Name, CreatedDate
    FROM Project__c
    WHERE CreatedDate = LAST_N_DAYS:30
];

// Common date literals:
// - TODAY, YESTERDAY, TOMORROW
// - LAST_WEEK, THIS_WEEK, NEXT_WEEK
// - LAST_MONTH, THIS_MONTH, NEXT_MONTH
// - LAST_N_DAYS:n, NEXT_N_DAYS:n
// - THIS_YEAR, LAST_YEAR

// Specific date range
List<Project__c> range = [
    SELECT Id, Name
    FROM Project__c
    WHERE CreatedDate >= :startDate
    AND CreatedDate <= :endDate
];
```

### 8. NULL Handling

```apex
// Check for NULL
List<Project__c> withoutBudget = [
    SELECT Id, Name
    FROM Project__c
    WHERE Budget__c = null
];

// Check for NOT NULL
List<Project__c> withBudget = [
    SELECT Id, Name
    FROM Project__c
    WHERE Budget__c != null
];
```

### 9. IN and NOT IN Clauses

```apex
// IN clause
Set<Id> accountIds = new Set<Id>{id1, id2, id3};
List<Contact> contacts = [
    SELECT Id, Name
    FROM Contact
    WHERE AccountId IN :accountIds
];

// NOT IN clause
List<String> excludedStatuses = new List<String>{'Cancelled', 'Deleted'};
List<Project__c> active = [
    SELECT Id, Name
    FROM Project__c
    WHERE Status__c NOT IN :excludedStatuses
];
```

### 10. SOQL For Loops (Large Data Sets)

```apex
// ✅ GOOD - Processes records in batches of 200
for (List<Project__c> projects : [
    SELECT Id, Name, Status__c
    FROM Project__c
    WHERE Status__c = 'Active'
]) {
    // Process batch of up to 200 records
    for (Project__c proj : projects) {
        // Process individual record
    }
}

// Prevents heap size issues with large result sets
```

## SOSL Best Practices

### 1. Basic SOSL Search

```apex
// Search across multiple objects
List<List<SObject>> searchResults = [
    FIND 'Health Center'
    IN ALL FIELDS
    RETURNING Account(Id, Name), Contact(Id, Name), Project__c(Id, Name)
];

List<Account> accounts = (List<Account>)searchResults[0];
List<Contact> contacts = (List<Contact>)searchResults[1];
List<Project__c> projects = (List<Project__c>)searchResults[2];
```

### 2. Field-Specific Search

```apex
// Search in specific fields
List<List<SObject>> results = [
    FIND 'john*'
    IN NAME FIELDS
    RETURNING Contact(Id, Name, Email)
];

// Search scopes:
// - ALL FIELDS
// - NAME FIELDS
// - EMAIL FIELDS
// - PHONE FIELDS
```

### 3. SOSL with Filters

```apex
List<List<SObject>> results = [
    FIND 'Health*'
    IN ALL FIELDS
    RETURNING Account(Id, Name WHERE Industry = 'Healthcare'),
              Contact(Id, Name WHERE AccountId IN :accountIds)
];
```

### 4. SOSL Wildcards

```apex
// * = zero or more characters
// ? = exactly one character

FIND 'john*'   // john, johnson, johnathan
FIND 'jo?n'    // john, joan (but not jon)
FIND '*smith'  // smith, blacksmith
```

## Performance Optimization

### 1. Query Selectivity

```apex
// ✅ GOOD - Selective query (uses index)
WHERE Id = :recordId
WHERE External_ID__c = :externalId
WHERE RecordTypeId = :recordTypeId
WHERE OwnerId = :userId

// ⚠️ LESS SELECTIVE - May not use index
WHERE Name LIKE '%test%'
WHERE Custom_Field__c = 'value'  // If not indexed
```

### 2. Index Usage

Fields that are automatically indexed:
- Id
- Name
- OwnerId
- RecordTypeId
- CreatedDate
- SystemModstamp
- External ID fields
- Unique fields
- Master-Detail fields

### 3. Query Plan Tool

```apex
// Use Query Plan in Developer Console to check if query uses index
// Setup → Developer Console → Query Editor → Query Plan
```

### 4. Avoid Query in Loops

```apex
// ❌ BAD - Query inside loop
for (Account acc : accounts) {
    List<Contact> contacts = [
        SELECT Id FROM Contact WHERE AccountId = :acc.Id
    ];
}

// ✅ GOOD - Single query with IN clause
Set<Id> accountIds = new Set<Id>();
for (Account acc : accounts) {
    accountIds.add(acc.Id);
}
List<Contact> contacts = [
    SELECT Id, AccountId FROM Contact WHERE AccountId IN :accountIds
];

// Group contacts by account
Map<Id, List<Contact>> contactsByAccount = new Map<Id, List<Contact>>();
for (Contact con : contacts) {
    if (!contactsByAccount.containsKey(con.AccountId)) {
        contactsByAccount.put(con.AccountId, new List<Contact>());
    }
    contactsByAccount.get(con.AccountId).add(con);
}
```

## Common Patterns

### Pattern 1: Get or Create Draft

```apex
public SObject getOrCreateDraft(String contextId) {
    // 1. Try to get existing draft
    List<Project__c> drafts = [
        SELECT Id, Name, Version__c
        FROM Project__c
        WHERE Context_Instance_Id__c = :contextId
        AND Is_Draft__c = true
        LIMIT 1
    ];
    
    if (!drafts.isEmpty()) {
        return drafts[0];
    }
    
    // 2. Clone latest version to create draft
    List<Project__c> latest = [
        SELECT Id, Name, Version__c
        FROM Project__c
        WHERE Context_Instance_Id__c = :contextId
        AND Is_Latest__c = true
        LIMIT 1
    ];
    
    if (!latest.isEmpty()) {
        Project__c draft = latest[0].clone(false, false, false, false);
        draft.Is_Draft__c = true;
        draft.Is_Latest__c = false;
        draft.Version__c = latest[0].Version__c + 1;
        insert draft;
        return draft;
    }
    
    // 3. Create fresh draft if no records exist
    Project__c newDraft = new Project__c(
        Context_Instance_Id__c = contextId,
        Is_Draft__c = true,
        Is_Latest__c = true,
        Version__c = 1
    );
    insert newDraft;
    return newDraft;
}
```

### Pattern 2: Bulk Query with Relationships

```apex
public Map<Id, Account> getAccountsWithContacts(Set<Id> accountIds) {
    Map<Id, Account> accountMap = new Map<Id, Account>([
        SELECT Id, Name,
            (SELECT Id, Name, Email FROM Contacts)
        FROM Account
        WHERE Id IN :accountIds
    ]);
    return accountMap;
}
```

### Pattern 3: Dynamic SOQL

```apex
public List<SObject> dynamicQuery(String objectName, Set<String> fields, String whereClause) {
    String query = 'SELECT ' + String.join(new List<String>(fields), ', ') +
                   ' FROM ' + objectName;
    
    if (String.isNotBlank(whereClause)) {
        query += ' WHERE ' + whereClause;
    }
    
    query += ' LIMIT 200';
    
    return Database.query(query);
}
```

## Testing Queries

### 1. Test with Large Data Sets

```apex
@isTest
static void testQueryWithLargeDataSet() {
    // Create 200+ records to test SOQL for loop
    List<Project__c> projects = new List<Project__c>();
    for (Integer i = 0; i < 250; i++) {
        projects.add(new Project__c(Name = 'Test ' + i));
    }
    insert projects;
    
    Test.startTest();
    Integer count = 0;
    for (List<Project__c> batch : [SELECT Id FROM Project__c]) {
        count += batch.size();
    }
    Test.stopTest();
    
    System.assertEquals(250, count);
}
```

### 2. Test Governor Limits

```apex
@isTest
static void testGovernorLimits() {
    Test.startTest();
    
    // Your code here
    
    Test.stopTest();
    
    // Verify limits not exceeded
    System.assert(Limits.getQueries() < Limits.getLimitQueries());
    System.assert(Limits.getQueryRows() < Limits.getLimitQueryRows());
}
```

## Common Errors and Solutions

### Error: "Non-selective query against large object"

**Solution:** Add indexed fields to WHERE clause or request a custom index

```apex
// ❌ BAD
SELECT Id FROM Account WHERE Custom_Field__c = 'value'

// ✅ GOOD - Add indexed field
SELECT Id FROM Account 
WHERE Custom_Field__c = 'value' 
AND CreatedDate = LAST_N_DAYS:30
```

### Error: "Too many SOQL queries: 101"

**Solution:** Bulkify code, avoid queries in loops

```apex
// Use SOQL for loops for large data sets
// Move queries outside loops
// Use collections to batch operations
```

### Error: "Aggregate query has too many rows for direct assignment"

**Solution:** Use LIMIT or more selective WHERE clause

```apex
AggregateResult[] results = [
    SELECT COUNT(Id) total, Status__c
    FROM Project__c
    GROUP BY Status__c
    LIMIT 200
];
```

## Quick Reference

### Query Limits
- SOQL queries per transaction: 100
- SOQL query rows: 50,000
- SOSL queries per transaction: 20
- Records per SOQL query: 50,000
- Records per DML statement: 10,000

### Best Practices Checklist
- ✅ Use WHERE clause with indexed fields
- ✅ Always use LIMIT (especially in testing)
- ✅ Use bind variables for dynamic values
- ✅ Avoid queries in loops
- ✅ Use SOQL for loops for large data sets
- ✅ Query only needed fields
- ✅ Use relationship queries instead of multiple queries
- ✅ Test with large data volumes

## Related Skills
- `skill_apex_testing.md` - Testing SOQL queries
- `skill_salesforce_development.md` - General Salesforce patterns
- `skill_database_design.md` - Data modeling
