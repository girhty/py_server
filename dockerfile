FROM python:3.10

COPY main.py /app/main.py

WORKDIR /app
RUN python get-pip.py
RUN pip install websockets redis asyncio

CMD ["python", "main.py"]
