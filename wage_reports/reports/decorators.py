from django.core.exceptions import PermissionDenied


from .models import Employer 


def user_is_an_employer(function):
    def wrapper(request, *args, **kwargs):
        if Employer.is_employer(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper



def user_is_a_specific_employer_for_employee(function):
    pass