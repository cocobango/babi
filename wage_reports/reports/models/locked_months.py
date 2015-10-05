from django.db import models
from . import Employer


class Locked_months(models.Model):
    """A table of keys specifying which employer has locked which month"""
    employer = models.ForeignKey(Employer)
    for_month = models.IntegerField(default=0) 
    for_year = models.IntegerField(default=0) 
    lock_time = models.DateTimeField(auto_now_add=True , blank=True)
    first_day_in_month = models.DateTimeField(blank=True)
