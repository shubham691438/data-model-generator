# Prompts Directory

This directory contains prompt templates and instructions for generating solution documents from Business Requirements Documents (BRDs).

## Available Prompts

### 1. `brd_to_solution_doc_prompt.txt`
Comprehensive prompt template for BRD to solution document generation, including:
- Primary prompt template
- Detailed prompt variations
- Integration-specific prompts
- Quality assurance prompts
- Usage instructions and best practices

## Quick Start

### Basic Usage
Copy the primary prompt template and customize it for your specific BRD:

```
Added the BRD in the BRD-Provided Folder, generate the solution document in the solution-doc-generated directory

1) Go through the template BRD-templates and solution-doc-templates, take .cursor rules into consideration to generate the solution doc
2) Create the solution-doc for the following file BRD in the .md format
3) Update the rule accordingly

Note: - if there is a need to use the python script and downloading libraries generate the virtual environment
```

### Advanced Usage
For more complex scenarios, use the detailed prompt variations:
- **New BRD Processing**: For single BRD file processing
- **Batch Processing**: For multiple BRD files
- **Template Updates**: For updating templates and rules
- **Integration-Specific**: For specific integration types (Mojo Apply, Easy Apply, CRM)

## Integration Types Supported

- **Mojo Apply**: Joveo's hosted application forms
- **Easy Apply**: ATS-integrated application buttons
- **CRM Integration**: Customer relationship management systems
- **Job Ingestion**: Job posting and management
- **Career Site**: Company career page integration
- **Chatbot**: AI-powered candidate interaction

## File Structure

```
prompts/
├── README.md                           # This file
├── brd_to_solution_doc_prompt.txt     # Main prompt template
└── [future prompt files]              # Additional specialized prompts
```

## Customization

Each prompt can be customized based on:
- **Client Requirements**: Specific client needs and constraints
- **Integration Type**: Different integration approaches
- **Document Format**: Markdown, Word, or other formats
- **Quality Level**: Draft, review, or final versions

## Best Practices

1. **Always specify the BRD file name** when using prompts
2. **Include integration type** in your request
3. **Mention any special requirements** or constraints
4. **Specify output format** (markdown, word, etc.)
5. **Request validation** for critical documents

## Examples

### Example 1: Basic Mojo Apply
```
Process the "Client_Name_Mojo_Apply.xlsx" BRD file and generate a solution document for Mojo Apply integration.
```

### Example 2: Complex Integration
```
Process the "Enterprise_Client_CRM.xlsx" BRD file for CRM integration with custom branding and domain access requirements.
```

### Example 3: Batch Processing
```
Process all BRD files in the BRD-provided directory and generate solution documents for each, focusing on Mojo Apply integrations.
```

## Support

For questions or issues with prompt usage:
1. Check the .cursorrules file for project guidelines
2. Review the BRD templates for expected structure
3. Examine existing solution documents for formatting examples
4. Consult the main project README for technical details
