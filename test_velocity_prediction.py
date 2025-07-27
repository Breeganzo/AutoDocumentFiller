from agents.sprint_velocity_predictor import SprintVelocityPredictor
from apis.jira_client import JiraClient
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def main():
    # Initialize JIRA client
    jira_client = JiraClient()
    
    # Get some issues first to check the data
    project_key = jira_client.project_key
    print(f"\nChecking JIRA setup for project {project_key}...")
    issues = jira_client.get_issues(project_key)
    
    if not issues:
        print("No issues found in the project.")
        return
        
    print(f"\nFound {len(issues)} issues. Checking first issue for field setup:")
    sample_issue = issues[0]
    print("\nAvailable fields:")
    for field_name, value in sample_issue.raw['fields'].items():
        print(f"{field_name}: {value}")
    
    # Initialize velocity predictor
    predictor = SprintVelocityPredictor(jira_client)
    
    # Collect sprint data (using default 5 sprints)
    print(f"\nCollecting sprint data for project {project_key}...")
    predictor.collect_sprint_data(project_key)
    
    # Get velocity prediction
    print("\nGenerating velocity prediction...")
    prediction = predictor.predict_velocity()
    
    # Create output directory if it doesn't exist
    output_dir = Path('analysis_output')
    output_dir.mkdir(exist_ok=True)
    
    # Save prediction results
    output_file = output_dir / 'velocity_prediction.json'
    with open(output_file, 'w') as f:
        json.dump(prediction, f, indent=2)
    
    # Print formatted results
    print("\nVelocity Prediction Results:")
    print("=" * 50)
    print(f"Predicted Velocity: {prediction['predicted_velocity']} issues per sprint")
    print(f"Confidence Interval: {prediction['confidence_interval']}")
    print("\nTrend Analysis:")
    print("-" * 30)
    for key, value in prediction['trend_analysis'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    if prediction['risk_factors']:
        print("\nRisk Factors:")
        print("-" * 30)
        for risk in prediction['risk_factors']:
            print(f"- {risk}")
    
    if prediction['recommendations']:
        print("\nRecommendations:")
        print("-" * 30)
        for rec in prediction['recommendations']:
            print(f"- {rec}")
    
    print(f"\nDetailed results saved to: {output_file}")

if __name__ == "__main__":
    main()
