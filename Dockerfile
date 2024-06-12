FROM python:3.12.4-slim
RUN apt update && apt install -y postgresql-client
COPY elt/elt_script.py .
COPY requirements.txt .
COPY .env.source .env.source
COPY .env.destination .env.destination
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "elt_script.py"]