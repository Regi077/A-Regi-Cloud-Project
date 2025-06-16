FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install flask flask-cors pydantic requests qdrant-client ruamel.yaml
EXPOSE 5020
CMD ["python", "app.py"]
