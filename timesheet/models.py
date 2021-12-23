from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timesince
from decimal import Decimal, getcontext
import datetime

from invoices.models import Invoice

User = settings.AUTH_USER_MODEL

# Create your models here.
class Timesheet(models.Model):    
    date_worked = models.DateField(auto_now=False, auto_now_add=False)
    clock_in = models.TimeField(auto_now=False, auto_now_add=False)
    clock_out_lunch = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    clock_in_lunch = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    clock_out = models.TimeField(auto_now=False, auto_now_add=False)
    total_hours_worked = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    bonus_amount = models.DecimalField(max_digits=6, decimal_places=2)
    hospital_name = models.CharField(max_length=70)
    invoice_number = models.ForeignKey(Invoice, null=True, blank=True, on_delete=models.SET_NULL)
    #invoice_number = models.CharField(max_length=10, blank=True, null=True)
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('timesheet:timesheet-detail', kwargs={'id':self.id})

    @property
    def get_hours_worked(self):
        clock_in = datetime.datetime.strptime(str(self.clock_in), '%H:%M:%S')
        clock_out = datetime.datetime.strptime(str(self.clock_out), '%H:%M:%S')
        clock_out_lunch = datetime.datetime.strptime(str(self.clock_out_lunch), '%H:%M:%S') if self.clock_out_lunch else datetime.datetime(1900,1,1,0,0,0)
        clock_in_lunch = datetime.datetime.strptime(str(self.clock_in_lunch), '%H:%M:%S') if self.clock_in_lunch else datetime.datetime(1900,1,1,0,0,0)
        
        clock_in_int = (clock_in.hour + (clock_in.minute / 60) + (clock_in.second / 360))
        clock_out_int = (clock_out.hour + (clock_out.minute / 60) + (clock_out.second / 360))
        clock_out_lunch_int = (clock_out_lunch.hour + (clock_out_lunch.minute / 60) + (clock_out_lunch.second / 360))
        clock_in_lunch_int = (clock_in_lunch.hour + (clock_in_lunch.minute / 60) + (clock_in_lunch.second / 360))

        hours_worked = ((clock_out_int - clock_in_int) - (clock_in_lunch_int - clock_out_lunch_int))
        self.total_hours_worked = '{0:.2f}'.format(hours_worked)
        return '{0:.2f}'.format(hours_worked)
    
    def get_daily_total_earned(self):
        daily_earned = (Decimal(self.total_hours_worked) * self.hourly_rate) + self.bonus_amount
        return Decimal('{0:.2f}'.format(daily_earned))
    
    # Overrides the save function to update fields in the database
    def save(self, *args, **kwargs):
        self.total_hours_worked = Decimal(self.get_hours_worked)
        super(Timesheet, self).save(*args, **kwargs)