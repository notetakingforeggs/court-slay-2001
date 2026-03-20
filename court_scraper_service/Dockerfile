FROM python:3.10-slim

# choose working dir
WORKDIR /app

# Install bash for entrypoint.sh
RUN apt-get update && apt-get install -y bash

COPY pyproject.toml .

# copying the inner package into a folder we create in the working dir of the container
COPY court_scraper/ court_scraper/

COPY entrypoint.sh ./entrypoint.sh

RUN pip install --no-cache-dir .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
