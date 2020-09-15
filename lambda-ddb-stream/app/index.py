# -*- coding: utf-8 -*-
import boto3, os, traceback

# ddb = boto3.resource('dynamodb', region_name=os.environ['TargetRegion'])
# table = ddb.Table(os.environ['TargetDB'])
ddb = boto3.client('dynamodb', region_name=os.environ['TargetRegion'])

def handler(event, context):
  try:
    print(event)
    for r in event['Records']:
      if r['eventName'] == 'INSERT':
        ddb.put_item(
          TableName=os.environ['TargetDB'],
          Item=r['dynamodb']['NewImage'])
          
      elif r['eventName'] == 'REMOVE':
        ddb.delete_item(
          TableName=os.environ['TargetDB'],
          Key=r['dynamodb']['Keys'])
          
      elif r['eventName'] == 'MODIFY':
        ddb.delete_item(
          TableName=os.environ['TargetDB'],
          Key=r['dynamodb']['Keys'])
        ddb.put_item(
          TableName=os.environ['TargetDB'],
          Item=r['dynamodb']['NewImage'])
          
      else:
        raise Exception('unknown eventName!')
        
    return event
  except Exception as e:
    traceback.print_exc()
    print(e)
    return False