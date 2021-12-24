from django.urls import path
from .views import (
    update_user_view
)

app_name = 'accounts'
urlpatterns = [
    path('<username>/update/', update_user_view, name='user-update'),
]