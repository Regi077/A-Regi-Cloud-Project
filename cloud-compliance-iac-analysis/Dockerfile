FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install flask flask-cors pydantic requests ruamel.yaml
EXPOSE 5030
CMD ["python", "app.py"]
