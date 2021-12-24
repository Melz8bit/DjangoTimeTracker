from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

STATE_CHOICES = [
    ('FL', 'Florida'),
    ('GA', 'Georgia')
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", unique=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length = 2, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=5)
    email = models.EmailField(max_length=254, default='N/A')
    telephone = models.CharField(max_length=10)  
