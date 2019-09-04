from django import forms
from django.contrib.auth import authenticate, get_user_model
from .choices import *
from utility.models import Employee

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError('User does not exists')
            if not user.check_password(password):
                raise forms.ValidationError('Wrong username or password')

        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length = 50)
    firstName = forms.CharField(max_length = 50)
    lastName = forms.CharField(max_length = 50)
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = [
            'username',
            'email',
            'password',
            'id',
            'department',
            'firstName',
            'lastName',
            'dateOfBirth',
            'address',
            'contactNo',
            'dateOfJoining',
        ]

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email = email)
        if email_qs.exists():
            raise forms.ValidationError('This email is already registered')

        return email
