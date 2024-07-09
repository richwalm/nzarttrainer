FROM tiangolo/meinheld-gunicorn-flask:latest
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY ./app /app
