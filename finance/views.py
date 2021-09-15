import self as self
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib import messages
from .models import *
# from django.core.exceptions import ValidationError
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.files.storage import FileSystemStorage

def EmployeeDetailView(request, pk):
    employee_name = PaidBy.objects.get(id=pk)
    # salaries = ProjectExpenses.objects.values_list(expense_type="salary")
    salaries = ""
    return render(request, 'employee_details.html',
                  {'employee': employee_name, 'salaries':salaries})


def ProjectDetailView(request, *args, **kwargs):
    p_pk = kwargs.get('pk')
    project_name_p_pk = ProjectName.objects.get(id=p_pk)
    ExpensesQ = ProjectExpenses.objects.filter(expenses_in_project=project_name_p_pk).order_by('date_of_expense')
    some_of_all_expenses = sum(ExpensesQ.values_list('expense_amount', flat=True))

    bills = Project_Bills.objects.filter(project_name=project_name_p_pk)

    sum_of_bills = sum(bills.values_list('bill_amount', flat=True))
    # print(bills)
    # ProjectName.objects.get(pk=p_pk)
    if request.method == 'POST':
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        remaining_budget = project_name_p_pk.budget_allocated - some_of_all_expenses
        searchresults = ProjectExpenses.objects.filter(expenses_in_project=project_name_p_pk).filter(date_of_expense__range=[fromdate, todate]).order_by('date_of_expense')
        some_of_all_expenses = sum(searchresults.values_list('expense_amount', flat=True))
        # searchresults = ProjectExpenses.objects.filter(date_of_expense__range=[fromdate, todate]).filter(expenses_in_project=psearch).order_by('date_of_expense')
    #search code above
        return render(request, 'projectdetails.html',
                      {'expenses': searchresults, 'sumofexpenses': some_of_all_expenses, 'project': project_name_p_pk,
                       'remaining_budget': remaining_budget, 'bills':bills, 'sum':sum_of_bills})

    remaining_budget= project_name_p_pk.budget_allocated - some_of_all_expenses


    # print(kwargs.values())

    return render(request, 'projectdetails.html', {'expenses': ExpensesQ, 'sumofexpenses': some_of_all_expenses, 'project':project_name_p_pk, 'remaining_budget': remaining_budget, 'bills':bills, 'sum': sum_of_bills})

# Create your views here.
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
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
                return redirect('login')

        context = {'form': form}
        return render(request, 'signup.html', context)


@login_required(login_url='login')
def home(request):
    # code fro mthis area
    paidbynames_all = PaidBy.objects.all()
    expenses_in_project = ProjectName.objects.all()
    expense_name = ExpenseType.objects.all()
    # print(expenses_in_project)

    # some_of_all_expenses = ProjectExpenses.objects.aggregate(Sum('expense_amount'))

    # date insertions
    if request.method == 'POST':

        print("this is post")
        expense_amount = request.POST['amountspent']
        expense_name_id = request.POST['expense_n']
        expense_typename = ExpenseType.objects.get(id=expense_name_id)
        expense_paidby_id = request.POST['paid_by']
        paidby = PaidBy.objects.get(id=expense_paidby_id)
        projectname_id = request.POST['pname']
        project_in_which_expenses_made = ProjectName.objects.get(id=projectname_id)
        date = request.POST['date']
        description = request.POST['description']

        if len(request.FILES) != 0:
            file_url = request.FILES.get('receipt')
        else:
            file_url = ""

        inst = ProjectExpenses(expense_amount=expense_amount, expense_type=expense_typename, description=description,
                               date_of_expense=date, PaidByName=paidby,
                               expenses_in_project=project_in_which_expenses_made, expense_receipt=file_url)
        inst.save()
    # end code of data insertions
    ExpensesQ = ProjectExpenses.objects.all().order_by('-id')
    some_of_all_expenses = sum(ExpensesQ.values_list('expense_amount', flat=True))

    return render(request, 'index.html',
                  {'expense_name': expense_name, 'expenses': ExpensesQ, 'paid_by': paidbynames_all,
                   'expenses_in_project': expenses_in_project, 'sumofexpenses': some_of_all_expenses})


