# Apex Testing Patterns

## Overview
Comprehensive patterns for writing effective Apex test classes, achieving code coverage, and ensuring quality in Salesforce development.

## Core Principles

### 1. Test Class Structure

```apex
@isTest
private class MyServiceTest {
    
    // Test data setup (runs once per class)
    @TestSetup
    static void setupTestData() {
        // Create common test data
        Account acc = new Account(Name = 'Test Account');
        insert acc;
    }
    
    // Test method naming: testMethodName_scenario_expectedResult
    @isTest
    static void testGetAccount_validId_returnsAccount() {
        // Arrange
        Account acc = [SELECT Id FROM Account LIMIT 1];
        
        // Act
        Test.startTest();
        Account result = MyService.getAccount(acc.Id);
        Test.stopTest();
        
        // Assert
        System.assertNotEquals(null, result);
        System.assertEquals(acc.Id, result.Id);
    }
    
    @isTest
    static void testGetAccount_invalidId_throwsException() {
        // Act & Assert
        Test.startTest();
        try {
            MyService.getAccount(null);
            System.assert(false, 'Expected exception was not thrown');
        } catch (Exception e) {
            System.assert(e.getMessage().contains('Invalid ID'));
        }
        Test.stopTest();
    }
}
```

### 2. Test.startTest() and Test.stopTest()

```apex
@isTest
static void testBulkOperation() {
    // Setup runs in separate governor limit context
    List<Account> accounts = new List<Account>();
    for (Integer i = 0; i < 200; i++) {
        accounts.add(new Account(Name = 'Test ' + i));
    }
    insert accounts;
    
    // Test.startTest() resets governor limits
    Test.startTest();
    
    // Your code to test (has fresh governor limits)
    MyService.processAccounts(accounts);
    
    // Test.stopTest() executes async operations and finalizes
    Test.stopTest();
    
    // Assertions run after async operations complete
    List<Account> updated = [SELECT Id, Status__c FROM Account];
    System.assertEquals(200, updated.size());
}
```

## Test Data Creation Patterns

### Pattern 1: Test Data Factory

```apex
@isTest
public class TestDataFactory {
    
    public static Account createAccount(String name, Boolean doInsert) {
        Account acc = new Account(
            Name = name,
            Industry = 'Healthcare',
            BillingCity = 'Test City'
        );
        if (doInsert) {
            insert acc;
        }
        return acc;
    }
    
    public static List<Account> createAccounts(Integer count, Boolean doInsert) {
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < count; i++) {
            accounts.add(new Account(Name = 'Test Account ' + i));
        }
        if (doInsert) {
            insert accounts;
        }
        return accounts;
    }
    
    public static Project__c createProject(String contextId, Boolean isDraft, Boolean doInsert) {
        Project__c proj = new Project__c(
            Project_Title__c = 'Test Project',
            Context_Instance_Id__c = contextId,
            Is_Draft__c = isDraft,
            Is_Latest__c = true,
            Version__c = 1
        );
        if (doInsert) {
            insert proj;
        }
        return proj;
    }
}
```

### Pattern 2: @TestSetup Method

```apex
@isTest
private class MyServiceTest {
    
    @TestSetup
    static void setupTestData() {
        // Runs once before all test methods
        // Data persists across test methods in the class
        
        Account acc = TestDataFactory.createAccount('Test Account', true);
        
        List<Contact> contacts = new List<Contact>();
        for (Integer i = 0; i < 5; i++) {
            contacts.add(new Contact(
                FirstName = 'Test',
                LastName = 'Contact ' + i,
                AccountId = acc.Id
            ));
        }
        insert contacts;
    }
    
    @isTest
    static void testMethod1() {
        // Can query data created in @TestSetup
        Account acc = [SELECT Id FROM Account LIMIT 1];
        System.assertNotEquals(null, acc);
    }
}
```

### Pattern 3: SeeAllData=true (Use Sparingly)

```apex
// ❌ AVOID - Makes tests dependent on org data
@isTest(SeeAllData=true)
static void testWithOrgData() {
    // Can see real org data - brittle tests
}

// ✅ PREFER - Create your own test data
@isTest
static void testWithTestData() {
    Account acc = TestDataFactory.createAccount('Test', true);
    // Test with controlled data
}

// ⚠️ EXCEPTION - Only use SeeAllData for:
// - Testing with metadata (RecordTypes, Profiles, etc.)
// - Integration with external systems
// - Specific Salesforce features that require it
```

