
## Building & Running

```
export VERSION=0.0.0
docker build -t aimeeb2/cumulus-ecs-task-python:$VERSION .
docker run aimeeb2/cumulus-ecs-task-python:$VERSION
```

## Pushing to docker

```
docker login
docker tag aimeeb2/cumulus-ecs-task-python:$VERSION aimeeb2/cumulus-ecs-task-python:$VERSION
docker push aimeeb2/cumulus-ecs-task-python:$VERSION
```
