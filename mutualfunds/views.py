from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import users

def home(request):
    if request.method=='POST':
        new_user=users(name=request.POST['name'], age = request.POST['age'], email = request.POST['email'], contact= request.POST['contact'])
        new_user.save()
        return HttpResponse("Success")
    else:
        return render(request, "home.html")
# Create your views here.
