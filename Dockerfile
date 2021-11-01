FROM python:3.8.10

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./sql ./sql

COPY ./manga_notify ./manga_notify

CMD ["python", "-m", "manga_notify.main"]
