# FROM ubuntu:22.04

# COPY fuzzer /
# RUN chmod +x /fuzzer

# CMD ["/bin/bash", "/fuzzer"]

FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "fuzzer.py"]