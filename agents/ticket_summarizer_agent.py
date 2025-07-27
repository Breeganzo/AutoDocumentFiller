import os
import requests
from dotenv import load_dotenv
from openai import OpenAI  # Original import
load_dotenv()

class TicketSummarizerAgent:
    def __init__(self):
        # Original OpenAI setup
        # api_key = os.getenv("OPENAI_API_KEY")
        # self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=api_key)
        
        # New Perplexity AI setup
        self.api_key = "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"
        self.url = "https://api.perplexity.ai/chat/completions"

    def summarize_ticket(self, ticket_details):
        with open('prompts/ticket_summary_prompt.txt', 'r') as f:
            prompt_template = f.read()
        prompt = prompt_template.format(**ticket_details)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar-pro",  # Using a supported model
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200 and "choices" in response_data:
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                error_message = response_data.get("error", {}).get("message", "Unknown error")
                print(f"API Error: {error_message}")
                print(f"Full response: {response_data}")
                return f"Error generating summary: {error_message}"
        except Exception as e:
            print(f"Error calling Perplexity API: {str(e)}")
            return f"Error generating summary: {str(e)}"
