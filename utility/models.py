from django.db import models
from accounts.choices import *
import django.contrib.auth.models as contrib

class Department(models.Model):
    id = models.CharField(max_length = 3, choices=DEPARTMENT, default='CSE', primary_key=True)

    def __str__(self):
        return str(dict(DEPARTMENT).get(self.id))+" : "+str(self.id)

class Employee(models.Model):
    user = models.OneToOneField(contrib.User, on_delete = models.CASCADE, null=True)
    id = models.CharField(max_length = 20, primary_key = True)
    active = models.CharField(max_length = 1, choices=BOOLEAN, default='Y')
    employeeType = models.IntegerField(choices=USER_TYPES, default=1)
    jobType = models.CharField(max_length = 2, choices=EMPLOYEE_TYPE, default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    dateOfBirth = models.DateField()
    address = models.TextField()
    dateOfJoining = models.DateField()
    contactNo = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)+" : "+str(self.user.first_name)+" "+str(self.user.last_name)

class HOD(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    hOD = models.ForeignKey(Employee, on_delete=models.CASCADE)
    dateOfAppointment = models.DateField(blank=False, null=False)
    lastDateOfService = models.DateField(blank=True, null=True)
    currentlyServing = models.CharField(choices = BOOLEAN, default='Y', max_length=1)

    def __str__(self):
        return str(self.department)+ " : "+str(self.hOD)
   
class Fund(models.Model):
    id = models.AutoField(primary_key = True)
    amount = models.FloatField(blank=False, null=False)
    dateOfFundReceive = models.DateField()
    financialYear = models.IntegerField(choices = ACADEMIC_SESSION, default=0)
    fundDescription = models.TextField(blank=False, null=False)
    fundDistributed = models.CharField(choices = BOOLEAN, default='N', max_length=1)

    def __str__(self):
        return str(self.id)+" : "+str(self.amount)

class FundDistribution(models.Model):
    id = models.AutoField(primary_key=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    totalAmountReceived = models.FloatField(default = 0.0)
    fundUsed = models.FloatField(default = 0.0)

    def __str__(self):
        return str(dict(DEPARTMENT).get(self.department.id))+" : "+str(self.totalAmountReceived)

class PurchaseRequest(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    dateofIndent = models.DateField(auto_now_add=True)
    purpose = models.TextField()
    specification = models.TextField()
    totalCost = models.FloatField(default = 0)
    currentStatus = models.IntegerField(choices = PURCHASE_STATUS, default=0)
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    moneyGranted = models.CharField(choices = BOOLEAN, max_length=1, default='N')
    log = models.TextField()

    def __str__(self):
        return str(self.totalCost)+" requested by "+str(self.employee)

class Notification(models.Model):
    id = models.AutoField(primary_key = True)
    purchaseRequest = models.ForeignKey(PurchaseRequest, on_delete = models.CASCADE)
    seen = models.CharField(choices = BOOLEAN, max_length = 1, default='N')
    statusUpdate = models.IntegerField(default = 0)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.purchaseRequest.purpose) + " status has changed to " + str(dict(PURCHASE_STATUS).get(self.statusUpdate))

class PurchaseReqLog(models.Model):
    purchaseRequest=models.ForeignKey(PurchaseRequest,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add= True)
    changedTo=models.IntegerField(choices = PURCHASE_STATUS, default=1)
    comments=models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.changedTo)+str(self.date)