#
FROM ubuntu:16.04
#
#ENV RUNTIME_ENV dev
ENV RUNTIME_ENV prod
#
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y curl
RUN apt-get install -y python3 python3-pip virtualenv
RUN apt-get install -y vim
RUN apt-get install -y sqlite3
#
RUN pip3 install --upgrade pip
#
COPY . /choral-touch-aws
#
WORKDIR /choral-touch-aws
RUN pip3 install -r requirements.txt
#
#ENTRYPOINT ["bin/runner.sh"]
#