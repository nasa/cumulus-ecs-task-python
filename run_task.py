#!/usr/local/bin/python3
import boto3
import json
import sys

client = boto3.client('stepfunctions', region_name = 'us-east-1')

def main():
  activity_arn = sys.argv[1]
  print('Polling')
  r = client.get_activity_task(activityArn = activity_arn)
  task_token = r['taskToken']
  client.send_task_success(taskToken=task_token, output=json.dumps({'message': 'Hello World'}))

if __name__ == "__main__":
    main()
