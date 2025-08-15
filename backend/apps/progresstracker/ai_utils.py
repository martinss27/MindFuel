import requests
import os
from dotenv import load_dotenv

load_dotenv()

def call_ai_api(prompt, system_content="Você é um assistente versátil para educação e recomendações."):
    """
   Define 'system' role context dynamically based on usage
    """
    
    API_URL = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
    API_KEY = os.getenv('OPENROUTER_API_KEY')
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not defined.")
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'openai/gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': system_content},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 512
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']
