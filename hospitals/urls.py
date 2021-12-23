from django.urls import path
from .views import (
    hospital_create_view,
    hospital_detail_view,
    hospital_list_view,
    hospital_update_view
)

app_name = 'hospitals'
urlpatterns = [
    path('', hospital_list_view, name='hopsital-list'),
    path('<int:id>/', hospital_detail_view, name='hospital-detail'),
    path('create/', hospital_create_view, name='hospital-create'),
    path('<int:id>/update/', hospital_update_view, name='hospital-update'),
]