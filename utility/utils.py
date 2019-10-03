from django.shortcuts import render, HttpResponse, reverse
import django.contrib.auth.models as contrib
# from django.contrib.auth.decorators import login_required
# from .forms import PurchaseRequestForm, PurchaseRequestFilterForm, FundForm, FundDistributionForm,TokenForm
from utility.models import Employee, PurchaseRequest, HOD, Fund, Department, FundDistribution, Notification, PurchaseReqLog
from django.utils import timezone
import datetime
from django.http import Http404, HttpResponseRedirect
from accounts.choices import PURCHASE_STATUS,USER_TYPES

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

def requiresForward(pid,uid):
    purchase_request=PurchaseRequest.objects.get(id = pid)
    status=purchase_request.currentStatus
    requestCreator=purchase_request.employee;
    employee = Employee.objects.get(user__id = uid)
    department_query = HOD.objects.filter(hOD__id = employee.id, currentlyServing = 'Y')
    if len(department_query)!=0 and requestCreator.department==department_query[0].department:
        if status==0:
            return True
    if employee.employeeType==1:
        # print('here')
        return False
    if employee.employeeType==2 and status==1:
        return True
    elif employee.employeeType==3 and status==2:
        return True
    elif employee.employeeType==4 and status==3:
        return True
    elif employee.employeeType==5 and status==4:
        return True
    return False

def purchase_requests_per_user_type(request,w_or_a):
    employee = Employee.objects.get(user__id = request.user.id)
    purchase_requests=PurchaseRequest.objects.all()
    if employee.employeeType==2:
        purchase_requests=purchase_requests.filter(currentStatus__in=[1,2,3,4,5])
        if w_or_a=='waiting':
            purchase_requests=purchase_requests.filter(currentStatus = 1 )
        elif w_or_a=='approved':
            purchase_requests=purchase_requests.filter(currentStatus__in=[2,3,4,5])
    elif employee.employeeType==3:
        purchase_requests=purchase_requests.filter(currentStatus__in=[2,3,4,5])
        if w_or_a=='waiting':
            purchase_requests=purchase_requests.filter(currentStatus = 2 )
        elif w_or_a=='approved':
            purchase_requests=purchase_requests.filter(currentStatus__in=[3,4,5])
    elif employee.employeeType==4:
        purchase_requests=purchase_requests.filter(currentStatus__in=[3,4,5])
        if w_or_a=='waiting':
            purchase_requests=purchase_requests.filter(currentStatus = 3 )
        elif w_or_a=='approved':
            purchase_requests=purchase_requests.filter(currentStatus__in=[4,5])
    elif employee.employeeType==5:
        purchase_requests=purchase_requests.filter(currentStatus__in=[4,5])
        if w_or_a=='waiting':
            purchase_requests=purchase_requests.filter(currentStatus = 4 )
        elif w_or_a=='approved':
            purchase_requests=purchase_requests.filter(currentStatus =5)
    elif employee.employeeType==1:
        try:
            department_query = HOD.objects.filter(hOD__id = employee.id, currentlyServing = 'Y')
            print(department_query)
            departments = [department.department.id for department in department_query]
        except:
            return {'result':False,'content':HttpResponse("Sorry, You don't have required previlideges to perform this action")}
            # return render(request,'ulility/view_all_purchase_requests.html',{'purchase_requests':purchase_requests, 'form':form,'formExists': False})
        if len(departments) > 0:
            try:
                purchase_requests=PurchaseRequest.objects.filter(department__id = departments[0])
                for i in range(1, len(departments)):
                    purchase_requests |= PurchaseRequest.objects.filter(department__id = departments[i])
                if w_or_a=='waiting':
                    purchase_requests=purchase_requests.filter(currentStatus = 0 )
                elif w_or_a=='approved':
                    purchase_requests=purchase_requests.filter(currentStatus__in=[1,2,3,4,5])
            except:
                return {'result':False,'content':HttpResponse("There are no purchase requests from your department")}
        if len(department_query)==0:
            return {'result':False,'content':HttpResponse("Sorry, You don't have required previlideges to perform this action")}
    return {'result':True,'content':purchase_requests}

def get_request_logs(id):
    try:
        reqLogs=PurchaseReqLog.objects.filter(purchaseRequest__id= id)
        ar=[]
        # print(id,reqLogs)
        for i in range(0,len(reqLogs)-1):
            content={'changedTo':PURCHASE_STATUS[reqLogs[i].changedTo][1],
            'date':reqLogs[i+1].date.date(),
            'comment':reqLogs[i+1].comments}
            # print('loop')
            # print(reqLogs[0].changedTo)
            if reqLogs[i].changedTo==0:
                content['changedTo']='approved by HOD on '
            elif reqLogs[i].changedTo==1:
                content['changedTo']='approved by accounts section on '
            elif reqLogs[i].changedTo==2:
                content['changedTo']='approved by registrar on '
            elif reqLogs[i].changedTo==3:
                content['changedTo']='approved by director on '
            elif reqLogs[i].changedTo==4:
                content['changedTo']='purchased on '
            ar.append(content)
        log=reqLogs[len(reqLogs)-1]
        if log.changedTo==6 or log.changedTo==5:
            ar[len(ar)-1]={'changedTo':PURCHASE_STATUS[log.changedTo][1]+' on ',
            'date':log.date.date(),
            'comment':log.comments}
            return ar

        if log.changedTo!=5 and log.changedTo!=6:
            ar.append({'changedTo':PURCHASE_STATUS[log.changedTo][1]+' as of ',
            'date':log.date.date(),
            'comment':log.comments})
        # else:
        #     ar.append({'changedTo':PURCHASE_STATUS[log.changedTo][1]+' as of ',
        #     'date':log.date.date(),
        #     'comment':log.comments})
        # for i in range(0,len(ar)-1):
            # ar[i]['date']=ar[i+1]['date']
            # ar[i]['comment']=ar[i+1]['comment']
        ar[len(ar)-1]['comment']=''
    except:
        print('except')
        ar=[]
    return ar

def get_stats_department(pid):
    purchase_request=PurchaseRequest.objects.get(id=pid)
    department=purchase_request.department    
    fund_distributions=FundDistribution.objects.filter(department__id=department.id)
    fund_used=0
    fund_alloted=0
    fund_required=purchase_request.totalCost
    fund_required_total=0
    for dist in fund_distributions:
        if dist.fund.financialYear==2019:
            fund_used+=dist.fundUsed
            fund_alloted+=dist.totalAmountReceived
    start_date=datetime.date(2019,4,1)
    end_date=datetime.date(2020,4,1)
    purchase_requests=PurchaseRequest.objects.filter(dateofIndent__range=(start_date, end_date))
    purchase_requests=purchase_requests.filter(department__id=department.id)
    # print('reached')
    for req in purchase_requests:
        fund_required_total+=req.totalCost
    return {
            'fund_remaining':fund_alloted-fund_used,
            'fund_required':fund_required,
            'fund_required_total':fund_required_total
            }
def getHTML(request):
    count=int(request.POST['count'])
    st=''
    index=10
    for i in range(count):
        st+='<tr><td>'+str(i+1)+'</td>'
        print('hi')
        # index=base+(count-1)*4
        st+='<td>'+request.POST[str(index)]+'</td>'
        index+=1
        st+='<td>'+request.POST[str(index)]+'</td>'
        index+=1
        st+='<td>'+request.POST[str(index)]+'</td>'
        index+=1
        st+='<td>'+request.POST[str(index)]+'</td>'
        index+=1
        st+='</tr>'
    return st





