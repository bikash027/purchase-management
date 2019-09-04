from django.urls import path
from .views import create_purchase_request, view_purchase_request_employee, view_purchase_request_department, view_purchase_request

urlpatterns = [
    path('create',create_purchase_request, name='create_purchase_request'),
    path('employee/view',view_purchase_request_employee, name='view_purchase_request_employee'),
    path('department/view',view_purchase_request_department, name='view_purchase_request_department'),
    path('view/<int:id>',view_purchase_request,name='view_purchase_request'),
]
