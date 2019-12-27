FROM ubuntu

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install nginx -y

# ssh
RUN useradd -m portforwarding
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd
COPY sshd_config /etc/ssh/sshd_config
RUN mkdir -p /home/portforwarding/.ssh
COPY authorized_keys /home/portforwarding/.ssh
RUN chown -R portforwarding:portforwarding /home/portforwarding && chmod -R go-rwx /home/portforwarding

COPY . .
RUN pip3 install -r requirements.txt
CMD nginx & /usr/sbin/sshd -D & python3 server.py