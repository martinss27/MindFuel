from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth import get_user_model
from apps.progresstracker.models import Quiz, Question, UserQuizResult, Answer
from .ai_utils import call_ai_api

User = get_user_model()

def build_quiz_prompt(user, milestone_title, previous_results):
    prompt = f"user: {user.username}\n"
    prompt += f"milestone: {milestone_title}\n"
    prompt += "last errors: "
    if previous_results:
        erros = ', '.join([r['topic'] for r in previous_results if not r['correct']])
        prompt += erros if erros else 'no errors.'
    else:
        prompt += 'old results not found'
    prompt += "\nGenerate 5 multiple-choice questions, 2 true/false questions, and 1 fill-in-the-blank question about the milestone above"
    return prompt

class GenerateQuizView(APIView):
    def post(self, request):
        user = request.user
        milestone_title = request.data.get('milestone_title')
        if not milestone_title:
            return Response({'error': 'milestone_title is required.'}, status=status.HTTP_400_BAD_REQUEST)

        previous_results = UserQuizResult.objects.filter(user=user).order_by('-completed_at')[:5]

        prompt = build_quiz_prompt(user, milestone_title, previous_results)

        system_content = "you are a quiz generator for knowledge validation."
        ai_content = call_ai_api(prompt, system_content=system_content)

        ai_response = json.loads(ai_content)

        quiz = Quiz.objects.create(title=f"quiz for {milestone_title}", milestone=milestone_title, created_by_AI=True)
        
        for q in ai_response['questions']:
            question = Question.objects.create(quiz=quiz, text=q['text'], question_type=q['type'])
            if q['type'] == 'multiple_choice' and 'choices' in q:
                for choice in q['choices']:
                    is_correct = (choice == q.get('answer'))
                    Answer.objects.create(question=question, text=choice, is_correct=is_correct)
            elif q['type'] in ['true_false', 'fill_in_the_blank'] and 'answer' in q:
                Answer.objects.create(question=question, text=q['answer'], is_correct=True)


        return Response({'quiz_id': quiz.id}, status=status.HTTP_201_CREATED)