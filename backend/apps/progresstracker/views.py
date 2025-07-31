from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.progresstracker.models import Quiz, Question
from .ai_utils import call_ai_api

User = get_user_model()

def build_quiz_prompt(user, milestone, previous_results):
    prompt = f"user: {user.username}\n"
    prompt += f"milestone: {milestone.title}\n"
    prompt += "last errors: "
    if previous_results:
        erros = ', '.join([r['topic'] for r in previous_results if not r['correct']])
        prompt += erros if erros else 'no errors.'
    else:
        prompt += 'old results not found'
    prompt += "\nGenerate 5 multiple-choice questions, 2 true/false questions, and 1 fill-in-the-blank question about the milestone above"
    return prompt
