FROM python:3.10

COPY main.py /app/main.py

WORKDIR /app

RUN pip install websockets redis asyncio

CMD ["python", "your_script.py"]
