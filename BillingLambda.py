import boto3
import datetime
import csv
import json
import re
from dateutil.relativedelta import relativedelta
from datetime import date
from os import environ

def lambda_handler(event, context):
    now = datetime.datetime.utcnow()
    last_day = date(now.year, now.month, 1) - relativedelta(days=1)
    client = boto3.client('ce')
    response_data = client.get_cost_and_usage(
        TimePeriod={
        'Start': (last_day - datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
        'End': last_day.strftime('%Y-%m-%d')
        },
        Metrics=['AmortizedCost'],
        Granularity='MONTHLY',
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}]
        )

for groups in response_data['ResultsByTime']:
    print("=====================================")
    print("Monthly Cost for the Account XYZ")
    print("=====================================")
    print("Start Date : ", groups['TimePeriod']['Start'])
    print("End Date : ", groups['TimePeriod']['End'])
    for resource in groups['Groups']:
        print("Price : ", resource['Metrics']['AmortizedCost']['Amount'] + " USD")
         
