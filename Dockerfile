FROM python

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "./run_task.py" ]
