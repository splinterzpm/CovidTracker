FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get -y install python3 python3-dev python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]