from django.conf.urls import url

from . import views

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^enter_employee_monthly_data$', views.enter_employee_monthly_data, name='enter_employee_monthly_data'),
#     url(r'^add_employee$', views.add_employee, name='add_employee'),
# ]



urlpatterns = [
    url(r'^$', views.general_views.index, name='index'),
    url(r'^store_data/$', views.general_views.store_data, name='store_data'),
    url(r'^store_data_gui/$', views.general_views.store_data_gui, name='store_data_gui'),
    

    url(r'^user_management$', views.user_management, name='user_management'),
    url(r'^user_management/add_employee$', views.add_employee, name='add_employee'),
    url(r'^user_management/view_all_employees$', views.view_all_employees, name='view_all_employees'),
    url(r'^user_management/toggle_employee_status$', views.toggle_employee_status, name='toggle_employee_status'),
    

    
    url(r'^view_history/(?P<user_id>[0-9]+)$', views.view_history, name='view_history'),
    url(r'^view_history_as/$', views.view_history_as, name='view_history_as'),
    
    # monthly employee report
    url(r'^view_history/view_monthly_employee_report_list/(?P<employee_user_id>[0-9]+)$', views.view_monthly_employee_report_list, name='view_monthly_employee_report_list'),
    url(r'^view_history/view_monthly_employee_report_list_by_year/(?P<employee_user_id>[0-9]+)/(?P<for_year>[0-9]{4})$', views.view_monthly_employee_report_list_by_year, name='view_monthly_employee_report_list_by_year'),
    url(r'^view_history/view_monthly_employee_report/(?P<employee_user_id>[0-9]+)/(?P<for_year>[0-9]{4})/(?P<for_month>[0-9]{1,2})$', views.view_monthly_employee_report, name='view_monthly_employee_report'),
    
    # monthly employer report
    url(r'^view_history/view_monthly_employer_report_list/(?P<employer_user_id>[0-9]+)$', views.view_monthly_employer_report_list, name='view_monthly_employer_report_list'),
    url(r'^view_history/view_monthly_employer_report_list_by_year/(?P<employer_user_id>[0-9]+)/(?P<for_year>[0-9]{4})$', views.view_monthly_employer_report_list_by_year, name='view_monthly_employer_report_list_by_year'),
    url(r'^view_history/view_monthly_employer_report/(?P<employer_user_id>[0-9]+)/(?P<for_year>[0-9]{4})/(?P<for_month>[0-9]{1,2})$', views.view_monthly_employer_report, name='view_monthly_employer_report'),


    # quarterly_social_security_report
    url(r'^view_history/view_quarterly_social_security_report_list/(?P<employer_user_id>[0-9]+)$', views.view_quarterly_social_security_report_list, name='view_quarterly_social_security_report_list'),
    url(r'^view_history/view_quarterly_social_security_report_list_by_year/(?P<employer_user_id>[0-9]+)/(?P<for_year>[0-9]{4})$', views.view_quarterly_social_security_report_list_by_year, name='view_quarterly_social_security_report_list_by_year'),
    url(r'^view_history/view_quarterly_social_security_report/(?P<employer_user_id>[0-9]+)/(?P<for_year>[0-9]{4})/(?P<for_month>[0-9]{1,2})$', views.view_quarterly_social_security_report, name='view_quarterly_social_security_report'),


    # yearly employee report
    url(r'^view_history/view_yearly_employee_report_list/(?P<employee_user_id>[0-9]+)$', views.view_yearly_employee_report_list, name='view_yearly_employee_report_list'),
    url(r'^view_history/view_yearly_employee_report/(?P<employee_user_id>[0-9]+)/(?P<for_year>[0-9]{4})$', views.view_yearly_employee_report, name='view_yearly_employee_report'),


    # yearly employer report
    url(r'^view_history/view_yearly_employer_report_list/(?P<employer_user_id>[0-9]+)$', views.view_yearly_employer_report_list, name='view_yearly_employer_report_list'),
    url(r'^view_history/view_yearly_employer_report/(?P<employer_user_id>[0-9]+)/(?P<for_year>[0-9]{4})$', views.view_yearly_employer_report, name='view_yearly_employer_report'),


    url(r'^current_month/show_entries/(?P<for_year>[0-9]{4})/(?P<for_month>[0-9]{1,2})$', views.show_entries, name='show_entries'),
    url(r'^current_month/pre_approve_month$', views.pre_approve_month, name='pre_approve_month'),
    url(r'^current_month/approve_this_month$', views.approve_this_month, name='approve_this_month'),
    url(r'^current_month/set_as_valid', views.set_as_valid, name='set_as_valid'),
    url(r'^current_month/withdraw_approval_of_single_entry$', views.withdraw_approval_of_single_entry, name='withdraw_approval_of_single_entry'),    
    url(r'^current_month/edit_specific_entry_by_employer/(?P<employee_user_id>[0-9]+)$', views.edit_specific_entry_by_employer, name='edit_specific_entry_by_employer'),
    url(r'^current_month/edit_specific_entry_by_employee/$', views.edit_specific_entry_by_employee, name='edit_specific_entry_by_employee'),   
    url(r'^current_month/edit_general_information_entry/(?P<employee_user_id>[0-9]+)$', views.edit_specific_monthly_employer_data, name='edit_specific_monthly_employer_data'),
]