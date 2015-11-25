from django.http import HttpResponseRedirect, HttpResponse , JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from .forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from .models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months


def get_single_entry_for_a_given_employee_and_month(employee , for_year , for_month):
    try:
        single_entry = Monthly_employee_data.objects.filter(employee=employee, for_year=for_year, for_month=for_month).latest('created')
        single_entry.has_data = True
        return single_entry
    except Monthly_employee_data.DoesNotExist:
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            single_entry.has_data = True
            single_entry.is_approved = False
            single_entry.for_year = for_year
            single_entry.for_month = for_month
            return single_entry
        except Monthly_employee_data.DoesNotExist:
            empty_entry = Monthly_employee_data(employee=employee)
            empty_entry.has_data = False
            return empty_entry 

def edit_specific_entry_post(request , employee , entered_by):
    form_entry = EmployeeMonthlyEntryForm(request.POST)
    if not form_entry.is_valid():
        return {
            'is_okay' : False,
            'message' : 'הרשומה לא נוספה למסד הנתונים. הקלט שהוזן לא היה תקין',
            'form' : form_entry
        }
    partial_monthly_entree = form_entry.save(commit=False)
    partial_monthly_entree.employee = employee
    partial_monthly_entree.entered_by = entered_by
    #FIXME: Generate better error messages
    if partial_monthly_entree.save():
        return {
            'is_okay' : True,
            'message': 'המידע התקבל בהצלחה'
        }
    return {
        'is_okay' : False,
        'message' : 'הרשומה לא נוספה למסד הנתונים. יש לוודא שקיימים ברשותך ההרשאות לבצע את הפעולה הזאת בזמן זה',
        'form': form_entry
    }

def edit_specific_entry_get(request , employee , error_message , action, form=None):
    if form is None:
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            form = EmployeeMonthlyEntryForm(instance=single_entry)
        except Monthly_employee_data.DoesNotExist:
            form = EmployeeMonthlyEntryForm()

    return render(request, 'reports/employee/monthly_entry.html' , { 'form' : form , 'employee_user_id' : employee.user.id , 'error_message': error_message , 'action':action})

def get_employer_and_employee(request, employee_user_id):
    employee = get_object_or_404(Employee , user_id=employee_user_id)
    employer = get_object_or_404(Employer , id=employee.employer.id)
    if request.user.id not in [employee.user.id, employer.user.id] and not request.user.is_superuser:
        raise PermissionDenied
    return employer, employee

def get_employer(request, employer_user_id):
    employer = get_object_or_404(Employer , user_id=employer_user_id)
    if employer.user.id !=  request.user.id and not request.user.is_superuser:
        raise PermissionDenied
    return employer












