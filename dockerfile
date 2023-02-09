FROM python:3.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3","main.py"]

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Add user
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Install Python 3, PyQt5
RUN apt-get update && apt-get install -y python3-pyqt5

RUN pip install -r requirements.txt

COPY . . 