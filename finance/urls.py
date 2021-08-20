from django.urls import path
from . import views

# from django.conf import settings
# from django.conf.urls.static import static




urlpatterns = [
    path('', views.home, name = 'index'),
    path('projects/', views.projects, name ='projects'),
    path('projects/<int:pk>/', views.ProjectDetailView, name='project_detail'),
    path('daily_activities/', views.daily_activities, name ='expensesdetails'),
    path('employes/', views.employes, name ='employes'),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('signup/', views.signuppage, name='signup'),
    path('search/', views.search, name ='search'),
    path('project-bills-search/', views.project_bills_search, name='project-bills-search'),
    path('companies/', views.companies, name ='companies'),
    path('incomes/', views.incomes, name ='incomes'),
    path('project_bills/', views.project_bills, name ='project_bills'),
    path('tender_details/', views.tender_details, name ='tender_details'),
    path('addexpensetype/', views.addexpensetype, name = 'expensetype'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='expensedelete'),
    path('delete_income/<int:pk>/', views.delete_income, name='incomedelete'),
    path('delete_activity/<int:pk>/', views.delete_activity, name='activity'),
    path('bill_delete/<int:pk>/', views.bill_delete, name='billdelete'),
    path('some_view/', views.some_view, name='some_view'),

    # path('add', views.add, name = 'add'),

    # path('update/<int:id>', views.update, name = 'update'),
    # path('delete/<int:id>', views.delete, name = 'delete')
]


# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)

