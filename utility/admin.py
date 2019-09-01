from django.contrib import admin
from .models import Employee, Department, PurchaseRequest, CoreFund, FundDistribution, HOD

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(PurchaseRequest)
admin.site.register(CoreFund)
admin.site.register(FundDistribution)
admin.site.register(HOD)