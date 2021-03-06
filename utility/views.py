from django.shortcuts import render, HttpResponse, reverse
import django.contrib.auth.models as contrib
from django.contrib.auth.decorators import login_required
from .forms import PurchaseRequestForm, PurchaseRequestFilterForm, FundForm, FundDistributionForm, TokenForm
from utility.models import Employee, PurchaseRequest, HOD, Fund, Department, FundDistribution, Notification, PurchaseReqLog
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect,JsonResponse
from accounts.choices import PURCHASE_STATUS, USER_TYPES, DEPARTMENT
from django.db.models import Q

from .utils import *


@login_required
def create_purchase_request(request):
    if request.method == 'GET':
        form = PurchaseRequestForm(request.POST or None)
        employee = Employee.objects.get(user__id__exact=request.user.id)
        department = dict(DEPARTMENT).get(employee.department.id)
        date = timezone.now()
        return render(request, 'utility/purchase_request.html', {'form': form, 'department': department, 'date': date})

    if request.method == 'POST':
        try:
            employee = Employee.objects.get(user__id__exact=request.user.id)
            department = employee.department

            purchase_request = PurchaseRequest(
                purpose=request.POST['purpose'],
                requirementProjection=request.POST['requirementProjection'],
                requirementUrgency=request.POST['requirementUrgency'],
                preferenceReason=request.POST['preferenceReason'],
                requirementPeriod=request.POST['requirementPeriod'],
                feasible=request.POST['feasible'],
                proprietary=request.POST['proprietary'],
                scheme=request.POST['scheme'],
                totalCost=request.POST['totalCost'],
                specification=getHTML(request),
                description=request.POST['description'],
                employee=employee,
                department=department,
                log="Purchase Request Created by on {}".format(timezone.now()),
            )
            purchase_request.save()
            purchase_request_log = PurchaseReqLog(
                purchaseRequest=purchase_request,
                changedTo=0
            )
            purchase_request_log.save()
            return HttpResponseRedirect(reverse('purchase:print_request', args=(purchase_request.id,)))
        except:
            return HttpResponse("Failed to generate purchase request")

    # return HttpResponse("Purchase request created")

@login_required
def print_request(request,id):
    try:
        purchase_request=PurchaseRequest.objects.get(id=id)
        context={
            'purchase_request': purchase_request,
            'department': dict(DEPARTMENT).get(purchase_request.department.id)
        }
        return render(request, 'utility/purchase_request_pdf.html',context)
    except:
        return HttpResponse("purchase request not found")


@login_required
def dashboard_view(request):
    employee = Employee.objects.get(user__id=request.user.id)
    hod = HOD.objects.filter(hOD__id=employee.id, currentlyServing='Y')
    notifications = get_all_notifications(employee.id)
    if len(hod) != 0:
        return render(request, 'utility/dashboard.html',
                      {'user_type': 'HOD', 'notifications': notifications,'department':hod[0].department }
                      )
    else:
        context = {
            'user_type': dict(USER_TYPES).get(employee.employeeType),
            'notifications': notifications,
        }
        return render(request, 'utility/dashboard.html', context)


@login_required
def view_purchase_request_employee(request):
    try:
        purchase_requests = PurchaseRequest.objects.filter(
            employee__user__id=request.user.id)
    except:
        return HttpResponse("You have not created any purchase request")
    # form = PurchaseRequestFilterForm()
    return render(request, 'utility/view_all_purchase_requests.html', {'purchase_requests': purchase_requests, 'formExists': False})


@login_required
def view_purchase_request_department(request, w_or_a='waiting'):
    purchase_requests = purchase_requests_per_user_type(request, w_or_a)
    if purchase_requests['result'] == True:
        form = PurchaseRequestFilterForm()
        context = {
            'purchase_requests': purchase_requests['content'], 'form': form, 'formExists': True, 'form': form}
        return render(request, 'utility/view_all_purchase_requests.html', context)
    else:
        return purchase_requests['content']


@login_required
def view_purchase_request(request, id):
    try:
        purchase_request = PurchaseRequest.objects.get(id=id)
    except:
        raise Http404("No such purchase request exists")
    user = purchase_request.employee.user
    employee_name = user.first_name + " " + user.last_name
    status = dict(PURCHASE_STATUS).get(purchase_request.currentStatus)
    ar = get_request_logs(id)
    context = {'purchase_request': purchase_request,
               'employee_name': employee_name,
               'status': status,
               'logs': ar,
               'ForwardReject': False,
               'accounts': False,
               'canReprint': False}
    if requiresForward(id, request.user.id) == True:
        context['ForwardReject'] = True
        if Employee.objects.get(user__id=request.user.id).employeeType == 2:
            context['accounts'] = True
    if user.id == request.user.id:
        context['canReprint'] = True
    return render(request, 'utility/view_purchase_request.html', context)


