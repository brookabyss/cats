from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
status=""
def index(request):
    return render(request,'login_reg/index.html')

def register(request):
    try:
        if request.method=="POST":
            #if the fields pass the vaildation the  object will be created in the database
            #the registration methhod inside the model, performs all of the checks, creates instances if tests pass and returns True and the current user. If there is an error it will return False and errors.
            validation_response=User.objects.registration(request.POST)
            print "registration"*100, validation_response
            if validation_response[0]:
                context={
                    'name': validation_response[1].first_name,
                    'action': "registered"
                }
                status="loggedin"
                messages.success(request,'Successfully registered')
                return render(request,'login_reg/show.html', context)
            else:
                for error in validation_response[1]:
                    messages.error(request,error)
                return redirect('auth:index')
        else:
            return redirect('auth:index')
    except:
        return render(request,'login_reg/error.html')


def login(request):
    try:
        if request.method=="POST":

            #the login methhod inside the model, performs all of the checks, returns true ,user if tests pass. If there is an error it will return False and errors.
            login=User.objects.login(request.POST)
            if login[0]==False:
                for error in login[1]:
                    messages.error(request,error)
                return redirect('auth:index')
            else:
                context={
                    'name': login[1].first_name,
                    'action': "logged in"
                }
                status="loggedin"
                messages.success(request,'Successfully logged in')
                return render(request,'login_reg/show.html', context)

        else:
            return redirect('auth:index')
    except:
        return render(request,'login_reg/error.html')

def logout(request):
    status='loggedout'
    request.session.clear()
    return redirect('auth:index')
