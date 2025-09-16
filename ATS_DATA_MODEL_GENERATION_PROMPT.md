# ATS Data Model Generation - Systematic Prompt Rule

## 🎯 Purpose
This document provides a systematic prompt rule for generating ATS (Applicant Tracking System) data model integrations. Follow this structured approach to create robust, standardized integrations.

## 📋 File Generation Rules

### Solution Document vs Integration Files
- **Solution Documents (.md)**: Generated when BRD is provided and only documentation is requested
- **Integration Files (.json)**: Generated when ATS integration development is explicitly requested
- **Both**: Generated when both solution document and ATS integration are requested
- **BRD Requirement**: A BRD must be present in the BRD-provided/ directory to trigger any generation

## 📋 Step-by-Step Process

### Step 1: Reference Integration Analysis

**Prompt Template:**
```
I need to create a write-to-ATS data model for ATS: [ATS_NAME]

Please look through the data models in ats_data/ and identify the most similar reference integration based on:

1. Authentication method (API_KEY, OAUTH_2, BASIC, SECURED_OAUTH2)
2. Data model type (APPLICATION, JOB, CANDIDATE, APPLICATION_STAGE, JOB_QUESTION)
3. Integration complexity (simple single API vs. chained integrations)
4. API patterns (REST, webhook, multipart uploads)

Reference ATS should be: [SUGGESTED_REFERENCE_ATS]

Please provide the complete data model from the reference integration.
```

**Example:**
```
I need to create a write-to-ATS data model for ATS: BambooHR

Please look through the data models in ats_data/ and identify the most similar reference integration. 
BambooHR uses API_KEY authentication and supports APPLICATION data model with simple single API calls.

Reference ATS should be: Apploi (similar API_KEY + APPLICATION pattern)

Please provide the complete data model from the Apploi integration.
```

### Step 2: API Discovery and Documentation

**Prompt Template:**
```
Based on the reference data model provided, I need to create a complete API documentation for [ATS_NAME].

Please list down ALL APIs that will be used in the integration with the following format:

## API Documentation for [ATS_NAME]

### 1. [API_PURPOSE] (e.g., "Get Jobs", "Create Application", "Upload Resume")
- **API Doc Link**: [PROVIDE_LINK_TO_OFFICIAL_DOCS]
- **Method**: GET/POST/PUT/PATCH
- **Endpoint**: [FULL_ENDPOINT_URL]
- **Authentication**: [AUTH_TYPE]
- **Purpose**: [DESCRIPTION_OF_WHAT_THIS_API_DOES]
- **Required Headers**: 
  ```
  [LIST_ALL_REQUIRED_HEADERS]
  ```
- **Request Body** (if applicable):
  ```json
  [SAMPLE_REQUEST_BODY]
  ```
- **Response Format**:
  ```json
  [SAMPLE_RESPONSE_BODY]
  ```
- **curl Command**:
  ```bash
  curl -X [METHOD] "[ENDPOINT]" \
       -H "Authorization: [AUTH_HEADER]" \
       -H "Content-Type: application/json" \
       -d '[REQUEST_BODY]'
  ```

### 2. [NEXT_API_PURPOSE]
[REPEAT_FORMAT_FOR_EACH_API]

### Integration Flow
1. [STEP_1_DESCRIPTION]
2. [STEP_2_DESCRIPTION]
3. [STEP_N_DESCRIPTION]
```

**Example:**
```
Based on the Apploi reference data model provided, I need to create a complete API documentation for BambooHR.

Please list down ALL APIs that will be used in the integration:

## API Documentation for BambooHR

### 1. Create Application
- **API Doc Link**: https://documentation.bamboohr.com/reference/post-employees
- **Method**: POST
- **Endpoint**: https://api.bamboohr.com/api/gateway.php/[COMPANY_DOMAIN]/v1/employees
- **Authentication**: API_KEY
- **Purpose**: Creates a new employee/application in BambooHR
- **Required Headers**: 
  ```
  Authorization: Basic [BASE64_ENCODED_API_KEY]
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "firstName": "John",
    "lastName": "Doe",
    "workEmail": "john.doe@example.com",
    "jobTitle": "Software Engineer",
    "department": "Engineering"
  }
  ```
- **Response Format**:
  ```json
  {
    "id": "12345",
    "status": "success"
  }
  ```
- **curl Command**:
  ```bash
  curl -X POST "https://api.bamboohr.com/api/gateway.php/[COMPANY_DOMAIN]/v1/employees" \
       -H "Authorization: Basic [BASE64_ENCODED_API_KEY]" \
       -H "Content-Type: application/json" \
       -d '{"firstName": "John", "lastName": "Doe", "workEmail": "john.doe@example.com"}'
  ```

### Integration Flow
1. Create employee/application with candidate data
2. Handle success/error responses
3. Return application ID and status
```

