import re

class StorySplitter:
    def __init__(self, jira_client):
        self.jira = jira_client
        self.complexity_keywords = {
            'high': ['complex', 'major', 'significant', 'extensive'],
            'medium': ['moderate', 'standard', 'normal'],
            'low': ['simple', 'minor', 'small', 'basic']
        }

    def analyze_story_complexity(self, description: str) -> str:
        """Assess complexity based on keywords in the description."""
        if not description:
            return 'unknown'

        desc_lower = description.lower()
        for level, keywords in self.complexity_keywords.items():
            for kw in keywords:
                if kw in desc_lower:
                    return level
        # Default if no keywords matched:
        return 'medium'

    def suggest_split(self, ticket_key: str) -> str:
        """Suggest how to split the user story if complex."""
        issue = self.jira.get_ticket_info(ticket_key)
        description = issue.get('description', '')
        complexity = self.analyze_story_complexity(description)

        if complexity in ['high', 'medium']:
            # Basic heuristic: split on 'and', ',' or listing-type structure
            splits = re.split(r',| and |;|\n|- ', description)
            splits = [s.strip() for s in splits if len(s.strip()) > 10]
            if len(splits) > 1:
                splitted_stories = "\n".join(f"{i+1}. {story}" for i, story in enumerate(splits))
                return f"Suggested smaller stories based on description split:\n{splitted_stories}"
            else:
                return "No clear split points found, consider manual review."
        else:
            return "Story complexity is low; splitting may not be necessary."

    def create_substories(self, parent_key: str):
        """Optional: Create subtasks in Jira based on suggested splits."""
        suggestion = self.suggest_split(parent_key)
        # Parse numbered stories from suggestion and create Jira issues
        # (Implementation dependent on your jira_client's create_ticket method)
        # Return list of created ticket keys or IDs
        # You can implement this based on your Jira client's capabilities.
        pass
