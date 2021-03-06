import json
import requests
import os
import time
import exchange_rate
import hist_data
import payment

from email_validator import validate_email

def create_order(event, context):
    """ Creates an order """

    delivery_email = None
    amount = None

    # Extract required data
    try:
        request_data = json.loads(event['body'])
        delivery_email = request_data['delivery_email']
        amount = float(request_data['amount'])
    except:
        return {
                "statusCode":400,
                "body": json.dumps({
                    'message':'request must include a body with valid delivery_email and amount'
                    })
                }

    # Make sure email address is valid
    v = None
    try:
        v = validate_email(delivery_email)
    except Exception as e:
        return {
                "statusCode":400,
                "body": json.dumps({
                    'message': "invalid delivery_email provided in request: " + str(e)
                    })
                }


    # Make sure the provided amount is greater then the minimum purchase amount
    min_amount = float(os.environ['MIN_PURCHASE_AMOUNT'])
    if amount < min_amount :
        return {
                "statusCode":400,
                "body": json.dumps({
                    'message':'invalid amount provided in request: amount must be > {} (was given: {})'.format(min_amount,amount)
                    })
                }

    # Record the creation time of the order
    created_at = int(time.time())

    # Obtain the current spot rate
    pair = os.environ['CURRENCY_PAIR']
    bid, ask = exchange_rate.spot(pair)

    # Compute the safety margin and the adjusted spot rate
    interval = 30
    since = created_at - interval * 100 * 60

    mean, stdev = hist_data.moments(pair, interval, since)

    bid -= 2 * stdev
    ask += 2 * stdev

    usdxmr = 1/bid

    # create a payment address and add order_id to the address as a label.
    address = payment.create_pay_address(label=None)

    # generate a unique ID for the order
    order_id = payment.create_order_id()

    return {
            "statusCode":200,
            "body": json.dumps({
                'order_id':order_id,
                'delivery_email':delivery_email,
                'amount': amount,
                'created_at':created_at,
                'usdxmr':usdxmr,
                })
            }


