FROM python:3.8-slim-bullseye

# Installing os dependencies
RUN apt-get update
RUN apt-get install binutils libproj-dev gdal-bin -y
RUN apt-get install python3-gdal -y
RUN apt-get install gettext -y

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY  requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY  entrypoint.sh /user/src/entrypoint.sh
RUN chmod 755 /user/src/entrypoint.sh
RUN pip install --user -r requirements.txt
# copy project
COPY ./src/ .

