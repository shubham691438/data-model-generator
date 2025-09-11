# ATS APPLICATION Data Model Write Rules

## Overview
This document defines comprehensive rules for creating APPLICATION data model write integrations based on the Ashby write-to-ATS patterns and existing ATS integration standards.

## Core Integration Patterns

### 1. Application Write Integration Chain Pattern
Based on Ashby's approach, APPLICATION write operations typically follow this chain:

1. **Start Chain Integration** - Dummy integration to support dependency fields
2. **Candidate Check/Create** - Verify or create candidate in ATS
3. **Resume Upload** - Upload candidate resume (if available)
4. **Application Creation** - Create the job application
5. **Response Handler** - Process and return final results

### 2. Integration Types for APPLICATION Writes

#### A. WRITE_REST_API
- Primary integration type for APPLICATION data model
- Handles candidate creation, application submission, and file uploads
- Uses chained integrations with dependency management

#### B. WRITE_API_RESPONSE_HANDLER
- Processes responses from multiple integrations
- Consolidates results and handles error scenarios
- Returns standardized response format

## Required Integration Structure

### 1. Start Chain Integration
```json
{
  "type": "WriteApiIntegration",
  "integrationId": "{ats}-candidate-application-post-start-chain",
  "method": "GET",
  "apiPath": "dummy",
  "dataModelRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "responseHandlers": [{
    "statusCode": 0,
    "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
    "jsonataConvertorExpression": "{\"errorMessage\": \"Integration not executed because this is dummy integration to support dependency fields for next integration.\"}"
  }],
  "executionEligibilityRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "false"}]
}
```

### 2. Candidate Check Integration
```json
{
  "type": "WriteApiIntegration",
  "integrationId": "{ats}-check-candidate-already-exists",
  "method": "POST",
  "apiPath": "/candidate.search",
  "dataModelRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "requestPayload": {
    "requestBody": "{\"email\": \"${email}\"}",
    "requestBodyConverter": []
  },
  "responseHandlers": [
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$count(results) > 0 and $exists(results[0].id) and $exists($.success) and $.success=true"}],
      "jsonataConvertorExpression": "{\"candidateId\": results[0].id, \"integrationId\": \"{ats}-check-candidate-already-exists\"}"
    },
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$count(results) = 0 and $exists($.success) and $.success=true"}],
      "jsonataConvertorExpression": "{\"errorMessage\": $.errors, \"integrationId\": \"{ats}-check-candidate-already-exists\"}"
    }
  ],
  "integrationDependency": {
    "dependentIntegrationId": "{ats}-candidate-application-post-start-chain",
    "dependencyFields": [{
      "type": "RestApiIntegrationField",
      "targetField": "email",
      "jsonataExpression": "inputData.candidate.email",
      "restApiIntegrationContext": "API_REQUEST_BODY"
    }],
    "jsonDataType": "TEXT_PRIMITIVE",
    "queryType": "SINGLE_ENTITY"
  },
  "executionEligibilityRules": [{
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$exists(inputData.candidate.email) and inputData.candidate.email != null"
  }]
}
```

