FROM python:3.11.3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY manage.py ./SocialMediaApp/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ['python','manage.py','runserver']