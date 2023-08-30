FROM python:3.11.0
ADD StudentTrackerBackend.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python3", "StudentTrackerBackend.py" ]