from django import forms
from django.db.models.fields import TimeField
from django.forms.widgets import TimeInput
from django.conf import settings
from .models import Invoice
from timesheet.models import Timesheet
from hospitals.models import Hospital

User = settings.AUTH_USER_MODEL

class DateInput(forms.DateInput):
    input_type = 'date'

class InvoiceModelForm(forms.ModelForm):
    hospital_name = forms.ModelChoiceField(queryset=Hospital.objects.all().order_by('name'), to_field_name='name')

    class Meta:
        model = Invoice
        fields = [
            'hospital_name',
            'date_from',
            'date_to',      
        ]

        widgets = {
            'date_from': DateInput(),
            'date_to': DateInput(),            
        }