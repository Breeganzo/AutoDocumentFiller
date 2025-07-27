import os
import json
from datetime import datetime

class SummaryStorage:
    def __init__(self):
        self.base_dir = "summaries"
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure all required directories exist"""
        for dir_name in ['jira', 'confluence', 'merge_requests']:
            dir_path = os.path.join(self.base_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)

    def _save_summary(self, category, identifier, content):
        """Save a summary to the appropriate directory in both JSON and TXT formats"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Create the summary data structure
        summary_data = {
            "content": content,
            "timestamp": timestamp,
            "identifier": identifier
        }
        
        # Define the file paths
        json_path = os.path.join(self.base_dir, category, f"{identifier}.json")
        txt_path = os.path.join(self.base_dir, category, f"{identifier}.txt")
        
        # Save the JSON summary with metadata
        with open(json_path, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        # Save the plain text content for easy reading
        with open(txt_path, 'w') as f:
            f.write(f"Summary for {identifier}\n")
            f.write(f"Generated on: {timestamp}\n")
            f.write("-" * 80 + "\n\n")
            f.write(content)
        
        return json_path, txt_path

    def save_jira_summary(self, ticket_id, summary):
        """Save a JIRA ticket summary"""
        return self._save_summary('jira', ticket_id, summary)

    def save_confluence_summary(self, page_title, summary):
        """Save a Confluence page summary"""
        # Convert page title to a valid filename
        safe_title = page_title.replace(" ", "_").replace("/", "_")
        return self._save_summary('confluence', safe_title, summary)

    def save_merge_request_summary(self, mr_id, summary):
        """Save a merge request summary"""
        return self._save_summary('merge_requests', f"mr_{mr_id}", summary)

    def get_latest_summary(self, category, identifier):
        """Get the latest summary for a given category and identifier"""
        file_path = os.path.join(self.base_dir, category, f"{identifier}.json")
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
