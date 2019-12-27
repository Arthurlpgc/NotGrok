FROM ubuntu

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
EXPOSE 1024:60000
EXPOSE 80:80
COPY . .
RUN pip3 install -r requirements.txt

CMD sleep 10000