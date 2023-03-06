from python:3.9-slim as base

FROM base as builder
RUN pip3 install pex setuptools
COPY *.py requirements.txt /src
RUN pip3 install -r /src/requirements.txt
RUN pex -D /src -r /src/requirements.txt setproctitle --inject-args 'main:app -b 0.0.0.0:8000 -c /app/gunicorn.conf.py' -c gunicorn -o /app/app.pex

FROM base as runtime
COPY --from=builder /app /app
COPY --from=builder /src/gunicorn.conf.py /app/gunicorn.conf.py
EXPOSE 8000
ENTRYPOINT ["/app/app.pex"]
