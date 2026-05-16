FROM python:3.14-slim-bookworm

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.
ENV NO_CONFIG_FILE=

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD [ "uvicorn", "--app-dir=..", "app.main:app", "--proxy-headers", "--forwarded-allow-ips=\"*\"", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug" ]
