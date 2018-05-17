
## Building

```
export VERSION=0.0.3
docker build -t aimeeb2/cumulus-ecs-task-python:$VERSION .
```

## Pushing to docker

```
docker login
docker tag aimeeb2/cumulus-ecs-task-python:$VERSION aimeeb2/cumulus-ecs-task-python:$VERSION
docker push aimeeb2/cumulus-ecs-task-python:$VERSION
```

## Testing

```
export AWS_ACCESS_KEY_ID=<ADDME>
export AWS_SECRET_ACCESS_KEY=<ADDME>

docker run -it -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  aimeeb2/cumulus-ecs-task-python:$VERSION \
  arn:aws:states:us-east-1:433612427488:activity:cce-DownloadTiles-Activity \
  arn:aws:lambda:us-east-1:433612427488:function:cce-ViirsProcessing
```
