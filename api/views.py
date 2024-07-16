from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import *
from .utils import *
from .constants import *
from .decorator import TokenRequired 
from datetime import datetime
from django.utils import timezone
import secrets
import string

# Create your views here.
class SignupView(APIView):

    def post(self, request, *args, **kwargs):
        """
            Handles user signup.

            POST Request:
            - Validates email uniqueness.
            - Hashes password and saves new user to database.
            - Returns success or failure response based on operation outcome.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            hashed_password = gen_password_hash(password)
            name = request.data.get('name')

            if ApplicationUser.objects.filter(email__iexact=email).exists():
                return JsonResponse({'res_status':'failed', 'res_code': 400 ,'res_str' : USER_EXIST},status=400)

            user_dict = {'email':email,'name':name,'password':hashed_password,'status':1}
            new_user = ApplicationUser(**user_dict)
            new_user.save()
            return JsonResponse({'res_status': 'success', 'res_code': 200, 'res_str' :USER_SUCCES_STR }, status=200)
        except Exception as e:
            return JsonResponse({'res_status':'failed', 'res_str': GENERIC_ERROR_STR , 'res_code': 400},status=400)

class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        """
            Handles user login.

            POST Request:
            - Validates user credentials.
            - Generates and saves login token for authenticated users.
            - Returns success or failure response based on operation outcome.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            hashed_password = gen_password_hash(password)
            user = ApplicationUser.objects.filter(email__iexact=email).first()

            if user and user.password == hashed_password:
                alphabet = string.ascii_letters + string.digits
                token = ''.join(secrets.choice(alphabet) for _ in range(64))
                login_record = UserLoginData(**{'user_id':user.id,'token':token})
                login_record.save()
                return JsonResponse({'res_status':'success', 'res_str': LOG_SUCCESS_STR,'token': token},status=200)
            return JsonResponse({'res_status':'error', 'res_str': INVALID_CRED_STR, 'res_code': 400}, status=400)
        except Exception as e:
            return JsonResponse({'res_status':'failed', 'res_str': GENERIC_ERROR_STR , 'res_code': 400},status=400)

class UserSearch(APIView):

    @TokenRequired()
    def get(self, request, *args, **kwargs):
        """
            Handles searching for users by email or name.

            GET Request:
            - Requires 'q' parameter for search query.
            - Retrieves users matching the search query.
            - Returns success or failure response based on operation outcome.
        """
        try:
            query = request.data.get('q', '')
            users = results = ApplicationUser.objects.filter(Q(email__iexact=query) | Q(name__icontains=query))
            user_data = [{'id': user.id, 'email': user.email, 'name': user.name} for user in users] 
            return JsonResponse({'res_status':'success', 'res_str': SEARCH_SUCCESS_STR,'data': user_data}, status=200)
        except Exception as e:
            return JsonResponse({'res_status':'failed', 'res_str': GENERIC_ERROR_STR , 'res_code': 400},status=400)

class FriendRequestView(APIView):
    """
        Handles friend requests.

        POST Request:
        - Requires 'to_user_id' and 'from_user_id' parameters.
        - Checks recent friend requests and limits them.
        - Saves the friend request and returns success or failure response based on operation outcome.

        GET Request:
        - Requires 'user_id' parameter for filtering pending friend requests.
        - Retrieves pending friend requests for the specified user.
        - Returns success or failure response based on operation outcome.
    """
    @TokenRequired()  # Apply TokenRequired decorator to the post method
    def post(self, request, *args, **kwargs):
        try:
            params = request.POST
            to_user_id = params.get('to_user_id')
            from_user_id = params.get('from_user_id') 

            # Check recent friend requests sent by the from_user_id within the last minute
            recent_requests_count = get_recent_friend_requests(from_user_id).count()

            # Check if recent requests exceed the limit (e.g., 3 requests in the last minute)
            if recent_requests_count > 3:
                return JsonResponse({'res_status': 'failed', 'res_str': MIN_3_REQ_STR, 'res_code': 400}, status=400)

            # Fetch from_user and to_user objects based on their IDs
            from_user = get_user(from_user_id)
            to_user = get_user(to_user_id)

            # Create a new FriendRequest instance
            friend_request = FriendRequest(from_user_id=from_user, to_user_id=to_user)
            friend_request.save()

            # Construct result string with current time and timezone
            result_string = f"FriendRequest from {from_user.name} to {to_user.name} at {datetime.now()} {str(timezone.get_current_timezone_name())}"
            return JsonResponse({'res_status': 'success', 'res_str': result_string, 'res_code': 200}, status=200)
        except ValueError as e:
            return JsonResponse({'res_status': 'failed', 'res_str': str(e), 'res_code': 400}, status=400)
        except Exception as e:
            return JsonResponse({'res_status': 'failed', 'res_str': GENERIC_ERROR_STR, 'res_code': 400}, status=400)

    @TokenRequired()
    def get(self, request, *args, **kwargs):
        try:
            user = request.GET.get('user_id')
            pending_requests = FriendRequest.objects.filter(from_user_id__email = user,status='pending')
            requests_data = [{'id': req.id, 'from_user': req.from_user_id.email,'timestamp': req.timestamp, 
                                'to_user': req.to_user_id.email, 'to_user_name':req.to_user_id.name} for req in pending_requests]
            return JsonResponse({'res_status':'success', 'res_str': PENDING_FRND_RQST_SUCCESS, 'data':requests_data})
        except Exception as e:
            return JsonResponse({'res_status':'failed', 'res_str': GENERIC_ERROR_STR , 'res_code': 400},status=400)

class FriendsList(APIView):

    @TokenRequired()
    def get(self, request, *args, **kwargs):
        """
            Handles retrieving the list of friends.

            GET Request:
            - Requires 'user_id' parameter for filtering accepted friend requests.
            - Retrieves accepted friend requests for the specified user.
            - Returns success or failure response based on operation outcome.
        """
        try:
            user_id = request.GET.get('user_id')
            friends = FriendRequest.objects.filter(from_user_id__email = user,status='accepted')
            friends_data = [{'id': friend.id, 'email': friend.email, 'name': friend.name} for friend in friends]
            return JsonResponse({'res_status':'success', 'res_str': FRND_LIST_STR_SUCCESS, 'data':friends_data},status=200)
        except Exception as e:
            return JsonResponse({'res_status':'failed', 'res_str': GENERIC_ERROR_STR , 'res_code': 400},status=400)

class FriendRequestAction(APIView):

    @TokenRequired()
    def post(self, request, *args, **kwargs):
        """
            Handles accepting or rejecting friend requests.

            POST Request:
            - Requires 'action' parameter (accepted/rejected) and user session information.
            - Validates the action parameter and updates the friend request status.
            - Returns success or failure response based on operation outcome.
        """
        try:
            user = request.session.get('user_id')
            action = request.data.get('action')
            if action not in ['accepted','rejected']:
                return JsonResponse({'res_status':'failed', 'res_str': INVALID_REQUEST_STR, 'res_code': 400},status=400)
            req = FriendRequest.objects.get(to_user_id__email = user)
            if req.status == 'pending':
                if action == 'accepted':
                    req.status = 'accepted'
                else:
                    req.status = 'rejected'
                req.save()
                return JsonResponse({'res_status':'success', 'res_str':'Request '+ str(req.status)},status=200)
            else: 
                return JsonResponse({'res_status':'failed', 'res_str': FRND_RQST_STR, 'res_code': 400},status=400)
        except Exception as e:
            return JsonResponse({'res_status':'failed', 'res_str': GENERIC_ERROR_STR , 'res_code': 400},status=400)
