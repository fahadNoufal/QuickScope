FROM python:3.10-slim

RUN apt update -y && apt install awscli -y
WORKDIR /app
COPY . /app
FROM python:3.10-slim

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade transformers accelerate bitsandbytes

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]