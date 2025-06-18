
FROM python:3.13

WORKDIR /app

COPY . .

# Install all Python dependencies via requirements.txt (make sure it's up to date!)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5010

CMD ["python", "app.py"]
