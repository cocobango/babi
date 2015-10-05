from django.db import models
from django.contrib.auth.models import User
from .employer import Employer

class Employee(models.Model):
    user = models.OneToOneField(User)
    employer = models.ForeignKey(Employer)
    birthday = models.DateField()
    government_id = models.IntegerField()
    def __str__(self):
        return self.user.username
