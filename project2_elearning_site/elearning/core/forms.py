from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.http.request import validate_host


class Registration_form(UserCreationForm):

    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        
        user = User.objects.filter(email=email)
        print(user.exists(),'===================================')
        if user.exists():
            raise ValidationError('email already exists')
        return email

       
class   Login_form(AuthenticationForm):

    username = forms.EmailField(max_length=30, required=True, label='Email Address')
    

    def clean(self):
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = None
        print(email, password)
        try:
            user = User.objects.get(email=email)
            result = authenticate(username=user.username,  password = password)
            
            if result is not None:  
                login(self.request, result)  
                return result
            raise ValidationError('email or password is invalid')
        except:
            raise ValidationError('email or password is invalid')




