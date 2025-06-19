
# =============================================================================
#  Dockerfile -- Rule Ingestion Microservice (Cloud Compliance)
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Builds a Python 3.13 container for the rule-ingestion pipeline.
#    - Ensures dependencies and runtime are reproducible for Docker Compose.
#    - Container entrypoint runs app.py on port 5010 (see EXPOSE).
# =============================================================================

FROM python:3.13

# Set working directory in container (best practice)
WORKDIR /app

# Copy project files to container (all code + requirements.txt)
COPY . .

# Always use up-to-date pip, then install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Idiot-proof: Make sure requirements.txt exists and includes *all* deps:
#   flask, flask_cors, requests, PyPDF2, qdrant-client, pika, etc.

# Ensure container listens on the correct port (matches app.py)
EXPOSE 5010

# CMD launches the microservice
CMD ["python", "app.py"]

# =============================================================================
#  End of Dockerfile (Phase 3: Rule Ingestion, copy-paste ready)
# =============================================================================
