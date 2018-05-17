#!/usr/local/bin/python3
import boto3
import json
import sys
from run_cumulus_task import run_cumulus_task
import requests, zipfile, io

client = boto3.client('stepfunctions', region_name = 'us-east-1')
lambda_client = boto3.client('lambda', region_name = 'us-east-1')

def handler(func, event, context):
    """handler that is provided to aws lambda"""
    return run_cumulus_task(func, event, context, {})

def get_lambda_function(lambda_arn):
  lambda_function = lambda_client.get_function(FunctionName=lambda_arn)
  lambda_code_url = lambda_function['Code']['Location']
  r = requests.get(lambda_code_url)
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall('task')
  module_str, function_str = lambda_function['Configuration']['Handler'].split('.')
  sys.path.insert(0, '../task')
  task = __import__('task.{0}'.format(module_str))
  module = getattr(task, module_str)
  return getattr(module, function_str)

def main():
  try:
    activity_arn = sys.argv[1]
    lambda_arn = sys.argv[2]
    r = client.get_activity_task(activityArn = activity_arn)
    task_token = r['taskToken']
    event_data = json.loads(r['input'])
    function = get_lambda_function(lambda_arn)
    result = handler(function, event_data, {})
    client.send_task_success(taskToken=task_token, output=json.dumps(result))
  except Exception as e:
    client.send_task_failure(taskToken=task_token, error=e)

if __name__ == "__main__":
    main()
