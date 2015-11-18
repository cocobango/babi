from django.core.exceptions import PermissionDenied


from .models import Employer, Employee


def user_is_an_employer(function):
    def wrapper(request, *args, **kwargs):
        if Employer.is_employer(request.user):
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper



class tester(object):
    """ based on http://www.artima.com/weblogs/viewpost.jsp?thread=240845 """
    def __init__(self, arg1=None, arg2=None):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.arg1 = arg1
        self.arg2 = arg2

    def __call__(self, function):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def wrapped_f(request, *args, **kwargs):
            # print(args)
            # print(kwargs)
            return function(request, *args, **kwargs)
        return wrapped_f



class user_is_a_specific_employer_for_employee(object):
    """ based on http://www.artima.com/weblogs/viewpost.jsp?thread=240845 """
    def __init__(self, employee_user_id_field_name=None, employee_user_id_arg_number=None):
        self.employee_user_id_field_name = employee_user_id_field_name
        self.employee_user_id_arg_number = employee_user_id_arg_number

    def __call__(self, function):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def wrapped_f(request, *args, **kwargs):
            employee_user_id = self.get_employee_user_id(request, *args, **kwargs)
            if Employee.objects.select_related('employer').filter(employer__user_id=request.user, user_id=employee_user_id):
                return function(request, *args, **kwargs)
            raise PermissionDenied
        return wrapped_f
    def get_employee_user_id(self, request, *args, **kwargs):
        try:
            return request.POST[self.employee_user_id_field_name]
        except Exception as e:
            pass

        try:
            return kwargs[self.employee_user_id_field_name]
        except Exception as e:
            pass

        try:
            return args[self.employee_user_id_arg_number]
        except Exception as e:
            pass

        raise PermissionDenied







