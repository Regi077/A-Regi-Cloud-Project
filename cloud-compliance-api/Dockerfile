# =============================================================================
#  Dockerfile  --  Cloud Compliance API Microservice Containerization
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  PURPOSE:
#    - Containerizes the Flask-based Cloud Compliance API for reliable, portable deployment.
#    - Installs Python 3.13, project dependencies, and sets up the app to run on port 5000.
#
#  BUILD & RUN:
#    - Place this Dockerfile in your ./cloud-compliance-api/ folder.
#    - Build:    docker build -t cloud-compliance-api .
#    - Run:      docker run -p 5000:5000 cloud-compliance-api
#    - In compose: This is referenced by your docker-compose.yml as cloud-compliance-api.
#
#  NOTES:
#    - The app expects a requirements.txt file listing all dependencies (Flask, Flask-CORS, etc.).
#    - Change CMD for production deployments as needed (e.g., use Gunicorn for WSGI).
# =============================================================================

FROM python:3.13             
WORKDIR /app                        
COPY . .                               
RUN pip install --upgrade pip         
RUN pip install -r requirements.txt    
EXPOSE 5000                            
CMD ["python", "app.py"]              

# =============================================================================
#  End of Dockerfile
# =============================================================================
