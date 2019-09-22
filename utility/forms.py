from django import forms
from .models import PurchaseRequest, Employee, Department, Fund
from accounts.choices import *
from datetime import datetime
from django.contrib.admin.widgets import AdminDateWidget

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = [
            'purpose', 'specification', 'totalCost'
        ]

class PurchaseRequestFilterForm(forms.Form):
    # purchase_request_id=forms.CharField(max_length)
    employee_id = forms.CharField(max_length = 50, required=False)
    department_id = forms.ChoiceField(choices = DEPARTMENT, required=False)
    currentStatus = forms.ChoiceField(choices = PURCHASE_STATUS, required=False)
    moneyGranted = forms.ChoiceField(choices = BOOLEAN, required=False)
    startDate = forms.DateField(required=False, 
                widget = forms.SelectDateWidget(
                    empty_label=("Choose Year", "Choose Month", "Choose Day"),
                    )
                )
    endDate = forms.DateField(required=False, 
                widget = forms.SelectDateWidget(
                    empty_label=("Choose Year", "Choose Month", "Choose Day"),
                    )
                )
    def clean(self, *args, **kwargs):
        emp_id = self.cleaned_data.get('employee_id')
        dept_id = self.cleaned_data.get('department_id')
        sDate = self.cleaned_data.get('startDate')
        eDate = self.cleaned_data.get('endDate')

        try:
            Employee.objects.get(emp_id)
        except:
            raise forms.ValidationError('Employee with given ID does not exists')

        try:
            Department.objects.get(dept_id)
        except:
            raise forms.ValidationError('Department with given ID does not exists')

        if datetime(sDate) > datetime(eDate):
            raise forms.ValidationError("Start Date should be before End Date") 
        
        return super(PurchaseRequestFilterForm, self).clean(*args, **kwargs)

class FundForm(forms.ModelForm):
    dateOfFundReceive = forms.DateField(required=False, 
                widget = forms.SelectDateWidget(
                    empty_label=("Choose Year", "Choose Month", "Choose Day"),
                    )
                )
    def clean(self, *args, **kwargs):
        return super(FundForm, self).clean(*args, **kwargs)
        
    class Meta:
        model = Fund
        fields = ['amount', 'dateOfFundReceive', 'financialYear', 'fundDescription']

class FundDistributionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n')
        super(FundDistributionForm, self).__init__(*args, **kwargs)
        departments = Department.objects.all()
        for i in range(n):
            self.n = n
            self.fields['department%d' %i] = forms.CharField(initial = departments[i].id, disabled = True)
            self.fields['amount%d' %i] = forms.FloatField(initial = 0.0)

class TokenForm(forms.Form):
    token = forms.IntegerField(label='token', required=True)
    comment=forms.CharField(label='comment',required=False)
