FROM python:3.12-slim

WORKDIR /workspace/services/chemistry

COPY services/chemistry/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/chemistry/app ./app

COPY data /workspace/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]