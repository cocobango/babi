from django.db import models
from django.contrib.auth.models import User

class Employer(models.Model):
    user = models.OneToOneField(User)
    business_id = models.IntegerField()
    income_tax_id = models.IntegerField()
    phone_number = models.BigIntegerField()
    name_of_contact = models.CharField(max_length=200)
    is_required_to_pay_vat = models.BooleanField(default=True) #is osek murshe
    is_npo = models.BooleanField(default=False) #is malkar (non profit organization)
    def __str__(self):
        return self.user.username

    def is_employer(user):
        try:
            employer = Employer.objects.get(user=user)
            return True
        except Exception as e:
            return False

    def get_employer_from_user(user):
        try:
            return Employer.objects.get(user=user)
        except Exception as e:
            return False