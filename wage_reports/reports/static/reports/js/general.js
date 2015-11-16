$(document).ready(function(){
	document_ready_functions();
});

document_ready_functions = function(){
	employer_monthly_entry_on_ready();
}

employer_monthly_entry_on_ready = function(){
	if (! inside_employer_monthly_entry){
		return;
	}
	$('#id_is_required_to_pay_income_tax').change(function(e){
		toggle_income_tax_visibility(document.getElementById('id_is_required_to_pay_income_tax').checked);
	});
	
}

toggle_income_tax_visibility = function(is_required_to_pay_income_tax){
	if(is_required_to_pay_income_tax){
		$('#id_lower_tax_threshold').prop('disabled', false);
		$('#id_upper_tax_threshold').prop('disabled', false);
		$('#id_income_tax_threshold').prop('disabled', false);
		$('#id_exact_income_tax_percentage').prop('disabled', false);
	} else {
		$('#id_lower_tax_threshold').val(0).prop('disabled', true);
		$('#id_upper_tax_threshold').val(0).prop('disabled', true);
		$('#id_income_tax_threshold').val(0).prop('disabled', true);
		$('#id_exact_income_tax_percentage').val(0).prop('disabled', true);
	}
}

toggle_user_status = function(user_id){
	$('#employee_user_id').val(user_id);
	$('#toggle_employee_status').submit();
}

toggle_employee_monthly_entry_approval = function(url , entry_id , employee_user_id , for_year , for_month , csrf_token){
	formData = {
		entry_id : entry_id,
		employee_user_id : employee_user_id,
		for_year : for_year,
		for_month : for_month,
	};
	generic_ajax_call(url , formData , csrf_token);
}

approve_and_lock_month = function(url , for_month , for_year , csrf_token){
	formData = {
		for_month : for_month,
		for_year : for_year
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
	alert('שגיאה! ודא שאתה מחובר לאינטרנט ובמידת הצורך פנה לתמיכה');
}

generic_get_call = function(url, formData, success_callback, error_callback){
	console.log(url);
	console.log(formData);
	$.ajax({
	    url : url,
	    type: "GET",
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

