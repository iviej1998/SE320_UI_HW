# Dockerfile to create the container image for the Cluster Visualization App (CVA)
FROM python:3.12
LABEL maintainer="Jillian Ivie <iviej@my.erau.edu>"

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Phoenix /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY . /se320_ui_hw
RUN pip install --no-cache-dir --upgrade -r /cva/requirements.txt
WORKDIR /se320_ui_hw/

EXPOSE 8000

#  prevents Python from writing .pyc files to disk
#  ensures that the python output is sent straight to terminal (e.g. the container log) without being first buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/cva
CMD ["python3.12",  "-m", "streamlit", "run", "--server.port", "8000", "./StJohns_Weather.py"]