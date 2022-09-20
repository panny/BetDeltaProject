FROM python:3.10-slim-buster
MAINTAINER Panny Yeung <panny.yeung@gmail.com>

ENV INSTALL_PATH /betdelta
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "BetDelta.app:create_app()"

