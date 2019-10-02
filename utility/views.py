from django.shortcuts import render, HttpResponse, reverse
import django.contrib.auth.models as contrib
from django.contrib.auth.decorators import login_required
from .forms import PurchaseRequestForm, PurchaseRequestFilterForm, FundForm, FundDistributionForm,TokenForm
from utility.models import Employee, PurchaseRequest, HOD, Fund, Department, FundDistribution, Notification, PurchaseReqLog
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from accounts.choices import PURCHASE_STATUS,USER_TYPES,DEPARTMENT

from .utils import * 


@login_required
def create_purchase_request(request):
    if request.method == 'GET':
        form = PurchaseRequestForm(request.POST or None)
        employee=Employee.objects.get(user__id__exact = request.user.id)
        department = dict(DEPARTMENT).get(employee.department.id)
        date=timezone.now()
        return render(request, 'utility/purchase_request.html', {'form':form,'department':department,'date':date})

    if request.method == 'POST':
        try:
            employee = Employee.objects.get(user__id__exact = request.user.id)
            department = employee.department
            
            purchase_request = PurchaseRequest(
                purpose = request.POST['purpose'], 
                specification = getHTML(request),
                totalCost = request.POST['totalCost'],
                description = request.POST['description'],
                employee = employee,
                department = department,
                log = "Purchase Request Created by on {}".format(timezone.now()),
                )
            purchase_request.save()
            purchase_request_log=PurchaseReqLog(
                purchaseRequest=purchase_request,
                changedTo=0
            )
            purchase_request_log.save()
            department = dict(DEPARTMENT).get(employee.department.id)
            date=timezone.now()
            context={'post':request.POST,'department':department,'date':date,'specification':getHTML(request)}
            return render(request,'utility/purchase_request_pdf.html',context)
        except:
            return HttpResponse("Failed to generate purchase request")

    return HttpResponse("Purchase request created")

@login_required
def dashboard_view(request):
    employee=Employee.objects.get(user__id=request.user.id)
    hod= HOD.objects.filter(hOD__id=employee.id,currentlyServing='Y')
    notifications = get_all_notifications(employee.id)
    if len(hod)!=0:
        return render(request,'utility/dashboard.html',
        {'user_type':'HOD','notifications':notifications,}
        )
    else:
        context={
            'user_type':dict(USER_TYPES).get(employee.employeeType),
            'notifications':notifications,
        }
        return render(request,'utility/dashboard.html',context)

@login_required
def view_purchase_request_employee(request):
    try:
        purchase_requests = PurchaseRequest.objects.filter(employee__user__id = request.user.id)
    except:
        return HttpResponse("You have not created any purchase request")
    # form = PurchaseRequestFilterForm()
    return render(request, 'utility/view_all_purchase_requests.html', {'purchase_requests':purchase_requests,'formExists':False})

@login_required
def view_purchase_request_department(request,w_or_a='waiting'):
    purchase_requests=purchase_requests_per_user_type(request,w_or_a)
    if purchase_requests['result']==True:
        form = PurchaseRequestFilterForm()
        context={'purchase_requests':purchase_requests['content'], 'form':form,'formExists': True,'form':form}
        return render(request, 'utility/view_all_purchase_requests.html',context)
    else:
        return purchase_requests['content']
        

@login_required
def view_purchase_request(request, id):
    try:
        purchase_requests = PurchaseRequest.objects.get(id = id)
        user=purchase_requests.employee.user
        employee_name = user.first_name + " " + user.last_name
        status = dict(PURCHASE_STATUS).get(purchase_requests.currentStatus)
        ar=get_request_logs(id)
        context={'purchase_request':purchase_requests,
             'employee_name':employee_name,
              'status':status,
              'logs': ar,
              'ForwardReject':False,
              'accounts':False}
        button=requiresForward(id,request.user.id)
        if button==True:
            context['ForwardReject']=True
            if Employee.objects.get(user__id=request.user.id).employeeType==2:
                context['accounts']=True
                context['stats']=get_stats_department(id)
                # print('reached')
            return render(request, 'utility/view_purchase_request.html', context)
        return render(request, 'utility/view_purchase_request.html', context)
    except:
        raise Http404("No such purchase request exists")

@login_required
def filter(request):
    if request.method == 'GET':
        form = PurchaseRequestFilterForm()
        return render(request, 'utility/purchase_request_filter.html', {'form':form})
    if request.method == 'POST':
        query_result=purchase_requests_with_filters(request.POST)
        form = PurchaseRequestFilterForm()
        context={'purchase_requests':query_result,'formExists': True,'form':form}
        return render(request, 'utility/view_all_purchase_requests.html', context)
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
def list_funds(request):
    employee=Employee.objects.get(user__id=request.user.id)
    if employee.employeeType!=4:
        return HttpResponse("you don't have access to this page")
    try:
        funds=Fund.objects.all()
        return render(request,'utility/list_funds.html',{'funds':funds})
    except:
        return HttpResponse('no funds yet')

@login_required
def distribute_fund(request, fid):
    n = len(Department.objects.all())
    form = FundDistributionForm(request.POST,n=n )
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
    
    return render(request, 'utility/fund_distribution.html', {'form':form, 'fund_stats':coreFund,'noOfDepts':n})

@login_required
def update_status(request, action, id):
    purchase_request = PurchaseRequest.objects.get(id = id)
    purchase_request_log=PurchaseReqLog(
            purchaseRequest=purchase_request,
            changedTo=purchase_request.currentStatus,
            comments=request.POST['comment']
    )
    employee=Employee.objects.get(user__id=request.user.id)
    if action=='forward':
        if employee.employeeType == 1:
            purchase_request.currentStatus = 1
            purchase_request_log.changedTo = 1
        elif employee.employeeType == 2:
            purchase_request.currentStatus = 2
            purchase_request_log.changedTo = 2
        elif employee.employeeType == 3:
            purchase_request.currentStatus = 3
            purchase_request_log.changedTo = 3
        elif employee.employeeType == 4:
            purchase_request.currentStatus = 4
            purchase_request_log.changedTo = 4
        elif employee.employeeType == 5:
            purchase_request.currentStatus = 5
            purchase_request_log.changedTo = 5
        else:
            return HttpResponse("Sorry, you don't have priviledege to perform this action")
    elif action=='reject':
        purchase_request.currentStatus = 6
        purchase_request_log.changedTo = 6
    purchase_request.save()
    purchase_request_log.save()
    new_notification = Notification(purchaseRequest = purchase_request, statusUpdate = purchase_request.currentStatus)
    new_notification.save()
    return HttpResponseRedirect(reverse('purchase:view_purchase_request', args=(id,)))

@login_required
def physical_token(request, id, action='forward'):
    form = TokenForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'utility/purchase_request_filter.html', {'form':form})

    if request.method == 'POST':
        form=TokenForm(request.POST)
        if form.is_valid():
            token=form.cleaned_data['token']
            # comment=form.cleaned_data['comment']
            try:
                #for now the token is the id
                PurchaseRequest.objects.get(id=token)
                return update_status(request,action,id)
            except :
                return HttpResponse('Invalid token')

def get_all_notifications(employee_id):
    notifications = Notification.objects.filter(purchaseRequest__employee__id = employee_id).order_by('date')
    notif_list = [(str(x),x.purchaseRequest.id) for x in notifications]
    return notif_list

@login_required
def view_notification(request,id):
    Notification.objects.filter(purchaseRequest__id = id).seen = 'Y'
    return HttpResponseRedirect(reverse('purchase:view_purchase_request', args=(id,)))
