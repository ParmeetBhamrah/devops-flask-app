FROM python:3.12-slim

LABEL maintainer="ParmeetBhamrah"
LABEL description="DevOps Flask App — production-like container"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

RUN adduser --disabled-password --gecos '' appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--log-level", "info", "app:app"]