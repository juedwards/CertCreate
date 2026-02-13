"""
WSGI entry point for Azure App Service
"""
from app import app as application

if __name__ == "__main__":
    application.run()
