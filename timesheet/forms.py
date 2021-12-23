from django import forms
from django.db.models.fields import TimeField
from django.forms.widgets import TimeInput
from django.conf import settings
from .models import Timesheet
from hospitals.models import Hospital

User = settings.AUTH_USER_MODEL

class DateInput(forms.DateInput):
    input_type = 'date'

class TimesheetModelForm(forms.ModelForm):
    hospital_name = forms.ModelChoiceField(queryset=Hospital.objects.all().order_by('name'), to_field_name='name')    
    clock_in = forms.TimeField(required=True, widget=TimeInput(attrs={'type':'time'}))
    clock_out_lunch = forms.TimeField(required=False, widget=TimeInput(attrs={'type':'time'}))
    clock_in_lunch = forms.TimeField(required=False, widget=TimeInput(attrs={'type':'time'}))    
    clock_out = forms.TimeField(required=True, widget=TimeInput(attrs={'type':'time'}))
    bonus_amount = forms.DecimalField(initial=0.00)

    """ def __init__(self, *args, **kwargs):
        username = kwargs.pop('username', None)
        super(Hospital, self).__init__(*args, **kwargs)

        if username:
            self.fields['username'].queryset = User.objects.filter(account=username) """

    class Meta:
        model = Timesheet
        fields = [
            'date_worked',
            'hospital_name',
            'clock_in',
            'clock_out_lunch',
            'clock_in_lunch',
            'clock_out',
            'hourly_rate',
            'bonus_amount',
        ]
        widgets = {            
            'date_worked': DateInput(),
            'clock_in': TimeInput(),
            'clock_out_lunch': TimeInput(),
            'clock_in_lunch': TimeInput(),
            'clock_out': TimeInput(),
        }