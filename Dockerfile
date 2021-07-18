FROM python:3.9-slim-buster

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install --upgrade pip wheel \
 && pip3 install -r requirements.txt

COPY bot bot
# Launch
CMD python3 -m bot
