FROM python:3.10

WORKDIR /app

COPY generate_data.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "generate_data.py"]