### 3. Candidate Create Integration
```json
{
  "type": "WriteApiIntegration",
  "integrationId": "{ats}-create-candidate",
  "method": "POST",
  "apiPath": "/candidate.create",
  "dataModelRules": [{
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$exists(inputData.candidate.email) and inputData.candidate.email != null and $exists(inputData.application.atsJobId) and inputData.application.atsJobId != null and $exists(inputData.candidate.fullName) and inputData.candidate.fullName != null"
  }],
  "requestPayload": {
    "requestBody": "$merge([{\n  \"name\": \"${name}\",\n  \"email\": \"${email}\",\n  \"phoneNumber\": \"${phoneNumber}\",\n  \"sourceId\": \"${sourceId}\",\n  \"location\": {\n    \"city\": \"${city}\",\n    \"region\":\"${state}\",\n    \"country\": \"${country}\"\n  }\n},\n(\n  $exists(inputData.application.customFields.questionAnswers.linkedInUrl) and inputData.application.customFields.questionAnswers.linkedInUrl !=null\n  ? {\"linkedInUrl\" : inputData.application.customFields.questionAnswers.linkedInUrl} : {}\n),\n(\n  $exists(inputData.application.customFields.questionAnswers.githubUrl) and inputData.application.customFields.questionAnswers.githubUrl !=null\n  ? {\"githubUrl\" : inputData.application.customFields.questionAnswers.githubUrl} : {}\n)\n])",
    "requestBodyConverter": []
  },
  "responseHandlers": [
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists(results.id) and results.id != null and $exists($.success) and $.success=true"}],
      "jsonataConvertorExpression": "{\"candidateId\": results.id, \"integrationId\": \"{ats}-create-candidate\"}"
    },
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists($.success) and $.success=false"}],
      "jsonataConvertorExpression": "{\"errorMessage\": $.errors}"
    }
  ],
  "integrationDependency": {
    "dependentIntegrationId": "{ats}-check-candidate-already-exists",
    "dependencyFields": [
      {
        "type": "RestApiIntegrationField",
        "targetField": "name",
        "jsonataExpression": "inputData.candidate.fullName",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      },
      {
        "type": "RestApiIntegrationField",
        "targetField": "email",
        "jsonataExpression": "inputData.candidate.email",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      },
      {
        "type": "RestApiIntegrationField",
        "targetField": "phoneNumber",
        "jsonataExpression": "inputData.candidate.phoneNumbers.phoneNumber",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      },
      {
        "type": "RestApiIntegrationField",
        "targetField": "city",
        "jsonataExpression": "inputData.candidate.address.city",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      },
      {
        "type": "RestApiIntegrationField",
        "targetField": "state",
        "jsonataExpression": "$exists(inputData.candidate.customFields.questionAnswers.province) and inputData.candidate.customFields.questionAnswers.province !=null ? inputData.candidate.customFields.questionAnswers.province : inputData.candidate.address.state",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      },
      {
        "type": "RestApiIntegrationField",
        "targetField": "country",
        "jsonataExpression": "inputData.candidate.address.country",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      }
    ],
    "jsonDataType": "TEXT_PRIMITIVE",
    "queryType": "SINGLE_ENTITY"
  },
  "executionEligibilityRules": [
    {
      "type": "BooleanExpressionRule",
      "jsonataExpression": "$exists(inputData.candidate.email) and inputData.candidate.email != null and $exists(inputData.application.atsJobId) and inputData.application.atsJobId != null and $exists(inputData.candidate.fullName) and inputData.candidate.fullName != null"
    },
    {
      "type": "BooleanExpressionRule",
      "jsonataExpression": "$not($exists(response.candidateId))"
    }
  ]
}
```

### 4. Resume Upload Integration
```json
{
  "type": "WriteApiIntegration",
  "integrationId": "{ats}-upload-resume",
  "method": "POST",
  "apiPath": "/candidate.uploadResume",
  "contentType": "MULTIPART_FORM_DATA",
  "dataModelRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "requestPayload": {
    "requestBody": "{\n  \"candidateId\" : \"${candidateId}\",\n  \"resume\": \"${attachmentContent}\"\n}",
    "requestBodyConverter": [{
      "field": "resume",
      "fileConvertType": "Base64ToFile"
    }]
  },
  "responseHandlers": [
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists(results.id) and results.id != null and $exists($.success) and $.success=true"}],
      "jsonataConvertorExpression": "{\"candidateId\": results.id, \"integrationId\": \"{ats}-upload-resume\"}"
    },
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists($.success) and $.success=false"}],
      "jsonataConvertorExpression": "{\"errorMessage\": $.errors}"
    }
  ],
  "integrationDependency": {
    "dependentIntegrationId": "{ats}-create-candidate",
    "dependencyFields": [
      {
        "type": "RestApiIntegrationField",
        "targetField": "candidateId",
        "jsonataExpression": "response.candidateId",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      },
      {
        "type": "RestApiIntegrationField",
        "targetField": "attachmentContent",
        "jsonataExpression": "inputData.application.attachment.attachmentContent",
        "restApiIntegrationContext": "API_REQUEST_BODY"
      }
    ],
    "jsonDataType": "TEXT_PRIMITIVE",
    "queryType": "SINGLE_ENTITY"
  },
  "executionEligibilityRules": [
    {
      "type": "BooleanExpressionRule",
      "jsonataExpression": "$exists(inputData.application.attachment) and inputData.application.attachment != null and $exists(inputData.application.attachment.attachmentContent) and inputData.application.attachment.attachmentContent != null"
    },
    {
      "type": "BooleanExpressionRule",
      "jsonataExpression": "$exists(response.candidateId)"
    }
  ]
}
```

