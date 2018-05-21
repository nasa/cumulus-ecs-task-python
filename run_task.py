#!/usr/local/bin/python3
import boto3
from botocore.client import Config
from botocore.vendored.requests.exceptions import ReadTimeout
import traceback
import json
import sys
from run_cumulus_task import run_cumulus_task
import requests, zipfile, io

client = boto3.client('stepfunctions', region_name = 'us-east-1')
lambda_client = boto3.client('lambda', region_name = 'us-east-1')

def handler(function, event, context):
    """handler that is provided to aws lambda"""
    return run_cumulus_task(function, event, context, {})

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

def step_function_handler(handler, activity_arn, lambda_arn):
    """ This function polls AWS Step Functions for new activities
    and run the process function for each message in activities
    """

    print('ics querying for task from %s' % activity_arn)
    # poll for new activities
    try:
        response = client.get_activity_task(activityArn=activity_arn)
        print('Received an activity. Processing it')
    except ReadTimeout:
        return
    except Exception as e:
        print('Activity Read error (%s). Trying again.' % str(e))
        return

    task_token = response.get('taskToken', None)
    output=None

    if task_token:
        try:
            function = get_lambda_function(lambda_arn)
            input = json.loads(response.get('input', '{}'))
            output = json.dumps(handler(function=function, event=input, context={}))
            return client.send_task_success(taskToken=task_token, output=output)
        except Exception as e:
            err = str(e)
            print("Exception when running task: %s" % err)
            tb = traceback.format_exc()
            err = (err[252] + ' ...') if len(err) > 252 else err
            client.send_task_failure(taskToken=task_token, error=err, cause=tb)
    else:
        print('No activity found')

def poll():
    config = Config(read_timeout=70)
    activity_arn = sys.argv[1]
    lambda_arn = sys.argv[2]
    print('outside of the loop')
    # loop forever
    while True:
        step_function_handler(handler, activity_arn, lambda_arn)

if __name__ == '__main__':
    poll()
