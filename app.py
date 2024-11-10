import streamlit as st
import json
import requests
from io import StringIO
from processing.audio_video_creation import generate_video

# App title and sidebar setup
st.set_page_config(page_title="Tạo Video từ Văn Bản")
with st.sidebar:
    st.title('Tạo Video từ Văn Bản')

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Nhập đoạn văn để tạo video."}]

uploaded_file = st.sidebar.file_uploader("Choose a file")
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Nhập đoạn văn để tạo video."}]

# Function to call the prediction API
def call_generation(prompt):
    try:
        with st.spinner("Đang tạo video..."):
            # Generate video and retrieve file path
            video_path = generate_video(prompt)
    
        # Display video
        if video_path:
            st.video(video_path)
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi API: {e}")
        return "Error occurred while creating video."

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user text input
if user_input := st.chat_input("Nhập đoạn văn để tạo video:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate response and display it
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            assistant_response = call_generation(user_input)
    
    # Append assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Handle file upload
if uploaded_file is not None:
    prompt = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display uploaded content as user message
    with st.chat_message("user"):
        st.write(prompt)
        
    # Generate response for uploaded content and display it
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            assistant_response = call_generation(prompt)
    
    # Append assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