### 5. Application Creation Integration
```json
{
  "type": "WriteApiIntegration",
  "integrationId": "{ats}-create-application",
  "method": "POST",
  "apiPath": "/application.create",
  "dataModelRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "requestPayload": {
    "requestBody": "{\n  \"candidateId\": \"${candidateId}\",\n  \"jobId\": \"${jobId}\",\n  \"sourceId\": \"${sourceId}\"\n}",
    "requestBodyConverter": []
  },
  "responseHandlers": [
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists(results.id) and results.id != null and $exists($.success) and $.success=true"}],
      "jsonataConvertorExpression": "{\"applicationId\": results.id, \"candidateId\": \"${candidateId}\", \"jobId\": \"${jobId}\"}"
    },
    {
      "statusCode": 200,
      "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists($.success) and $.success=false"}],
      "jsonataConvertorExpression": "{\"errorMessage\": $.errors}"
    }
  ],
  "integrationDependency": {
    "dependentIntegrationId": "{ats}-upload-resume",
    "dependencyFields": [
      {
        "type": "RestApiIntegrationField",
        "targetField": "candidateId",
        "jsonataExpression": "response.candidateId",
        "restApiIntegrationContext": "API_RESPONSE_BODY"
      },
      {
        "type": "RestApiIntegrationField",
        "targetField": "jobId",
        "jsonataExpression": "inputData.application.atsJobId",
        "restApiIntegrationContext": "API_RESPONSE_BODY"
      }
    ],
    "jsonDataType": "TEXT_PRIMITIVE",
    "queryType": "SINGLE_ENTITY"
  },
  "executionEligibilityRules": [
    {
      "type": "BooleanExpressionRule",
      "jsonataExpression": "$exists(inputData.application.atsJobId) and inputData.application.atsJobId != null"
    },
    {
      "type": "BooleanExpressionRule",
      "jsonataExpression": "$exists(response.candidateId)"
    }
  ]
}
```

### 6. Response Handler Integration
```json
{
  "type": "WriteApiIntegration",
  "integrationId": "{ats}-application-api-response-handler-chain",
  "method": "POST",
  "apiPath": "dummy",
  "dataModelRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "responseHandlers": [{
    "statusCode": 0,
    "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
    "jsonataConvertorExpression": "($candidateId := {ats}_create_candidate[0].candidateId; $applicationId := {ats}_create_application[0].applicationId; $customFields := function($keys) { $merge($map($keys, function($key) { { $key: $lookup($, $key) } })) }; $exists($candidateId) ? { \"data\": { \"candidateId\": $string($candidateId), \"applicationId\": $string($applicationId), \"customFields\": $customFields([\"{ats}_create_candidate\", \"{ats}_upload_resume\", \"{ats}_create_application\"]) }, \"errors\": [] } : { \"data\": null, \"errors\": [{\"errorCode\":null, \"errorType\":null, \"message\":$string($), \"params\":{}}] })"
  }],
  "executionEligibilityRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "false"}]
}
```

