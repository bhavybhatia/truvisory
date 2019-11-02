from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse

def home(request):
    if request.method=='POST':
        name = request.POST['name']
        age = request.POST['age']
        email = request.POST['email']
        contact= request.POST['contact']
        print(name,age,email,contact)
        return HttpResponse("Success")
    else:
        return render(request, "home.html")
# Create your views here.
