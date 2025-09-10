from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json
import logging
from django.contrib.auth import get_user_model
from apps.progresstracker.models import Quiz, Question, UserQuizResult, Answer
from .ai_utils import call_ai_api
from .ai_parser import parse_ai_response

logger = logging.getLogger(__name__)

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

# parsing logic moved to apps.progresstracker.ai_parser

class GenerateQuizView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        milestone_title = request.data.get('milestone_title')
        if not milestone_title:
            return Response({'error': 'milestone_title is required.'}, status=status.HTTP_400_BAD_REQUEST)

        previous_results = UserQuizResult.objects.filter(user=user).order_by('-completed_at')[:5]

        prompt = build_quiz_prompt(user, milestone_title, previous_results)

        system_content = "you are a quiz generator for knowledge validation."
        try:
            ai_content = call_ai_api(prompt, system_content=system_content)
        except Exception as e:
            logger.exception('AI API call failed')
            return Response({'error': 'AI API call failed', 'details': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        logger.debug('AI raw response: %s', ai_content)

        try:
            ai_response = parse_ai_response(ai_content)
        except Exception as e:
            logger.exception('Failed to parse AI response')
            return Response({'error': 'Invalid AI response', 'details': str(e), 'ai_raw': ai_content}, status=status.HTTP_502_BAD_GATEWAY)

        quiz = Quiz.objects.create(title=f"quiz for {milestone_title}", milestone=milestone_title, created_by_AI=True)
        print(f"Quiz criado: {quiz} | ID: {quiz.id}")

        created_questions = []
        for q in ai_response.get('questions', []):
            question = Question.objects.create(quiz=quiz, text=q.get('text', ''), question_type=q.get('type', 'multiple_choice'))
            q_record = {
                'id': question.id,
                'text': question.text,
                'type': question.question_type,
                'choices': [],
                'answer': None,
            }
            if q.get('type') == 'multiple_choice' and 'choices' in q:
                for choice in q['choices']:
                    is_correct = (choice == q.get('answer'))
                    a = Answer.objects.create(question=question, text=choice, is_correct=is_correct)
                    q_record['choices'].append({'id': a.id, 'text': a.text})
                    if is_correct:
                        q_record['answer'] = a.text
            elif q.get('type') in ['true_false', 'fill_in_the_blank'] and 'answer' in q:
                a = Answer.objects.create(question=question, text=q['answer'], is_correct=True)
                q_record['choices'] = [{'id': a.id, 'text': a.text}]
                q_record['answer'] = a.text

            created_questions.append(q_record)

        response_data = {
            'quiz_id': quiz.id,
            'quiz': {
                'title': quiz.title,
                'milestone': quiz.milestone,
                'questions': created_questions
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    