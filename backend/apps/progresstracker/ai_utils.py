import requests
import os

def call_ai_api(prompt, system_content="Você é um assistente versátil para educação e recomendações."):
    """
   Define 'system' role context dynamically based on usage
    """
    
    API_URL = os.getenv('AI_API_URL', 'https://api.openai.com/v1/chat/completions')
    API_KEY = os.getenv('AI_API_KEY', 'SUA_CHAVE_AQUI')
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
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
