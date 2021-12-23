from typing import List
from django.db.models.base import Model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Timesheet
from .forms import TimesheetModelForm

# Create your views here.
class TimesheetCreateView(CreateView):
    template_name = 'timesheets/timesheet_create.html'
    form_class = TimesheetModelForm
    queryset = Timesheet.objects.all()

    def form_valid(self, form):
        resp = super().form_valid(form)
        print(form.cleaned_data)
        return resp

class TimesheetDetailView(DetailView):
    template_name = 'timesheets/timesheet_detail.html'
    queryset = Timesheet.objects.all()

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Timesheet, id=id_)

class TimesheetListView(ListView):
    template_name = 'timesheets/timesheet_list.html'
    queryset = Timesheet.objects.all().order_by('date_worked')

class TimesheetUpdateview(UpdateView):
    template_name = 'timesheets/timesheet_create.html'
    form_class = TimesheetModelForm
    queryset = Timesheet.objects.all()

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Timesheet, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