## Testing Patterns

### Pattern 1: Test Bulk Operations

```apex
@isTest
static void testBulkInsert_200Records_allProcessed() {
    // Create 200+ records to test bulkification
    List<Project__c> projects = new List<Project__c>();
    for (Integer i = 0; i < 250; i++) {
        projects.add(new Project__c(
            Project_Title__c = 'Test Project ' + i,
            Context_Instance_Id__c = 'CI-TEST-' + i
        ));
    }
    
    Test.startTest();
    insert projects;
    MyService.processProjects(projects);
    Test.stopTest();
    
    // Verify all processed
    List<Project__c> processed = [
        SELECT Id, Status__c 
        FROM Project__c 
        WHERE Status__c = 'Processed'
    ];
    System.assertEquals(250, processed.size());
}
```

### Pattern 2: Test Exception Handling

```apex
@isTest
static void testInvalidInput_throwsException() {
    Test.startTest();
    try {
        MyService.processProject(null);
        System.assert(false, 'Expected exception was not thrown');
    } catch (MyService.InvalidInputException e) {
        System.assert(e.getMessage().contains('Project cannot be null'));
    } catch (Exception e) {
        System.assert(false, 'Unexpected exception type: ' + e.getTypeName());
    }
    Test.stopTest();
}
```

### Pattern 3: Test Versioning Logic

```apex
@isTest
static void testGetOrCreateDraft_existingDraft_returnsDraft() {
    // Arrange
    Project__c draft = TestDataFactory.createProject('CI-TEST-001', true, true);
    
    // Act
    Test.startTest();
    Project__c result = MyService.getOrCreateDraft('CI-TEST-001');
    Test.stopTest();
    
    // Assert
    System.assertEquals(draft.Id, result.Id);
    System.assertEquals(true, result.Is_Draft__c);
}

@isTest
static void testGetOrCreateDraft_noDraft_createsDraft() {
    // Arrange
    Project__c latest = TestDataFactory.createProject('CI-TEST-001', false, true);
    latest.Is_Latest__c = true;
    update latest;
    
    // Act
    Test.startTest();
    Project__c result = MyService.getOrCreateDraft('CI-TEST-001');
    Test.stopTest();
    
    // Assert
    System.assertNotEquals(latest.Id, result.Id);
    System.assertEquals(true, result.Is_Draft__c);
    System.assertEquals(latest.Version__c + 1, result.Version__c);
}
```

### Pattern 4: Test Trigger Logic

```apex
@isTest
static void testTrigger_beforeInsert_setsDefaults() {
    // Arrange
    Project__c proj = new Project__c(
        Project_Title__c = 'Test Project'
    );
    
    // Act
    Test.startTest();
    insert proj;
    Test.stopTest();
    
    // Assert
    Project__c inserted = [
        SELECT Id, Is_Draft__c, Is_Latest__c, Version__c
        FROM Project__c
        WHERE Id = :proj.Id
    ];
    System.assertEquals(true, inserted.Is_Draft__c);
    System.assertEquals(true, inserted.Is_Latest__c);
    System.assertEquals(1, inserted.Version__c);
}
```

### Pattern 5: Test Async Operations

```apex
@isTest
static void testFutureMethod_processesRecords() {
    // Arrange
    Account acc = TestDataFactory.createAccount('Test', true);
    
    // Act
    Test.startTest();
    MyService.processAccountAsync(acc.Id);
    Test.stopTest(); // Future methods execute here
    
    // Assert
    Account updated = [SELECT Id, Status__c FROM Account WHERE Id = :acc.Id];
    System.assertEquals('Processed', updated.Status__c);
}

@isTest
static void testQueueable_chainsCorrectly() {
    // Arrange
    List<Account> accounts = TestDataFactory.createAccounts(10, true);
    
    // Act
    Test.startTest();
    System.enqueueJob(new MyQueueable(accounts));
    Test.stopTest(); // Queueable executes here
    
    // Assert
    List<Account> processed = [
        SELECT Id FROM Account WHERE Status__c = 'Processed'
    ];
    System.assertEquals(10, processed.size());
}
```

### Pattern 6: Test Batch Apex

```apex
@isTest
static void testBatch_processesAllRecords() {
    // Arrange
    List<Account> accounts = TestDataFactory.createAccounts(250, true);
    
    // Act
    Test.startTest();
    Database.executeBatch(new MyBatchClass(), 200);
    Test.stopTest(); // Batch executes here
    
    // Assert
    List<Account> processed = [
        SELECT Id FROM Account WHERE Status__c = 'Processed'
    ];
    System.assertEquals(250, processed.size());
}
```

