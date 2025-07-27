docautofiller/
│
├── agents/
│   ├── doc_autofiller_agent.py
│   └── ticket_summarizer_agent.py    # <-- New!
├── apis/
│   ├── gitlab_client.py
│   ├── confluence_client.py
│   └── jira_client.py                # <-- New!
├── prompts/
│   └── ticket_summary_prompt.txt     # <-- New or add in 'prompts/'
├── main.py                          # Add CLI/API support here
...