### Step 3: API Testing and Validation

**Prompt Template:**
```
Now I need to test all the APIs listed above for [ATS_NAME].

Please help me execute the curl commands and analyze the responses:

## API Testing Results

### Test 1: [API_NAME]
**curl Command**: [COPY_FROM_STEP_2]
**Expected Response**: [COPY_FROM_STEP_2]
**Actual Response**: [PASTE_ACTUAL_RESPONSE_HERE]
**Status**: ✅ Success / ❌ Error
**Notes**: [ANY_IMPORTANT_OBSERVATIONS]

### Test 2: [NEXT_API_NAME]
[REPEAT_FOR_EACH_API]

## Analysis Summary
- **Authentication Working**: ✅/❌
- **API Endpoints Accessible**: ✅/❌
- **Response Format Matches Documentation**: ✅/❌
- **Required Fields Identified**: [LIST_REQUIRED_FIELDS]
- **Error Handling Patterns**: [DESCRIBE_ERROR_RESPONSES]
- **Rate Limits**: [IF_ANY]
- **Special Requirements**: [ANY_SPECIAL_CONSIDERATIONS]
```

### Step 4: Data Model Generation

**Prompt Template:**
```
Based on the reference data model and API testing results, please generate the complete data model for [ATS_NAME].

## Requirements:
1. **Reference Model**: [REFERENCE_ATS_NAME] data model
2. **Target ATS**: [ATS_NAME]
3. **Data Model Type**: [APPLICATION/JOB/CANDIDATE/etc.]
4. **Authentication**: [AUTH_TYPE]
5. **Integration Pattern**: [SIMPLE/CHAINED/WEBHOOK]

## API Information:
[PASTE_ALL_API_DETAILS_FROM_STEP_2_AND_3]

## Generate Complete Data Model:
Please create a JSON file following this exact structure:

```json
{
  "status": "success",
  "ats_name": "[ATS_NAME_LOWERCASE]",
  "data": [
    {
      "dataModel": "[DATA_MODEL_TYPE]",
      "integrationType": "[INTEGRATION_TYPE]",
      "integrations": [
        {
          "type": "[WriteApiIntegration/ReadApiIntegration]",
          "integrationId": "[ats]-[action]-[entity]",
          "responseConfig": {
            "responseType": "[SINGLE_ENTITY/ARRAY_OF_ENTITIES]",
            "jsonataExpression": "$",
            "resPassingJsonataExpression": null
          },
          "dataModelRules": [
            {
              "type": "BooleanExpressionRule",
              "jsonataExpression": "[VALIDATION_LOGIC]"
            }
          ],
          "dataModelTarget": null,
          "integrationDependency": {
            "dependentIntegrationId": "[PREVIOUS_INTEGRATION_ID]",
            "dependencyFields": [
              {
                "type": "RestApiIntegrationField",
                "targetField": "[FIELD_NAME]",
                "jsonataExpression": "[DATA_MAPPING]",
                "restApiIntegrationContext": "[API_REQUEST_BODY/API_RESPONSE_BODY/API_PATH]"
              }
            ],
            "jsonDataType": "TEXT_PRIMITIVE",
            "queryType": "SINGLE_ENTITY"
          },
          "failSilently": false,
          "method": "[HTTP_METHOD]",
          "authTypes": ["[AUTH_TYPE]"],
          "apiPath": "[FULL_ENDPOINT_URL]",
          "headers": {
            "[HEADER_NAME]": "[HEADER_VALUE]"
          },
          "queryParams": {},
          "contentType": "[APPLICATION_JSON/MULTIPART_FORM_DATA/etc.]",
          "requestPayload": {
            "requestBody": "[REQUEST_BODY_TEMPLATE]",
            "requestBodyConverter": []
          },
          "responseHandlers": [
            {
              "statusCode": [HTTP_STATUS_CODE],
              "bodyRules": [
                {
                  "type": "BooleanExpressionRule",
                  "jsonataExpression": "[SUCCESS_CONDITION]"
                }
              ],
              "jsonataConvertorExpression": "[SUCCESS_RESPONSE_MAPPING]"
            },
            {
              "statusCode": [ERROR_STATUS_CODE],
              "bodyRules": [
                {
                  "type": "BooleanExpressionRule",
                  "jsonataExpression": "true"
                }
              ],
              "jsonataConvertorExpression": "[ERROR_RESPONSE_MAPPING]"
            }
          ],
          "headersInResponse": false,
          "executionEligibilityRules": [
            {
              "type": "BooleanExpressionRule",
              "jsonataExpression": "[EXECUTION_CONDITION]"
            }
          ]
        }
      ]
    }
  ]
}
```

## Key Requirements:
1. **Follow Reference Pattern**: Use the same structure as [REFERENCE_ATS_NAME]
2. **Adapt Authentication**: Change to [AUTH_TYPE] method
3. **Update Endpoints**: Use [ATS_NAME] specific endpoints
4. **Implement JSONata**: Create proper data transformation expressions
5. **Error Handling**: Include comprehensive response handlers
6. **Validation Rules**: Add appropriate data model rules
7. **Integration Chain**: Follow the same dependency pattern if applicable

Please generate the complete data model JSON.
```

