from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
  
  def process_request(self, request):
    auth_header = request.headers.get('Authorization')
    excluded_paths = ['/admin/', '/auth/','/test','/swagger','/redoc','/accounts']
    if any(request.path.startswith(path) for path in excluded_paths):
        return None  

    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({'error': 'No token provided'}, status=401)

    token = auth_header.split(' ')[1]

    try:
      access_token = AccessToken(token)
      request.user= access_token
    except Exception as e:
      return JsonResponse({'error': 'Invalid token'}, status=401)
