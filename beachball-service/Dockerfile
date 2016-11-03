FROM debian:jessie

MAINTAINER Lion Krischer

# Set the env variables to non-interactive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBIAN_PRIORITY critical
ENV DEBCONF_NOWARNINGS yes

RUN echo "\ndeb http://deb.obspy.org jessie main"  >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install wget -y
RUN wget --quiet -O - https://raw.github.com/obspy/obspy/master/misc/debian/public.key | apt-key add -
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-obspy python3-pip -y
RUN pip3 install flask flask-cache gevent

COPY launch_server.py launch_server.py
