FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install fastai==1.0.37

COPY app app/

RUN python app/server.py

EXPOSE 4000

CMD ["python", "app/server.py", "serve"]
