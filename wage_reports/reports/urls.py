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
    url(r'^current_month/show_entries/(?P<past_or_current_month>[a-z]+)$', views.show_entries, name='show_entries'),
    url(r'^current_month/pre_approve_month$', views.pre_approve_month, name='pre_approve_month'),
    url(r'^current_month/approve_this_month$', views.approve_this_month, name='approve_this_month'),
    url(r'^current_month/set_as_valid/(?P<past_or_current_month>[a-z]+)$', views.set_as_valid, name='set_as_valid'),
    url(r'^current_month/withdraw_approval_of_single_entry$', views.withdraw_approval_of_single_entry, name='withdraw_approval_of_single_entry'),    
    url(r'^current_month/edit_specific_entry/(?P<employee_user_id>[0-9]+)$', views.edit_specific_entry, name='edit_specific_entry'),
    url(r'^current_month/edit_specific_entry$', views.edit_specific_entry, name='edit_specific_entry'),
    url(r'^current_month/edit_general_information_entry/(?P<employee_user_id>[0-9]+)$', views.edit_specific_monthly_employer_data, name='edit_specific_monthly_employer_data'),
]