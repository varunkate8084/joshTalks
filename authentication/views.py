import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from helper import generate_token
from django.db import transaction
from rest_framework.decorators import api_view
from .serializers import UserSerializer


@csrf_exempt
@swagger_auto_schema(
    method='post',
    operation_description="Register a new user with username, email, and password",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="User's username"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User's email"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="User's password"),
        },
    ),
    responses={
        200: openapi.Response("Register Success", UserSerializer),
        400: openapi.Response("Bad Request"),
    }
)
@api_view(['POST'])
def register(request):
    print("register:")
    try:
      with transaction.atomic():
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
          return JsonResponse({'status': 'failed', 'error': 'All fields are required'}, status=400)
        if User.objects.filter(email=email).exists():
          return JsonResponse({'status': 'failed', 'error': 'email already taken'}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        # print("user:",user)
        token = generate_token(user)
        user_data = UserSerializer(user).data
        print("token:",token)
        return JsonResponse({'Message': 'Register Success', 'status':True,'user':user_data,'token':token}, status=200)
    except json.JSONDecodeError:
      return JsonResponse({'status': 'failed', 'error': 'Invalid JSON'}, status=400)



@csrf_exempt
@swagger_auto_schema(
    method='post',
    operation_description="Log in with email and password",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User's email"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="User's password"),
        },
    ),
    responses={
        200: openapi.Response("Logged In Success", UserSerializer),
        400: openapi.Response("Invalid email or password"),
    }
)
@api_view(['POST'])
def login(request):
    try:
      data = json.loads(request.body)
      email = data.get('email')
      password = data.get('password')

      if not email or not password:
        return JsonResponse({'status': 'failed', 'error': 'All fields are required'}, status=400)
      user = User.objects.filter(email=email).first()
      if user is None:
        return JsonResponse({'status': 'failed', 'error': 'Invalid email or password'}, status=400)

      # Check password hash
      if user.check_password(password):
        token = generate_token(user)
        user_data = UserSerializer(user).data
        return JsonResponse({'message': 'Logged In Success', 'status': True, 'token': token,'user':user_data}, status=200)
      else:
        return JsonResponse({'status': 'failed', 'error': 'Invalid email or password'}, status=400)
    
    except json.JSONDecodeError:
      return JsonResponse({'status': 'failed', 'error': 'Invalid JSON'}, status=400)



