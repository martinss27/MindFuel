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
                Quero que você atue como um planejador de trilhas de aprendizado com foco em pessoas autodidatas.

                Dado um tema qualquer, sua tarefa é gerar uma trilha estruturada em **níveis de domínio** (por exemplo: Iniciante, Intermediário, Avançado). Cada nível deve conter de 2 a 4 marcos de aprendizado, ordenados de forma lógica e progressiva.

                Cada marco de aprendizado deve conter:
                - Um **título curto e direto**
                - Uma **descrição clara e motivadora**, explicando o que será aprendido e **por que isso importa**
                - Um pequeno **desafio prático** ou hábito recomendado (curto e simples)

                O estilo da resposta deve ser **acessível, encorajador e inspirador**, como se você estivesse guiando alguém que está tentando aprender por conta própria e precisa de direção sem se sentir sobrecarregado.

                Evite jargões técnicos. Responda em **formato estruturado**, com o nome de cada nível em destaque e os marcos numerados dentro de cada um.

                Tema: **"{theme}"**
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