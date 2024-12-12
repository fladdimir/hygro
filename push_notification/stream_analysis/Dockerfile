FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY *.py .
CMD ["python3", "./stream_analysis.py"]
