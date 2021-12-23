from django import forms
import django_filters
from django_filters import DateFilter, ModelChoiceFilter
from .models import Timesheet
from hospitals.models import Hospital

user = ''

class DateInput(forms.DateInput):
    input_type = 'date'

class TimesheetFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TimesheetFilter, self).__init__(*args, **kwargs)
        self.filters['hospital_name_filter'].queryset = Hospital.objects.filter(username=self.user).order_by('name')

    start_date = DateFilter(field_name='date_worked', lookup_expr='gte', label='Start Date', widget=DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='date_worked', lookup_expr='lte', label='End Date', widget=DateInput(attrs={'type': 'date'}))        
    hospital_name_filter = ModelChoiceFilter(
        field_name='hospital_name', 
        queryset=None,
        label='Hospital Name'
    )

    class Meta:
        model = Timesheet
        fields = [
            'start_date',
            'end_date',
            'hospital_name_filter',
        ]
        
        