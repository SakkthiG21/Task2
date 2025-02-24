import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
import google.generativeai as genai

st.title("Titanic Dataset Chat Agent")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
    return df

df = load_data()

def get_gender_percentage():
    gender_counts = df['Sex'].value_counts(normalize=True) * 100
    male_percentage = gender_counts.get('male', 0)
    return f"{male_percentage:.1f}% of passengers were male"

def plot_age_histogram():
    fig = px.histogram(df, x='Age', title='Distribution of Passenger Ages')
    return fig

def get_average_fare():
    avg_fare = df['Fare'].mean()
    return f"The average ticket fare was ${avg_fare:.2f}"

def plot_embarkation_counts():
    embark_counts = df['Embarked'].value_counts()
    fig = px.bar(x=embark_counts.index, y=embark_counts.values,
                title='Passenger Count by Embarkation Port')
    return fig

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Ask me anything about the Titanic dataset:", key="query")

if st.button("Send"):
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        try:
            if "percentage" in query.lower() and "male" in query.lower():
                result = get_gender_percentage()
            elif "age" in query.lower() and "histogram" in query.lower():
                result = plot_age_histogram()
            elif "average" in query.lower() and "fare" in query.lower():
                result = get_average_fare()
            elif "embark" in query.lower():
                result = plot_embarkation_counts()
            else:
                result = "I can answer questions about passenger gender percentages, age distributions, average fares, and embarkation ports."
            
            st.session_state.chat_history.append({"role": "assistant", "content": result})
            
            if isinstance(result, go.Figure):
                st.plotly_chart(result)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.write("You: " + message["content"])
    else:
        st.write("Assistant: " + str(message["content"])) 