@login_required(login_url='login')
def search(request):
    ExpensesQ = ProjectExpenses.objects.order_by('-id')

    some_of_all_expenses = sum(ExpensesQ.values_list('expense_amount', flat=True))

    paidbynames_all = PaidBy.objects.all()
    expenses_in_project = ProjectName.objects.all()
    expense_name = ExpenseType.objects.all()
    # search code testing

    if request.method == 'POST':
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        projectname_id = request.POST['pname']
        psearch = ProjectName.objects.get(id=projectname_id)

        if len(request.FILES) != 0:
            file_url = request.FILES.get('receipt')
        else:
            file_url = ""

        searchresults = ProjectExpenses.objects.filter(date_of_expense__range=[fromdate, todate]).filter(expenses_in_project=psearch).order_by('date_of_expense')

        some_of_all_expenses = sum(searchresults.values_list('expense_amount', flat=True))


        # print(fromdate, todate)
        return render(request, 'index.html',
                      {'expense_name': expense_name, 'expenses': searchresults, 'paid_by': paidbynames_all,
                       'expenses_in_project': expenses_in_project, 'sumofexpenses': some_of_all_expenses})
    else:

        return render(request, 'index.html',
                      {'expense_name': expense_name, 'expenses': ExpensesQ, 'paid_by': paidbynames_all,
                       'expenses_in_project': expenses_in_project, 'sumofexpenses': some_of_all_expenses})


# search code end


@login_required(login_url='login')
def projects(request):
    projects = ProjectName.objects.all()
    companies = Company.objects.all()

    print(projects)
    if request.method == 'POST':
        project_name = request.POST['projectname']
        company_name_id = request.POST['cname']
        company_name = Company.objects.get(id=company_name_id)
        location = request.POST['projectlocation']
        # budget_allocated = request.POST['budget_allocated']
        tender_date = request.POST['tender_date']
        work_order_date = request.POST['work_order_date']
        govt_department_name = request.POST['govt_department_name']
        date = request.POST['date']
        #code
        actual_budget_allocated = request.POST['pbudget']
        above_below = request.POST['abovebelow']
        project_percentage = request.POST['ppercent']
        inst = ProjectName(project_name=project_name, tender_date=tender_date, work_order_date=work_order_date,
                           govt_department_name=govt_department_name,
                           project_location=location, project_company=company_name,
                           date_create=date, p_budget=actual_budget_allocated,above_below=above_below, percent=project_percentage)
        print(inst)
        inst.save()


    return render(request, 'projects.html', {'projects_names': projects, 'companies': companies})


@login_required(login_url='login')
def daily_activities(request):
    if request.method == 'POST':
        print("this is post")
        activity = request.POST['activity']
        description = request.POST['description']
        projectname_id = request.POST['pname']
        project_name = ProjectName.objects.get(id=projectname_id)
        date = request.POST['date']

        inst = DailyActivities(project_name=project_name, activity=activity, description=description,
                               date=date)
        inst.save()

        # Code end
    p_names = ProjectName.objects.all()
    daily_activities = DailyActivities.objects.all()

    return render(request, 'daily_activities.html', {'all_activities': daily_activities, 'p_names': p_names})


@login_required(login_url='login')
def employes(request):
    if request.method == 'POST':

        name = request.POST['name']
        position_in_company = request.POST['position']
        cnic = request.POST['cnic']
        monthlysalary = request.POST['monthlysalary']
        date = request.POST['date']
        inst = PaidBy(PaidBy_name=name, salary=monthlysalary, cnic=cnic, position_in_company=position_in_company, date_create=date)
        inst.save()


    EmployesNames = PaidBy.objects.all()
    return render(request, 'employes.html', {'employes_of_NAF': EmployesNames})


@login_required(login_url='login')
def companies(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})


@login_required(login_url='login')
def incomes(request):
    if request.method == 'POST':
        print("this is post")
        income_amount = request.POST['amount']
        source = request.POST['source']
        date = request.POST['date']
        description = request.POST['description']
        inst = All_Incomes(income_amount=income_amount, source=source, date=date, description=description)
        inst.save()
        print("data is stored")

    ExpensesQ = ProjectExpenses.objects.all()
    sum_of_all_expenses = sum(ExpensesQ.values_list('expense_amount', flat=True))

    all_incomes = All_Incomes.objects.order_by('date')
    sum_of_all_incomes = sum(all_incomes.values_list('income_amount', flat=True))

    remaining_amount = sum_of_all_incomes - sum_of_all_expenses

    return render(request, 'incomes.html', {'all_incomes': all_incomes, 'sum_of_all_expenses': sum_of_all_expenses,
                                            'sum_of_all_incomes': sum_of_all_incomes,
                                            'remaining_amount': remaining_amount})


