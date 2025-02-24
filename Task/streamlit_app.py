import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Titanic Dataset Chat Agent")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
    return df

df = load_data()

def get_gender_percentage():
    gender_counts = df['Sex'].value_counts(normalize=True) * 100
    male_percentage = gender_counts.get('male', 0)
    female_percentage = gender_counts.get('female', 0)
    return f"Male passengers: {male_percentage:.1f}%, Female passengers: {female_percentage:.1f}%"

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

def get_children_count():
    children = df[df['Age'] < 18]
    return f"There were {len(children)} children on board the Titanic"

def get_survival_stats():
    survived = df['Survived'].value_counts()
    return f"Survivors: {survived[1]} passengers, Did not survive: {survived[0]} passengers"

def get_class_distribution():
    class_counts = df['Pclass'].value_counts().sort_index()
    return f"1st Class: {class_counts[1]} passengers\n2nd Class: {class_counts[2]} passengers\n3rd Class: {class_counts[3]} passengers"

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Ask me anything about the Titanic dataset:", key="query")

if st.button("Send"):
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        try:
            if "children" in query.lower():
                result = get_children_count()
            elif "gender" in query.lower() or "male" in query.lower() or "female" in query.lower():
                result = get_gender_percentage()
            elif "age" in query.lower() and "histogram" in query.lower():
                result = plot_age_histogram()
            elif "fare" in query.lower():
                result = get_average_fare()
            elif "embark" in query.lower() or "port" in query.lower():
                result = plot_embarkation_counts()
            elif "survive" in query.lower() or "survived" in query.lower():
                result = get_survival_stats()
            elif "class" in query.lower():
                result = get_class_distribution()
            else:
                result = """I can answer questions about:
                - Number of children on board
                - Passenger gender distribution
                - Age distribution (histogram)
                - Average ticket fares
                - Embarkation ports
                - Survival statistics
                - Passenger class distribution"""
            
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