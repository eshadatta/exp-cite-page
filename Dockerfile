FROM python:3.8-alpine
RUN apk update
RUN apk upgrade
RUN apk add git
COPY . /static-site-pid-generator
RUN mkdir /static-site-pid-generator/website-repo
WORKDIR /static-site-pid-generator
RUN pip install -r requirements.txt
