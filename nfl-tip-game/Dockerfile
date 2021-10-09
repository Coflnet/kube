FROM python:3.10.0-buster


RUN apt-get update -y
RUN apt-get install libpq-dev python3-dev libevent-dev libzbar-dev -y
RUN pip3 install django psycopg2-binary selenium Pillow


COPY . .

CMD python3 tippspiel/manage.py migrate && python3 tippspiel/manage.py runserver 0.0.0.0:8000