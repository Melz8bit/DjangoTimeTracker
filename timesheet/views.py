from typing import List
from django.db.models.base import Model
from django.forms import formsets
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from .filters import TimesheetFilter
from .models import Timesheet
from .forms import TimesheetModelForm
from hospitals.forms import Hospital

# Create your views here.
@login_required
def timesheet_create_view(request, *args, **kwargs):
    template_name = 'timesheets/timesheet_create.html'

    if request.method == 'POST':
        form = TimesheetModelForm(request.POST or None)
        form.fields['hospital_name'].queryset = Hospital.objects.filter(username=request.user) # Doesn't cause multiple hospital error

        if form.is_valid():                        
            obj = form.save(commit=False)
            obj.username = request.user
            obj.save()           

            form = TimesheetModelForm()
            
        return HttpResponseRedirect('/timesheet/' + str(obj.id))
    else:
        form = TimesheetModelForm()
        form.fields['hospital_name'].queryset = Hospital.objects.filter(username_id=request.user.id)
    
    return render(request, template_name, {'form': form})     

@login_required
def timesheet_detail_view(request, id):
    template_name = 'timesheets/timesheet_detail.html'    
    obj = get_object_or_404(Timesheet, id=id)
    return render(request, template_name, {'object': obj}) 
    
@login_required
def timesheet_list_view(request, *args, **kwargs):
    template_name = 'timesheets/timesheet_list.html'
    queryset = Timesheet.objects.filter(username=request.user)

    my_filter = TimesheetFilter(request.GET, queryset=queryset, user=request.user)
    queryset = my_filter.qs

    """ if request.method == 'POST':        
        form = DateRangeFilterForm(request.POST)
        print(form.as_p)
        if form.is_valid():
            queryset = Timesheet.objects.filter(
                username=request.user, 
                date_worked__range=(
                    form.cleaned_data['start_date'],
                    form.cleaned_data['end_date']
                ),
                hospital_name=form.cleaned_data['hospital_filter']
            )
        else:
            print(form.errors) """

    context = {
        'object_list': queryset,
        'my_filter': my_filter
    }

    return render(request, template_name, context)

@login_required
def timesheet_update_view(request, id):
    template_name = 'timesheets/timesheet_create.html'
    
    try:
        instance = get_object_or_404(Timesheet, id=id)
        form = TimesheetModelForm(request.POST or None, instance=instance)          
        form.fields['hospital_name'].queryset = Hospital.objects.filter(username=request.user)
                    
        if form.is_valid():            
            instance = form.save(commit=False)
            instance.save()
            
            form = TimesheetModelForm()      
        
    except Timesheet.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        return render(request, template_name, {'form': form}) 
    else:
        return HttpResponseRedirect('/timesheet/' + str(instance.id))