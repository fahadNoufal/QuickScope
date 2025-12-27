FROM python:3.10-slim

RUN apt update -y && apt install awscli -y
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade transformers accelerate bitsandbytes

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]