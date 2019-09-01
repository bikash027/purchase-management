from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import UserLoginForm, UserRegisterForm
from utility.models import Employee

User = get_user_model()

@login_required
def test(request):
    return HttpResponse("Working!")

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    return render(request, 'accounts/login.html', {'form':form})

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = User(username=form.cleaned_data.get('Username'),email=form.cleaned_data.get('Email'))
        password = form.cleaned_data.get('Password')
        user.set_password(password)
        user.save()
        employee = Employee(User = user, 
        EmpID = form.cleaned_data.get('EmpID'),
        DeptID = form.cleaned_data.get('DeptID'),
        DOB = form.cleaned_data.get('DOB'),
        Address = form.cleaned_data.get('Address'),
        DOJ = form.cleaned_data.get('DOJ'),
        ContactNo = form.cleaned_data.get('ContactNo'),
        )
        employee.save()
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    return render(request, 'accounts/register.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

