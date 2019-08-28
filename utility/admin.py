from django.contrib import admin
from .models import Employee, Department, PurchaseRequest, AccountSection, CoreFund, FundDistribution

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(PurchaseRequest)
admin.site.register(AccountSection)
admin.site.register(CoreFund)
admin.site.register(FundDistribution)