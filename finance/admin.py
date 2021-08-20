from django.contrib import admin

# Register your models here.
from .models import ProjectName, ProjectExpenses, DailyActivities, PaidBy, ExpenseType, Company, All_Incomes, Project_Bills


# @admin.register(ExpensesDetails)
class DailyActivitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'activity', 'description', 'date')


class ProjectNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'project_company', 'tender_date', 'work_order_date', 'govt_department_name',
                    'budget_allocated', 'project_location', 'date_create')


class PaidByAdmin(admin.ModelAdmin):
    list_display = ('id', 'PaidBy_name', 'position_in_company', 'date_create')


class ProjectExpensesAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'expense_amount', 'expense_type', 'description', 'expenses_in_project', 'PaidByName', 'date_of_expense')


class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'expense_name')


class All_IncomesAdmin(admin.ModelAdmin):
    list_display = ('id', 'income_amount', 'source', 'description', 'date')


class Project_BillsAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'bill_amount', 'bill_number', 'description', 'date')

# class Tender_DetailsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'p_name', 'p_budget', 'above_below', 'percent','amount', 'date')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'company_description', 'company_total_budget', 'company_creation_date')

admin.site.register(Project_Bills, Project_BillsAdmin)
# admin.site.register(Tender_Details, Tender_DetailsAdmin)
admin.site.register(ExpenseType, ExpenseTypeAdmin)
admin.site.register(ProjectName, ProjectNameAdmin)
admin.site.register(All_Incomes, All_IncomesAdmin)
admin.site.register(PaidBy, PaidByAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(DailyActivities, DailyActivitiesAdmin)
admin.site.register(ProjectExpenses, ProjectExpensesAdmin)
admin.site.site_header = "NAF Finance Application"
admin.site.index_title = "Admin Panel"
