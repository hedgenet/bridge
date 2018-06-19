import json
import requests
import os
import time
import exchange_rate
import hist_data
import payment
import order
import boto3
import socket

from decimal import Decimal

from email_validator import validate_email

# save the order in the database
if os.getenv('AWS_SAM_LOCAL', ''):
    table = boto3.resource('dynamodb', endpoint_url='http://dynamodb:8000').Table('order')
else:
    table = boto3.resource('dynamodb').Table(os.getenv("ORDER_TABLE_NAME"))

def get_order(event, context):

    order_id = None
    try:
        order_id = event['queryStringParameters']['order_id'][0]
    except:
        return {
            "statusCode":400,
            "body": json.dumps({
                'message': 'request must contain query parameter string order_id'
                })
        }

    # get the item in the database
    response = table.get_item(
            Key = {
                'order_id':order_id
                })

    item = response.get('Item', None)
    return {
            "statusCode":200,
            "body": json.dumps(item)
        }

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
    since = created_at - ( interval * 100 * 60 )

    mean, stdev = hist_data.moments(pair, interval, since)

    bid -= 2 * stdev
    ask += 2 * stdev

    usdxmr = 1/bid

    valid_until = created_at + ( 30 * 60 )

    # create a payment address and add order_id to the address as a label.
    pay = payment.Payment(
            os.environ['SSH_KEY_BUCKET_NAME'],
            os.environ['SSH_KEY_OBJECT'],
            os.environ['DAEMON_HOST'],
            os.environ['DAEMON_USERNAME'],
            int(os.environ['DAEMON_PORT']),
            int(os.environ['ORDER_ACCOUNT_INDEX'])
            )
    address = pay.create_pay_address(label=order_id)

    # generate a unique ID for the order
    order_id = order.create_order_id()

    # assemble the created order
    init_state = 'WAITPAY'
    created_order = {
        'order_id':order_id,
        'delivery_email':delivery_email,
        'amount': str(amount),
        'quantity': str(1),
        'created_at':str(created_at),
        'usdxmr':str(usdxmr),
        'state':init_state,
        'pay_address':address,
        'valid_until':str(valid_until)
    }



    table.put_item(Item=created_order)

    http_result = {
            "statusCode":200,
            "body": json.dumps(created_order)
            }

    return http_result


