from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken
load_dotenv()

def generate_token(user):
  refresh = RefreshToken.for_user(user)
  access_token = refresh.access_token
  
  # Add custom claims
  access_token['user_id'] = user.id
  access_token['email'] = user.email
  access_token['is_superuser'] = user.is_superuser
  
  return str(access_token)
