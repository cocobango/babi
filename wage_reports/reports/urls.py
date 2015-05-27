from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^enter_employee_monthly_data$', views.enter_employee_monthly_data, name='enter_employee_monthly_data'),
    url(r'^add_employee$', views.add_employee, name='add_employee'),
]