from django.utils import timezone
from .models import Monthly_employee_data, Employee , Employer , Locked_months


def is_employer(user):
    try:
        employer = Employer.objects.get(user=user)
        return True
    except Exception as e:
        return False

def get_employer_from_user(user):
    try:
        employer = Employer.objects.get(user=user)
        return employer
    except Exception as e:
        return False


def get_latest_locked_month_by_employer(employer_user_id):
    locked_month = Locked_months.objects.select_related('employer').filter(employer__user=employer_user_id).latest('lock_time')
    return locked_month.id

def get_month_in_question_for_employer_locking():
    this_month = timezone.now()
    month_in_question = this_month.month - 1
    if month_in_question == 0:
        return 12
    return month_in_question

def get_year_in_question_for_employer_locking():
    this_month = timezone.now()
    year_in_question = this_month.year
    month_in_question = get_month_in_question_for_employer_locking()
    if month_in_question == 12:
        return year_in_question - 1
    return year_in_question