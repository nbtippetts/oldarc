# pull official base image
FROM balenalib/raspberry-pi-debian-python:latest

RUN apt-get update && apt-get upgrade
RUN apt-get install -y python3-dev gcc python3-opencv \
		libhdf5-dev libhdf5-serial-dev libatlas-base-dev \
		libjasper-dev libqtgui4 libqt4-test

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
# copy project
COPY ./arc /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]



