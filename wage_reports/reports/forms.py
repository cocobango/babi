from django import forms
from django.forms import ModelForm, Textarea , EmailField , CharField
from reports.models import Monthly_employee_data , Employee , Monthly_employer_data
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Html5DateInput(forms.DateInput):
    input_type = 'date'


class EmployeeForm(ModelForm):
    class Meta:
        widgets = {
            'birthday': Html5DateInput()
        }
        model = Employee
        fields = fields = ['birthday' , 'government_id']
        labels = {
            # 'name': _('Writer'),
        }
        help_texts = {
            # 'name': _('Some useful help text.'),
        }
        error_messages = {
            # 'name': {
            #     'max_length': _("This writer's name is too long."),
            # },
        }




class EmployeeMonthlyEntryForm(ModelForm):
    class Meta:
        model = Monthly_employee_data
        fields = ['for_year' , 'for_month' , 'gross_payment' , 'travel_expenses' , 'gross_or_cost' , 'is_required_to_pay_social_security' , 'is_employer_the_main_employer' , 'gross_payment_from_others']
        help_texts = {
            'for_month': _('month as a number from 1-12, For example, July is 7'),
            'for_year': _('year as a number like YYYY, For example, 2015'),
        }
    def save(self, commit=True):
        monthly_employee_data = super(EmployeeMonthlyEntryForm, self).save(commit=False)
        if commit:
            if not self.is_valid_month(monthly_employee_data):
                return False
            monthly_employee_data.save()
        return monthly_employee_data
    # @todo check locked months
    def is_valid_month(self , monthly_employee_data):
        """ 
        Need to check if this entry can be added.
        An employee cannot add to a month that an employer had entered data for
        An employee cannot add after a month is over
        An employee and an employer cannot add to a locked month
        """
        latest_entry = Monthly_employee_data.objects.filter(employee=monthly_employee_data.employee_id).latest('created')
        if monthly_employee_data.entered_by == 'employee':
            if latest_entry.entered_by == 'employer':
                return False
            now = timezone.now()
            if not (latest_entry.created.month == now.month and latest_entry.created.year == now.year):
                return False
        


class UserCreateForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True)
    first_name = CharField(label=_("first_name"), required=True,)
    last_name = CharField(label=_("last_name"), required=True)
 
    class Meta:
        model = User
        fields = ("username", "email", "first_name" , "last_name" , "password1", "password2")
 
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
