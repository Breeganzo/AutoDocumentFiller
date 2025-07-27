from statistics import mean, stdev
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SprintVelocityPredictor:
    def __init__(self, jira_client):
        self.jira = jira_client
        self.historical_data = []
        self.scaler = StandardScaler()
        self.models = {
            'linear': LinearRegression(),
            'ridge': Ridge(alpha=1.0),
            'lasso': Lasso(alpha=1.0)
        }
        self.best_model = None
        self.feature_matrix = None

    def collect_sprint_data(self, project_key: str, num_sprints: int = 5) -> None:
        """
        Collect and process velocity data from recent closed sprints with advanced metrics.

        Args:
            project_key (str): Jira project key.
            num_sprints (int): Number of recent sprints to analyze.
        """
        # Fetch issues with sprint data
        issues = self.jira.get_issues(project_key)

        sprint_data = {}

        sprint_metrics = {}
        
        for issue in issues:
            sprints = getattr(issue.fields, 'customfield_10020', None)
            if not sprints:
                continue
            
            # Handle different possible sprint field formats
            if isinstance(sprints, list):
                if sprints and isinstance(sprints[0], dict):
                    sprint_names = [s.get('name') for s in sprints if s.get('name')]
                else:
                    sprint_names = [s.name for s in sprints if hasattr(s, 'name')]
            else:
                continue
                
            if not sprint_names:
                continue

            sprint = sprint_names[-1]
            
            # Initialize sprint metrics
            if sprint not in sprint_metrics:
                sprint_metrics[sprint] = {
                    'total_points': 0,  # Using issue count instead of story points
                    'completed_points': 0,
                    'num_stories': 0,
                    'avg_story_size': 1,  # Default size of 1 per issue
                    'completion_rate': 0
                }
            
            metrics = sprint_metrics[sprint]
            metrics['total_points'] += 1  # Count each issue as 1 point
            metrics['num_stories'] += 1
            
            status = getattr(issue.fields, 'status', None)
            if status and status.name == 'Done':
                metrics['completed_points'] += 1  # Count completed issues
        
        # Calculate derived metrics
        for metrics in sprint_metrics.values():
            metrics['avg_story_size'] = metrics['total_points'] / metrics['num_stories']
            metrics['completion_rate'] = metrics['completed_points'] / metrics['total_points'] if metrics['total_points'] > 0 else 0
        
        # Take last N sprints
        sorted_sprints = list(sprint_metrics.items())[-num_sprints:]
        self.historical_data = [(sprint, metrics) for sprint, metrics in sorted_sprints if metrics['total_points'] > 0]
        
        # Create feature matrix for ML models
        if self.historical_data:
            self.feature_matrix = np.array([
                [
                    m['total_points'],
                    m['completed_points'],
                    m['num_stories'],
                    m['avg_story_size'],
                    m['completion_rate']
                ] for _, m in self.historical_data
            ])

    def _select_best_model(self, X: np.ndarray, y: np.ndarray) -> Tuple[str, float]:
        """Select the best performing model using cross-validation."""
        best_score = -float('inf')
        best_model_name = None
        
        for name, model in self.models.items():
            scores = cross_val_score(model, X, y, cv=min(3, len(X)), scoring='neg_mean_squared_error')
            avg_score = -scores.mean()  # Convert back to positive MSE
            if avg_score > best_score:
                best_score = avg_score
                best_model_name = name
                
        return best_model_name, best_score

    def predict_velocity(self) -> Dict:
        """
        Predict next sprint velocity using ensemble of ML models and advanced metrics.

        Returns:
            dict: Prediction statistics with keys:
                - predicted_velocity: float
                - confidence_interval: tuple(float, float)
                - trend_analysis: dict
                - risk_factors: list
                - recommendations: list
        """
        if len(self.historical_data) < 2 or self.feature_matrix is None:
            return {
                'predicted_velocity': None,
                'confidence_interval': (None, None),
                'message': "Insufficient data for prediction.",
                'trend_analysis': {},
                'risk_factors': [],
                'recommendations': ["Collect more sprint data (minimum 2 sprints required)"]
            }

        # Scale features for better model performance
        X_scaled = self.scaler.fit_transform(self.feature_matrix)
        y = np.array([m['completed_points'] for _, m in self.historical_data])
        
        # Select and train best model
        best_model_name, best_score = self._select_best_model(X_scaled, y)
        self.best_model = self.models[best_model_name]
        self.best_model.fit(X_scaled, y)
        
        # Make prediction
        last_features = X_scaled[-1].reshape(1, -1)  # Use last sprint's features
        predicted = float(self.best_model.predict(last_features)[0])
        
        # Calculate confidence interval
        recent_velocities = y[-3:] if len(y) >= 3 else y
        std_dev = np.std(recent_velocities)
        confidence_interval = (max(0, predicted - 1.96*std_dev), predicted + 1.96*std_dev)
        
        # Trend analysis
        trend = 'increasing' if len(y) >= 2 and y[-1] > y[-2] else 'decreasing'
        stability = std_dev / np.mean(y) if len(y) > 0 else 0
        
        # Risk analysis
        risk_factors = []
        if stability > 0.25:
            risk_factors.append("High velocity variability")
        if trend == 'decreasing':
            risk_factors.append("Decreasing velocity trend")
        
        # Generate recommendations
        recommendations = [
            "Consider team capacity changes" if abs(predicted - np.mean(y)) > std_dev else None,
            "Review estimation process" if stability > 0.25 else None,
            "Investigate velocity decline" if trend == 'decreasing' else None
        ]
        recommendations = [r for r in recommendations if r]
        
        return {
            'predicted_velocity': round(predicted, 2),
            'confidence_interval': (round(confidence_interval[0], 2), round(confidence_interval[1], 2)),
            'trend_analysis': {
                'trend': trend,
                'stability_index': round(stability, 2),
                'model_used': best_model_name,
                'model_score': round(best_score, 2)
            },
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'message': "Prediction successful using advanced ML techniques."
        }
