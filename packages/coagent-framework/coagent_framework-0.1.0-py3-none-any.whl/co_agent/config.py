# linkedin_summarizer/config.py
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

llm_config = {
    "model": "gemini-1.5-flash", # replace it with your desired google model
    "api_key": "Google_API_Key", # replace it with your Google Gemini API Key 
    "temperature": 0.7,
    "max_tokens": 200,
    "max_retries": 2
}
