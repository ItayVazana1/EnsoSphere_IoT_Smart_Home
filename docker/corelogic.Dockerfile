FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r corelogic/requirements.txt
ENV PYTHONPATH=/app
CMD ["python", "corelogic/corelogic_main.py"]
