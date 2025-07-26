import os
import requests
from dotenv import load_dotenv
# from langchain.llms import OpenAI  # Original import
load_dotenv()

class DocAutoFillerAgent:
    def __init__(self):
        # Original OpenAI setup
        # api_key = os.getenv("OPENAI_API_KEY")
        # self.llm = OpenAI(model = 'gpt-3.5-turbo-instruct', temperature = 0.2, openai_api_key = api_key)
        
        # New Perplexity AI setup
        self.api_key = "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"
        self.url = "https://api.perplexity.ai/chat/completions"

    def generate_text(self, template_path, variables):
        with open(template_path, 'r') as f:
            template = f.read()
        prompt = template.format(**variables)
        
        # Original OpenAI code
        # response = self.llm(prompt)
        # return response.strip()
        
        # New Perplexity AI code
        payload = {
            "model": "sonar-pro",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 2000,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Using Perplexity AI API
        response = requests.post(self.url, headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"].strip()
    
    def generate_pr_description(self, context):
        return self.generate_text('Prompts/templates.txt', {'context': context})
    
    def generate_tickets(self, title, context, pr_url):
        return self.generate_text('Prompts/tickets.txt', {'title': title, 'context': context, 'pr_url': pr_url})
    
    def generate_spec(self, reason, diff, pr_url):
        return self.generate_text('specs/spec_template.txt', {'reason': reason, 'diff': diff, 'pr_url': pr_url})
    
    