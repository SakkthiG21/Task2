import pandas as pd
import plotly.express as px
import os

class DataAnalyzer:
    def __init__(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_path = os.path.join(current_dir, 'data', 'titanic.csv')
        self.df = pd.read_csv(data_path)
    
    def get_gender_percentage(self):
        gender_counts = self.df['Sex'].value_counts(normalize=True) * 100
        male_percentage = gender_counts.get('male', 0)
        return f"{male_percentage:.1f}% of passengers were male"
    
    def plot_age_histogram(self):
        fig = px.histogram(self.df, x='Age', title='Distribution of Passenger Ages')
        return fig
    
    def get_average_fare(self):
        avg_fare = self.df['Fare'].mean()
        return f"The average ticket fare was ${avg_fare:.2f}"
    
    def plot_embarkation_counts(self):
        embark_counts = self.df['Embarked'].value_counts()
        fig = px.bar(x=embark_counts.index, y=embark_counts.values,
                    title='Passenger Count by Embarkation Port')
        return fig 