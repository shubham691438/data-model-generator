# Tetra Pak Mojo Apply Integration Solution Document

**Document Version:** 1.0  
**Date:** December 2024  
**Project:** Tetra Pak Mojo Apply Integration

---

## 🔷 Section 1: Client and Context

| Field | Details |
|-------|---------|
| **Client Name** | Tetra Pak International S.A. |
| **ATS Name** | Tetra Pak Internal ATS System |
| **BRD Link** | [Tetra Pak Mojo Apply BRD](BRD-provided/Mojo Apply _Tetra Pak.xlsx) |
| **Request Type** | Mojo Apply / Easy Apply / Job Ingestion |
| **Requested By (POC)** | Tetra Pak HR Technology Team - [hr-tech@tetrapak.com](mailto:hr-tech@tetrapak.com) |

🔗 **Important:** This Solution Document is linked to the corresponding BRD document in the BRD-provided directory. The BRD document contains comprehensive business requirements and technical specifications for this integration.

---

## 🔷 Section 2: Scope of Implementation

### Integration Types:
- ✅ **Mojo Apply** - Enhanced application features with advanced candidate experience
- ✅ **Easy Apply** - Streamlined candidate application process
- ✅ **Job Ingestion** - Automated job posting and management
- ✅ **Funnel Tracking** - Candidate journey analytics and conversion tracking
- ✅ **Career Site Integration** - Seamless integration with Tetra Pak career portal

### Products Involved:
- Tetra Pak ATS System
- Joveo Mojo Apply Platform
- Tetra Pak Career Portal
- Joveo Job Ingestion Engine
- Joveo Analytics & Reporting Platform
- Tetra Pak HR Management System

### Goal of Implementation:
Implement a comprehensive Mojo Apply integration that enhances Tetra Pak's candidate experience, streamlines the application process, provides real-time job synchronization, and delivers advanced analytics for recruitment optimization while maintaining data security and compliance with Tetra Pak's HR policies.

---

## 🔷 Section 3: Solution Components

### 🧩 3.1 Authentication & Authorization

| Field | Details |
|-------|---------|
| **Auth Type** | OAuth 2.0 + API Key Authentication |
| **Token Expiry & Refresh Strategy** | JWT tokens expire in 2 hours, refresh tokens valid for 30 days with automatic refresh mechanism |
| **Security Considerations** | Multi-factor authentication (MFA), Role-based access control (RBAC), AES-256 encryption, TLS 1.3, comprehensive audit logging, GDPR compliance |

### 🗂 3.2 Data Exchange & Architecture

#### 📌 Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                    Tetra Pak Career Portal                     │
│                    (Frontend Application)                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Joveo API Gateway                           │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Load          │   Rate          │      Authentication         │
│  Balancer       │  Limiting       │      & Authorization        │
└─────────────────┴─────────────────┴─────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Joveo Service Layer                         │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Mojo Apply    │  Job Ingestion  │      Analytics Service      │
│     Service     │     Service     │                             │
├─────────────────┼─────────────────┼─────────────────────────────┤
│  Sync Service   │  Career Site    │      Funnel Tracking        │
│                 │     Service     │         Service             │
└─────────────────┴─────────────────┴─────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Tetra Pak ATS System                        │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Job Management│  Application    │      Candidate Management   │
│     Module      │   Processing    │         Module              │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

#### 💬 Data Flow Description
The architecture follows a secure, event-driven approach with:
- **Tetra Pak Career Portal** serves as the candidate-facing interface
- **Joveo API Gateway** handles authentication, rate limiting, and security
- **Joveo Service Layer** provides specialized services for Mojo Apply functionality
- **Tetra Pak ATS System** manages job postings, applications, and candidate data
- **Real-time synchronization** through secure webhooks and message queues
- **Event-driven architecture** ensures data consistency and real-time updates

### ⚙️ 3.3 Setup & Configuration

#### Prerequisites
- Tetra Pak ATS API access and credentials
- Joveo platform environment setup
- SSL certificates for secure communication
- Tetra Pak network whitelist configuration
- GDPR compliance documentation

#### Steps to Configure Systems
1. **Infrastructure Setup**
   - Configure Tetra Pak ATS API endpoints
   - Set up Joveo platform environment
   - Establish secure communication channels
   - Configure monitoring and logging

2. **Service Configuration**
   - Deploy Mojo Apply service
   - Configure Job Ingestion service
   - Set up Analytics service
   - Configure Career Site integration

3. **Data Synchronization Setup**
   - Configure job data synchronization
   - Set up application data flow
   - Configure candidate data mapping
   - Establish audit trails

