from django.shortcuts import render
import requests
import json
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
            I want you to act as a learning path designer for self-taught learners.

            Given any theme, generate a structured learning path with three mastery levels (Beginner, Intermediate, Advanced). Each level should have 2 to 4 milestones.

            Each milestone must have:
            - "title": a short clear title
            - "learn": what will be learned
            - "why": why this matters
            - "challenge": a small practical task

            Your response must be a valid JSON object exactly in this format (without any extra text or code blocks):

            {{
            "levels": [
                {{
                "name": "Beginner",
                "milestones": [
                    {{
                    "title": "...",
                    "learn": "...",
                    "why": "...",
                    "challenge": "..."
                    }}
                ]
                }},
                {{
                "name": "Intermediate",
                "milestones": [ ... ]
                }},
                {{
                "name": "Advanced",
                "milestones": [ ... ]
                }}
            ]
            }}

            IMPORTANT: Return **only** the JSON object — no explanations, no code blocks, no extra characters or quotes.
            Return ONLY a valid JSON object, without any line breaks or extra formatting.


            Theme: "{theme}"
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
    roadmap = json.loads(content)
    return roadmap