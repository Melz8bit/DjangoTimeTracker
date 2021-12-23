from django.db import models
from django.urls import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL

STATE_CHOICES = [
    ('FL', 'Florida'),
    ('GA', 'Georgia')
]

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=70)
    hospital_code = models.CharField(max_length=4, null=False, blank=False)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length = 2, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=5)
    email = models.EmailField(max_length=254, default='N/A')
    telephone = models.CharField(max_length=10)    
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)    
    max_invoice_number = models.IntegerField(default=0, blank=False, null=False)

    def get_absolute_url(self):
        return reverse('hospitals:hospital-detail', kwargs={'id':self.id})
    
    def get_username(self):
        return self.username
    
    def increase_invoice_number(self):
        return self.max_invoice_number + 1

    # Overrides the save function to update fields in the database
    def save(self, *args, **kwargs):
        self.max_invoice_number = self.increase_invoice_number()
        super(Hospital, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name