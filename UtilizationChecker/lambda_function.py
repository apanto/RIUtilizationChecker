from __future__ import print_function
import os
from datetime import date, timedelta

import boto3

#The utilization threshold set in the environment variable UTIL_THRESHOLD
UtilThreshold = int(os.environ['UTIL_THRESHOLD'])
#The SNS topic we should post a message to in case utilization is below threshold
TopicArn = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
  #The latest utilization data in CE is from 3 days ago so start_date is 3 days ago...
  start_date = str(date.today() - timedelta(days=3))
  #and end date is next day
  end_date = str(date.today() - timedelta(days=2))
  period = {'Start': start_date , 'End': end_date}

  ce = boto3.client('ce', region_name='us-east-1')
  r = ce.get_reservation_utilization(TimePeriod=period)

  if r['ResponseMetadata']['HTTPStatusCode'] == 200:
    for result in r['UtilizationsByTime']:
      if result['TimePeriod']['Start'] == start_date:
        msg = "RI utilization during {} - {}: {}%".format(
          result['TimePeriod']['Start'], 
          result['TimePeriod']['End'], 
          result['Total']['UtilizationPercentage']
          )
        print("LOG: "+msg)

        #Check if utilization is below configured threshold. If it is post a mesage to 
        #the SNS topic
        if float(result['Total']['UtilizationPercentage']) < UtilThreshold:
          print("Unutilized RIs found, sending notification...")

          sns = boto3.client('sns')
          sns.publish(TopicArn=TopicArn, Message=msg, Subject='Low RI utilization')