#### Environment Variables
```bash
# Tetra Pak ATS Configuration
TETRAPAK_ATS_API_URL=https://ats.tetrapak.com/api/v1
TETRAPAK_ATS_API_KEY={{api_key}}
TETRAPAK_ATS_CLIENT_ID={{client_id}}
TETRAPAK_ATS_CLIENT_SECRET={{client_secret}}

# Joveo Platform Configuration
JOVEO_API_URL=https://api.joveo.com/v1
JOVEO_CUSTOMER_ID={{customer_id}}
JOVEO_ENVIRONMENT=production

# Security Configuration
JWT_SECRET={{jwt_secret}}
ENCRYPTION_KEY={{encryption_key}}
```

#### Scheduled Jobs
- **Job Synchronization:** Every 15 minutes
- **Application Data Sync:** Every 5 minutes
- **Analytics Data Processing:** Every hour
- **Data Cleanup:** Daily at 2:00 AM CET
- **Backup Jobs:** Daily at 1:00 AM CET

### 🌐 3.4 APIs Used

| API Name | Method | Endpoint | Purpose | Rate Limit | Notes |
|----------|--------|----------|---------|------------|-------|
| **Tetra Pak Jobs API** | GET | `/api/v1/jobs` | Fetch active job postings | 1000/hr | Paginated, filtered by status |
| **Tetra Pak Jobs API** | GET | `/api/v1/jobs/{id}` | Fetch specific job details | 2000/hr | Includes full job description |
| **Tetra Pak Applications API** | POST | `/api/v1/applications` | Submit new application | 500/hr | Mojo Apply integration |
| **Tetra Pak Applications API** | GET | `/api/v1/applications` | Fetch application status | 1000/hr | Paginated, filtered by date |
| **Tetra Pak Candidates API** | POST | `/api/v1/candidates` | Create candidate profile | 500/hr | Profile creation |
| **Tetra Pak Candidates API** | PUT | `/api/v1/candidates/{id}` | Update candidate profile | 500/hr | Profile updates |
| **Joveo Analytics API** | POST | `/api/v1/analytics/events` | Track application events | 10000/hr | Real-time tracking |
| **Joveo Sync API** | POST | `/api/v1/sync/trigger` | Trigger data synchronization | 100/hr | Manual sync trigger |

### 🧬 3.5 API Response Field Mapping

#### Tetra Pak Job Response
```json
{
  "id": "string",
  "title": "string",
  "department": "string",
  "location": "string",
  "description": "text",
  "requirements": "text",
  "benefits": "text",
  "employment_type": "enum: full-time, part-time, contract",
  "experience_level": "enum: entry, mid, senior, executive",
  "remote_allowed": "boolean",
  "status": "enum: active, inactive, filled, expired",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "application_deadline": "timestamp",
  "hiring_manager": {
    "name": "string",
    "email": "string"
  },
  "recruiter": {
    "name": "string",
    "email": "string"
  }
}
```

#### Tetra Pak Application Response
```json
{
  "id": "string",
  "candidate_id": "string",
  "job_id": "string",
  "status": "enum: applied, under_review, shortlisted, interviewed, rejected, hired",
  "applied_date": "timestamp",
  "source": "string",
  "resume_url": "string",
  "cover_letter": "text",
  "answers": [
    {
      "question_id": "string",
      "question": "string",
      "answer": "string"
    }
  ],
  "custom_fields": {
    "work_authorization": "string",
    "relocation_willingness": "boolean",
    "salary_expectation": "number"
  }
}
```

