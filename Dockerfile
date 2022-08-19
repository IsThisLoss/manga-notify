FROM python:3.8.10

RUN apt update && apt install -y supervisor sqlite

# supervisord
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf

COPY . ./var/build

RUN python -m pip install /var/build
RUN rm -rf /var/build

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
