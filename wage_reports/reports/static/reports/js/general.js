toggle_user_status = function(user_id){
	$('#employee_user_id').val(user_id);
	$('#toggle_employee_status').submit();
}

approve_employee_monthly_entry = function(entry_id){
	alert(entry_id + 'will be approved');
}

exclude_from_this_report = function(entry_id){
	alert(entry_id + 'will be approved');
}