#### Tetra Pak Candidate Response
```json
{
  "id": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "address": {
    "street": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "postal_code": "string"
  },
  "experience_years": "number",
  "current_position": "string",
  "current_company": "string",
  "skills": ["string"],
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "graduation_year": "number"
    }
  ],
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### 🚫 3.6 Known Limitations & Unknowns

#### Known Limitations
- **API Rate Limits:** Tetra Pak ATS has conservative rate limits for data synchronization
- **File Upload Size:** Maximum resume file size of 5MB
- **Browser Support:** Requires modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- **Data Retention:** Application data retained for 2 years per Tetra Pak policy
- **Language Support:** Currently supports English, Swedish, and German

#### Unknowns
- **Peak Load Handling:** Performance during high-volume recruitment periods
- **Integration Complexity:** Some Tetra Pak ATS features may require custom development
- **Data Volume:** Expected application volume during peak hiring seasons
- **Third-party Dependencies:** Impact of Tetra Pak ATS updates on integration

### 🧾 3.7 Custom Asks / Business-Specific Logic

#### Custom Fields Required
- **Tetra Pak-specific fields:** Division, business unit, location preferences
- **Job-specific fields:** Travel requirements, language requirements, security clearance
- **Candidate-specific fields:** Work authorization status, relocation willingness, salary expectations

#### Custom Data Transformation
- **Job parsing:** Intelligent extraction of Tetra Pak-specific requirements and benefits
- **Resume parsing:** Skills extraction and matching against Tetra Pak job requirements
- **Data normalization:** Standardizing job titles and department names across Tetra Pak divisions

#### Manual Validation Required
- **High-priority positions:** Manual review of senior-level applications
- **International applications:** Visa and work authorization validation
- **Technical roles:** Skills assessment and technical evaluation
- **Integration errors:** Manual resolution of data synchronization conflicts

### 🗓 3.8 Timeline & Milestones

| Milestone | Planned Date | Actual Date | Owner | Status |
|-----------|--------------|-------------|-------|--------|
| **Project Kickoff** | Week 1 | TBD | Project Manager | ⏳ Planned |
| **Requirements Finalization** | Week 2 | TBD | Business Analyst | ⏳ Planned |
| **Technical Architecture** | Week 4 | TBD | Technical Lead | ⏳ Planned |
| **Development Phase 1** | Week 8 | TBD | Development Team | ⏳ Planned |
| **Integration Testing** | Week 12 | TBD | QA Team | ⏳ Planned |
| **User Acceptance Testing** | Week 14 | TBD | Tetra Pak HR Team | ⏳ Planned |
| **Production Deployment** | Week 16 | TBD | DevOps Team | ⏳ Planned |
| **Go-Live & Support** | Week 17 | TBD | Support Team | ⏳ Planned |

### 🔗 3.9 Dependencies

| Dependency | Owner | Risk of Delay |
|------------|-------|----------------|
| **Tetra Pak ATS API Access** | Tetra Pak IT Team | Medium - API credentials and documentation |
| **Tetra Pak Network Configuration** | Tetra Pak IT Team | Low - Standard firewall configuration |
| **Joveo Platform Setup** | Joveo DevOps Team | Low - Standard platform deployment |
| **Security Review** | Tetra Pak Security Team | Medium - Corporate security compliance |
| **User Training** | Tetra Pak HR Team | Low - Training materials in development |
| **Data Migration** | Tetra Pak Data Team | Medium - Historical data migration |

---

## 🔷 Section 4: Review & Sign-off

| Role | Name | Reviewed (Y/N) | Comments |
|------|------|----------------|----------|
| **Technical Lead** | TBD | ⏳ Pending | Technical architecture review |
| **Security Engineer** | TBD | ⏳ Pending | Security compliance review |
| **Business Analyst** | TBD | ⏳ Pending | Business requirements validation |
| **DevOps Engineer** | TBD | ⏳ Pending | Infrastructure readiness review |
| **Project Manager** | TBD | ⏳ Pending | Overall project alignment |
| **Tetra Pak HR Director** | TBD | ⏳ Pending | Business value validation |
| **Tetra Pak IT Director** | TBD | ⏳ Pending | Technical feasibility review |

---

## 📎 Appendix

### Jira Ticket Link
- **Epic:** [TETRA-1000: Mojo Apply Integration](https://tetrapak.atlassian.net/browse/TETRA-1000)
- **Phase 1:** [TETRA-1001: Foundation & API Integration](https://tetrapak.atlassian.net/browse/TETRA-1001)
- **Phase 2:** [TETRA-1002: Mojo Apply Implementation](https://tetrapak.atlassian.net/browse/TETRA-1002)
- **Phase 3:** [TETRA-1003: Testing & Deployment](https://tetrapak.atlassian.net/browse/TETRA-1003)

### Postman Collection
- **Tetra Pak ATS API Collection:** [Tetra Pak ATS APIs](https://api.postman.com/collections/tetrapak-ats)
- **Joveo Integration APIs:** [Joveo Integration APIs](https://api.postman.com/collections/joveo-integration)
- **End-to-End Testing:** [Integration Tests](https://api.postman.com/collections/integration-tests)

### Sample Payloads
- **Job Creation:** [job-create.json](sample-payloads/job-create.json)
- **Application Submission:** [application-submit.json](sample-payloads/application-submit.json)
- **Candidate Profile:** [candidate-profile.json](sample-payloads/candidate-profile.json)

### Knowledge Base Docs
- **Technical Architecture:** [Tetra Pak Integration Architecture](technical-docs/architecture.md)
- **API Documentation:** [Tetra Pak ATS API Reference](api-docs/tetrapak-ats-api.md)
- **Deployment Guide:** [Deployment Instructions](deployment/tetrapak-deployment.md)
- **User Guide:** [Tetra Pak HR User Guide](user-guides/tetrapak-hr-guide.md)

### Data Model Integration Files
- **Job Integration:** [tetrapak_job_data_model_integrations.json](data-models/tetrapak_job_data_model_integrations.json)
- **Application Integration:** [tetrapak_application_data_model_integrations.json](data-models/tetrapak_application_data_model_integrations.json)
- **Candidate Integration:** [tetrapak_candidate_data_model_integrations.json](data-models/tetrapak_candidate_data_model_integrations.json)

---

**Document Control**
- **Version:** 1.0
- **Last Updated:** December 2024
- **Next Review:** January 2025
- **Prepared By:** Joveo Development Team
- **Reviewed By:** Tetra Pak HR Technology Team
