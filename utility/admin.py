from django.contrib import admin
from .models import Employee, Department, PurchaseRequest, Fund, FundDistribution, HOD, Notification, PurchaseReqLog

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(PurchaseRequest)
admin.site.register(Fund)
admin.site.register(FundDistribution)
admin.site.register(HOD)
admin.site.register(Notification)
admin.site.register(PurchaseReqLog)