## Data Model Rules

### Required Data Model Rules
```json
"dataModelRules": [
  {
    "type": "BooleanExpressionRule",
    "jsonataExpression": "($exists(inputData.candidate.firstName) and inputData.candidate.firstName != null and $exists(inputData.candidate.lastName) and inputData.candidate.lastName != null) or ($exists(inputData.candidate.atsCandidateId) and inputData.candidate.atsCandidateId != null)"
  },
  {
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$exists(inputData.application.atsJobId) and inputData.application.atsJobId != null"
  },
  {
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$exists(inputData.candidate.email) and inputData.candidate.email != null"
  }
]
```

### Execution Eligibility Rules
```json
"executionEligibilityRules": [
  {
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$exists(inputData.candidate.email) and inputData.candidate.email != null and $exists(inputData.application.atsJobId) and inputData.application.atsJobId != null and $exists(inputData.candidate.fullName) and inputData.candidate.fullName != null"
  },
  {
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$not($exists(response.candidateId))"
  }
]
```

## Response Handler Patterns

### Success Response Handler
```json
{
  "statusCode": 200,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists(results.id) and results.id != null and $exists($.success) and $.success=true"}],
  "jsonataConvertorExpression": "{\"applicationId\": results.id, \"candidateId\": \"${candidateId}\", \"jobId\": \"${jobId}\"}"
}
```

### Error Response Handler
```json
{
  "statusCode": 200,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists($.success) and $.success=false"}],
  "jsonataConvertorExpression": "{\"errorMessage\": $.errors}"
}
```

### HTTP Error Handlers
```json
{
  "statusCode": 400,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "jsonataConvertorExpression": "{\"errorMessage\": \"Bad Request - Invalid data provided\"}"
},
{
  "statusCode": 401,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "jsonataConvertorExpression": "{\"errorMessage\": \"Unauthorized - Invalid credentials\"}"
},
{
  "statusCode": 404,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "jsonataConvertorExpression": "{\"errorMessage\": \"Not Found - Resource not found\"}"
},
{
  "statusCode": 500,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "jsonataConvertorExpression": "{\"errorMessage\": \"Internal Server Error\"}"
}
```

## File Upload Patterns

### Resume Upload with Base64 Conversion
```json
"requestPayload": {
  "requestBody": "{\n  \"candidateId\" : \"${candidateId}\",\n  \"resume\": \"${attachmentContent}\"\n}",
  "requestBodyConverter": [{
    "field": "resume",
    "fileConvertType": "Base64ToFile"
  }]
}
```

### Resume Upload with JSON Format
```json
"requestPayload": {
  "requestBody": "{\"filename\":\"${fileName}\", \"type\":\"resume\", \"content\":\"${content}\", \"content_type\":\"${contentType}\"}",
  "requestBodyConverter": []
}
```

## Authentication Patterns

### BASIC Authentication
```json
"authTypes": ["BASIC"],
"headers": {
  "Authorization": "Basic {{basic_auth_token}}",
  "Content-Type": "application/json"
}
```

### API Key Authentication
```json
"authTypes": ["API_KEY"],
"headers": {
  "X-API-KEY": "{{api_key}}",
  "Content-Type": "application/json"
}
```

### OAuth2 Authentication
```json
"authTypes": ["OAUTH_2"],
"headers": {
  "Authorization": "Bearer {{access_token}}",
  "Content-Type": "application/json"
}
```

## Content Type Patterns

### JSON Content
```json
"contentType": "APPLICATION_JSON"
```

### Multipart Form Data
```json
"contentType": "MULTIPART_FORM_DATA"
```

### Form URL Encoded
```json
"contentType": "APPLICATION_FORM_URLENCODED"
```

## Integration Naming Conventions

### Integration ID Patterns
- Start Chain: `{ats}-candidate-application-post-start-chain`
- Candidate Check: `{ats}-check-candidate-already-exists`
- Candidate Create: `{ats}-create-candidate`
- Resume Upload: `{ats}-upload-resume`
- Application Create: `{ats}-create-application`
- Response Handler: `{ats}-application-api-response-handler-chain`

