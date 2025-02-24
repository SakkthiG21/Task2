import streamlit as st
import requests
import plotly.graph_objects as go
import json

st.title("Titanic Dataset Chat Agent")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

API_URL = "http://127.0.0.1:8000/query"

query = st.text_input("Ask me anything about the Titanic dataset:", key="query")

if st.button("Send"):
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        try:
            response = requests.post(
                API_URL,
                json={"text": query},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()["response"]
                
                st.session_state.chat_history.append({"role": "assistant", "content": result})
                
                if isinstance(result, dict) and "data" in result:
                    fig = go.Figure(result)
                    st.plotly_chart(fig)
            else:
                st.error(f"Error: Server returned status code {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend server. Please make sure it's running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.write("You: " + message["content"])
    else:
        st.write("Assistant: " + message["content"]) 