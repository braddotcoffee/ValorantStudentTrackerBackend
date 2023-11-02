FROM python:3.11.0
WORKDIR /app
ADD requirements.txt /app

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 5000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "app:app" ]