### API Path Patterns
- Candidate Search: `/candidate.search`
- Candidate Create: `/candidate.create`
- Candidate Update: `/candidate.update`
- Resume Upload: `/candidate.uploadResume`
- Application Create: `/application.create`

## Error Handling Patterns

### Standard Error Messages
```json
{
  "statusCode": 0,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "jsonataConvertorExpression": "{\"errorMessage\": \"Integration not executed because data might be missing-{integration-id}.\"}"
}
```

### Validation Error Messages
```json
{
  "statusCode": 422,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "jsonataConvertorExpression": "{\"errorMessage\": $string($)}"
}
```

## Best Practices

### 1. Dependency Management
- Always use `integrationDependency` to chain integrations
- Use `dependentIntegrationId` to reference the previous integration
- Use `dependencyFields` to pass data between integrations

### 2. Error Handling
- Implement comprehensive response handlers for all status codes
- Use descriptive error messages
- Handle both API errors and validation errors

### 3. Data Validation
- Use `dataModelRules` to validate input data
- Use `executionEligibilityRules` to control integration execution
- Validate required fields before processing

### 4. Response Processing
- Use `responseHandlers` to process different response scenarios
- Extract relevant data from responses
- Handle both success and error cases

### 5. File Handling
- Support both Base64 and direct file uploads
- Use appropriate content types for file uploads
- Validate file existence before processing

### 6. Custom Fields
- Support custom field mapping
- Use conditional logic for optional fields
- Preserve custom field data in responses

## Testing Requirements

### 1. Unit Testing
- Test each integration individually
- Validate JSONata expressions
- Test error scenarios

### 2. Integration Testing
- Test complete integration chains
- Validate data flow between integrations
- Test with real ATS endpoints

### 3. Error Testing
- Test all error response handlers
- Validate error message formats
- Test edge cases and invalid data

### 4. Performance Testing
- Test with large files
- Validate timeout handling
- Test concurrent requests

## Security Considerations

### 1. Authentication
- Never hardcode credentials
- Use template variables for sensitive data
- Support multiple authentication methods

### 2. Data Validation
- Validate all input data
- Sanitize user inputs
- Prevent injection attacks

### 3. Error Handling
- Don't expose sensitive information in errors
- Log errors securely
- Handle authentication failures gracefully

## Maintenance Guidelines

### 1. Version Control
- Use semantic versioning
- Document changes
- Maintain backward compatibility

### 2. Monitoring
- Log integration executions
- Monitor error rates
- Track performance metrics

### 3. Updates
- Test updates thoroughly
- Maintain integration chains
- Update documentation

This comprehensive set of rules provides a solid foundation for creating robust APPLICATION data model write integrations that follow the established patterns and best practices.

# Vendor-Specific APPLICATION Write Variants

The baseline chain above varies per ATS. Use the following guidance when building `APPLICATION` write integrations for each vendor:

- Greenhouse
  - Flow A (existing candidate): update candidate by `atsCandidateId` → create application on candidate → attach resume to application.
  - Flow B (new candidate): create candidate with embedded application → attach resume to application.
  - Attachments: JSON body with base64 to `/applications/${applicationId}/attachments` or `/candidates/${candidateId}/attachments`.
  - Auth: BASIC; often requires `On-Behalf-Of` header.

- Jobvite
  - Single POST to `/api/v2/candidate` creates candidate and application together; include API headers `x-jvi-sc`, `x-jvi-api`.
  - Resume optional; include only when base64 present and contentType is `application/pdf`.
  - 201 returns `application.EId` and `application.candidate.EId`; handle 400/404/409 error bodies.

- Apploi
  - Single POST to `easy-apply` with candidate, `jobId`, and resume (filename/content/contentType).
  - Requires `email`, `fullName` (or first/last), `atsJobId`.
  - Auth: API_KEY.

