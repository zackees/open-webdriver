# FROM ubuntu:22.04
FROM python:3.10

# Might be necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# RUN apt-get install software-properties-common -y
#RUN add-apt-repository ppa:deadsnakes/ppa -y
#RUN apt update
#RUN apt install python3.10 -y


WORKDIR /open_webdriver

# Install all the dependencies as it's own layer.
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Add requirements file and install.
COPY . .

# Allow files to be pulled off the container easily.
RUN python -m pip install -U magic-wormhole
RUN python -m pip install -e .

RUN apt-get update && apt-get -y install sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

# RUN useradd -u 1111 admin
# Change to non-root privilege
# USER admin

# Expose the port and then launch the app.
EXPOSE 80

#Blah
#CMD ["python", "-m", "http.server", "80"]
CMD /bin/bash
