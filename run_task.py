#!/usr/local/bin/python3
import boto3
import json
import sys
from run_cumulus_task import run_cumulus_task
import parallel_wget

client = boto3.client('stepfunctions', region_name = 'us-east-1')

def task(event, context):
    """simple task that returns the event unchanged"""
    # example logging inside of a task using CumulusLogger
    config = event['config']
    parallel_wget.parallel_wget(
       host=config['provider']['host'],
       path=config['collection']['provider_path'],
       files=event['input']
    )
    # return the output of the task
    return { "result": "Files downloaded" }

def handler(event, context):
    """handler that is provided to aws lambda"""
    return run_cumulus_task(task, event, context, {})

def main():
  activity_arn = sys.argv[1]
  r = client.get_activity_task(activityArn = activity_arn)
  task_token = r['taskToken']
  try:
    event_data = json.loads(r['input'])
    result = handler(event_data, {})
    client.send_task_success(taskToken=task_token, output=json.dumps(result))
  except Exception as e:
    client.send_task_failure(taskToken=task_token, error=e)

if __name__ == "__main__":
    main()