- Hoops HR
  - Single POST to `/rest/applicants/create/${refNumber}.json` with candidate details and resume.
  - Requires city/state/country and resume fields; Auth via API key header `TOKEN`.

- UKG
  - Lookup by email → create candidate if missing → create application → upload resume to `/api/applications/${applicationId}/documents` (multipart with `file` field and metadata).
  - Applicant source and screening question responses may be required.
  - Auth: OAUTH_2.

- Dayforce
  - Get job questionnaire for `atsJobId` → submit to `CandidateSourcing` with candidate, source, resume, and mapped question responses.
  - Treat `CANDIDATE_HAS_ALREADY_APPLIED` as idempotent success and return identifiers if present.
  - Auth: OAUTH_2.

- Tal.ai
  - Single webhook POST (JSON or multipart) including candidate, `atsJobId`, resume filename/content.
  - Auth: BASIC.

# Per-ATS Eligibility Add-ons

Extend `dataModelRules`/`executionEligibilityRules` based on vendor:

- Greenhouse: for new candidate+application, require `firstName`, `lastName`, `atsJobId`; for attachments require `applicationId`, `attachmentFileName`, `attachmentContent`, `attachmentContentType`.
- Jobvite: require `firstName`, `lastName`, `email`; resume fields optional and included conditionally.
- Apploi: require `email`, `atsJobId`, and either `candidate.customFields.fullName` or `firstName`/`lastName`; resume filename/content/contentType required.
- Hoops HR: require `firstName`, `lastName`, `email`, `phoneNumber`, address (city/state/country), and resume content/type.
- UKG: lookup needs `email`; create needs `firstName`, `lastName`, `email`; application needs `atsJobId` (and often `availableStartDate`, `source`).
- Dayforce: require `atsJobId`, `firstName`, `email`, phone, `source`, resume, and questionnaire mapping.
- Tal.ai: require `atsJobId`, `firstName`, `lastName`, `email`, `phoneNumber`, resume content and filename.

# Additional Upload and Auth Patterns

Multipart Upload on Application (UKG):
```json
{
  "contentType": "MULTIPART_FORM_DATA",
  "apiPath": "/api/applications/${applicationId}/documents",
  "requestPayload": {
    "requestBody": "{ \n  \\\"file\\\":\\\"${attachmentContent}\\\", \n  \\\"metadata\\\":{ \n    \\\"file_name\\\":\\\"${fileName}\\\", \n    \\\"description\\\":\\\"${attachmentText}\\\", \n    \\\"document_type\\\":\\\"Resume\\\" \n  }\n}",
    "requestBodyConverter": [{"fileConvertType":"Base64ToFile", "field":"file"}]
  }
}
```

Multipart Upload with Content-Disposition Header (iCIMS):
```json
{
  "contentType": "MULTIPART_FORM_DATA",
  "headers": {
    "Content-Disposition": "form-data; name=\"resume\"; filename=\"${attachmentFileName}\"",
    "Content-Length": "0"
  },
  "requestPayload": {
    "requestBody": {"resume": "${attachmentContent}"},
    "requestBodyConverter": [{"fileConvertType":"Base64ToFile", "field":"resume"}]
  }
}
```

API Key with Vendor Headers (Jobvite):
```json
{
  "authTypes": ["BASIC"],
  "headers": {
    "x-jvi-sc": "${api-secret}",
    "x-jvi-api": "${api-key}"
  }
}
```

# Naming Notes

Some ATSes use split flows and thus split integration IDs (e.g., `ukg-create-applications-one/two`, `greenhouse-candidate-update-application-post`, `apploi-application-submission`, `jobvite-candidate-application-create`). Maintain consistency and intent across a vendor’s set.

# Idempotent Success Cases

For vendors like Dayforce, interpret known duplicate-apply responses as success-like and return identifiers instead of failing the chain, to keep writes idempotent.