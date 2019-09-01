from django.db import models
from accounts.choices import *
import django.contrib.auth.models as contrib

class Department(models.Model):
    DeptID = models.CharField(max_length = 3, choices=DEPARTMENT, default=1, primary_key=True)

    def __str__(self):
        return "Department :"+str(dict(DEPARTMENT).get(self.DeptID))

class Employee(models.Model):
    User = models.OneToOneField(contrib.User, on_delete = models.CASCADE, null=True)
    EmpID = models.CharField(max_length = 20, primary_key = True)
    ActiveStatus = models.CharField(max_length = 1, choices=BOOLEAN, default='Y')
    UserType = models.IntegerField(choices=USER_TYPES, default=1)
    EmpType = models.CharField(max_length = 2, choices=EMPLOYEE_TYPE, default=1)
    DeptID = models.ForeignKey(Department, on_delete=models.CASCADE)
    DOB = models.DateField()
    Address = models.TextField()
    DOJ = models.DateField()
    ContactNo = models.CharField(max_length=10)

    def __str__(self):
        return "Employee ID is "+str(self.EmpID)

class HOD(models.Model):
    DeptID = models.ForeignKey(Department, on_delete=models.CASCADE)
    HODID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    DateOfAppointment = models.DateField(blank=False, null=False)
    LastDateOfService = models.DateField(blank=True, null=True)
    CurrentlyServing = models.CharField(choices = BOOLEAN, default='Y', max_length=1)

    def __str__(self):
        return "HOD of dept "+str(self.DeptID)+ " is "+str(self.HODID)

    
class CoreFund(models.Model):
    FundID = models.AutoField(primary_key = True)
    Amount = models.FloatField(blank=False, null=False)
    DateOfFundReceive = models.DateField()
    FinancialYear = models.IntegerField(choices = ACADEMIC_SESSION, default=0)
    FundDescription = models.TextField(blank=False, null=False)
    FundDistributed = models.CharField(choices = BOOLEAN, default='N', max_length=1)

    def __str__(self):
        return "Amount "+str(self.Amount)+" received in Session "+str(dict(ACADEMIC_SESSION).get(self.FinancialSession))

class FundDistribution(models.Model):
    DistID = models.AutoField(primary_key=True)
    FundID = models.ForeignKey(CoreFund, on_delete=models.CASCADE)
    DeptID = models.ForeignKey(Department, on_delete=models.CASCADE)
    TotalAmountReceived = models.FloatField(default = 0.0)
    FundUsed = models.FloatField(default = 0.0)

    def __str__(self):
        return "Fund for Deprtment"+str(dict(DEPARTMENT).get(self.DeptID))+" is "+str(self.TotalAmountReceived)

class PurchaseRequest(models.Model):
    PurchaseID = models.AutoField(primary_key=True, blank=False, null=False)
    DateofIndent = models.DateField(auto_now_add=True)
    Purpose = models.TextField()
    Specification =models.TextField()
    RatePerUnit = models.FloatField()
    NoOfItemsReq = models.IntegerField()
    CurrentStatus = models.IntegerField(choices = PURCHASE_STATUS, default=0)
    EmpID = models.ForeignKey(Employee, on_delete = models.CASCADE)
    DeptID = models.ForeignKey(Department, on_delete = models.CASCADE)
    MoneyGranted = models.CharField(choices = BOOLEAN, max_length=1, default='N')
    Log = models.TextField()

    def __str__(self):
        return "PurchaseRequest "+str(self.PID)

# class AccountSection(models.Model):
#     AccountID = models.AutoField(primary_key=True)
#     PurchaseID = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
#     MoneyGranted = models.CharField(choices = BOOLEAN, max_length=1)
#     AccountOfficer = models.ForeignKey(Employee, on_delete=models.CASCADE)

#     def __str__(self):
#         return "AccountID "+str(self.AccountID)
