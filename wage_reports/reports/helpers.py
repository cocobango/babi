import logging
logger = logging.getLogger('reports')

from decimal import *
getcontext().prec = 6

from django.utils import timezone

def get_month_in_question_for_employee_locking():
    this_month = timezone.now()
    month_in_question = this_month.month
    return int(month_in_question)

def get_year_in_question_for_employee_locking():
    this_month = timezone.now()
    year_in_question = this_month.year
    return int(year_in_question)

def get_month_in_question_for_employer_locking():
    this_month = timezone.now()
    month_in_question = this_month.month - 1
    if month_in_question == 0:
        return int(12)
    return int(month_in_question)

def get_year_in_question_for_employer_locking():
    this_month = timezone.now()
    year_in_question = this_month.year
    month_in_question = get_month_in_question_for_employer_locking()
    if month_in_question == 12:
        return int(year_in_question - 1)
    return int(year_in_question)

def get_quarter_from_month(month):
    if int(month) % 3 == 1:
        return month
    
    month = month - 1
    if int(month) % 3 == 1:
        return month
    return month - 1

def calculate_social_security_employer(overall_gross,social_security_threshold,lower_employer_social_security_percentage,upper_employer_social_security_percentage,is_required_to_pay_social_security):
    return calculate_social_security_generic(overall_gross,social_security_threshold,lower_employer_social_security_percentage,upper_employer_social_security_percentage,is_required_to_pay_social_security, '_employer')

def calculate_social_security_employee(overall_gross,social_security_threshold,lower_employee_social_security_percentage,upper_employee_social_security_percentage,is_required_to_pay_social_security , is_employer_the_main_employer, gross_payment_from_others, lower_health_insurance_percentage, upper_health_insurance_percentage): 
    if is_employer_the_main_employer:
        updated_threshold = social_security_threshold
    else:
        if gross_payment_from_others == 0:
            updated_threshold = 0
        else:
            updated_threshold = Decimal(social_security_threshold) - Decimal(gross_payment_from_others)
            if updated_threshold < 0:
                updated_threshold = 0

    generic_calculation = calculate_social_security_generic(overall_gross,updated_threshold,lower_employee_social_security_percentage,upper_employee_social_security_percentage,is_required_to_pay_social_security , '_employee')
    generic_calculation['health_insurance'] = calculate_social_security_generic(overall_gross,updated_threshold, lower_health_insurance_percentage,upper_health_insurance_percentage, is_required_to_pay_social_security , '_employee')['total_employee']
    return generic_calculation

def calculate_social_security_generic(overall_gross,social_security_threshold,lower_social_security_percentage,upper_social_security_percentage,is_required_to_pay_social_security , extension):
    if not is_required_to_pay_social_security:
        return { 'sum_to_calculate_as_lower_social_security_percentage{0}'.format(extension) : 0 , 'sum_to_calculate_as_upper_social_security_percentage{0}'.format(extension) : 0 ,'diminished_sum{0}'.format(extension) : 0 , 'standard_sum{0}'.format(extension) : 0 , 'total{0}'.format(extension) : 0}   
    if overall_gross <= social_security_threshold:
        sum_to_calculate_as_lower_social_security_percentage = overall_gross
        sum_to_calculate_as_upper_social_security_percentage = 0
    else:
        sum_to_calculate_as_lower_social_security_percentage = social_security_threshold
        sum_to_calculate_as_upper_social_security_percentage = Decimal(overall_gross) - Decimal(social_security_threshold)
    
    diminished_sum = Decimal(sum_to_calculate_as_lower_social_security_percentage) * Decimal(lower_social_security_percentage)
    standard_sum = Decimal(sum_to_calculate_as_upper_social_security_percentage) * Decimal(upper_social_security_percentage)
    total = Decimal(diminished_sum) + Decimal(standard_sum)
    return { 'sum_to_calculate_as_lower_social_security_percentage{0}'.format(extension) : sum_to_calculate_as_lower_social_security_percentage , 'sum_to_calculate_as_upper_social_security_percentage{0}'.format(extension) : sum_to_calculate_as_upper_social_security_percentage ,'diminished_sum{0}'.format(extension) : diminished_sum , 'standard_sum{0}'.format(extension) : standard_sum , 'total{0}'.format(extension) : total}

def calculate_income_tax(overall_gross,income_tax_threshold,lower_tax_threshold,upper_tax_threshold,is_required_to_pay_income_tax,exact_income_tax_percentage,accumulated_gross_including_this_month,accumulated_income_tax_not_including_this_month,vat_due_this_month):
    if not is_required_to_pay_income_tax:
        return 0
    if exact_income_tax_percentage > 0: 
        return (Decimal(overall_gross) + Decimal(vat_due_this_month)) * Decimal(exact_income_tax_percentage)
    if accumulated_gross_including_this_month <= income_tax_threshold:
        return ( Decimal(accumulated_gross_including_this_month) * Decimal(lower_tax_threshold) ) - Decimal(accumulated_income_tax_not_including_this_month)
    standard_sum = ( Decimal(accumulated_gross_including_this_month) - Decimal(income_tax_threshold) ) * Decimal(upper_tax_threshold)
    diminished_sum = Decimal(income_tax_threshold) * Decimal(lower_tax_threshold)
    # print('upper_tax_threshold: {0}'.format(upper_tax_threshold))
    # print('diminished_sum: {0}'.format(diminished_sum))
    # print('standard_sum: {0}'.format(standard_sum))
    return Decimal(standard_sum) + Decimal(diminished_sum) - Decimal(accumulated_income_tax_not_including_this_month)

def calculate_output_tax(overall_gross,vat_percentage,is_required_to_pay_vat):
    if not is_required_to_pay_vat:
        return 0
    return overall_gross * vat_percentage

def calculate_input_tax(overall_gross,vat_percentage,is_required_to_pay_vat,is_npo):
    if not is_npo:
        return 0
    if is_required_to_pay_vat:
        return 0
    return overall_gross * vat_percentage

def calculate_monthly_net(overall_gross, output_tax, social_security_employee, income_tax ):
    return Decimal(overall_gross) + Decimal(output_tax) - Decimal(social_security_employee) - Decimal(income_tax)

def calculate_gross_when_cost_or_or_gross_is_set_to_cost(cost , lower_employer_social_security_percentage , upper_employer_social_security_percentage , social_security_threshold):
    if cost <= Decimal(social_security_threshold) * ( 1 + Decimal(lower_employer_social_security_percentage) ):
        return Decimal(cost) / ( 1 + Decimal(lower_employer_social_security_percentage) )
    a = Decimal(cost) - ( Decimal(social_security_threshold) * ( 1 + Decimal(lower_employer_social_security_percentage) ) )
    b = Decimal(upper_employer_social_security_percentage) + 1
    return ( Decimal(a / b) ) + Decimal(social_security_threshold)

def can_edit_past_months(user):
    return user.groups.filter(name='can_edit_past_months').exists()