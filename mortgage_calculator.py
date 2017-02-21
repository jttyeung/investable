import re

def calculate_mortgage(mortgage_details):
    """
    Calculates mortgage monthly payment rate.

    Tests:
        >>> calculate_mortgage({'price': '$1,000,000', 'rate': '5.25', 'downpayment': '200000', 'loan': '30'})
        ('$4,418', '$1,590,347')

        >>> calculate_mortgage({'price': '$650,000', 'rate': '3.83', 'downpayment': '169000', 'loan': '20'})
        ('$2,872', '$689,246')

        >>> calculate_mortgage({'price': '$240,000', 'rate': '1.12', 'downpayment': '240000', 'loan': '15'})
        ('$0', '$0')
    """

    MONTHS_IN_YEAR = 12
    PERCENT_CONVERSION = 100

    # Get price, mortgage rate, downpayment amount
    price = int(mortgage_details['price'].replace('$','').replace(',',''))
    rate = ((float(mortgage_details['rate'])/PERCENT_CONVERSION)/MONTHS_IN_YEAR)
    downpayment = int(re.sub('[^\d.]+', '', mortgage_details['downpayment']))

    # Translate loan term in years to months
    loan = mortgage_details['loan']
    loan_payments = int(loan[0:2]) * MONTHS_IN_YEAR

    # Calculate and format monthly payment
    if rate == 0:
        monthly_payment = float(price)/loan_payments
    else:
        monthly_payment = (price - downpayment) * (rate * (1 + rate) ** loan_payments) / ((1 + rate) ** loan_payments - 1)
    formatted_monthly_payment = '${:,}'.format(int(round(monthly_payment)))

    # Calculate total interest paid in span of loan
    total_interest_paid = monthly_payment * loan_payments - price
    formatted_total_interest_paid = '${:,}'.format(int(round(monthly_payment * loan_payments - price)))

    # Calculate the total mortgage paid with interest
    total_mortgage_payment = '${:,}'.format(int(round(price + total_interest_paid)))

    return (formatted_monthly_payment, total_mortgage_payment)
