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
        fields = ['for_year' , 'for_month' , 'salary' , 'general_expenses' , 'gross_or_cost' , 'is_required_to_pay_social_security' , 'is_employer_the_main_employer' , 'gross_payment_from_others']
        help_texts = {
            'for_month': _('month as a number from 1-12, For example, July is 7'),
            'for_year': _('year as a number like YYYY, For example, 2015'),
        }

class EmployerMonthlyEntryForm(ModelForm):
    class Meta:
        model = Monthly_employer_data
        fields = ['for_year' , 'for_month' , 'is_required_to_pay_vat' , 'is_required_to_pay_income_tax' , 'lower_tax_threshold' , 'upper_tax_threshold' , 'income_tax_threshold' , 'exact_income_tax_percentage']
        help_texts = {
            'for_month': _('month as a number from 1-12, For example, July is 7'),
            'for_year': _('year as a number like YYYY, For example, 2015'),
        }


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
