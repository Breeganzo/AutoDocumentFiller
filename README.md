# AutoDocFiller Project

## Project Overview
AutoDocFiller is an automated documentation and workflow management system that integrates multiple services (GitLab, JIRA, Confluence) to streamline the infrastructure change process. It uses AI to generate human-readable documentation, summaries, and specifications.

## Key Features
- 🔄 **Automated Workflow Integration**: Seamlessly connects GitLab, JIRA, and Confluence
- 🤖 **AI-Powered Documentation**: Uses Perplexity AI for generating clear, context-aware documentation
- 📝 **Smart Ticket Management**: Creates and updates JIRA tickets with detailed summaries
- 📚 **Specification Generation**: Automatically creates technical specifications in Confluence
- 💾 **Local Storage**: Maintains local copies of all generated content for backup and reference

## High-Level Workflow
```mermaid
graph TD
    A[Infrastructure Change] --> B[Create GitLab Branch]
    B --> C[Generate Merge Request]
    C --> D[Create JIRA Ticket]
    D --> E[Generate Tech Spec]
    E --> F[Update Confluence]
    F --> G[Store Summaries Locally]
```

## Components
1. **GitLab Integration**
   - Manages code changes
   - Creates branches and merge requests
   - Tracks infrastructure modifications

2. **JIRA Integration**
   - Creates and updates tickets
   - Tracks work progress
   - Generates AI-powered summaries

3. **Confluence Integration**
   - Stores technical specifications
   - Maintains documentation history
   - Ensures knowledge persistence

4. **Local Storage System**
   - Maintains JSON and TXT formats
   - Organizes by category (JIRA, Confluence, Merge Requests)
   - Provides easy access to historical data

## Project Structure
```
AutoDocumentFiller/
├── agents/                 # AI Agents for content generation
├── apis/                  # API clients for external services
├── Prompts/               # Templates for AI generation
├── specs/                 # Specification templates
├── summaries/            # Local storage for generated content
│   ├── jira/            
│   ├── confluence/       
│   └── merge_requests/   
└── terraform/            # Infrastructure code
```

## Getting Started
1. Set up environment variables:
   ```bash
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_USER=your-email
   JIRA_TOKEN=your-token
   GITLAB_URL=your-gitlab-url
   GITLAB_TOKEN=your-token
   CONFLUENCE_SPACE=your-space
   ```

2. Run the main workflow:
   ```bash
   python main.py
   ```

## Use Cases
1. **Infrastructure Changes**
   - Automates documentation for terraform changes
   - Creates complete audit trail
   - Maintains consistent documentation

2. **Status Updates**
   - Generates concise ticket summaries
   - Updates JIRA tickets automatically
   - Provides quick access to historical changes

3. **Documentation Management**
   - Centralizes technical specifications
   - Maintains version history
   - Ensures documentation consistency

## Benefits
- ⏱️ **Time Savings**: Automates repetitive documentation tasks
- 🎯 **Consistency**: Ensures uniform documentation across projects
- 📊 **Traceability**: Maintains clear links between changes, tickets, and docs
- 🤝 **Collaboration**: Improves team communication through centralized documentation

For detailed technical documentation, see [TECHNICAL_DOCS.md](./TECHNICAL_DOCS.md)
