from django.urls import path
from .views import (
    invoice_create_view,
    invoice_detail_view,
    #invoice_list_view,
    #invoice_update_view,
    invoice_pdf_view,
)

app_name = 'invoices'
urlpatterns = [
    #path('', invoice_list_view, name='invoice-list'),
    path('<int:id>/', invoice_detail_view, name='invoice-detail'),
    path('create/', invoice_create_view, name='invoice-create'),
    #path('<int:id>/update/', invoice_update_view, name='invoice-update'),
    path('<int:id>/invoice_pdf/', invoice_pdf_view, name='invoice-pdf'),
]