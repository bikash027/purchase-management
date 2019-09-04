from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PurchaseRequestForm
from utility.models import Employee, PurchaseRequest, HOD
from django.utils import timezone
from django.http import Http404

# NOTE : CREATE PENDING AND SOLVED REQUESTS METHODS
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

        return HttpResponse(purchase_requests)
    except:
        return HttpResponse("You have not created any purchase request")

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
            return HttpResponse(purchase_requests)
        except:
            return HttpResponse("There are no purchase requests from your department")

@login_required
def view_purchase_request(request, id):
    try:
        purchase_requests = PurchaseRequest.objects.get(id = id)
        return HttpResponse(purchase_requests)
    except:
        raise Http404("No such purchase request exists")
        return HttpResponse()