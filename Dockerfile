FROM python:3.12-alpine

WORKDIR /usr/app

RUN pip install -U pip

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python main.py
