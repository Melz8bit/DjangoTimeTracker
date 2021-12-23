from typing import List
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Hospital
from .forms import HospitalModelForm

# Create your views here.
def hospital_create_view(request, *args, **kwargs):
    template_name = 'hospitals/hospital_create.html'
    
    if request.method == 'POST':
        form = HospitalModelForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.user
            obj.save()

            form = HospitalModelForm()
        
        return HttpResponseRedirect('/')
    else:
        form = HospitalModelForm()

    return render(request, template_name, {'form': form})
        

def hospital_detail_view(request, id):
    template_name = 'hospitals/hospital_detail.html'
    obj = get_object_or_404(Hospital, id=id)
    return render(request, template_name, {'object': obj})

def hospital_list_view(request, *args, **kwargs):
    template_name = 'hospitals/hospital_list.html'
    queryset = Hospital.objects.filter(username=request.user)
    context = {'object_list': queryset}
    return render(request, template_name, context)

def hospital_update_view(request, id):
    template_name = 'hospitals/hospital_create.html'
    
    try:
        instance = get_object_or_404(Hospital, id=id)
        form = HospitalModelForm(request.POST or None, instance=instance)          
                    
        if form.is_valid():            
            instance = form.save(commit=False)
            instance.save()
            
            form = HospitalModelForm()      
        
    except Hospital.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        return render(request, template_name, {'form': form}) 
    else:
        return HttpResponseRedirect('/')