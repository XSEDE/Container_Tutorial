#Using a slim Debian base image tagged at a specific date
FROM debian:buster-20210621-slim

#The next two steps install OS-level dependencies
RUN apt update

RUN apt install -y zlib1g-dev \
                   libjpeg-dev \
                   libfreetype6-dev \
                   liblcms2-dev \
                   libopenjp2-7-dev \
                   libtiff-dev \
                   tk-dev \
                   tcl-dev \
                   libharfbuzz-dev \
                   libfribidi-dev \
                   python3 \
                   python3-pip

#Here, we install python deps - this could be done via a requirements.txt file as well
#  but left explicit here for illustrative purposes
RUN  python3 --version && \
     python3 -m pip install --upgrade pip wheel && \
     python3 -m pip install --upgrade Pillow numpy && \
     python3 -m pip list && \
     which python3

#Add our python scripts into the container where they're available to the
# default $PATH
COPY  ./parallel_mandle.py /usr/local/bin/mandle/parallel_mandle.py
COPY  ./zoom_mandle.py /usr/local/bin/mandle/zoom_mandle.py

#Make the main script executable
RUN chmod 755 /usr/local/bin/mandle/zoom_mandle.py

#Set the entrypoint to our app with extra CMD to run --help by default
ENTRYPOINT ["/usr/local/bin/mandle/zoom_mandle.py"]
CMD ["--help"]
