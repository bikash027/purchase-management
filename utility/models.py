from django.db import models
from accounts.choices import *

class Employee(models.Model):
    EmpID = models.CharField(max_length = 20, primary_key = True)
    FirstName = models.CharField(max_length = 100)
    LastName = models.CharField(max_length = 100)
    DOB = models.DateField()
    Designation = models.IntegerField(choices=DESIGNATION, default=1)
    DeptID = models.ForeignKey('Department', models.SET_NULL, blank=True, null=True,)
    Address = models.TextField()
    DOJ = models.DateField()
    ContactNo = models.CharField(max_length=10)
    ActiveStatus = models.CharField(max_length = 1, choices=BOOLEAN, default=1)
    EmpType = models.CharField(max_length = 1, choices=EMPLOYEE_TYPE, default=1)

    def __str__(self):
        return "Employee name is "+str(self.FirstName)+" "+str(self.LastName)

class Department(models.Model):
    DeptID = models.CharField(max_length = 3, choices=DEPARTMENT, default=1, primary_key = True)
    HODID = models.ForeignKey(Employee, on_delete = models.SET_NULL, blank=True, null = True)   

    def __str__(self):
        return "Department :"+str(DEPARTMENT[self.DeptID])
    
class CoreFund(models.Model):
    FundID = models.AutoField(primary_key = True)
    FyStart = models.DateField()
    Amount = models.FloatField()

    def __str__(self):
        return "Fund for year "+str(self.FY_Start)+" is "+str(self.Amount)

class FundDistribution(models.Model):
    DistID = models.AutoField(primary_key=True)
    FundID = models.ForeignKey(CoreFund, on_delete=models.CASCADE)
    DeptID = models.ForeignKey(Department, on_delete=models.CASCADE)
    TotalAmountReceived = models.FloatField()
    FundUse = models.FloatField()

    def __str__(self):
        return "Fund for Deprtment"+str(DEPARTMENT[self.DeptID])+" is "+str(self.TotalAmountReceived)

class PurchaseRequest(models.Model):
    PurchaseID = models.AutoField(primary_key=True)
    DeptID = models.ForeignKey(Department, on_delete=models.CASCADE)
    DateofIndent = models.DateField()
    Purpose = models.TextField()
    Specification =models.TextField()
    RatePerUnit = models.FloatField()
    NoOfItemsReq = models.IntegerField()
    CurrentStatus = models.IntegerField(choices = PURCHASE_STATUS)
    EmpID = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return "PurchaseRequest "+str(self.PID)

class AccountSection(models.Model):
    AccountID = models.AutoField(primary_key=True)
    PurchaseID = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
    MoneyGranted = models.CharField(choices = BOOLEAN, max_length=1)
    AccountOfficer = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return "AccountID "+str(self.AccountID)
