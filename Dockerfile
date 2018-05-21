FROM python

ADD . /code
WORKDIR /code
RUN mkdir -p task
RUN touch task/__init__.py
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "./cumulus-ecs-task" ]
