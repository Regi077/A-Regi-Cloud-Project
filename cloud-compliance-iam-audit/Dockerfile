FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install flask flask-cors pydantic
EXPOSE 5040
CMD ["python", "app.py"]
