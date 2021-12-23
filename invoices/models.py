from datetime import datetime, timezone
from decimal import Decimal
from django.db import models
from django.conf import settings
from hospitals.models import Hospital

# Create your models here.
User = settings.AUTH_USER_MODEL

class Invoice(models.Model):
    hospital_name = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    invoice_status = models.CharField(max_length=20, null=True, blank=True, default="CREATED")
    status_date = models.DateField(auto_now_add=False)    
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_from = models.DateField(auto_now=False, auto_now_add=False)
    date_to = models.DateField(auto_now=False, auto_now_add=False)
    invoice_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    created_date = models.DateField(auto_now_add=False)

    def create_invoice_number(self):
        hospital_code = self.hospital_name.hospital_code
        max_invoice_number = self.hospital_name.max_invoice_number + 1
        self.invoice_number = max_invoice_number
        
        return hospital_code + str(max_invoice_number).zfill(5)
    
    # Overrides the save function to update fields in the database
    def save(self, *args, **kwargs):
        # On invoice creation, set today's date on status and creation fields
        if not self.id:
            self.created_date = datetime.now().date()
            self.status_date = datetime.now().date()

        self.invoice_number = self.create_invoice_number()
        super(Invoice, self).save(*args, **kwargs)