def adjust_fund(pid, action):
    purchase_request = PurchaseRequest.objects.get(id=pid)
    if action == 'grant':
        current_session_year = datetime.datetime.now().year
        if(datetime.datetime.now().month < 4):
            current_session_year -= 1
        fundGranted = 0

        for fund in FundDistribution.objects.filter(department=purchase_request.department.id):
            if fund.fund.financialYear == current_session_year and fund.fundUsed < fund.totalAmountReceived:
                fundChangeAmount = min(
                    purchase_request.totalCost - fundGranted, fund.totalAmountReceived - fund.fundUsed)
                fund.fundUsed += fundChangeAmount
                fundGranted += fundChangeAmount
                fund.save()

            if fundGranted == purchase_request.totalCost:
                break

        purchase_request.financialYear = current_session_year
        purchase_request.save()
        p = PurchaseRequest.objects.get(id = pid)


    if action == 'reject':
        current_session_year = purchase_request.financialYear
        fundRecovered = 0
        for fund in FundDistribution.objects.filter(department=purchase_request.department.id):
            if fund.fund.financialYear == current_session_year and fund.fundUsed > 0:
                fundChangeAmount = min(
                    purchase_request.totalCost - fundRecovered, fund.fundUsed)
                fund.fundUsed -= fundChangeAmount
                fundRecovered += fundChangeAmount
                fund.save()

            if fundRecovered == purchase_request.totalCost:
                break


@login_required
def filter(request):
    if request.method == 'GET':
        form = PurchaseRequestFilterForm()
        return render(request, 'utility/purchase_request_filter.html', {'form': form})
    if request.method == 'POST':
        query_result = purchase_requests_with_filters(request.POST)
        form = PurchaseRequestFilterForm()
        context = {'purchase_requests': query_result,
                   'formExists': True, 'form': form}
        return render(request, 'utility/view_all_purchase_requests.html', context)
    return HttpResponse("Invalid Query")


@login_required
def add_fund(request):
    form = FundForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'utility/purchase_request_filter.html', {'form': form})
    if request.method == 'POST':
        new_fund = Fund(
            amount=form.data.get('amount'),
            dateOfFundReceive=datetime.datetime(
                int(form.data.get('dateOfFundReceive_year')),
                int(form.data.get('dateOfFundReceive_month')),
                int(form.data.get('dateOfFundReceive_day')),
            ),
            financialYear=form.data.get('financialYear'),
            fundDescription=form.data.get('fundDescription'),
        )
        new_fund.save()
        return HttpResponseRedirect(reverse('purchase:dashboard'))


@login_required
def list_funds(request):
    employee = Employee.objects.get(user__id=request.user.id)
    employeeType=dict(USER_TYPES).get(employee.employeeType)
    if employeeType!='DIRECTOR' and employeeType!='ACCOUNT':
        return HttpResponse("you don't have access to this page")
    try:
        context={
            'funds':Fund.objects.all(),
            'employeeType':employeeType
        }
        return render(request, 'utility/list_funds.html',context)
    except:
        return HttpResponse('no funds yet')


@login_required
def distribute_fund(request, fid):
    n = len(Department.objects.all())
    form = FundDistributionForm(request.POST, n=n)
    try:
        coreFund = Fund.objects.get(id=fid)
    except:
        return HttpResponse("Fund ID doesn't exist")

    if form.is_valid() == True:
        sum_total = 0
        for i in range(len(Department.objects.all())):
            sum_total += form.cleaned_data.get('amount%d' % i)
        fund_id = fid
        _fund = Fund.objects.get(id=fund_id)
        available = _fund.amount
        if sum_total <= available:
            for i in range(len(Department.objects.all())):
                _department = Department.objects.get(
                    id=form.cleaned_data.get('department%d' % i))
                fd = FundDistribution(
                    fund=_fund,
                    department=_department,
                    totalAmountReceived=form.cleaned_data.get('amount%d' % i)
                )
                fd.save()
            _fund.fundDistributed = 'Y'
            _fund.save()
            return HttpResponseRedirect(reverse('purchase:dashboard'))
        else:
            return HttpResponse("Fund distribution could not be done as the total exceeds the available fund")

    return render(request, 'utility/fund_distribution_gui.html', {'form': form, 'fund_stats': coreFund, 'noOfDepts': n})


