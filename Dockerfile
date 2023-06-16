FROM python:3.10.9
COPY main.py /app/main.py
WORKDIR /app
RUN pip install websockets redis asyncio pymongo
EXPOSE 6079
CMD ["python", "main.py"]
