FROM python:3.12-slim

# zabrania Pythonowi tworzenia plików z bajtkodem
ENV PYTHONDONTWRITEBYTECODE=1 \ PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY generate.py protocols.yaml ./

# Uruchamia się jednorazowo, wypełnia bazę danych danymi początkowymi, a następnie kończy działanie (używane jako zadanie Kubernetes / kompozycja typu „one-shot”)
CMD ["python", "generate.py"]
