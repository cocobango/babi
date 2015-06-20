from django.conf.urls import url

from . import views

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^enter_employee_monthly_data$', views.enter_employee_monthly_data, name='enter_employee_monthly_data'),
#     url(r'^add_employee$', views.add_employee, name='add_employee'),
# ]



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user_management$', views.user_management, name='user_management'),
    url(r'^user_management/add_employee$', views.add_employee, name='add_employee'),
    url(r'^user_management/view_all_employees$', views.view_all_employees, name='view_all_employees'),
    url(r'^user_management/toggle_employee_status$', views.toggle_employee_status, name='toggle_employee_status'),
    url(r'^view_history$', views.view_history, name='view_history'),
    url(r'^view_history/view_all_months$', views.view_all_months, name='view_all_months'),
    url(r'^view_history/view_a_single_month/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.view_a_single_month, name='view_a_single_month'),
    url(r'^view_history/view_report_of_type/(?P<report_type>[a-z]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.view_report_of_type, name='view_report_of_type'),
    url(r'^current_month$', views.current_month, name='current_month'),
    url(r'^current_month/show_entries$', views.show_entries, name='show_entries'),
    url(r'^current_month/pre_aprove_month$', views.pre_aprove_month, name='pre_aprove_month'),
    url(r'^current_month/set_as_valid/(?P<entry_id>[0-9]+)$', views.set_as_valid, name='set_as_valid'),
    url(r'^current_month/edit_specific_entry/(?P<employee_user_id>[0-9]+)$', views.edit_specific_entry, name='edit_specific_entry'),
    url(r'^current_month/edit_specific_entry$', views.edit_specific_entry, name='edit_specific_entry'),
]