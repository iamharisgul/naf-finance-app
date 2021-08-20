from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib import messages
from . models import *

# Create your views here.
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method =="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password =password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'User name Or password is incorrect')

        return render(request, 'login.html')



def logoutuser(request):
    logout(request)
    return redirect('login')



def signuppage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account is just created for ' + user)
                return  redirect('login')

        context = {'form':form}
        return render(request, 'signup.html', context)




@login_required(login_url='login')
def home(request):
    ExpensesQ = ProjectExpenses.objects.all()
    paidbynames_all =PaidBy.objects.all()
    expenses_in_project = ProjectName.objects.all()
    expense_name = ExpenseType.objects.all()
    # date insertions
    if request.method == 'POST':
        print("this is post")
        expense_amount =request.POST['amountspent']
        expense_name_id = request.POST['expense_n']
        expense_typename=ExpenseType.objects.get(id=expense_name_id)
        expense_paidby_id = request.POST['paid_by']
        paidby= PaidBy.objects.get(id=expense_paidby_id)
        projectname_id= request.POST['pname']
        project_in_which_expenses_made=ProjectName.objects.get(id=projectname_id)
        date = request.POST['date']
        description = request.POST['description']

        inst= ProjectExpenses(expense_amount=expense_amount,expense_type=expense_typename,description=description, date_of_expense=date, PaidByName=paidby,
                              expenses_in_project = project_in_which_expenses_made)
        inst.save()
    # end code of data insertions

    # search code testing
    if request.method == 'POST':
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        searchresults = ProjectExpenses.objects.filter(created_at_range=(fromdate, todate))
        return render(request, 'index.html',
                      {'expense_name': expense_name, 'expenses': searchresults, 'paid_by': paidbynames_all,
                       'expenses_in_project': expenses_in_project})
    else:
    # search code end
        return render(request, 'index.html', {'expense_name':expense_name, 'expenses':ExpensesQ, 'paid_by': paidbynames_all, 'expenses_in_project': expenses_in_project})





@login_required(login_url='login')
def projects(request):
    if request.method == 'POST':
        project_name=request.POST['projectname']
        location=request.POST['projectlocation']
        date=request.POST['date']
        inst= ProjectName(project_name=project_name,project_location=location, date_create=date)
        inst.save()
        print("data is stored")

    Projects = ProjectName.objects.all()
    return render(request, 'projects.html', {'projects_names':Projects})




@login_required(login_url='login')
def expenses_details(request):
    Expenses_details = ExpensesDetails.objects.all()

    return render(request, 'daily_activities.html', {'expenses_details': Expenses_details})




@login_required(login_url='login')
def employes(request):

    if request.method == 'POST':
        print("this is post")
        name=request.POST['name']
        position_in_company=request.POST['position']
        date=request.POST['date']
        inst= PaidBy(PaidBy_name=name,position_in_company=position_in_company, date_create=date)
        inst.save()
        print("data is stored")

    EmployesNames = PaidBy.objects.all()
    return render(request, 'employes.html', {'employes_of_NAF':EmployesNames})

