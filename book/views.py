from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import View
from book.forms import BookForm,RegistrationForm,LoginForm
from book.models import books
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
           messages.error(request,"invalid session")
           return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
    
@method_decorator(signin_required,name="dispatch")
class BookListView(View):
    def get(self,request,*args,**kwargs):
        qs=books.objects.all()
        return render(request,"book_list.html",{"data":qs})
    

@method_decorator(signin_required,name="dispatch")
class BookDetailsView(View):
    def get(self,request,*args,**kwargs):
        # if not  request.user.is_authenticated:
        #    return redirect("signin")
        id=kwargs.get("pk")
        qs=books.objects.get(id=id)
        return render(request,"book_detail.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")   
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        id=kwargs.get("pk")
        books.objects.get(id=id).delete()
        messages.success(request,"mobile has been removed")
        return redirect('book-all')
@method_decorator(signin_required,name="dispatch")   
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BookForm()
        return render(request,"book_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=BookForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book has been added")
            return redirect("book-all")
        else:
            messages.error(request,"failed to add messages")
            return render(request,"book_add.html",{"form":form})


        


class BookUpdateView(View):
    def get(self,request,*args,**kwrags):
        id=kwrags.get("pk")
        obj=books.objects.get(id=id)
        form=BookForm(instance=obj)
        return render(request,"book_edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=books.objects.get(id=id)
        form=BookForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book has been updated")
            return redirect("book-all")
        else:
            messages.error(request,"failed to updates books")
            return render(request,'book_edit.html',{"form":form})


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render (request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)
            
            messages.success(request,"Account created successfully")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"failed to create account")
            return render(request,"register.html",{"form":form})
        

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
           unname=form.cleaned_data.get("username")
           pwd=form.cleaned_data.get("password")
           print(unname,pwd)
           user_object=authenticate(request,username=unname,password=pwd)
           if user_object:
               print("valid credential")
               login(request,user_object)
               print(request.user)
               return redirect("book-all")
           else:
               print("invalid credentials")
               
            

           return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
        

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


        



    




