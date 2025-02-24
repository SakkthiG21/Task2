import google.generativeai as genai
from ..utils.data_utils import DataAnalyzer

class TitanicAgent:
    def __init__(self, api_key):
        self.analyzer = DataAnalyzer()
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def process_query(self, query):
        try:
            if "percentage" in query.lower() and "male" in query.lower():
                result = self.analyzer.get_gender_percentage()
                return result
            elif "age" in query.lower() and "histogram" in query.lower():
                return self.analyzer.plot_age_histogram()
            elif "average" in query.lower() and "fare" in query.lower():
                return self.analyzer.get_average_fare()
            elif "embark" in query.lower():
                return self.analyzer.plot_embarkation_counts()
            else:
                response = self.model.generate_content(
                    f"Answer this question about Titanic dataset: {query}"
                )
                return response.text
        except Exception as e:
            return f"Error processing query: {str(e)}" 