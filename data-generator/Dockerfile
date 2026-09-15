FROM python:3.12-slim

# zabrania Pythonowi tworzenia plików z bajtkodemYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY generate.py protocols.yaml ./

# Runs once, seeds the database, then exits (used as a Kubernetes Job / compose one-shot).
CMD ["python", "generate.py"]
