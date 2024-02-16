# Release Docker File
FROM python:3-slim

LABEL author="Zi Data Science Team zi@zi.de"
LABEL name="Zi Web Counter"

COPY . /api

WORKDIR /api/

# Install pip requirements
RUN pip install -r requirements.txt

CMD ["pytest","--maxfail=1"]
