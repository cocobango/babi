from django.db import models
from django.contrib.auth.models import User
from .employer import Employer

class Employee(models.Model):
    user = models.OneToOneField(User)
    employer = models.ForeignKey(Employer)
    birthday = models.DateField()
    government_id = models.IntegerField()
    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)
    
    def get_employee_from_user(user):
        try:
            return Employee.objects.get(user=user)
        except Exception as e:
            return False