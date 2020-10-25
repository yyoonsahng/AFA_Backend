FROM python:3.7.5

ENV PYTHONUNBUFFERED 1

RUN mkdir /django
WORKDIR /django

ADD requirements.txt /django/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /django/
CMD python manage.py runserver 0.0.0.0:8000

EXPOSE 8000
