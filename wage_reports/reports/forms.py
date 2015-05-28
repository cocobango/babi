from django.forms import ModelForm, Textarea
from reports.models import Monthly_employee_data , Employee
from django.utils.translation import ugettext_lazy as _

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
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
        fields = '__all__'
