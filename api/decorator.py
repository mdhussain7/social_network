# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         request = args[1] 
#         try:
#             token = request.headers.get('token')
#         except:
#             token = ''
        
#         tk = verify_token(token)
#         if tk['status'] == 'fail':
#             return JsonResponse({'status': 'fail', 'message': 'Invalid Login Token'})
#         request.session['user_id'] = tk['user_id']
#         return func(*args, **kwargs)
#     return decorated

from django.http import JsonResponse
from functools import wraps
from .models import UserLoginData

def verify_token(token):
    response_log = UserLoginData.objects.filter(token=token).first()
    if response_log:
        return {'status': 'success', 'user_id': response_log.user_id}
    return {'status': 'failed'}

class TokenRequired(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if len(args) > 1:
                request = args[1]
            else:
                request = args[0]

            try:
                token = request.headers.get('token', '')
            except Exception as e:
                token = ''
            
            response_token = verify_token(token)
            if response_token['status'] == 'failed':
                return JsonResponse({'status': 'failed', 'message': 'Login failed due to invalid token'})
            
            request.session['user_id'] = response_token['user_id']
            return func(*args, **kwargs)

        return decorated_view

