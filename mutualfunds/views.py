from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import users, income

def home(request):
    if request.method=='POST':
        new_user=users(name=request.POST['name'], age = request.POST['age'], email = request.POST['email'], contact= request.POST['contact'], marital=request.POST.get('marital'), retire=request.POST['retire'])
        new_user.save()
        return HttpResponseRedirect('/portfolio/')
    else:
        return render(request, "form1.html")
# Create your views here.
def portfolio(request):
    if request.method=='POST':

        add_income = income(sal_and_bonus=request.POST['sal_and_bonus'],sal_ends=request.POST['sal_ends'], exp_sal_growth_in_per=request.POST['exp_sal_growth_in_per'], rent=request.POST['rent'], rent_ends=request.POST['rent_ends'], exp_growth=request.POST['exp_growth'], business=request.POST['business'], business_ends=request.POST['business_ends'], business_growth=request.POST['business_growth'],
        other=request.POST['other'], other_ends=request.POST['other_ends'], other_growth=request.POST['other_growth'])
        add_income.save()

        add_expenses = expenses(regular=request.POST['regular'], regular_ends=request.POST['regular_ends'], exp_inf_reg=request.POST['exp_inf_reg'],
        uti=request.POST['uti'], uti_ends=request.POST['uti_ends'],exp_inf_uti=request.POST['exp_inf_uti'],grocery=request.POST['grocery'],
        grocery_ends=request.POST['grocery_ends'], exp_inf_groc=request.POST['exp_inf_groc'], mon_leisure=request.POST['mon_leisure'], leisure_ends=request.POST['leisure_ends'],
        exp_les_inf=request.POST['exp_les_inf'], me=request.POST['me'], me_ends=request.POST['me_ends'], me_inf=request.POST['me_inf'],  ds=request.POST['ds'],
        ds_ends=request.POST['ds_ends'], exp_ds_inf=request.POST['exp_ds_inf'])
        add_expenses.save()

        return HttpResponse("Done")
    else:
        return render(request, "portfolio.html")
