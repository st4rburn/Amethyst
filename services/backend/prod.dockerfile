FROM python:3.14-slim-bookworm

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug" ]
