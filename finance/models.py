from django.db import models

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=255, null=True)
    company_description = models.TextField()
    company_total_budget = models.IntegerField()
    company_creation_date = models.DateField(auto_now_add=False, auto_now=False)

    def __str__(self):
        return self.company_name


class ProjectName(models.Model):
    project_name = models.CharField(max_length=200, null=True)
    tender_date = models.DateField(auto_now_add=False)
    work_order_date = models.DateField(auto_now_add=False)
    p_budget = models.DecimalField(max_digits=10, decimal_places=2)
    above_below = models.CharField(max_length=10, null=True)
    percent = models.DecimalField(max_digits=4, decimal_places=2)
    govt_department_name = models.CharField(max_length=255)
    budget_allocated = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    project_location = models.CharField(max_length=200, null=True)
    date_create = models.DateField(auto_now_add=False , auto_now=False)
    project_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    two_percent = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    five_percent = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    eight_percent = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    def save(self):
        if self.above_below == 'Above':

            total = 100 + float(self.percent)
            self.budget_allocated = ((float(self.p_budget) * 1000000) * total) / 100

            self.two_percent = ((float(self.p_budget) * 1000000) * 2) / 100
            self.five_percent = (self.budget_allocated * 5) / 100
            self.eight_percent = ((float(self.p_budget) * 1000000) * 8) / 100

            return super(ProjectName, self).save()
        else:
            total = 100.0 - float(self.percent)
            self.budget_allocated = ((float(self.p_budget) * 1000000) * total) / 100

            self.two_percent = ((float(self.p_budget) * 1000000) * 2) / 100
            self.five_percent = (float(self.budget_allocated) * 5) / 100
            self.eight_percent = ((float(self.p_budget) * 1000000) * 8) / 100

            return super(ProjectName, self).save()

    def __str__(self):
        return self.project_name

class PaidBy(models.Model):
    PaidBy_name = models.CharField(max_length=200, null=True)
    salary = models.IntegerField()
    cnic = models.CharField(max_length=133, null=True)
    date_create = models.DateField(auto_now_add=False , auto_now=False)
    position_in_company = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.PaidBy_name

class ExpenseType(models.Model):
    expense_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.expense_name

class ProjectExpenses(models.Model):
    expense_amount = models.IntegerField()
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    description = models.TextField()
    date_of_expense = models.DateField(auto_now_add=False , auto_now=False)
    expenses_in_project = models.ForeignKey(ProjectName, on_delete=models.CASCADE)
    expense_receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    PaidByName = models.ForeignKey(PaidBy, on_delete=models.CASCADE)

    def __str__(self):
        return "expenses"



class DailyActivities(models.Model):
    project_name = models.ForeignKey(ProjectName, on_delete=models.CASCADE)
    activity = models.TextField(max_length=1000, null=True)
    description = models.CharField(max_length=200, null=True)
    date = models.DateField(auto_now_add=False, auto_now=False)


    def __str__(self):
        return "self.expenses.total"


class All_Incomes(models.Model):
    income_amount = models.IntegerField(null=True, default=0)
    source = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    date = models.DateField(auto_now_add=False, auto_now=False)

    def __str__(self):
        return self.source

class Project_Bills(models.Model):
    project_name = models.ForeignKey(ProjectName, on_delete=models.CASCADE)
    bill_amount = models.IntegerField(null=True, default=0)
    bill_type = models.CharField(max_length=255, null=True)
    bill_number = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    date = models.DateField(auto_now_add=False, auto_now=False)

    def __str__(self):
        return "testing project Bills"



