from rest_framework.views import APIView
from rest_framework import generics, permissions
from .serializers import HabitSerializer
from .models import Habit
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import json

class GenerateRecommendationsView(APIView):
    def post(self,request):
        theme = request.data.get('theme')
        if not theme:
            return Response({"error": "theme is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            recommendations = generate_recommendations(theme)
            return Response({"recommendations": recommendations})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def generate_recommendations(theme):
    prompt = f"""
        Você é um designer de experiências de aprendizado. Para o tema abaixo, gere:
        - 3 sugestões de hábitos (leve, médio, intenso), cada uma com: "nome", "descrição", "nível" (leve/médio/intenso)
        - 3 perfis/redes sociais relevantes (YouTube, X, etc.), cada um com: "nome", "plataforma", "link", "por que seguir"
        Responda apenas com um JSON neste formato:
        {{
            "habits": [
                {{"nome": "...", "descrição": "...", "nível": "..."}}
            ],
            "profiles": [
                {{"nome": "...", "plataforma": "...", "link": "...", "por_que_seguir": "..."}}
            ]
        }}
        Tema: "{theme}"
        IMPORTANTE: Retorne apenas o JSON, sem explicações ou formatação extra.
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
    return json.loads(content)

class UserHabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class UserHabitUpdateView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
class UserHabitDeleteView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

