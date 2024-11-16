FROM python:3.11-slim

WORKDIR /src

RUN apt-get update && apt-get install -y libmagic1

RUN apt-get update && apt-get install -y qemu-user-static qemu-user

COPY requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /src/

ENV PYTHONUNBUFFERED=1

CMD ["./fuzzer.py"]