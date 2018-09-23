from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
#log_reg users

def index(request):
    return render(request, 'users/index.html')

def register(request):
    result = User.objects.validate_reg(request.POST)
    print "above if"*5
    if type(result) == list:
        for err in result:
            messages.error(request,err)
            print "inside for"*5
        return redirect('/')    
    request.session['user_id'] = result.id
    messages.success(request,"Successful registration") 
    print "above last return"*5   
    return redirect('/quotes')

def log_in(request):
    result = User.objects.validate_log(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return (redirect('/'))
    request.session['user_id'] = result.id
    messages.success(request, "logged in")    
    return redirect('/quotes')        

def success(request):    
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }        
    return render(request,'users/success.html', context)

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')    