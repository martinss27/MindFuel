from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class GenerateLearningPathView(APIView):
    def post(self, request):
        theme = request.data.get("theme")
        if not theme:
            return Response({"error": "O campo 'theme' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            roadmap = generate_learning_path(theme)
            return Response({"roadmap": roadmap})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_learning_path(theme):
    prompt = f"""
        I want you to act as a **learning path designer** for self-taught learners.

        Given any theme, your task is to generate a structured learning path divided into **three levels of mastery** (e.g., Beginner, Intermediate, Advanced). Each level should include **2 to 4 learning milestones**, presented in a logical and progressive order.

        Each milestone should contain:
        - A **short, clear title**
        - A **practical and encouraging description**, explaining what will be learned and **why it matters**
        - A simple **challenge or recommended habit** to apply the knowledge in practice

        The tone should be **friendly, motivating, and accessible**, as if you're guiding someone learning on their own who needs clarity without feeling overwhelmed.

        Avoid overly technical language. Respond in a **structured format**, with each level labeled and milestones numbered within each level.

        Here is the theme: **"{theme}"**
                """
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Referer": "http://localhost:8000",
        "X-Title": "Mindfuel Project"
    }
    data = {
        "model": "openrouter/cypher-alpha:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    # Opcional: transformar a resposta em lista de etapas
    etapas = [linha.strip() for linha in content.split('\n') if linha.strip()]
    return etapas