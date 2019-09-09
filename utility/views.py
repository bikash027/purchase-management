from django.shortcuts import render, HttpResponse, reverse
import django.contrib.auth.models as contrib
from django.contrib.auth.decorators import login_required
from .forms import PurchaseRequestForm, PurchaseRequestFilterForm, FundForm, FundDistributionForm
from utility.models import Employee, PurchaseRequest, HOD, Fund, Department, FundDistribution, Notification
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from accounts.choices import PURCHASE_STATUS

# GENERIC FUNCTION TO FILTER PURCHASE REQUESTS
def purchase_requests_with_filters(kwargs):
    query_result = PurchaseRequest.objects.all()

    if 'employee_id' in kwargs and len(kwargs['employee_id'].strip(' ')) > 0:
        query_result = query_result.filter(employee__id = kwargs['employee_id'])

    if 'department_id' in kwargs:
        # filter only if valid department is selected
        # else all departments is selected
        try:
            Department.objects.get(kwargs['department_id'])
            query_result = query_result.filter(department__id = kwargs['department_id'])
        except:
            pass

    if 'currentStatus' in kwargs:
        temp_result = query_result.filter(currentStatus = int(kwargs['currentStatus'][0]) )
        for i in range(1,len(kwargs['currentStatus'])):
            temp_result |= query_result.filter(currentStatus = int(kwargs['currentStatus'][i]) )
        query_result = temp_result

    if 'moneyGranted' in kwargs:
        query_result = query_result.filter(moneyGranted = kwargs['moneyGranted'])
        
    if 'date' in kwargs:
        query_result = query_result.filter(dateOfIndent__gte = kwargs['date'][0], dateOfIndent__lte = kwargs['date'][1])
    
    for x in kwargs:
        print(x,kwargs[x])
    
    return query_result

@login_required
def create_purchase_request(request):
    if request.method == 'GET':
        form = PurchaseRequestForm(request.POST or None)
        return render(request, 'utility/purchase_request.html', {'form':form})

    if request.method == 'POST':
        try:
            employee = Employee.objects.get(user__id__exact = request.user.id)
            department = employee.department
            
            purchase_request = PurchaseRequest(
                purpose = request.POST['purpose'], 
                specification = request.POST['specification'],
                totalCost = request.POST['totalCost'],
                employee = employee,
                department = department,
                log = "Purchase Request Created by on {}".format(timezone.now()),
                )
            purchase_request.save()

        except:
            return HttpResponse("Failed to generate purchase request")

    return HttpResponse("Purchase request created")

@login_required
def view_purchase_request_employee(request):
    try:
        purchase_requests = PurchaseRequest.objects.filter(employee__user__id = request.user.id)
    except:
        return HttpResponse("You have not created any purchase request")
    return render(request, 'utility/view_all_purchase_requests.html', {'purchase_requests':purchase_requests})

@login_required
def view_purchase_request_department(request):
    employee = Employee.objects.get(user__id = request.user.id)
    try:
        department_query = HOD.objects.filter(hOD__id = employee.id, currentlyServing = 'Y')
        departments = [department.department.id for department in department_query]
    except:
        return HttpResponse("Sorry, You don't have required previlideges to perform this action")
    if len(departments) > 0:
        try:
            purchase_requests = PurchaseRequest.objects.filter(department__id = departments[0])
            for i in range(1, len(departments)):
                purchase_requests |= PurchaseRequest.objects.filter(department__id = departments[i])
            return render(request, 'utility/view_all_purchase_requests.html', {'purchase_requests':purchase_requests})
        except:
            return HttpResponse("There are no purchase requests from your department")

@login_required
def view_purchase_request(request, id):
    try:
        purchase_requests = PurchaseRequest.objects.get(id = id)
        user = contrib.User.objects.get(id = request.user.id)
        employee_name = user.first_name + " " + user.last_name
        status = dict(PURCHASE_STATUS).get(purchase_requests.currentStatus)
        return render(request, 'utility/view_purchase_request.html', 
            {'purchase_request':purchase_requests, 'employee_name':employee_name, 'status':status})
    except:
        raise Http404("No such purchase request exists")

@login_required
def filter(request):
    if request.method == 'GET':
        form = PurchaseRequestFilterForm()
        return render(request, 'utility/purchase_request_filter.html', {'form':form})
    if request.method == 'POST':
        purchase_requests_with_filters(request.POST)
        return HttpResponse("Processing")
    return HttpResponse("Invalid Query")

@login_required
def add_fund(request):
    form = FundForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'utility/purchase_request_filter.html', {'form':form})
    
    if request.method == 'POST':
        new_fund = Fund(
            amount = form.data.get('amount'),
            dateOfFundReceive = form.data.get('dateOfFundReceive'),
            financialYear = form.data.get('financialYear'),
            fundDescription = form.data.get('fundDescription'),
        )
        new_fund.save()
        return HttpResponse("Added to core fund")

@login_required
def distribute_fund(request, fid):

    print("fid",fid)
    form = FundDistributionForm(request.POST, n = len(Department.objects.all()))
    try:
        coreFund = Fund.objects.get(id = fid)
    except:
        return HttpResponse("Fund ID doesn't exist")

    if form.is_valid() == True:
        sum_total = 0
        for i in range(len(Department.objects.all())):
            sum_total += form.cleaned_data.get('amount%d'%i)
        fund_id = fid
        _fund = Fund.objects.get(id = fund_id)
        available = _fund.amount
        if sum_total <= available:
            for i in range(len(Department.objects.all())):
                _department = Department.objects.get(id = form.cleaned_data.get('department%d'%i))
                fd = FundDistribution(
                    fund = _fund, 
                    department = _department, 
                    totalAmountReceived = form.cleaned_data.get('amount%d'%i)
                )
                fd.save()
        else:
            return HttpResponse("Fund distribution could not be done as the total exceeds the available fund")
    
    return render(request, 'utility/fund_distribution.html', {'form':form, 'fund_stats':coreFund})

@login_required
def update_status(request, id):
    purchase_request = PurchaseRequest.objects.get(id = id)
    purchase_request.currentStatus += 1
    purchase_request.save()

    new_notification = Notification(purchaseRequest = purchase_request, statusUpdate = purchase_request.currentStatus)
    new_notification.save()
  
    return HttpResponseRedirect(reverse('purchase:view_purchase_request', args=(id,)))

@login_required
def get_all_notifications(employee_id):
    notifications = Notification.objects.filter(purchaseRequest__employee__id = employee_id).order_by('date')
    return notifications
