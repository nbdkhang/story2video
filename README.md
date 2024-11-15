# RAG Chatbot with VnExpress Articles

## Prerequisites

- Python 3.10

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/
   cd 
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   pip install torch==2.2.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html

   pip install torchvision==0.17.2+cu118 -f https://download.pytorch.org/whl/torch_stable.html
## Configuration
1. Gemini API Key:
   - Get Key free :D : https://aistudio.google.com/app/apikey

# Running the Application

1. Khởi động ứng dụng Streamlit:
   ```
   streamlit run ChatBot.py
   ```