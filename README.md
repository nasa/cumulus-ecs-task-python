# cumulus-ecs-task-python

Use this Docker image to run a Python AWS Lambda function in AWS [ECS](https://aws.amazon.com/ecs/). It mimics [cumulus-ecs-tas](https://github.com/cumulus-nasa/cumulus-ecs-task) for Node.js AWS Lambda functions.

## About

cumulus-ecs-task-python is a Docker image that can run Lambda functions as ECS services.

When included in a Cumulus workflow and deployed to AWS, it will download a specified Lambda function, and act as an activity in a Step Functions workflow.

## Usage

[See documentation in cumulus-ecs-task](https://github.com/cumulus-nasa/cumulus-ecs-task/blob/master/README.md#usage).

## Building

```
export VERSION=0.0.2
docker build -t cumuluss/cumulus-ecs-task-python:$VERSION .
```

## Pushing to docker

```
# docker login
docker tag cumuluss/cumulus-ecs-task-python:$VERSION cumuluss/cumulus-ecs-task-python:$VERSION
docker push cumuluss/cumulus-ecs-task-python:$VERSION
```

## Testing

```
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

docker run -it -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  cumuluss/cumulus-ecs-task-python:$VERSION \
  cumulus-ecs-task \
  --activityArn arn:aws:states:us-east-1:433612427488:activity:cce-DownloadTiles-Activity \
  --lambdaArn arn:aws:lambda:us-east-1:433612427488:function:cce-ViirsProcessing
```
