FROM python

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN rm Dockerfile

ENTRYPOINT [ "python" ]

CMD [ "application.py" ]
