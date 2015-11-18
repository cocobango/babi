from django import forms
from django.forms import ModelForm, Textarea , EmailField , CharField, IntegerField, DateField
from reports.models import Monthly_employee_data , Employee , Monthly_employer_data 
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EmployeeForm(ModelForm):
    government_id = IntegerField(label=_("תעודת זהות"), required=True)
    birthday = DateField(label=_("תאריך לידה"), required=True)
    class Meta:
        model = Employee
        fields = ['birthday' , 'government_id']
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
        fields = ['for_year' , 'for_month' , 'salary' , 'general_expenses' , 'is_required_to_pay_social_security' , 'is_employer_the_main_employer' , 'gross_payment_from_others']
        help_texts = {
            'for_month': _('חודש כמספר מהטווח 1-12, לדוגמא, יולי הוא 7'),
            'for_year': _('שנה כמספר בעל ארבע ספרות בפורמט YYYY, לדוגמא, 2015'),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeMonthlyEntryForm, self).__init__(*args, **kwargs)
        self.fields['for_year'].label = "עבור שנה"
        self.fields['for_month'].label = "עבור חודש"
        self.fields['salary'].label = "תשלום עבור הרצאות"
        self.fields['general_expenses'].label = "החזר הוצאות"
        self.fields['is_required_to_pay_social_security'].label = "האם חייב בביטוח לאומי"
        self.fields['is_employer_the_main_employer'].label = "האם המשלם הוא המעסיק עיקרי"
        self.fields['gross_payment_from_others'].label = "ברוטו ממעסיק אחר"

class EmployerMonthlyEntryForm(ModelForm):
    class Meta:
        model = Monthly_employer_data
        fields = ['for_year' , 'for_month' , 'is_required_to_pay_vat' , 'gross_or_cost' , 'is_required_to_pay_income_tax' , 'lower_tax_threshold' , 'upper_tax_threshold' , 'income_tax_threshold' , 'exact_income_tax_percentage']
        help_texts = {
            'for_month': _('חודש כמספר מהטווח 1-12, לדוגמא, יולי הוא 7'),
            'for_year': _('שנה כמספר בעל ארבע ספרות בפורמט YYYY, לדוגמא, 2015'),
        }
    def __init__(self, *args, **kwargs):
        super(EmployerMonthlyEntryForm, self).__init__(*args, **kwargs)
        self.fields['for_year'].label = "עבור שנה"
        self.fields['for_month'].label = "עבור חודש"
        self.fields['is_required_to_pay_vat'].label = "האם עוסק מורשה"
        self.fields['gross_or_cost'].label = "האם חישוב פשוט לפי ברוטו"
        self.fields['is_required_to_pay_income_tax'].label = "האם חייב במס הכנסה"
        self.fields['lower_tax_threshold'].label = "אחוז מס נמוך"
        self.fields['upper_tax_threshold'].label = "אחוז מס גבוה"
        self.fields['income_tax_threshold'].label = "סכום המדרגה למס"
        self.fields['exact_income_tax_percentage'].label = "אחוז מס קבוע"


class UserCreateForm(UserCreationForm):
    email = EmailField(label=_("כתובת אימייל"), required=True)
    first_name = CharField(label=_("שם פרטי"), required=True,)
    last_name = CharField(label=_("שם משפחה"), required=True,)
    username = CharField(label=_("שם משתמש"), required=True)
    password1 = CharField(label=_("סיסמא"), required=True, widget=forms.PasswordInput())
    password2 = CharField(label=_("ודא סיסמא"), required=True, widget=forms.PasswordInput())
 
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
