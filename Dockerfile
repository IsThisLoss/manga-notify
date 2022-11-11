FROM python:3.8.15-slim

# supervisord
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
RUN python -m pip install supervisor

# install requirments
COPY requirements.txt /tmp/build/requirements.txt
RUN python -m pip install -r /tmp/build/requirements.txt

# install main application
COPY README.md /tmp/build/README.md
COPY pyproject.toml /tmp/build/pyproject.toml
COPY manga_notify /tmp/build/manga_notify
RUN cd /tmp/build && python -m pip install .

# cleanup
RUN rm -rf /tmp/build && python -m pip cache purge

CMD ["python", "-m", "supervisor.supervisord", "-c", "/etc/supervisor/supervisord.conf"]
