FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5040
CMD ["python", "app.py"]
