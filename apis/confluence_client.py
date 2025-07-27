from atlassian import Confluence
import os
from dotenv import load_dotenv
load_dotenv()

class ConfluenceClient:
    def __init__(self):
        url = os.getenv('CONFLUENCE_URL')
        username = os.getenv('CONFLUENCE_USER')
        token = os.getenv('CONFLUENCE_TOKEN')
        if not url or not username or not token:
            raise RuntimeError("Missing one of CONFLUENCE_URL, CONFLUENCE_USER, CONFLUENCE_TOKEN (currently got url=%r, username=%r, token=%r)" % (url, username, token))
        self.confluence = Confluence(url=url, username=username, password=token)

    def create_page(self, space, title, body, parent_id=None):
        # Try to find if the page already exists
        existing_page = self.confluence.get_page_by_title(space=space, title=title)
        
        if existing_page:
            # If page exists, update it
            return self.confluence.update_page(
                page_id=existing_page['id'],
                title=title,
                body=body,
                parent_id=parent_id,
                version_comment="Updated by AutoDocFiller"
            )
        else:
            # If page doesn't exist, create it
            return self.confluence.create_page(
                space=space,
                title=title,
                body=body,
                parent_id=parent_id,
            )