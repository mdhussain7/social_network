# api/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class ApplicationUser(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'application_user'
    
    def __str__(self):
        return self.name + " ("+ self.email+")"
    
class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    
    from_user_id = models.ForeignKey(
        ApplicationUser, 
        related_name='sent_friend_requests', 
        on_delete=models.CASCADE
    )
    to_user_id = models.ForeignKey(
        ApplicationUser, 
        related_name='received_friend_requests', 
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"FriendRequest from {self.from_user_id.name} to {self.to_user_id.name}"

    class Meta:
        db_table = 'friend_request'
        unique_together = ('from_user_id', 'status')  # Enforce one request per user with 'pending' status

    def save(self, *args, **kwargs):
        if self.status == 'pending':
            # Check if there is already a pending request from this user
            existing_requests = FriendRequest.objects.filter(from_user_id=self.from_user_id, status='pending').exists()
            if existing_requests:
                raise ValueError("User already has a pending friend request.")
        
        super().save(*args, **kwargs)

class UserLoginData(models.Model):
    user_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_login_data'
    
    def __str__(self):
        return self.user_id