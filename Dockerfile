FROM python

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "./cumulus-ecs-task" ]
