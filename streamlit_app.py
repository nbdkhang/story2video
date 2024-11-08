import streamlit as st
import requests
import json
import pandas as pd
from io import StringIO

# App title
st.set_page_config(page_title="Dự đoán độ khó tiếng Việt")

#Sidebar setup
with st.sidebar:
    st.title('Story to video')

    add_questions = st.selectbox('Câu hỏi bổ sung', ['Có', 'Không'], key='add_questions')

    # Model type based on selection
    match add_questions:
        case 'Có':
            model_type = True
        case 'Không':
            model_type = False

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Nhập đoạn văn"}]



# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if prompt := st.chat_input("Nhập đoạn văn cần phân tích"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat
    with st.chat_message("user"):
        st.write(prompt)

    # Add selectbox for options after user input
    with st.chat_message("assistant"):
        with st.spinner("Đang phân tích..."):
            # Example response (can be replaced with actual API call)
            assistant_message = f"Đoạn văn '{prompt}' đã được phân tích."
            
            # Create a selectbox with dynamic options (replace these options as needed)
            option = st.selectbox(
                "Chọn một lựa chọn:", 
                ["Lựa chọn 1", "Lựa chọn 2", "Lựa chọn 3"]
            )

            # Display assistant message and the selected option
            st.write(assistant_message)
            st.write(f"Bạn đã chọn: {option}")
    
    # Append assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    st.session_state.messages.append({"role": "assistant", "content": f"Bạn đã chọn: {option}"})


# Function to call the API
def additional_questions(prompt, model_type):
    inputs = {"text": prompt, "type": model_type}
    try:
        return
        # r = requests.post(url='http://127.0.0.1:8000/predict', data=json.dumps(inputs))
        # r.raise_for_status()  # Raise an exception for bad status codes
        # response_data = r.json()
        # predicted_class = response_data.get('predicted_class')
        # return difficulty.get(predicted_class, "Không xác định")
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "Error occurred while predicting difficulty."