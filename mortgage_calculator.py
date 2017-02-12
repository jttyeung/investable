import re

def calculate_mortgage(mortgage_details):
    """ Calculates mortgage monthly payment rate. """

    price = int(mortgage_details['price'].replace('$','').replace(',',''))
    rate = ((int(mortgage_details['rate'])/100.00)/12)
    downpayment = int(re.sub('[^\d.]+', '', mortgage_details['downpayment']))
    loan = mortgage_details['loan']
    loan_payments = int(loan[0:2]) * 12

    if rate == 0:
        monthly_payment = float(price)/loan_payments
    else:
        monthly_payment = (price - downpayment) * (rate * (1 + rate) ** loan_payments) / ((1 + rate) ** loan_payments - 1)
    formatted_monthly_payment = '${:,}'.format(int(round(monthly_payment)))

    total_interest_paid = monthly_payment * loan_payments - price
    formatted_total_interest_paid = '${:,}'.format(int(round(monthly_payment * loan_payments - price)))

    total_mortgage_payment = '${:,}'.format(int(round(price + total_interest_paid)))

    return (formatted_monthly_payment, total_mortgage_payment)
