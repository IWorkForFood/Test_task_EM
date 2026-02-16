FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Установка Pandoc
RUN apt-get update && \
    apt-get install -y wget && \
    wget  --no-check-certificate https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-1-amd64.deb && \
    dpkg -i pandoc-3.1.11-1-amd64.deb && \
    rm pandoc-3.1.11-1-amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]