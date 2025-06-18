# This Dockerfile sets up a Python environment with Flask and Flask-CORS for a web application.
# It copies the current directory contents into the container, installs the necessary Python packages,
# exposes port 5050, and specifies the command to run the application using Python.
# The application is expected to be defined in app.py.


FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5050
CMD ["python", "app.py"]
