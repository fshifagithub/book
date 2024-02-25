from django import forms
from django.forms import Form
from book.models import books
from django.contrib.auth.models import User



class BookForm(forms.ModelForm):
    class Meta:
        model=books
        fields="__all__"
        widgets={
             "name":forms.TextInput(attrs={"class":"form-control"}),
             "author":forms.TextInput(attrs={"class":"form-control"}),
             "price":forms.TextInput(attrs={"class":"form-control"}),
             "publisher":forms.TextInput(attrs={"class":"form-control"}),
            

        }
class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()