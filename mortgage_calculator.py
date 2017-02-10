from server import *

def calculate_mortgage():
    """ Calculates mortgage monthly payment rate. """
    price = int(mortgage_details['price'])
    rate = float(mortgage_details['rate'])/100
    downpayment = int(mortgage_details['downpayment'])
    loan = mortgage_details['loan']

    print price
    print rate
    print downpayment
    print loan

    if loan == '30-fixed':
        loan_years = 30
    else:
        loan_years = 15


    monthly_payment = price * (rate * (1 + rate) ** loan_years) / ((1 + rate) ** loan_years - 1)

    return monthly_payment
