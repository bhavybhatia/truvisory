from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import users, income

def home(request):
    if request.method=='POST':
        new_user=users(name=request.POST['name'], age = request.POST['age'], email = request.POST['email'], contact= request.POST['contact'], marital=request.POST.get('marital'), retire=request.POST['retire'])
        new_user.save()
        return HttpResponseRedirect(url_for('personal'))
    else:
        return render(request, "home.html")
# Create your views here.
