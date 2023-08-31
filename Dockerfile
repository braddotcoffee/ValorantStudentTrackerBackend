FROM python:3.11.0
ADD requirements.txt /

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD app.py /
ADD config.py /
ADD lib /lib

EXPOSE 5000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "app:app" ]