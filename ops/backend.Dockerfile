FROM python:3.11-slim

WORKDIR /app

COPY backend /app/backend
COPY backend/pyproject.toml backend/setup.cfg /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

ENV PYTHONPATH=/app/backend
CMD ["uvicorn", "tms.api:app", "--host", "0.0.0.0", "--port", "8000"]
