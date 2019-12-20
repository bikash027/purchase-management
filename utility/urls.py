from django.urls import path,re_path
from .views import (create_purchase_request, 
view_purchase_request_employee, view_purchase_request_department, view_purchase_request,dashboard_view,
purchase_requests_with_filters, filter, add_fund,list_funds, distribute_fund, update_status, physical_token,
view_notification,show_distribution, print_request,get_stats)

app_name = 'utility'

urlpatterns = [
	path('',dashboard_view,name="dashboard"),
    path('create',create_purchase_request, name='create_purchase_request'),
    path('employee/view',view_purchase_request_employee, name='view_purchase_request_employee'),
    path('department/view/<str:w_or_a>',view_purchase_request_department, name='view_purchase_request_department'),
    path('view/<int:id>',view_purchase_request,name='view_purchase_request'),
    path('print/<int:id>',print_request,name='print_request'),
    path('notification/<int:id>',view_notification,name='view_notification'),
    path('filter',filter,name='filter'),
    path('add_fund',add_fund, name='add_fund'),
    path('list_funds',list_funds, name='list_funds'),
    path('distribute_fund/<int:fid>',distribute_fund, name='distribute_fund'),
    path('update_status/<int:id>',update_status, name='update_status'),
    path('token/<int:id>/<str:action>',physical_token, name='physical_token'),
    path('show_distribution/<int:fid>',show_distribution, name='show_distribution'),
    path('get_stats/<str:statType>/',get_stats,name="stats"),
]
