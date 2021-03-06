# Generated by Django 3.2.5 on 2021-08-23 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='All_Incomes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_amount', models.IntegerField(default=0, null=True)),
                ('source', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('company_description', models.TextField()),
                ('company_total_budget', models.IntegerField()),
                ('company_creation_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaidBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PaidBy_name', models.CharField(max_length=200, null=True)),
                ('salary', models.IntegerField()),
                ('cnic', models.CharField(max_length=133, null=True)),
                ('date_create', models.DateField()),
                ('position_in_company', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200, null=True)),
                ('tender_date', models.DateField()),
                ('work_order_date', models.DateField()),
                ('p_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('above_below', models.CharField(max_length=10, null=True)),
                ('percent', models.DecimalField(decimal_places=2, max_digits=4)),
                ('govt_department_name', models.CharField(max_length=255)),
                ('budget_allocated', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('project_location', models.CharField(max_length=200, null=True)),
                ('date_create', models.DateField()),
                ('two_percent', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('five_percent', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('eight_percent', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('project_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.company')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_amount', models.IntegerField()),
                ('description', models.TextField()),
                ('date_of_expense', models.DateField()),
                ('expense_receipt', models.ImageField(blank=True, null=True, upload_to='receipts/')),
                ('PaidByName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.paidby')),
                ('expense_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.expensetype')),
                ('expenses_in_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.projectname')),
            ],
        ),
        migrations.CreateModel(
            name='Project_Bills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_amount', models.IntegerField(default=0, null=True)),
                ('bill_type', models.CharField(max_length=255, null=True)),
                ('bill_number', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('date', models.DateField()),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.projectname')),
            ],
        ),
        migrations.CreateModel(
            name='DailyActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.TextField(max_length=1000, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('date', models.DateField()),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.projectname')),
            ],
        ),
    ]
