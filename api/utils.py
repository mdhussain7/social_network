from datetime import datetime, timedelta
from django.utils import timezone
from .models import FriendRequest, ApplicationUser
import hashlib

def get_recent_friend_requests(from_user_id):
    # Calculate the datetime threshold for the past 1 minute
    threshold_time = timezone.now() - timedelta(minutes=1)

    # Query using Django ORM
    recent_requests = FriendRequest.objects.filter(
        from_user_id__email=from_user_id,
        timestamp__gte=threshold_time
    )

    return recent_requests

def get_user(user_id):
    try:
        user = ApplicationUser.objects.get(email=user_id)
        return user
    except Exception as e:
        return None

def gen_password_hash(password):
    encoded_password = password.encode('utf-8')
    return str(hashlib.sha256(encoded_password).hexdigest())