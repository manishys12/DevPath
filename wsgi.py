"""
WSGI entry point for the EdgeRoute application.
This file is used by production WSGI servers like Gunicorn.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the application factory
from app import create_app

# Create the application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'production')

if __name__ == "__main__":
    app.run()
