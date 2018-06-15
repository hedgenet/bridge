#!/usr/bin/env python

import boto3
import argparse
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='ca-central-1', endpoint_url='http://localhost:8000')

def create_table(table_name, hash):
    """ Creates DynamoDB table with given Hash and Range key as strings"""
    print("[+] Creating Table {}...".format(table_name))
    params = {
        "TableName": table_name,
        "KeySchema": [
            {
                'AttributeName': str(hash),
                'KeyType': 'HASH'
            }
        ],
        "AttributeDefinitions" : [
            {
                'AttributeName': str(hash),
                'AttributeType': 'S'
            }
        ],
        "ProvisionedThroughput": {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    }
    table = dynamodb.create_table(**params)
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    return table


def does_table_exist(table_name):
    """Quick check on table"""
    try:
        table = dynamodb.Table(table_name)
        if "ACTIVE" in table.table_status:
            return True
    except ClientError as error_message:
        return False


def main():

    table = 'order'
    hash_key = 'order_id'
    if does_table_exist(table):
        print("[*] Table {} already exists! Skipping creation...".format(table))
    else:
        create_table(table, hash_key)

    print('{} is not accessible in DynamoDB container'.format(table))

if __name__ == '__main__':
    main()
