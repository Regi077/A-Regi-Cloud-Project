FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install flask flask-cors PyPDF2 requests qdrant-client ollama
EXPOSE 5010
CMD ["python", "app.py"]

# Dockerfile for Cloud Compliance Rule Ingestion Service
# 
# Usage:
#   Build: docker build -t cloud-compliance-rule-ingestion .
#   Run:   docker run -p 5010:5010 cloud-compliance-rule-ingestion
#
# Make sure app.py and all required files are in the same directory as this Dockerfile.
