FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY . .
RUN pip install --upgrade pip && pip install ./backend

ENV HB_LOG_CONTEXT=api
CMD ["uvicorn", "tms.main:app", "--host", "0.0.0.0", "--port", "8000"]