## 🔧 Complete Example Workflow

### Example: Creating BambooHR Integration

**Step 1 - Reference Analysis:**
```
I need to create a write-to-ATS data model for ATS: BambooHR

Please look through the data models in ats_data/ and identify the most similar reference integration. 
BambooHR uses API_KEY authentication and supports APPLICATION data model with simple single API calls.

Reference ATS should be: Apploi (similar API_KEY + APPLICATION pattern)

Please provide the complete data model from the Apploi integration.
```

**Step 2 - API Documentation:**
```
Based on the Apploi reference data model provided, I need to create a complete API documentation for BambooHR.

Please list down ALL APIs that will be used in the integration:

## API Documentation for BambooHR

### 1. Create Application
- **API Doc Link**: https://documentation.bamboohr.com/reference/post-employees
- **Method**: POST
- **Endpoint**: https://api.bamboohr.com/api/gateway.php/[COMPANY_DOMAIN]/v1/employees
- **Authentication**: API_KEY
- **Purpose**: Creates a new employee/application in BambooHR
- **Required Headers**: 
  ```
  Authorization: Basic [BASE64_ENCODED_API_KEY]
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "firstName": "John",
    "lastName": "Doe", 
    "workEmail": "john.doe@example.com",
    "jobTitle": "Software Engineer",
    "department": "Engineering"
  }
  ```
- **Response Format**:
  ```json
  {
    "id": "12345",
    "status": "success"
  }
  ```
- **curl Command**:
  ```bash
  curl -X POST "https://api.bamboohr.com/api/gateway.php/[COMPANY_DOMAIN]/v1/employees" \
       -H "Authorization: Basic [BASE64_ENCODED_API_KEY]" \
       -H "Content-Type: application/json" \
       -d '{"firstName": "John", "lastName": "Doe", "workEmail": "john.doe@example.com"}'
  ```

### Integration Flow
1. Create employee/application with candidate data
2. Handle success/error responses
3. Return application ID and status
```

**Step 3 - API Testing:**
```
Now I need to test all the APIs listed above for BambooHR.

Please help me execute the curl commands and analyze the responses:

## API Testing Results

### Test 1: Create Application
**curl Command**: 
```bash
curl -X POST "https://api.bamboohr.com/api/gateway.php/[COMPANY_DOMAIN]/v1/employees" \
     -H "Authorization: Basic [BASE64_ENCODED_API_KEY]" \
     -H "Content-Type: application/json" \
     -d '{"firstName": "John", "lastName": "Doe", "workEmail": "john.doe@example.com"}'
