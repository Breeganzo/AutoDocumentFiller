import os
from apis.gitlab_client import GitLabClient
from apis.confluence_client import ConfluenceClient  # Commented out
from agents.doc_autofiller_agent import DocAutoFillerAgent
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
    confluence_space = os.getenv('CONFLUENCE_SPACE')  # Commented out
    reason = "Traffic requires more web EC2 instances."

    # Prepare clients
    gitlab_client = GitLabClient(gitlab_url, gitlab_token)
    conf_client = ConfluenceClient()  # Commented out
    agent = DocAutoFillerAgent()

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

    # Step 4: Ticket (generate/imitate—could create in Jira, etc.)
    ticket = agent.generate_tickets("Auto: Scale Up EC2", context, pr_url)
    print(f"\nTicket Content:\n{ticket}")

    # Step 5: Spec doc (commented out Confluence integration)
    diff = load_terraform_changes()
    spec = agent.generate_spec(reason, diff, pr_url)
    print(f"\nSpec Content:\n{spec}")
    page_title = f"Spec: MR {mr.iid} Scaling EC2"
    conf_client.create_page(confluence_space, page_title, spec)
    print(f"Confluence page created: {page_title}")

if __name__ == "__main__":
    main()
