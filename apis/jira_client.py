from jira import JIRA
import os

class JiraClient:
    def __init__(self):
        server = os.getenv("JIRA_URL")  # e.g., https://yourdomain.atlassian.net
        username = os.getenv("JIRA_USER")  # your email
        api_token = os.getenv("JIRA_TOKEN")  # Jira API token

        if not server or not username or not api_token:
            raise RuntimeError("Missing JIRA_URL, JIRA_USER or JIRA_TOKEN!")

        self.jira = JIRA(server=server, basic_auth=(username, api_token))

    def get_ticket_info(self, ticket_id):
        issue = self.jira.issue(ticket_id)
        comments = self.jira.comments(issue)
        latest_comments = '\n'.join(
            [f"{c.author.displayName}: {c.body}" for c in comments[-3:]]
        )  # Only last 3, for brevity

        return {
            "title": issue.fields.summary,
            "description": issue.fields.description or "",
            "status": issue.fields.status.name,
            "reporter": issue.fields.reporter.displayName,
            "assignee": getattr(issue.fields.assignee, "displayName", "Unassigned"),
            "comments": latest_comments,
        }
    
    def update_ticket(self, ticket_id, summary=None, description=None):
        """Update a JIRA ticket with new summary and/or description"""
        issue = self.jira.issue(ticket_id)
        update_fields = {}
        
        if summary:
            update_fields['summary'] = summary
        if description:
            update_fields['description'] = description
            
        if update_fields:
            issue.update(fields=update_fields)
            
        return issue
    
    def add_comment(self, ticket_id, comment):
        """Add a comment to a JIRA ticket"""
        issue = self.jira.issue(ticket_id)
        self.jira.add_comment(issue, comment)

    def create_ticket(self, project_key, summary, description, issue_type='Task'):
        """Create a new JIRA ticket. Returns the created issue."""
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        return self.jira.create_issue(fields=issue_dict)

    def update_ticket_status(self, ticket_id, status):
        """Update the status of an existing ticket
        status can be: 'To Do', 'In Progress', 'Done'
        """
        issue = self.jira.issue(ticket_id)
        transitions = self.jira.transitions(issue)
        
        # Find the transition that leads to our desired status
        for t in transitions:
            if t['to']['name'].lower() == status.lower():
                self.jira.transition_issue(issue, t['id'])
                return True
        return False

    def update_ticket_description(self, ticket_id, description):
        """Update just the description of an existing ticket"""
        issue = self.jira.issue(ticket_id)
        issue.update(fields={'description': description})
        return issue

    def assign_ticket(self, ticket_id, assignee):
        """Assign a ticket to someone"""
        issue = self.jira.issue(ticket_id)
        issue.update(fields={'assignee': {'name': assignee}})
