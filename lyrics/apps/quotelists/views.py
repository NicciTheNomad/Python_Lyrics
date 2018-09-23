from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Prefetch
from .models import *
from ..users.models import User

# Create your views here.
#quotes - quotelists

def dashboard(request):
    try:
        request.session['user_id']   
    except KeyError:
        return redirect('/')
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'quotes':Quote.objects.all(),
        # 'favorites':Favorite.objects.all(),
        'favorites':Favorite.objects.filter(id=request.session['user_id']),
        'reduced_quotes':Quote.objects.exclude(quote_creator=request.session['user_id']),
        'users_quotes':Quote.objects.filter(quote_creator=request.session['user_id']),
    }
    return render(request, 'quotelists/landing.html', context)

def add(request):
    try:
        request.session['user_id']   
    except KeyError:
        return redirect('/')
    result = Quote.objects.validate_quote(request.POST, request.session['user_id'])
    if type(result) == list:
        for err in result:
            messages.error(request,err)
        return redirect('/') 
    messages.success(request, 'quote added to Quotable Quotes') 
    request.session['quote_id'] = result.id
    favorite_result = Favorite.objects.validate_favorite(request.POST, request.session['user_id'],request.session['quote_id'])   
    messages.success(request, 'quote added to fav quote list')
    return redirect('/quotes')   

def add_to_logged_user_list(request, quote_id):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    record = Quote.objects.get(id=quote_id)
    record.quote_creator = User.objects.get(id=request.session['user_id'])
    record.save() 
    messages.success(request, 'quote added to fav quote list')
    return redirect('/quotes')

def remove_from_logged_user_list(request, quote_id):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    # 'favorites':Favorite.objects.filter(id=request.session['user_id']'  

    record = Quote.objects.get(id=quote_id)
    record.quote_creator = User.objects.get(id=request.session['user_id'])
    record.save()
    
    return redirect('/quotes')

def display(request, name):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    # name = name
    print name    
    context = {
        'name': name,
        'all_your_quotes': User.objects.get(name=name).creator_of_quote.all()
    }   
    return render(request, 'quotelists/quote.html', context) 


