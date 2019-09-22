from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return redirect('/purchase-request')