$(document).ready(function(){
	document_ready_functions();
});

document_ready_functions = function(){
	employer_monthly_entry_on_ready();
	add_employee_on_ready_functions();
	show_all_employees_on_ready();
}

show_all_employees_on_ready = function(){
	$('#all_employees_table').dataTable();
}

add_employee_on_ready_functions = function(){
	$('#id_government_id').change(function(e){ if( ! IDValidator($('#id_government_id').val())){ alert('מספר תעודת הזהות שהוזן לא תקין') }   });
	$('#id_birthday').datetimepicker({
		format: 'YYYY-MM-DD',
	});
}

employer_monthly_entry_on_ready = function(){
	if (typeof inside_employer_monthly_entry === 'undefined'){
		return;
	}



	$('#id_is_required_to_pay_income_tax').change(function(e){
		toggle_income_tax_visibility(document.getElementById('id_is_required_to_pay_income_tax').checked);
	});

	$('#has_exact').click(function(e){
		toggle_exact_or_threshold_choice(true);
	});

	$('#has_threshold').click(function(e){
		toggle_exact_or_threshold_choice(false);
	});
	
	$('#threshold_fields').hide();
	$('#exact_fields').hide();

	$('#employer_monthly_entry_form').submit(function(e){
		employer_monthly_entry_form_handle_submit(e);
	});

	show_fields_as_percentages(['id_lower_tax_threshold', 'id_upper_tax_threshold', 'id_exact_income_tax_percentage']);
}

employer_monthly_entry_form_handle_submit = function(e){
	convert_fields_from_percentages(['id_lower_tax_threshold', 'id_upper_tax_threshold', 'id_exact_income_tax_percentage']);
}

convert_fields_from_percentages = function(field_list){
	var change_single_val = function(field_id){
		$('#' + field_id).val(from_percentage($('#' + field_id).val()));

	}
	field_list.forEach(change_single_val);
}

show_fields_as_percentages = function(field_list){
	var change_single_val = function(field_id){
		$('#' + field_id).val(to_percentage($('#' + field_id).val()));
	}
	field_list.forEach(change_single_val);
}

from_percentage = function(val_of_input_field){
	return val_of_input_field * 1 / 100;
}

to_percentage = function (val_of_input_field){
	return val_of_input_field * 100;
}

toggle_income_tax_visibility = function(is_required_to_pay_income_tax){
	if(is_required_to_pay_income_tax){
		toggle_exact_or_threshold_choice_visibility(true);
	} else {
		toggle_exact_or_threshold_choice_visibility(false);
		$('#id_lower_tax_threshold').val(0);
		$('#id_upper_tax_threshold').val(0);
		$('#id_income_tax_threshold').val(0);
		$('#id_exact_income_tax_percentage').val(0);
	}
}

toggle_exact_or_threshold_choice_visibility = function(is_show){
	if (is_show) {
		$('#exact_or_threshold_choice').show();
	} else {
		$('#exact_or_threshold_choice').hide();
	}
}

toggle_exact_or_threshold_choice = function(is_exact_income_tax) {
	if(is_exact_income_tax ){
		$('#threshold_fields').hide();
		$('#exact_fields').show();
		$('#id_lower_tax_threshold').val(0);
		$('#id_upper_tax_threshold').val(0);
		$('#id_income_tax_threshold').val(0);
	} else {
		$('#threshold_fields').show();
		$('#exact_fields').hide();
		$('#id_exact_income_tax_percentage').val(0);
	}
}

toggle_threshold_tax_visibility = function(exact_income_tax){
	
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


function IDValidator(id)
{
	id += ""; //cast as string
	if (id.length != 9 || isNaN(id)) {
		return false;
	}
	var counter = 0, incNum;
	for (i in id) {
		incNum = Number(id[i]) * ((i % 2) + 1);//multiply digit by 1 or 2
		counter += (incNum > 9) ? incNum - 9 : incNum;//sum the digits up and add to counter
	}
	return (counter % 10 == 0);
}


