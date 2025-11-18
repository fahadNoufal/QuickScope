FROM python:3.10-slim
RUN apt update -y && apt install awscli -y
WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3","app.py"]