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
        user = User(username=form.cleaned_data.get('username'),email=form.cleaned_data.get('email'))
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.first_name = form.cleaned_data.get('firstName')
        user.last_name = form.cleaned_data.get('lastName')
        user.save()

        employee = Employee(
        user = user, 
        id = form.cleaned_data.get('id'),
        department = form.cleaned_data.get('department'),
        dateOfBirth = form.cleaned_data.get('dateOfBirth'),
        address = form.cleaned_data.get('address'),
        dateOfJoining = form.cleaned_data.get('dateOfJoining'),
        contactNo = form.cleaned_data.get('contactNo'),
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
    