## Mocking and Test Isolation

### Pattern 1: HTTP Callout Mocking

```apex
@isTest
global class MockHttpResponse implements HttpCalloutMock {
    global HTTPResponse respond(HTTPRequest req) {
        HttpResponse res = new HttpResponse();
        res.setHeader('Content-Type', 'application/json');
        res.setBody('{"status":"success"}');
        res.setStatusCode(200);
        return res;
    }
}

@isTest
static void testCallout_success_returnsData() {
    // Set mock
    Test.setMock(HttpCalloutMock.class, new MockHttpResponse());
    
    Test.startTest();
    String result = MyService.makeCallout('https://api.example.com');
    Test.stopTest();
    
    System.assertEquals('success', result);
}
```

### Pattern 2: Database Mock (Test Stub)

```apex
@isTest
public class MockDatabaseService implements MyService.IDatabaseService {
    public List<Account> getAccounts() {
        return new List<Account>{
            new Account(Id = '001000000000001', Name = 'Mock Account')
        };
    }
}

@isTest
static void testWithMock_returnsExpectedData() {
    // Inject mock
    MyService.setDatabaseService(new MockDatabaseService());
    
    Test.startTest();
    List<Account> accounts = MyService.getAccounts();
    Test.stopTest();
    
    System.assertEquals(1, accounts.size());
    System.assertEquals('Mock Account', accounts[0].Name);
}
```

## Code Coverage Strategies

### 1. Aim for 100% Coverage

```apex
// ✅ GOOD - Test all branches
@isTest
static void testMethod_condition1_result1() {
    // Test when condition is true
}

@isTest
static void testMethod_condition2_result2() {
    // Test when condition is false
}

@isTest
static void testMethod_exception_handled() {
    // Test exception path
}
```

### 2. Test Positive and Negative Cases

```apex
@isTest
static void testValidation_validData_passes() {
    // Test with valid data
    Project__c proj = new Project__c(Project_Title__c = 'Valid Title');
    ValidationResult result = MyService.validate(proj);
    System.assertEquals(true, result.isValid);
}

@isTest
static void testValidation_invalidData_fails() {
    // Test with invalid data
    Project__c proj = new Project__c(Project_Title__c = null);
    ValidationResult result = MyService.validate(proj);
    System.assertEquals(false, result.isValid);
}
```

### 3. Test Governor Limits

```apex
@isTest
static void testBulkOperation_staysWithinLimits() {
    List<Account> accounts = TestDataFactory.createAccounts(200, true);
    
    Test.startTest();
    MyService.processAccounts(accounts);
    Test.stopTest();
    
    // Verify limits not exceeded
    System.assert(Limits.getQueries() < Limits.getLimitQueries());
    System.assert(Limits.getDMLStatements() < Limits.getLimitDMLStatements());
    System.assert(Limits.getDMLRows() < Limits.getLimitDMLRows());
}
```

## Assertion Best Practices

### 1. Use Specific Assertions

```apex
// ❌ WEAK - Generic assertion
System.assert(result != null);

// ✅ STRONG - Specific assertion
System.assertNotEquals(null, result, 'Result should not be null');
System.assertEquals('Expected Value', result.field, 'Field should match expected value');
```

### 2. Assert Multiple Conditions

```apex
@isTest
static void testCreateProject_setsAllFields() {
    Test.startTest();
    Project__c proj = MyService.createProject('Test Project', 'CI-001');
    Test.stopTest();
    
    // Assert all expected fields
    System.assertEquals('Test Project', proj.Project_Title__c);
    System.assertEquals('CI-001', proj.Context_Instance_Id__c);
    System.assertEquals(true, proj.Is_Draft__c);
    System.assertEquals(true, proj.Is_Latest__c);
    System.assertEquals(1, proj.Version__c);
}
```

### 3. Use System.assert() for Boolean Conditions

```apex
// Check complex conditions
System.assert(
    result.Status__c == 'Active' || result.Status__c == 'Pending',
    'Status should be Active or Pending'
);
```

## Common Testing Patterns

### Pattern 1: Test User Context

```apex
@isTest
static void testAsStandardUser_hasLimitedAccess() {
    User standardUser = [SELECT Id FROM User WHERE Profile.Name = 'Standard User' LIMIT 1];
    
    System.runAs(standardUser) {
        Test.startTest();
        List<Account> accounts = MyService.getAccounts();
        Test.stopTest();
        
        // Verify user sees only their records
        System.assert(accounts.size() <= 10);
    }
}
```

