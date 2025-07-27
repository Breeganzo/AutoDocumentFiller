# AutoDocFiller Project Explanation

This document explains how the different components of the AutoDocFiller project work together, with a special focus on the agents and JIRA integration.

## Overview of Components

### 1. Agents
There are two main agent classes:

#### DocAutoFillerAgent (in `agents/doc_autofiller_agent.py`)
This agent is responsible for:
- Generating pull request descriptions
- Creating documentation tickets
- Generating technical specifications
- Uses Perplexity AI for text generation
- Takes context from terraform changes and generates human-readable documentation

#### TicketSummarizerAgent (in `agents/ticket_summarizer_agent.py`)
This agent:
- Takes JIRA ticket information as input
- Uses Perplexity AI to generate concise summaries
- Useful for standup meetings and quick status updates
- Processes ticket title, description, status, and recent comments

### 2. API Clients

#### JiraClient (in `apis/jira_client.py`)
- Connects to your JIRA instance using authentication from environment variables
- Retrieves ticket information including:
  - Title
  - Description
  - Current status
  - Reporter name
  - Assignee
  - Latest comments (last 3)
- Used by the TicketSummarizerAgent to get ticket details

#### GitLabClient (in `apis/gitlab_client.py`)
- Handles GitLab operations
- Creates branches
- Commits changes
- Creates merge requests

#### ConfluenceClient (in `apis/confluence_client.py`)
- Manages Confluence documentation
- Creates and updates documentation pages
- Used for storing generated specifications

## Workflow Example

1. When you run `main.py`, the following happens:

```
GitLab Operations:
└── Creates a new branch
└── Commits terraform changes
└── Creates a merge request with AI-generated description

Documentation Generation:
└── Generates ticket content using DocAutoFillerAgent
└── Creates/updates Confluence page with specifications

JIRA Integration:
└── When summarize_ticket() is called:
    └── JiraClient fetches ticket details from JIRA
    └── TicketSummarizerAgent generates a summary
    └── Summary is displayed or used in other processes
```

### How JIRA is Used

JIRA integration happens in two main places:

1. In `main.py`:
   ```python
   def summarize_ticket(ticket_id):
       jira_client = JiraClient()
       details = jira_client.get_ticket_info(ticket_id)
       summary = agent.summarize_ticket(details)
   ```

2. In `jira_client.py`:
   ```python
   def get_ticket_info(self, ticket_id):
       # Fetches complete ticket information
       # Including title, description, status, etc.
   ```

The JIRA workflow:
1. You provide a ticket ID (e.g., "SMP-7")
2. JiraClient connects to your JIRA instance
3. Retrieves all ticket information
4. TicketSummarizerAgent processes this information
5. Generates a concise, standup-friendly summary

## Environment Setup

To use JIRA functionality, you need these environment variables:
- `JIRA_URL`: Your Atlassian domain (e.g., https://yourcompany.atlassian.net)
- `JIRA_USER`: Your Atlassian email
- `JIRA_TOKEN`: Your JIRA API token

## Example Usage

```python
# To summarize a JIRA ticket:
ticket_id = "PROJECT-123"
jira_client = JiraClient()
ticket_details = jira_client.get_ticket_info(ticket_id)
summarizer = TicketSummarizerAgent()
summary = summarizer.summarize_ticket(ticket_details)
print(summary)
```

This will fetch the ticket details from JIRA and generate a concise summary using the Perplexity AI model.
