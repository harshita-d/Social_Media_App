# anything we specify in this file need not to be pre installed, docker itself will pull the image of it
FROM python:3.9-alpine3.13
# here python is the image name and 3.9-alpine3.13 is the tag name
# alpine is a lightweight version of linux and is ideal for running docker container

LABEL maintainer="harshita"
# maintainer is the one who is going to maintain the docker

ENV PYTHONUNBUFFERED 1
# By specifying 1 means the output will be printed directly to the console, which prevents any delays of messages from our python running applicatione
# this is to see logs immediately

COPY ./requirements.txt /tmp/requirements.txt
# the above line tells to copy "./requirements.txt" from local to "/tmp/requirements.txt" a Docker image and we can use that to install python requirements

COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# the above line tells to copy "./requirements.dev.txt" from local to "/tmp/requirements.dev.txt" a Docker image and we can use that to install python requirements

COPY ./app /app
# "./app" is the local directory for django which will be copied to docker conatiner "/app"

WORKDIR /app
# WORKDIR tells us the default directory in docker image   whose commands are going to be run when we run commands on docker image

EXPOSE 8000
# expose port 8000 from container to machine means access the port on the conatiner that's running from our image

ARG DEV=false
# setting the default value of DEV to false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# RUN runs a command on alpine image that we are using  and if for every command we write RUN then it will create new image layer but we want to keep our images light weight
# so to concatenate multiple commands into single RUN we use "&& \"
# 1. "python -m venv /py"=> this creates a virtual environment that we use to create our dependencies
# Althought we using Docker and in this case we do not need a virtual environmnet but there migth be some edge cases where there are some dependencies on actual base image that might conflict with your python dependencies of our project
# 2. "/py/bin/pip install --upgrade pip" is used to upgrade pip inside virtual env
# 3. "python/bin/pip install -r /tmp/requirements.txt" this specifies that requirements.txt file should get installed in docker image and it will be installed in virtual environment as we specified the venv
# 4. "rm -rf /tmp" is removing the tmp directory as we do not want any extra dependencies on our docker image as docker images are meant to be lightweight
# 5. "adduser \" command adds new user in image as we do not use the root user and root user user has full access nad permission to do everything on the server
# "--disabled-password"  add user we disabled password mean no password is required to logon to it
# "--no-create-home"  does not create a home directory for the user
# "django-user" specifies the name of the user
# "apk add --update --no-cache postgresql-client && \":- Here we installed the postresql client and jpeg-dev that will be installed inside our alpine image in order for Psycopg2 package to be able to connect to postgres
# "apk add --update --no-cache --virtual .tmp-build-deps \":- "--virtual .tmp-build-deps" this sets a virtual dependency package group called ".tmp-build-deps". Here it groups the dependency that we install in this.
# "build-base postresql-dev musl-dev && \":- Here we have listed the packages that are needed in order to install our PostreSQL adapter.
# "apk del .tmp-build-deps && \":- here we our removing ".tmp-build-deps"

ENV PATH="/py/bin:$PATH"

# The above updates the environment variables inside the image and we will update the path which is an env variable which is automatically craeted on Linux OS
# PATH defines all of the directories where executable files can be run, so when we run any command in our project we do not have to specify the full path of environment

USER django-user

# if we do not specify the USER then everything is done as root user but here we specify the user as django-user and also untill this line everthing is done as root user
# the conatiners that is created out of this image is will run using the last user the image switched to
#