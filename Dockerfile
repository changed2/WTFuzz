FROM python:3.11-slim

WORKDIR /src

RUN apt-get update && apt-get install -y libmagic1

RUN apt-get update && apt-get install qemu-user-static

COPY requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /src/

CMD ["./fuzzer.py"]