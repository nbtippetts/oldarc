# pull official base image
FROM balenalib/raspberry-pi-debian:latest

RUN apt-get install -y python3 python-pip-whl python3-pip
RUN apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev \
		libhdf5-dev libhdf5-serial-dev libatlas-base-dev \
		libjasper-dev libqtgui4 libqt4-test
RUN apt-get install -y python3-dev gcc
RUN apt-get install -y python3-venv
RUN apt-get install libpq-dev
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN mkdir /arc
RUN mkdir /arc/static
# set work directory
WORKDIR /arc
RUN pip -V
# install dependencies
ENV PYTHONPATH /usr/lib/python3/dist-packages
RUN apt install python3-opencv
RUN pip install psycopg2
COPY ./requirements.txt /arc/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get install -y libilmbase-dev\
	libopenexr-dev \
	libgstreamer1.0-dev
COPY . /arc
# copy project
RUN python -V
COPY ./platform_detect.py /opt/venv/lib/python3.7/site-packages/Adafruit_DHT/platform_detect.py



