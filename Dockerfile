FROM python

ADD . /code
WORKDIR /code
RUN pip3 install boto3

ENTRYPOINT [ "./run_task.py" ]
