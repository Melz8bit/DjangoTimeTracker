from django.urls import path
from .views import (
    timesheet_create_view,
    timesheet_detail_view,
    timesheet_list_view,
    timesheet_update_view,
)

app_name = 'timesheet'
urlpatterns = [
    path('', timesheet_list_view, name='timesheet-list'),
    path('<int:id>/', timesheet_detail_view, name='timesheet-detail'),
    path('create/', timesheet_create_view, name='timesheet-create'),
    path('<int:id>/update/', timesheet_update_view, name='timesheet-update'),
]