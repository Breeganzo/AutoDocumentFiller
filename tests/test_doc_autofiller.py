import unittest
from agents.doc_autofiller_agent import DocAutoFillerAgent

class TestDocAutoFillerAgent(unittest.TestCase):
    def test_generate_pr_description(self):
        agent = DocAutoFillerAgent()
        context = "Increase instance count"
        desc = agent.generate_pr_description(context)
        self.assertIn("Description:", desc)

if __name__ == '__main__':
    unittest.main()
