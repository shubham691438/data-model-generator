# Data Model Generator

A comprehensive toolkit for generating solution documents from Business Requirements Documents (BRDs) and managing ATS (Applicant Tracking System) data model integrations. This project provides standardized patterns, templates, and workflows for creating robust integrations with various ATS platforms and generating client-ready solution documents.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [BRD to Solution Document Generation](#brd-to-solution-document-generation)
- [ATS Integration Workflow](#ats-integration-workflow)
- [Data Models](#data-models)
- [Integration Patterns](#integration-patterns)
- [Best Practices](#best-practices)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Contributing](#contributing)

## 🎯 Overview

The Data Model Generator is designed to streamline two main processes:

### 1. BRD to Solution Document Generation
- **Automated Document Creation**: Generate comprehensive solution documents from Business Requirements Documents
- **Template-Based Processing**: Use standardized BRD templates for consistent output
- **Multi-Format Support**: Generate documents in Markdown and Word formats
- **Client-Ready Output**: Professional documents ready for client review

### 2. ATS Integration Management
- **Standardized Integration Patterns**: Consistent structure across all ATS integrations
- **Template-Based Development**: Pre-built templates for common integration scenarios
- **Comprehensive Rules Engine**: Validation and execution rules for data models
- **Multi-ATS Support**: Support for 30+ ATS platforms including Greenhouse, Workday, SAP, UKG, and more

## 📁 Project Structure

```
data-model-generator/
├── BRD-provided/                               # Input BRD files from clients
│   └── Mojo Apply _Tetra Pak.xlsx
├── BRD_Template/                              # BRD templates for different integration types
│   ├── Mojo + Easy Apply _ BRD Template .xlsx
│   ├── CRM _ BRD Template .xlsx
│   └── ... (other integration templates)
├── solution_doc_template/                     # Solution document templates (Word format)
│   ├── Solution Doc For Family First.docx
│   └── Solution Document_ ScionHealth.docx
├── solution-doc-generated/                    # Generated solution documents (Markdown format)
│   └── Tetra_Pak_Mojo_Apply_Solution_Document.md
├── prompts/                                   # Prompt templates for document generation
│   ├── brd_to_solution_doc_prompt.txt
│   └── README.md
├── ats_data/                                  # ATS integration files
│   ├── greenhouse_data_model_integrations.json
│   ├── workday_data_model_integrations.json
│   ├── sap_data_model_integrations.json
│   └── ... (30+ ATS integrations)
├── venv/                                      # Python virtual environment
├── .cursorrules                               # Cursor IDE rules and guidelines
├── requirements.txt                           # Python dependencies
├── .gitignore                                 # Git ignore rules
└── README.md                                  # This file
```

### Key Files

#### BRD to Solution Document Generation
- **`BRD-provided/`**: Input BRD files from clients
- **`BRD_Template/`**: Standardized BRD templates for different integration types
- **`solution_doc_template/`**: Word document templates for solution documents
- **`solution-doc-generated/`**: Generated solution documents in Markdown format
- **`prompts/`**: Prompt templates for automated document generation
- **`.cursorrules`**: Cursor IDE rules and guidelines for document generation

#### ATS Integration Management
- **`ats_data/`**: Contains individual ATS integration configurations
- **`ats_application_write_rules.md`**: Comprehensive rules for APPLICATION data model writes
- **`ats_application_write_templates.json`**: Reusable templates for common patterns
- **Ashby files**: Reference implementations and webhook configurations

## 📄 BRD to Solution Document Generation

### Quick Start

1. **Place BRD File**: Add your BRD Excel file to the `BRD-provided/` directory
2. **Use Prompt Template**: Copy the prompt from `prompts/brd_to_solution_doc_prompt.txt`
3. **Generate Document**: Run the generation process using Cursor AI
4. **Review Output**: Check the generated document in `solution-doc-generated/`

### Supported Integration Types

- **Mojo Apply**: Joveo's hosted application forms
- **Easy Apply**: ATS-integrated application buttons  
- **CRM Integration**: Customer relationship management systems
- **Job Ingestion**: Job posting and management
- **Career Site**: Company career page integration
- **Chatbot**: AI-powered candidate interaction

### Document Structure

Generated solution documents include:
- Client information and context
- Integration scope and objectives
- Technical implementation details
- Features configuration
- Question setup (static and job-filter level)
- Testing strategy and deployment plan
- Risk assessment and support details

### Usage Example

```
Added the BRD in the BRD-Provided Folder, generate the solution document in the solution-doc-generated directory

1) Go through the template BRD-templates and solution-doc-templates, take .cursor rules into consideration to generate the solution doc
2) Create the solution-doc for the following file BRD in the .md format
3) Update the rule accordingly

Note: - if there is a need to use the python script and downloading libraries generate the virtual environment
```

## 🔄 ATS Integration Workflow

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
Testing prompt: - 
For solution Doc- 
"Added the BRD in the BRD-Provided Folder, generate the solution document in the solution-doc-generated directory
1) go throught the template BRD-templates and solution-doc-templates, take .cursor rules in considaration to g   enerate the solution doc 
2) Create the solution-doc for the following file BRD in the .md format
3) update the rule accordingly
Note: - if there is a need to use the python script and downloading libraries generate the virtual Enviroment
"


*Last updated: December 2024*
