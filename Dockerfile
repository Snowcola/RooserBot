FROM python:3.9.5-slim-buster

LABEL Author=enigma.ca@gmail.com

WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y libffi-dev libnacl-dev python3-dev ffmpeg git
RUN mkdir /log
RUN pip install --upgrade pip
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app

ENTRYPOINT [ "python" ]
CMD [ "/app/main.py" ]
