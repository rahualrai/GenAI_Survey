# GPT Streamlit

## Installation

1. Clone the repository:
```bash
git clone 
cd GenAI_Survey/gpt_streamlit
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Setting up the OpenAI API Key

1. Create an OpenAI API key:
- Go to the OpenAI API and sign up or log in.
- Navigate to the API keys section and create a new API key.

2. Store the OpenAI API key as a secret key:
- Create a new folder called `.streamlit`:
```bash
mkdir .streamlit
```

3. Inside the .streamlit directory, create a file named secrets.toml and add your API key to this file in the following format:
```toml
[openai]
api_key = "your-openai-api-key"
```


## Running the Streamlit App

run the following command:
```bash
streamlit run main.py --server.enableCORS=false
```