```
**Expected Response**: 
```json
{
  "id": "12345",
  "status": "success"
}
```
**Actual Response**: [PASTE_ACTUAL_RESPONSE_HERE]
**Status**: ✅ Success / ❌ Error
**Notes**: [ANY_IMPORTANT_OBSERVATIONS]

## Analysis Summary
- **Authentication Working**: ✅/❌
- **API Endpoints Accessible**: ✅/❌
- **Response Format Matches Documentation**: ✅/❌
- **Required Fields Identified**: firstName, lastName, workEmail
- **Error Handling Patterns**: 400 for validation errors, 401 for auth failures
- **Rate Limits**: None specified
- **Special Requirements**: Company domain required in URL
```

**Step 4 - Data Model Generation:**
```
Based on the Apploi reference data model and API testing results, please generate the complete data model for BambooHR.

## Requirements:
1. **Reference Model**: Apploi data model
2. **Target ATS**: BambooHR
3. **Data Model Type**: APPLICATION
4. **Authentication**: API_KEY
5. **Integration Pattern**: SIMPLE

## API Information:
[PASTE_ALL_API_DETAILS_FROM_STEP_2_AND_3]

## Generate Complete Data Model:
Please create a JSON file following the exact structure provided in the template above.

## Key Requirements:
1. **Follow Reference Pattern**: Use the same structure as Apploi
2. **Adapt Authentication**: Change to API_KEY method with Basic auth
3. **Update Endpoints**: Use BambooHR specific endpoints
4. **Implement JSONata**: Create proper data transformation expressions
5. **Error Handling**: Include comprehensive response handlers
6. **Validation Rules**: Add appropriate data model rules
7. **Integration Chain**: Follow simple single API pattern

Please generate the complete data model JSON.
```

## 📝 Checklist for Each Step

### Step 1: Reference Analysis ✅
- [ ] Identified similar ATS based on authentication method
- [ ] Matched data model type (APPLICATION, JOB, etc.)
- [ ] Considered integration complexity
- [ ] Retrieved complete reference data model

### Step 2: API Documentation ✅
- [ ] Listed all required APIs
- [ ] Provided official API documentation links
- [ ] Included complete curl commands
- [ ] Documented request/response formats
- [ ] Specified authentication requirements
- [ ] Outlined integration flow

### Step 3: API Testing ✅
- [ ] Executed all curl commands
- [ ] Documented actual responses
- [ ] Verified authentication works
- [ ] Confirmed endpoint accessibility
- [ ] Identified required fields
- [ ] Analyzed error patterns
- [ ] Noted special requirements

### Step 4: Data Model Generation ✅
- [ ] Followed reference pattern structure
- [ ] Adapted authentication method
- [ ] Updated endpoints and headers
- [ ] Implemented proper JSONata expressions
- [ ] Added comprehensive error handling
- [ ] Included validation rules
- [ ] Maintained integration dependencies
- [ ] Generated complete JSON structure

## 🚀 Quick Start Commands

### Find Reference Integration
```bash
# Browse available ATS integrations
ls ats_data/

# Look for similar patterns
grep -r "API_KEY" ats_data/ | grep "APPLICATION"
grep -r "OAUTH_2" ats_data/ | grep "JOB"
```

### Test API Endpoints
```bash
# Test authentication
curl -X GET "https://api.example-ats.com/test" \
     -H "Authorization: Bearer [TOKEN]"

# Test application creation
curl -X POST "https://api.example-ats.com/applications" \
     -H "Authorization: Bearer [TOKEN]" \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
```

## 📚 Additional Resources

- **ATS Application Write Rules**: `ats_application_write_rules.md`
- **Integration Templates**: `ats_application_write_templates.json`
- **JSONata Testing**: [try.jsonata.org](https://try.jsonata.org)
- **Curl Command Generator**: [curl.trillworks.com](https://curl.trillworks.com)

---

*This systematic approach ensures consistent, robust ATS integrations following established patterns and best practices.*
