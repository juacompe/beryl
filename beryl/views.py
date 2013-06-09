from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    c = RequestContext(request)
    c.update(csrf(request))
    return render_to_response('home.html', c)

def mylogin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
        return HttpResponseRedirect('/')

def mylogout(request):
        logout(request)
        return HttpResponseRedirect('/')

