from django.urls import path
from .views import (create_purchase_request, 
view_purchase_request_employee, view_purchase_request_department, view_purchase_request,
purchase_requests_with_filters, filter, add_fund, distribute_fund, update_status)

app_name = 'utility'

urlpatterns = [
    path('create',create_purchase_request, name='create_purchase_request'),
    path('employee/view',view_purchase_request_employee, name='view_purchase_request_employee'),
    path('department/view',view_purchase_request_department, name='view_purchase_request_department'),
    path('view/<int:id>',view_purchase_request,name='view_purchase_request'),
    path('filter',filter,name='filter'),
    path('add_fund',add_fund, name='add_fund'),
    path('distribute_fund/<int:fid>',distribute_fund, name='distribute_fund'),
    path('update_status/<int:id>',update_status, name='update_status'),
]
