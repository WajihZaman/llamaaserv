FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# Extract tar.gz and move ALL contents to bin/ (llama-server needs the .so files)
RUN tar -xzf /app/bin/llama-b8994-bin-ubuntu-x64.tar.gz -C /app/bin/ \
    && mv /app/bin/llama-b8994/* /app/bin/ \
    && rm -rf /app/bin/llama-b8994 \
    && rm /app/bin/llama-b8994-bin-ubuntu-x64.tar.gz \
    && chmod +x /app/bin/llama-server

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME=FastAPI

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]