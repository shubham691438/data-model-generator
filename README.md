# ATS Data Model Generator

A comprehensive toolkit for generating and managing ATS (Applicant Tracking System) data model integrations. This project provides standardized patterns, templates, and workflows for creating robust integrations with various ATS platforms.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Workflow Guide](#workflow-guide)
- [Data Models](#data-models)
- [Integration Patterns](#integration-patterns)
- [Best Practices](#best-practices)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Contributing](#contributing)

## 🎯 Overview

The ATS Data Model Generator is designed to streamline the creation of integrations with various Applicant Tracking Systems. It provides:

- **Standardized Integration Patterns**: Consistent structure across all ATS integrations
- **Template-Based Development**: Pre-built templates for common integration scenarios
- **Comprehensive Rules Engine**: Validation and execution rules for data models
- **Multi-ATS Support**: Support for 30+ ATS platforms including Greenhouse, Workday, SAP, UKG, and more

## 📁 Project Structure

```
ats-data-model-generator/
├── ats_data/                                    # ATS integration files
│   ├── greenhouse_data_model_integrations.json
│   ├── workday_data_model_integrations.json
│   ├── sap_data_model_integrations.json
│   └── ... (30+ ATS integrations)
├── ats_application_write_rules.md              # Comprehensive write rules
├── ats_application_write_templates.json        # Integration templates
├── ashby_*.json                               # Ashby-specific configurations
└── README.md                                  # This file
```

### Key Files

- **`ats_data/`**: Contains individual ATS integration configurations
- **`ats_application_write_rules.md`**: Comprehensive rules for APPLICATION data model writes
- **`ats_application_write_templates.json`**: Reusable templates for common patterns
- **Ashby files**: Reference implementations and webhook configurations

## 🔄 Workflow Guide

### Step 1: Identify a Reference Integration (~15 minutes)

**Objective**: Review existing WTA Data Model and find a similar integration pattern.

1. **Review Existing Integrations**
   ```bash
   # Browse available ATS integrations
   ls ats_data/
   ```

2. **Select Reference Integration**
   - Look for ATS with similar API patterns
   - Consider authentication methods (API_KEY, OAUTH_2, BASIC)
   - Match data model requirements (JOB, CANDIDATE, APPLICATION, etc.)

3. **Analyze Reference Structure**
   - Study integration chain patterns
   - Review authentication mechanisms
   - Understand data model rules

### Step 2: API Discovery with Cursor

**Objective**: Discover and analyze all required APIs for the new WTA.

1. **List Required APIs**
   - Identify all endpoints needed for the integration
   - Document authentication requirements
   - Note request/response formats

2. **Generate curl Commands**
   ```bash
   # Example API discovery commands
   curl -X GET "https://api.example-ats.com/jobs" \
        -H "Authorization: Bearer {{access_token}}" \
        -H "Content-Type: application/json"
   ```

3. **Execute and Analyze**
   - Run curl commands to understand API behavior
   - Document response structures
   - Identify required fields and validation rules

4. **Generate Data Model**
   - Use reference integration as template
   - Adapt patterns to new ATS requirements
   - Implement JSONata expressions for data transformation

### Step 3: Review & Testing

**Objective**: Validate the generated data model and prepare for testing.

1. **Structure Validation**
   - Ensure alignment with WTA rules
   - Verify ATS-specific requirements
   - Check integration chain dependencies

2. **JSONata Expression Testing**
   - Test expressions on [try.jsonata.org](https://try.jsonata.org)
   - Validate data transformations
   - Ensure error handling coverage

3. **Move to Testing Phase**
   - Deploy integration for testing
   - Validate with real ATS endpoints
   - Monitor execution logs

## 📊 Data Models

### Supported Data Models

| Data Model | Description | Use Case |
|------------|-------------|----------|
| **JOB** | Job posting data with locations, departments, recruiters | Job synchronization |
| **CANDIDATE** | Candidate profile data with addresses, phone numbers | Candidate management |
| **APPLICATION** | Job application data with status tracking | Application processing |
| **APPLICATION_STAGE** | Application workflow stages with audit trails | Status tracking |
| **JOB_QUESTION** | Job-specific questions, forms, screening questions | Application forms |

### Data Model Structure

```json
{
  "dataModel": "APPLICATION",
  "integrationType": "WRITE_REST_API",
  "integrations": [
    {
      "type": "WriteApiIntegration",
      "integrationId": "{ats}-create-application",
      "method": "POST",
      "apiPath": "/api/applications",
      "authTypes": ["API_KEY"],
      "dataModelRules": [...],
      "responseHandlers": [...]
    }
  ]
}
```

## 🔧 Integration Patterns

### Authentication Patterns

#### API Key Authentication
```json
{
  "authTypes": ["API_KEY"],
  "headers": {
    "X-API-KEY": "{{api_key}}",
    "Content-Type": "application/json"
  }
}
```

#### OAuth2 Authentication
```json
{
  "authTypes": ["OAUTH_2"],
  "headers": {
    "Authorization": "Bearer {{access_token}}",
    "Content-Type": "application/json"
  }
}
```

#### Basic Authentication
```json
{
  "authTypes": ["BASIC"],
  "headers": {
    "Authorization": "Basic {{basic_auth_token}}",
    "Content-Type": "application/json"
  }
}
```

### Integration Types

| Type | Description | Use Case |
|------|-------------|----------|
| **REST_API** | Read operations from ATS (GET requests) | Data synchronization |
| **WRITE_REST_API** | Write operations to ATS (POST/PUT/PATCH) | Data submission |
| **WEBHOOK** | Real-time event processing | Event handling |
| **REST_API_RESPONSE_HANDLER** | Response processing for complex workflows | Data transformation |
| **WRITE_API_RESPONSE_HANDLER** | Write operation response handling | Result processing |

### Common Integration Chains

#### Application Write Chain (Ashby Pattern)
1. **Start Chain** - Dummy integration for dependency support
2. **Candidate Check** - Verify candidate exists
3. **Candidate Create** - Create new candidate if needed
4. **Resume Upload** - Upload candidate resume
5. **Application Create** - Create job application
6. **Response Handler** - Process final results

#### Simple Application Write
1. **Single API Call** - Create application with candidate data
2. **Response Processing** - Handle success/error responses

## 🎯 Best Practices

### JSONata Expression Guidelines

#### Robust Date Parsing
```jsonata
$date != null and $date != "" and $count($split($date, "/")) = 3 
? $fromMillis($toMillis($split($date, "/")[3] & "-" & 
  ($number($split($date, "/")[1]) < 10 ? "0" & $split($date, "/")[1] : $split($date, "/")[1]) & 
  "-" & ($number($split($date, "/")[2]) < 10 ? "0" & $split($date, "/")[2] : $split($date, "/")[2]) & 
  "T00:00:00Z")) : null
```

#### Array Processing
```jsonata
$map($array, function($item) {
  $merge([$item, {"processed": true}])
})
```

#### Conditional Logic
```jsonata
$exists($field) and $field != null 
? $field 
: "default_value"
```

### Error Handling Patterns

#### Comprehensive Response Handlers
```json
{
  "statusCode": 200,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "$exists(results.id) and $exists($.success) and $.success=true"}],
  "jsonataConvertorExpression": "{\"applicationId\": results.id, \"candidateId\": candidateId}"
},
{
  "statusCode": 400,
  "bodyRules": [{"type": "BooleanExpressionRule", "jsonataExpression": "true"}],
  "jsonataConvertorExpression": "{\"errorMessage\": \"Bad Request - Invalid data provided\"}"
}
```

### File Upload Patterns

#### Base64 File Upload
```json
{
  "contentType": "MULTIPART_FORM_DATA",
  "requestPayload": {
    "requestBody": "{\"file\": \"${attachmentContent}\"}",
    "requestBodyConverter": [{"field": "file", "fileConvertType": "Base64ToFile"}]
  }
}
```

## 🛠️ Development Guidelines

### File Naming Conventions

- **Integration Files**: `{ats_name}_data_model_integrations.json`
- **Integration IDs**: `{ats}-{action}-{entity}` (e.g., `cornerstone-get-applications`)
- **Template Files**: `{pattern}_template.json`

### Integration ID Patterns

| Pattern | Example | Description |
|---------|---------|-------------|
| Start Chain | `{ats}-candidate-application-post-start-chain` | Dummy integration for dependencies |
| Candidate Check | `{ats}-check-candidate-already-exists` | Verify candidate existence |
| Candidate Create | `{ats}-create-candidate` | Create new candidate |
| Resume Upload | `{ats}-upload-resume` | Upload candidate resume |
| Application Create | `{ats}-create-application` | Create job application |
| Response Handler | `{ats}-application-api-response-handler-chain` | Process final results |

### Data Model Rules

#### Basic Validation
```json
"dataModelRules": [
  {
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$exists(inputData.candidate.email) and inputData.candidate.email != null"
  },
  {
    "type": "BooleanExpressionRule", 
    "jsonataExpression": "$exists(inputData.application.atsJobId) and inputData.application.atsJobId != null"
  }
]
```

#### Execution Eligibility
```json
"executionEligibilityRules": [
  {
    "type": "BooleanExpressionRule",
    "jsonataExpression": "$exists(inputData.candidate.email) and inputData.candidate.email != null and $exists(inputData.application.atsJobId) and inputData.application.atsJobId != null"
  }
]
```

## 🧪 Testing

### Unit Testing Checklist

- [ ] Test each integration individually
- [ ] Validate JSONata expressions
- [ ] Test error scenarios
- [ ] Verify authentication mechanisms

### Integration Testing Checklist

- [ ] Test complete integration chains
- [ ] Validate data flow between integrations
- [ ] Test with real ATS endpoints
- [ ] Monitor execution logs

### Error Testing Checklist

- [ ] Test all response handlers
- [ ] Validate error message formats
- [ ] Test edge cases and invalid data
- [ ] Verify timeout handling

## 🚀 Quick Start

### 1. Choose Your ATS
```bash
# Browse available integrations
ls ats_data/
```

### 2. Select Reference Pattern
- Review similar ATS integration
- Identify authentication method
- Understand data model requirements

### 3. Generate Integration
- Use templates from `ats_application_write_templates.json`
- Adapt patterns to your ATS
- Implement JSONata expressions

### 4. Test and Deploy
- Validate structure and rules
- Test with real endpoints
- Monitor execution

## 📚 Resources

### Documentation
- [ATS Application Write Rules](ats_application_write_rules.md) - Comprehensive write integration guidelines
- [Integration Templates](ats_application_write_templates.json) - Reusable patterns and templates

### External Tools
- [JSONata Playground](https://try.jsonata.org) - Test JSONata expressions
- [Curl Command Generator](https://curl.trillworks.com/) - Generate curl commands

### Supported ATS Platforms

| ATS Platform | Authentication | Data Models | Status |
|--------------|----------------|-------------|---------|
| Greenhouse | BASIC | APPLICATION, JOB, CANDIDATE | ✅ Active |
| Workday | OAUTH_2 | APPLICATION_STAGE, JOB | ✅ Active |
| SAP | SECURED_OAUTH2 | APPLICATION, JOB | ✅ Active |
| UKG | OAUTH_2 | APPLICATION, JOB | ✅ Active |
| Jobvite | BASIC | APPLICATION | ✅ Active |
| Apploi | API_KEY | APPLICATION | ✅ Active |
| iCIMS | OAUTH_2 | APPLICATION, JOB | ✅ Active |
| SmartRecruiters | OAUTH_2 | APPLICATION, JOB | ✅ Active |
| Dayforce | OAUTH_2 | APPLICATION | ✅ Active |
| Tal.ai | BASIC | APPLICATION | ✅ Active |

*And 20+ more ATS platforms...*

## 🤝 Contributing

### Adding New ATS Integration

1. **Follow Naming Convention**: `{ats_name}_data_model_integrations.json`
2. **Use Established Patterns**: Reference existing integrations
3. **Implement Comprehensive Error Handling**: Cover all response scenarios
4. **Test Thoroughly**: Validate with real ATS endpoints
5. **Document Changes**: Update relevant documentation

### Code Review Checklist

- [ ] Follows established patterns and conventions
- [ ] Implements comprehensive error handling
- [ ] Uses proper JSONata expressions
- [ ] Includes appropriate data model rules
- [ ] Tests with real ATS endpoints
- [ ] Updates documentation

## 📄 License

This project is proprietary to Joveo Technologies. All rights reserved.

## 📞 Support

For questions or support regarding ATS integrations:

- **Documentation**: Review `ats_application_write_rules.md`
- **Templates**: Use `ats_application_write_templates.json`
- **Examples**: Study existing integrations in `ats_data/`
- **Testing**: Use [JSONata Playground](https://try.jsonata.org) for expression validation

---

*Last updated: December 2024*
