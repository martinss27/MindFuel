from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            user = serializer.validated_data['user'] 
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            # Return tokens in response body (helpful for clients like Postman)
            data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }
            response = Response(data)
            # also set HttpOnly cookies (optional)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False, 
                samesite='Lax'
            )
            response.set_cookie( 
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            return response
        return Response({'detail': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)