### Pattern 2: Test Record Type Logic

```apex
@isTest
static void testRecordType_healthcare_usesHealthcareLogic() {
    RecordType healthcareRT = [
        SELECT Id FROM RecordType 
        WHERE SObjectType = 'Account' AND DeveloperName = 'Healthcare'
        LIMIT 1
    ];
    
    Account acc = new Account(
        Name = 'Test Hospital',
        RecordTypeId = healthcareRT.Id
    );
    insert acc;
    
    Test.startTest();
    MyService.processAccount(acc.Id);
    Test.stopTest();
    
    Account processed = [SELECT Id, Industry FROM Account WHERE Id = :acc.Id];
    System.assertEquals('Healthcare', processed.Industry);
}
```

### Pattern 3: Test Sharing Rules

```apex
@isTest
static void testSharing_userCanAccessOwnRecords() {
    User testUser = TestDataFactory.createUser('test@example.com', true);
    
    System.runAs(testUser) {
        // Create record as user
        Account acc = new Account(Name = 'Test Account');
        insert acc;
        
        Test.startTest();
        List<Account> accessible = [SELECT Id FROM Account WHERE Id = :acc.Id];
        Test.stopTest();
        
        System.assertEquals(1, accessible.size());
    }
}
```

## Test Class Organization

### 1. Group Related Tests

```apex
@isTest
private class ProjectServiceTest {
    
    // Group 1: CRUD Operations
    @isTest static void testCreate_validData_insertsRecord() {}
    @isTest static void testRead_validId_returnsRecord() {}
    @isTest static void testUpdate_validData_updatesRecord() {}
    @isTest static void testDelete_validId_deletesRecord() {}
    
    // Group 2: Versioning
    @isTest static void testGetDraft_existingDraft_returnsDraft() {}
    @isTest static void testGetDraft_noDraft_createsDraft() {}
    @isTest static void testPublish_draft_createsNewVersion() {}
    
    // Group 3: Validation
    @isTest static void testValidate_validData_passes() {}
    @isTest static void testValidate_missingTitle_fails() {}
    @isTest static void testValidate_invalidBudget_fails() {}
}
```

### 2. Use Descriptive Test Names

```apex
// ❌ BAD - Unclear what is being tested
@isTest static void test1() {}
@isTest static void testProject() {}

// ✅ GOOD - Clear intent
@isTest static void testCreateProject_validData_insertsRecord() {}
@isTest static void testGetProject_invalidId_throwsException() {}
```

## Debugging Tests

### 1. Use System.debug()

```apex
@isTest
static void testComplexLogic() {
    System.debug('Starting test...');
    System.debug('Input data: ' + inputData);
    
    Test.startTest();
    Result result = MyService.process(inputData);
    Test.stopTest();
    
    System.debug('Result: ' + result);
    System.debug('Expected: ' + expectedResult);
    
    System.assertEquals(expectedResult, result);
}
```

### 2. Check Limits

```apex
@isTest
static void testPerformance() {
    Test.startTest();
    MyService.process();
    Test.stopTest();
    
    System.debug('SOQL Queries: ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
    System.debug('DML Statements: ' + Limits.getDMLStatements() + '/' + Limits.getLimitDMLStatements());
    System.debug('Heap Size: ' + Limits.getHeapSize() + '/' + Limits.getLimitHeapSize());
}
```

## Quick Reference

### Coverage Requirements
- Minimum: 75% for deployment
- Target: 100% for quality
- Triggers: Must have test coverage
- Classes: All public methods should be tested

### Test Limits
- Test methods per class: No limit
- Test execution time: 10 minutes per test class
- Total test execution: 1 hour for all tests

### Best Practices Checklist
- ✅ Use @TestSetup for common data
- ✅ Test.startTest() / Test.stopTest() for governor limit reset
- ✅ Test positive and negative cases
- ✅ Test bulk operations (200+ records)
- ✅ Use specific assertions with messages
- ✅ Mock external dependencies
- ✅ Test all code branches
- ✅ Use descriptive test method names
- ✅ Avoid SeeAllData=true
- ✅ Test as different user profiles

## Related Skills
- `skill_soql_sosl.md` - Query patterns for test data
- `skill_salesforce_development.md` - General development patterns
- `skill_salesforce_deployment.md` - Deployment and code coverage
