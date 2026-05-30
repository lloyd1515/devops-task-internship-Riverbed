FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Copy requirements and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create a non-privileged user to run the app
RUN useradd --create-home appuser && chown -R appuser:appuser /code
USER appuser

# Copy application files with proper ownership
COPY --chown=appuser:appuser app/ ./app/
WORKDIR /code/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