@login_required(login_url='login')
def project_bills(request):
    if request.method == 'POST':
        print("this is post")
        bill_amount = request.POST['bill_amount']
        project_name_id = request.POST['pname']
        project_name = ProjectName.objects.get(id=project_name_id)
        bill_type = request.POST['billtype']
        bill_number = request.POST['bill_number']
        date = request.POST['date']
        description = request.POST['description']
        inst = Project_Bills(bill_amount=bill_amount, project_name=project_name, bill_number=bill_number, date=date,
                             description=description,bill_type=bill_type)
        inst.save()
        print("data is stored")

    all_bills = Project_Bills.objects.order_by('date')
    p_names = ProjectName.objects.all()
    sum_of_all_bills = sum(all_bills.values_list('bill_amount', flat=True))

    return render(request, 'project_bills.html',
                  {'all_bills': all_bills, 'sum_of_bills': sum_of_all_bills, 'p_names': p_names})

#below is code for project bills search
@login_required(login_url='login')
def project_bills_search(request):
    all_bills = Project_Bills.objects.order_by('date')
    p_names = ProjectName.objects.all()
    sum_of_all_bills = sum(all_bills.values_list('bill_amount', flat=True))
    expenses_in_project = ProjectName.objects.all()

    if request.method == 'POST':
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        projectname_id = request.POST['pname']
        psearch = ProjectName.objects.get(id=projectname_id)

        searchresults = Project_Bills.objects.filter(date__range=[fromdate, todate]).filter(project_name=psearch).order_by('date')
        sum_of_all_bills = sum(searchresults.values_list('bill_amount', flat=True))


        # print(fromdate, todate)
        return render(request, 'project_bills.html',
                      {'all_bills': searchresults, 'sum_of_bills': sum_of_all_bills, 'p_names': p_names})
    else:
        return render(request, 'project_bills.html',
                      {'all_bills': all_bills, 'sum_of_bills': sum_of_all_bills, 'p_names': p_names})


# search code end

@login_required(login_url='login')
def tender_details(request):
    tender_details = ProjectName.objects.all()
    # tender_details = Tender_Details.objects.filter(tender)


    return render(request, 'tender_details.html', {'tenders': tender_details})

@login_required(login_url='login')
def addexpensetype(request):
    paidbynames_all = PaidBy.objects.all()
    expenses_in_project = ProjectName.objects.all()
    expense_name = ExpenseType.objects.all()

    if request.method == 'POST':
        expensetype = request.POST['expensetype']
        expensetype = expensetype.lower()

        if ExpenseType.objects.filter(expense_name=expensetype).exists():
            # print("this is error")
            messages.info(request, 'Expense Type already exists.')

        else:
            inst = ExpenseType(expense_name=expensetype)
            inst.save()
            print("data is stored")

    ExpensesQ = ProjectExpenses.objects.all().order_by('date_of_expense')
    some_of_all_expenses = sum(ExpensesQ.values_list('expense_amount', flat=True))

    return render(request, 'index.html',
                  {'expense_name': expense_name, 'expenses': ExpensesQ, 'paid_by': paidbynames_all,
                   'expenses_in_project': expenses_in_project, 'sumofexpenses': some_of_all_expenses})


@login_required(login_url='login')
def delete_expense(request, pk):
    expense_record = ProjectExpenses.objects.get(id=pk)
    expense_record.delete()
    return redirect("/")

@login_required(login_url='login')
def delete_income(request, pk):
    income_record = All_Incomes.objects.get(id=pk)
    income_record.delete()
    return redirect("/incomes")

@login_required(login_url='login')
def delete_activity(request, pk):
    activity_record = DailyActivities.objects.get(id=pk)
    activity_record.delete()
    return redirect("/daily_activities")

@login_required(login_url='login')
def bill_delete(request, pk):
    bill_record = Project_Bills.objects.get(id=pk)
    bill_record.delete()
    return redirect("/project_bills")

def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    textob=p.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)

    ExpensesQ = ProjectExpenses.objects.all().order_by('date_of_expense')
    records=[]
    for expense in ExpensesQ:
        # print("loop")
        records.append(expense.id)
        records.append(expense.date_of_expense)
        records.append(expense.expense_type)
        records.append(expense.expense_amount)
        records.append(expense.description)
        records.append(expense.PaidByName)
        records.append(expense.expenses_in_project)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    for record in records:
        textob.textLine(str(record))

    p.drawText(textob)
    # p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report.pdf')


