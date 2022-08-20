FROM python:3.8.10

RUN apt update && apt install -y supervisor

# supervisord
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf

# src
COPY setup.py /tmp/build/setup.py
COPY requirements.txt /tmp/build/requirements.txt
COPY manga_notify /tmp/build/manga_notify

RUN python -m pip install /tmp/build
# RUN rm -rf /var/build

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
