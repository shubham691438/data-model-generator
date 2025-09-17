#!/usr/bin/env python3
"""
Solution Document Generator for Data Model Generator
Generates comprehensive solution documents from processed BRD data
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

class SolutionDocumentGenerator:
    def __init__(self, data_file="solution-doc-generated/processed_brd_data.json", 
                 output_directory="solution-doc-generated"):
        self.data_file = Path(data_file)
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(exist_ok=True)
        
    def load_processed_data(self):
        """Load processed BRD data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Data file {self.data_file} not found. Please run process_brd.py first.")
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    
    def generate_solution_document(self, client_name, brd_data):
        """Generate solution document for a specific client"""
        
        # Extract client information
        customer_details = brd_data.get('Customer Details', {})
        features_request = brd_data.get('Features Request', {})
        integration_type = brd_data.get('Integration Type', 'Unknown')
        
        # Determine integration type from features or data
        if brd_data.get('Integration Type'):
            integration_type = brd_data.get('Integration Type')
        elif 'Mojo Apply' in str(features_request) or 'Mojo' in str(brd_data):
            integration_type = 'Mojo Apply'
        elif 'S2S' in str(brd_data) or 'Server-to-Server' in str(brd_data):
            integration_type = 'S2S Funnel Tracking'
        elif 'CRM' in str(brd_data):
            integration_type = 'CRM Integration'
        
        # Generate document content
        doc_content = self._generate_document_content(client_name, brd_data, integration_type)
        
        # Save document
        filename = f"{client_name}_{integration_type.replace(' ', '_')}_Solution_Document.md"
        output_path = self.output_directory / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"Solution document generated: {output_path}")
        return output_path
    
    def _generate_document_content(self, client_name, brd_data, integration_type):
        """Generate the complete solution document content"""
        
        customer_details = brd_data.get('Customer Details', {})
        features_request = brd_data.get('Features Request', {})
        static_questions = brd_data.get('Static Client Level Question', [])
        job_filter_questions = brd_data.get('Job Filter Level Questions', [])
        apply_form = brd_data.get('Apply Form', {})
        domain_access = brd_data.get('Domain Access', {})
        
        # Clean client name for display
        display_name = customer_details.get('Client Name', client_name)
        
        content = f"""# 📄 Solution Design Document

## Client: {display_name}
**ATS:** {customer_details.get('ATS', 'To be determined')}  
**ATS API Documentation:** To be provided  
**Business Requirements Document (BRD):** Attached  
**Prime Ticket:** To be created  

**Date:** {datetime.now().strftime('%d %B %Y')}  
**Prepared by:** Technical Team  
**Reviewed by:** Technical Lead  

---

## 🎯 Objective

The primary objective of this project is to implement **{integration_type}** integration for {display_name} to enable seamless job application processing and data tracking.

**Integration Needs:** {self._get_integration_needs(features_request, integration_type)}

---

## 🔷 Section 1: Client and Context

### Client Information
- **Client Name:** {display_name}
- **CRM Client ID:** {customer_details.get('CRM Client ID', 'To be assigned')}
- **Customer Career Site:** {customer_details.get('Career Site URL', 'To be provided')}
- **Integration Type:** {integration_type}

### Integration Scope
This implementation focuses on enabling **{integration_type}** functionality to provide a seamless job application experience and data tracking for candidates.

---

## 🔷 Section 2: Scope of Implementation

### Integration Types:
{self._format_integration_types(features_request, integration_type)}

### Products Involved:
{self._format_products_involved(integration_type)}

---

## 🔷 Section 3: Solution Components

### 🗂 3.1 Data Exchange & Architecture

#### 📌 Diagram
{self._generate_architecture_diagram(integration_type)}

#### 💬 Data Flow Description
{self._generate_data_flow_description(integration_type)}

### ⚙️ 3.2 Solution Flow

{self._generate_solution_flow(integration_type)}

---

## 🔷 Section 4: Features Implementation

{self._format_features_implementation(features_request, integration_type)}

---

## 🔷 Section 5: Technical Implementation

### 5.1 Integration Requirements

**API Endpoints:**
{self._format_api_endpoints(integration_type)}

**Data Format:**
{self._format_data_format(integration_type)}

### 5.2 Security Considerations

- Secure data transmission (HTTPS)
- Data validation and sanitization
- Privacy compliance (GDPR/CCPA)
- Access control and authentication

### 5.3 Performance Requirements

- Response time: < 3 seconds
- Data processing: < 5 seconds
- 99.9% uptime availability
- Support for concurrent users

---

## 🔷 Section 6: Testing Strategy

### 6.1 Test Scenarios

{self._format_test_scenarios(integration_type)}

### 6.2 Success Criteria

- All functionality works as expected
- Data validation works correctly
- Successful integration with target systems
- User-friendly interface
- Performance meets requirements

---

## 🔷 Section 7: Deployment Plan

### 7.1 Implementation Phases

{self._format_implementation_phases(integration_type)}

### 7.2 Rollout Strategy

- Staged deployment approach
- Pilot testing with limited scope
- Full rollout after validation
- Post-deployment monitoring

---

## 🔷 Section 8: Support and Maintenance

### 8.1 Ongoing Support

- 24/7 technical support
- Regular system monitoring
- Performance optimization
- Issue resolution

### 8.2 Maintenance Activities

- Regular security updates
- Performance monitoring
- Feature enhancements
- User feedback incorporation

---

## 🔷 Section 9: Risk Assessment

### 9.1 Identified Risks

{self._format_risk_assessment(integration_type)}

### 9.2 Mitigation Strategies

- Comprehensive testing approach
- Phased implementation
- Regular stakeholder communication
- Contingency planning

---

## 🔷 Section 10: Conclusion

This solution document outlines the complete implementation plan for {integration_type} integration for {display_name}. The proposed solution provides a robust, scalable, and user-friendly platform that meets all specified requirements.

**Next Steps:**
1. Review and approve this solution document
2. Begin Phase 1 implementation
3. Schedule regular progress reviews
4. Prepare for user acceptance testing

---

*Document Generated on: {datetime.now().strftime('%d %B %Y at %H:%M')}*  
*Version: 1.0*  
*Status: Draft for Review*
"""
        
        return content
    
    def _get_integration_needs(self, features_request, integration_type):
        """Get integration needs based on features and type"""
        if integration_type == 'S2S Funnel Tracking':
            return "Need to enable Server-to-Server funnel tracking integration"
        elif integration_type == 'Mojo Apply':
            return "Need to enable Mojo Apply integration"
        elif integration_type == 'CRM Integration':
            return "Need to enable CRM integration"
        else:
            return f"Need to enable {integration_type} integration"
    
    def _format_integration_types(self, features_request, integration_type):
        """Format integration types section"""
        if integration_type == 'S2S Funnel Tracking':
            return """- ✅ **S2S Funnel Tracking** - Server-to-server data tracking
- ❌ **Mojo Apply** - Not requested
- ❌ **Client Branded Form** - Not requested
- ❌ **Domain Access** - Not requested"""
        elif integration_type == 'Mojo Apply':
            return """- ✅ **Mojo Apply** - Joveo's hosted application offering
- ❌ **Client Branded Form** - Not requested
- ❌ **Domain Access** - Not requested
- ❌ **Visual Branding** - Not requested"""
        else:
            return f"- ✅ **{integration_type}** - Primary integration type"
    
    def _format_products_involved(self, integration_type):
        """Format products involved section"""
        if integration_type == 'S2S Funnel Tracking':
            return """- **S2S Tracking Platform**
- **Joveo CRM Integration**
- **Data Analytics Dashboard**"""
        elif integration_type == 'Mojo Apply':
            return """- **Mojo Apply Platform**
- **Joveo CRM Integration**"""
        else:
            return f"- **{integration_type} Platform**\n- **Joveo CRM Integration**"""
    
    def _generate_architecture_diagram(self, integration_type):
        """Generate architecture diagram based on integration type"""
        if integration_type == 'S2S Funnel Tracking':
            return """```
[Client ATS] → [S2S Tracking] → [Joveo Processing] → [Analytics Dashboard]
     ↓              ↓                    ↓                ↓
[Job Data] → [Funnel Events] → [Data Processing] → [Reporting]
```"""
        elif integration_type == 'Mojo Apply':
            return """```
[Job Board] → [Mojo Apply Form] → [Joveo Processing] → [Client ATS]
     ↓              ↓                    ↓                ↓
[Job Details] → [Application Data] → [Data Validation] → [ATS Integration]
```"""
        else:
            return """```
[Source System] → [Integration Layer] → [Joveo Processing] → [Target System]
     ↓                    ↓                    ↓                ↓
[Source Data] → [Data Transformation] → [Validation] → [Target Integration]
```"""
    
    def _generate_data_flow_description(self, integration_type):
        """Generate data flow description based on integration type"""
        if integration_type == 'S2S Funnel Tracking':
            return "The process begins with job data from the client's ATS system. Funnel tracking events are captured and processed through Joveo's S2S tracking platform. The processed data is then made available through analytics dashboards for comprehensive reporting and insights."
        elif integration_type == 'Mojo Apply':
            return "The process begins with jobs published from the client's career site. Users visit the Joveo-hosted job application page where they fill in the Mojo Apply form. The application data is processed, validated, and integrated with the client's ATS system."
        else:
            return f"The process involves data exchange between source and target systems through Joveo's {integration_type} platform, ensuring seamless integration and data flow."
    
    def _generate_solution_flow(self, integration_type):
        """Generate solution flow steps based on integration type"""
        if integration_type == 'S2S Funnel Tracking':
            return """1. **Data Collection**: Capture job and application data from client ATS
2. **Event Tracking**: Monitor funnel events and user interactions
3. **Data Processing**: Process and validate tracking data
4. **Analytics Generation**: Generate insights and reports
5. **Dashboard Updates**: Update analytics dashboards with latest data
6. **Reporting**: Provide comprehensive reporting to stakeholders"""
        elif integration_type == 'Mojo Apply':
            return """1. **Job Discovery**: Candidates discover jobs through the client's career site
2. **Application Initiation**: Candidates click "Apply" and are redirected to Mojo Apply form
3. **Form Completion**: Candidates fill out the application form with required information
4. **Data Processing**: Joveo processes and validates the application data
5. **ATS Integration**: Processed data is sent to the client's ATS system
6. **Confirmation**: Candidate receives confirmation of successful application"""
        else:
            return f"""1. **Data Collection**: Gather data from source systems
2. **Data Processing**: Process and validate collected data
3. **Integration**: Connect with target systems
4. **Data Synchronization**: Ensure data consistency across systems
5. **Monitoring**: Monitor integration health and performance
6. **Reporting**: Provide status updates and analytics"""
    
    def _format_features_implementation(self, features_request, integration_type):
        """Format features implementation section"""
        if integration_type == 'S2S Funnel Tracking':
            return """### 4.1 S2S Funnel Tracking Configuration

**Status:** ✅ **Enabled**

**Description:** Server-to-server funnel tracking that allows:
- Real-time data capture from ATS systems
- Comprehensive funnel analytics
- Custom event tracking
- Advanced reporting capabilities

**Implementation Details:**

#### S2S Funnel Tracking
- **Status:** ✅ **Enabled**
- **Description:** Server-to-server integration for comprehensive funnel tracking and analytics
- **Comments:** Provides real-time insights into candidate journey and application funnel performance"""
        elif integration_type == 'Mojo Apply':
            return """### 4.1 Mojo Apply Configuration

**Status:** ✅ **Enabled**

**Description:** Joveo's hosted application offering that allows:
- Forms hosted on Joveo's domain
- Questions based on custom job level filters
- Multi-page form capability
- Custom question configuration

**Implementation Details:**

#### MOJO Apply 
- **Status:** ✅ **Enabled**
- **Description:** Joveo's hosted application offering with customizable forms and questions
- **Comments:** Provides seamless application experience for candidates"""
        else:
            return f"""### 4.1 {integration_type} Configuration

**Status:** ✅ **Enabled**

**Description:** {integration_type} integration that provides:
- Seamless data exchange
- Real-time synchronization
- Comprehensive monitoring
- Advanced analytics

**Implementation Details:**

#### {integration_type}
- **Status:** ✅ **Enabled**
- **Description:** Complete {integration_type} solution for data processing and integration
- **Comments:** Provides robust integration capabilities"""
    
    def _format_api_endpoints(self, integration_type):
        """Format API endpoints based on integration type"""
        if integration_type == 'S2S Funnel Tracking':
            return """- Funnel event tracking endpoints
- Data analytics API
- Real-time reporting endpoints
- Historical data retrieval"""
        elif integration_type == 'Mojo Apply':
            return """- Job data retrieval from client ATS
- Application data submission to client ATS
- Question configuration management
- Form rendering endpoints"""
        else:
            return f"""- Data exchange endpoints
- Integration status monitoring
- Configuration management
- Analytics and reporting"""
    
    def _format_data_format(self, integration_type):
        """Format data format requirements"""
        return """- JSON for API communication
- CSV export capability for data analysis
- Standardized data schema
- Real-time data streaming support"""
    
    def _format_test_scenarios(self, integration_type):
        """Format test scenarios based on integration type"""
        if integration_type == 'S2S Funnel Tracking':
            return """1. **Data Tracking Testing**
   - Event capture accuracy
   - Data processing validation
   - Analytics generation
   - Dashboard functionality

2. **Integration Testing**
   - ATS connectivity
   - Data mapping accuracy
   - Error handling
   - Performance testing

3. **User Acceptance Testing**
   - End-to-end data flow
   - Report accuracy
   - Dashboard usability
   - Performance validation"""
        elif integration_type == 'Mojo Apply':
            return """1. **Form Functionality Testing**
   - Form rendering and display
   - Question validation
   - Multi-page navigation
   - Data submission

2. **Integration Testing**
   - ATS connectivity
   - Data mapping accuracy
   - Error handling
   - Performance testing

3. **User Acceptance Testing**
   - End-to-end application flow
   - Cross-browser compatibility
   - Mobile responsiveness
   - User experience validation"""
        else:
            return f"""1. **{integration_type} Functionality Testing**
   - Core feature validation
   - Data processing accuracy
   - Integration connectivity
   - Performance testing

2. **System Integration Testing**
   - End-to-end data flow
   - Error handling
   - Security validation
   - Scalability testing

3. **User Acceptance Testing**
   - Complete workflow validation
   - User interface testing
   - Performance requirements
   - Business logic validation"""
    
    def _format_implementation_phases(self, integration_type):
        """Format implementation phases"""
        if integration_type == 'S2S Funnel Tracking':
            return """**Phase 1: Setup and Configuration**
- S2S tracking platform setup
- ATS integration configuration
- Event tracking setup

**Phase 2: Integration Development**
- Data processing implementation
- Analytics dashboard development
- Testing and validation

**Phase 3: Deployment and Go-Live**
- Production deployment
- User acceptance testing
- Go-live support"""
        elif integration_type == 'Mojo Apply':
            return """**Phase 1: Setup and Configuration**
- Mojo Apply platform setup
- Question configuration
- Form customization

**Phase 2: Integration Development**
- ATS API integration
- Data mapping implementation
- Testing and validation

**Phase 3: Deployment and Go-Live**
- Production deployment
- User acceptance testing
- Go-live support"""
        else:
            return f"""**Phase 1: Setup and Configuration**
- {integration_type} platform setup
- System configuration
- Initial setup

**Phase 2: Integration Development**
- Core functionality development
- Integration implementation
- Testing and validation

**Phase 3: Deployment and Go-Live**
- Production deployment
- User acceptance testing
- Go-live support"""
    
    def _format_risk_assessment(self, integration_type):
        """Format risk assessment section"""
        return """1. **Technical Risks**
   - System compatibility issues
   - Data mapping challenges
   - Performance bottlenecks

2. **Business Risks**
   - User adoption challenges
   - Integration delays
   - Data quality issues

3. **Operational Risks**
   - System downtime
   - Data security concerns
   - Maintenance complexity"""
    
    def generate_all_solution_documents(self):
        """Generate solution documents for all processed BRD data"""
        data = self.load_processed_data()
        
        if not data:
            print("No processed data found. Please run process_brd.py first.")
            return
        
        generated_docs = []
        for client_name, brd_data in data.items():
            try:
                doc_path = self.generate_solution_document(client_name, brd_data)
                generated_docs.append(doc_path)
            except Exception as e:
                print(f"Error generating document for {client_name}: {e}")
        
        print(f"\nGenerated {len(generated_docs)} solution documents:")
        for doc in generated_docs:
            print(f"  - {doc}")
        
        return generated_docs

if __name__ == "__main__":
    generator = SolutionDocumentGenerator()
    generator.generate_all_solution_documents()
