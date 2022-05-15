FROM python:3.10-slim

ENV PORT_HTTP 80

# pour avoir les logs avec docker
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY *.py ./
COPY fichiers ./fichiers/

CMD [ "python", "./webdemineur.py" ]
