toggle_user_status = function(user_id){
	$('#employee_user_id').val(user_id);
	$('#toggle_employee_status').submit();
}

toggle_employee_monthly_entry_approval = function(url , entry_id , employee_user_id , csrf_token){
	formData = {
		entry_id : entry_id,
		employee_user_id : employee_user_id
	};
	generic_ajax_call(url , formData , csrf_token);
}

approve_and_lock_month = function(url , month_in_question , year_in_question , csrf_token){
	formData = {
		for_month : month_in_question,
		for_year : year_in_question
	};
	generic_ajax_call(url , formData , csrf_token);
}


default_success_callback = function(data){
	json = data;
	// json = JSON.parse(data);
	if (json.is_okay) {
		alert('Success!');
	} else {
		alert(json.message);
	}
}

default_error_callback = function(){
	alert('Error, Check your internet connection or contact support!');
}

generic_ajax_call = function(url , formData , csrf_token , success_callback , error_callback){
	console.log(url);
	console.log(formData);
	formData.csrfmiddlewaretoken = csrf_token;
	$.ajax({
	    url : url,
	    type: "POST",
	    data : formData,
	    success: function(data, textStatus, jqXHR)
	    {
    	    success_callback = typeof success_callback !== 'undefined' ? success_callback : default_success_callback;
	        success_callback(data);
	    },
	    error: function (jqXHR, textStatus, errorThrown)
	    {
    	    error_callback = typeof error_callback !== 'undefined' ? error_callback : default_error_callback;
	        error_callback();
	    }
	});

}

