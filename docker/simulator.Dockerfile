FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r simulator/requirements.txt
ENV PYTHONPATH=/app
CMD ["python", "simulator/simulator_main.py"]
