FROM python:3.10.9
COPY get-pip.py /app/get-pip.py
COPY main.py /app/main.py

WORKDIR /app
RUN python get-pip.py
RUN pip install websockets redis asyncio

CMD ["python", "main.py"]
