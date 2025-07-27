import os
from apis.gitlab_client import GitLabClient
from apis.confluence_client import ConfluenceClient
from agents.doc_autofiller_agent import DocAutoFillerAgent
from apis.jira_client import JiraClient
from agents.ticket_summarizer_agent import TicketSummarizerAgent
from apis.summary_storage import SummaryStorage
from dotenv import load_dotenv
load_dotenv()

def load_terraform_changes():
    # Simulating a diff, in practice parse git/terraform diff
    return "Changed aws_instance.web count from 2 to 5"

def main():
    # Set up environment/config
    project_id = int(os.getenv('GITLAB_PROJECT_ID'))
    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    tf_path = 'terraform/main.tf'
    branch_name = 'scale-up-ec2-instances'
    commit_message = 'Increase EC2 instance count for scaling'
    confluence_space = os.getenv('CONFLUENCE_SPACE')
    reason = "Traffic requires more web EC2 instances."

    # Prepare clients
    gitlab_client = GitLabClient(gitlab_url, gitlab_token)
    conf_client = ConfluenceClient()
    agent = DocAutoFillerAgent()
    storage = SummaryStorage()

    # Step 1: Branch
    gitlab_client.create_branch(project_id, branch_name)

    # Step 2: Commit (create or update terraform file)
    tf_content = """provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  count         = 5
  tags = {
    Name = "DemoWebServer"
  }
}"""
    gitlab_client.commit_file(project_id, branch_name, tf_path, tf_content, commit_message)

    # Step 3: Pull Request
    context = f"Terraform update: increase EC2 instances.\nFile: {tf_path}\nCommit: {commit_message}"
    pr_description = agent.generate_pr_description(context)
    mr = gitlab_client.create_merge_request(project_id, branch_name, description=pr_description, title="Scale Up EC2 Instances")
    pr_url = mr.web_url
    print(f"Merge Request created: {pr_url}")
    
    # Store merge request summary
    mr_json, mr_txt = storage.save_merge_request_summary(mr.iid, pr_description)
    print(f"Merge request summary saved in:")
    print(f"- JSON format: {mr_json}")
    print(f"- Text format: {mr_txt} (for easy reading)")

    # Step 4: Create new JIRA ticket for the new task
    ticket_summary = "Auto: Scale Up EC2"
    ticket = agent.generate_tickets(ticket_summary, context, pr_url)
    
    # Initialize JIRA client
    jira_client = JiraClient()
    
    # Create a new ticket in the SMP project
    jira_issue = jira_client.create_ticket(
        project_key="SMP",
        summary=ticket_summary,
        description=ticket
    )
    ticket_id = jira_issue.key  # This will be something like "SMP-8", "SMP-9", etc.
    print(f"\nJIRA Ticket {ticket_id} created/updated")
    print(f"\nTicket Content:\n{ticket}")
    
    # Store ticket content locally
    ticket_json, ticket_txt = storage.save_jira_summary(ticket_id, ticket)
    print(f"Ticket summary saved in:")
    print(f"- JSON format: {ticket_json}")
    print(f"- Text format: {ticket_txt} (for easy reading)")
    print(f"- JIRA ticket: {ticket_id}")

    # Step 5: Spec doc
    diff = load_terraform_changes()
    spec = agent.generate_spec(reason, diff, pr_url)
    print(f"\nSpec Content:\n{spec}")
    page_title = f"Spec: MR {mr.iid} Scaling EC2"
    conf_client.create_page(confluence_space, page_title, spec)
    print(f"Confluence page created: {page_title}")
    
    # Store Confluence spec
    conf_json, conf_txt = storage.save_confluence_summary(page_title, spec)
    print(f"Confluence spec saved in:")
    print(f"- JSON format: {conf_json}")
    print(f"- Text format: {conf_txt} (for easy reading)")

def summarize_ticket(ticket_id, new_status=None):
    """
    Summarize a JIRA ticket and optionally update its status
    Args:
        ticket_id: The JIRA ticket ID (e.g., "SMP-7")
        new_status: Optional new status ('To Do', 'In Progress', or 'Done')
    """
    jira_client = JiraClient()
    agent = TicketSummarizerAgent()
    storage = SummaryStorage()
    
    details = jira_client.get_ticket_info(ticket_id)
    summary = agent.summarize_ticket(details)
    
    # Store the JIRA ticket summary locally
    json_path, txt_path = storage.save_jira_summary(ticket_id, summary)
    
    # Update the actual JIRA ticket
    jira_client.add_comment(ticket_id, 
        "Auto-generated summary:\n\n" + summary)
    
    # Update status if requested
    if new_status:
        if jira_client.update_ticket_status(ticket_id, new_status):
            print(f"Updated ticket status to {new_status}")
        else:
            print(f"Failed to update ticket status to {new_status}")
    
    print("\nTicket Summary:\n", summary)
    print(f"Summary saved in:")
    print(f"- JSON format: {json_path}")
    print(f"- Text format: {txt_path} (for easy reading)")
    print(f"- Added as a comment to JIRA ticket {ticket_id}")

if __name__ == "__main__":
    main()
