from django import forms
from django.forms import ModelForm, Textarea , EmailField , CharField
from reports.models import Monthly_employee_data , Employee
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
        fields = ['gross_payment' , 'travel_expenses' , 'gross_or_cost' , 'is_required_to_pay_social_security' , 'is_employer_the_main_employer' , 'gross_payment_from_others']

    def save(self, commit=True):
        monthly_employee_data = super(EmployeeMonthlyEntryForm, self).save(commit=False)
        
        if commit:
            monthly_employee_data.save()
        return monthly_employee_data


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
