FROM ubuntu:latest

## Install Packages/Libraries ##
RUN apt-get update -y && \
    apt-get install -y \
        python3-pip \
        python3-dev \
        gfortran \
        libopenblas-dev \
        liblapack-dev \
        wget \
        unzip \
        vim \
        curl \
        sudo

COPY ./requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN pip3 install gunicorn

## Environment Setup ##
EXPOSE 5000

# Create system user group and add new user.
RUN groupadd -r sim_user && useradd -r -s /bin/false -g sim_user sim_user

# Make new user owner of project directory.
RUN mkdir /app
WORKDIR   /app
# COPY .    /app

RUN chown -R sim_user:sim_user /app

# Switch to non-root user after setup and installations.
USER sim_user

CMD ["python3", "flask_app.py"]
