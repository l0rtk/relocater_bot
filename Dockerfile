FROM python:3.8.10

WORKDIR /app

RUN apt-get update -y && apt-get install g++ gcc libxslt-dev zlib1g-dev libffi6 libffi-dev libxslt1-dev libxml2-dev python-dev -y


COPY main.py /app/main.py

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python3", "/app/main.py"]