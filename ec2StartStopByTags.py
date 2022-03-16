import json
import boto3
from os import environ
import traceback
from datetime import datetime, timedelta 
import mysql.connector
import pytz


roleName = environ['CROSS_ACCOUNT_ROLE']

# TAG-KEY-NAME is the tag key assciated with ec2 instance which is being deleted

def handler(event, context):
    try:
      
        ec2 = boto3.client('ec2', region_name='us-east-1',
            aws_access_key_id=credential['AccessKeyId'],
            aws_secret_access_key=credential['SecretAccessKey'], 
            aws_session_token=credential['SessionToken']
            )
        rds = boto3.client('rds', region_name='us-east-1',
            aws_access_key_id=credential['AccessKeyId'],
            aws_secret_access_key=credential['SecretAccessKey'], 
            aws_session_token=credential['SessionToken']
            )

        stop_instance(ec2, power_scheduled_resources)    
        start_instance(ec2, power_scheduled_resources)
            
    except Exception as e:
        print("ERROR: " + repr(e))
        traceback.print_exc()

def stop_instance(ec2, power_scheduled_resources):  
    try:
   
        instances = ec2.describe_instances(Filters=[{'Name':'tag-key','Values':['TAG-KEY-NAME']}, {'Name': 'instance-state-name', 'Values': ['running']}])
        for Instances in instances['Reservations']:
            for Instance in Instances['Instances']:
                try:
                    for tag in Instance['Tags']:
                        try:
                            if tag['Key'] == 'TAG-KEY-NAME':
                                ec2_stop(ec2, Instance['InstanceId'])
                                break
                            else:
                                print("Tags not found")
                        except Exception as e:
                            print(e)
                            traceback.print_exc()
                            continue
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    continue
    except Exception as e:
        print("ERROR: " + repr(e))
        traceback.print_exc()


def ec2_stop(ec2, Instance):
    try:
        stoppingInstance = ec2.stop_instances(InstanceIds=[Instance])
        print('Instances Stopped : ', Instance)
    except Exception as e:
        print("ERROR: " + repr(e))
        traceback.print_exc()
    
    
def start_instance(ec2, power_scheduled_resources):  
    try:
        instances = ec2.describe_instances(Filters=[{'Name':'tag-key','Values':['TAG-KEY-NAME']}, {'Name': 'instance-state-name', 'Values': ['stopped']}])
        for Instances in instances['Reservations']:
            for Instance in Instances['Instances']:
                try:
                    for tag in Instance['Tags']:
                        try:
                            if tag['Key'] == 'TAG-KEY-NAME':
                                ec2_start(ec2, Instance['InstanceId']) 
                                break    
                            else:
                                print("Tags not found")    
                        except Exception as e:
                            print("ERROR: " + repr(e))
                            traceback.print_exc()
                            continue
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    continue     
    except Exception as e:
        print("ERROR: " + repr(e))
        traceback.print_exc()
        
def ec2_start(ec2, Instance):
    try:
        startingInstance = ec2.start_instances(InstanceIds=[Instance])
        print('Instances Started : ', Instance)
    except Exception as e:
        print("ERROR: " + repr(e))
        traceback.print_exc()