@login_required
def show_distribution(request, fid):
    try:
        fund_distributions = FundDistribution.objects.filter(fund__id=fid)
        try:
            amount = Fund.objects.get(id=fid).amount
        except:
            return HttpResponse("no fund-distribution found")
        return render(request, 'utility/view_fund_distribution.html', {'distributions': fund_distributions, 'amount': amount})
    except:
        return HttpResponse("no fund-distribution found")


@login_required
def update_status(request, action, id):
    purchase_request = PurchaseRequest.objects.get(id=id)
    purchase_request_log = PurchaseReqLog(
        purchaseRequest=purchase_request,
        changedTo=purchase_request.currentStatus,
        comments=request.POST['comment']
    )
    employee = Employee.objects.get(user__id=request.user.id)
    if action == 'forward':
        if employee.employeeType == 1:
            purchase_request.currentStatus = 1
            purchase_request_log.changedTo = 1
        elif employee.employeeType == 2:
            deptId=purchase_request.department.id
            stats=get_stats_department(deptId);
            if stats['fund remaining']<purchase_request.totalCost:
                return HttpResponse("Cannot forward due to lack of fund")
            adjust_fund(id, 'grant')
            purchase_request = PurchaseRequest.objects.get(id = id)
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
    elif action == 'reject':
        adjust_fund(id, 'reject')
        purchase_request.currentStatus = 6
        purchase_request_log.changedTo = 6
    purchase_request.save()
    purchase_request_log.save()
    new_notification = Notification(
        purchaseRequest=purchase_request, statusUpdate=purchase_request.currentStatus)
    new_notification.save()
    return HttpResponseRedirect(reverse('purchase:view_purchase_request', args=(id,)))


@login_required
def physical_token(request, id, action='forward'):
    form = TokenForm(request.POST or None)
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            # comment=form.cleaned_data['comment']
            try:
                # for now the token is the id
                PurchaseRequest.objects.get(id=token)
                # print('token:',token)
                # for x in PurchaseRequest.objects.all():
                #     print (x.id, "id")
                return update_status(request, action, id)
            except:
                return HttpResponse('Invalid token')
    return render(request, 'utility/purchase_request_filter.html', {'form': form})


def get_all_notifications(employee_id):
    notifications = Notification.objects.filter(
        purchaseRequest__employee__id=employee_id).order_by('date')
    notif_list = [(str(x), x.purchaseRequest.id, x.seen)
                  for x in notifications]
    return notif_list


@login_required
def view_notification(request, id):
    notifications = Notification.objects.filter(purchaseRequest__id=id)
    for x in notifications:
        x.seen = 'Y'
        x.save()
    return HttpResponseRedirect(reverse('purchase:view_purchase_request', args=(id,)))


@login_required
def get_stats(request,statType):
    deptId=request.GET.get('id','all')
    if statType == 'department_fund':
        currentDate=datetime.datetime.now()
        financialYear=currentDate.year
        if currentDate.month<4:
            financialYear-=1
        funds=Fund.objects.filter(financialYear=financialYear)

        if deptId == 'all':
            departments=list(Department.objects.all().order_by('id').values('id'))
            for i in range(len(departments)):
                departments[i]=departments[i]['id']
            data=[]
            for fund in funds:
                fund_distributions=FundDistribution.objects.filter(fund_id=fund.id).order_by('department_id').values('totalAmountReceived')
                fund_distributions=list(fund_distributions)
                for i in range(len(fund_distributions)):
                    fund_distributions[i]=fund_distributions[i]['totalAmountReceived']
                data.append(fund_distributions)
            return render(request,'utility/department-stats.html',{'deptId': deptId,'data':data,'departments':departments})

        funds=funds.values('id')
        fund_distributions=FundDistribution.objects.filter(department_id=deptId)
        fund_distributions=fund_distributions.filter(fund_id__in=funds)
        return render(request,'utility/department-stats.html',{'deptId':deptId,'fund_distributions':fund_distributions})

    elif statType == 'department_fund_summary':
        context=get_stats_department(deptId)
        return JsonResponse(context)
    else:
        raise Http404("no stats found")
