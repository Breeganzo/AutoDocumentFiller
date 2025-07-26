# AutoDocumentFiller
Automatically generate documentation (PR, tickets, specs) in Confluence or GitLab


docautofiller/
│
├── terraform/
│   └── main.tf                        # Sample Terraform code
├── agents/
│   └── doc_autofiller_agent.py        # Agent logic for LLM prompting
├── apis/
│   ├── gitlab_client.py               # GitLab API client
│   └── confluence_client.py           # Confluence API client
├── prompts/
│   └── templates.txt                  # Prompt templates for AI
├── tickets/
│   └── ticket_template.txt            # Ticket template text
├── specs/
│   └── spec_template.txt              # Spec template text
├── main.py                            # Entrypoint, full pipeline
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation (see below)
└── tests/
    └── test_doc_autofiller.py         # Unit/integration tests

# DocAutoFiller: Automated Documentation for Infrastructure as Code

This project demonstrates how to **automatically generate documentation** (PR/MR descriptions, tickets, specs) for Terraform infrastructure changes. When you update the code (e.g., increase EC2 instance count), the system:

- Creates a new GitLab branch and commits the change.
- Auto-generates a Merge Request (MR/PR) with an LLM-powered description.
- Outputs a ticket template describing the change.
- Publishes a detailed specification page in Confluence.

## Project Structure

- **terraform/main.tf:** Your sample Terraform AWS EC2 configuration.
- **agents/:** Agent logic for AI writing.
- **apis/:** API clients for GitLab and Confluence.
- **prompts/, tickets/, specs/:** Templates for description, tickets, and specs.
- **main.py:** Orchestrates the code, from committing to documentation.
- **tests/:** Minimal tests.

## Prerequisites

- Python 3.8+
- **VSCode** or your preferred editor.
- **Git** installed
- **GitLab** account and API Token
- **Confluence** account and API Token
- **OpenAI API key** (or update agent logic for another LLM provider)
- Your GitLab project must already exist (store its numeric project ID)

## Setup

1. **Clone this repository**  
2. **Install dependencies:**  
