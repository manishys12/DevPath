# EdgeRoute Deployment Guide

This guide provides instructions for deploying the EdgeRoute application in various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
  - [Traditional Server Deployment](#traditional-server-deployment)
  - [Docker Deployment](#docker-deployment)
  - [Heroku Deployment](#heroku-deployment)
  - [Render Deployment](#render-deployment)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [SSL Configuration](#ssl-configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying EdgeRoute, ensure you have:

- Python 3.9+ installed
- PostgreSQL database (recommended for production)
- Web server (Nginx or Apache)
- Domain name (for production)
- SSL certificate (for production)

## Deployment Options

### Traditional Server Deployment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/edgeroute.git
   cd edgeroute
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**:
   ```bash
   flask db upgrade
   ```

6. **Set up Gunicorn and Supervisor**:
   ```bash
   # Copy the supervisor configuration
   sudo cp supervisor/edgeroute.conf /etc/supervisor/conf.d/
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start edgeroute
   ```

7. **Configure Nginx**:
   ```bash
   # Copy the Nginx configuration
   sudo cp nginx/conf.d/edgeroute.conf /etc/nginx/sites-available/edgeroute
   sudo ln -s /etc/nginx/sites-available/edgeroute /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Docker Deployment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/edgeroute.git
   cd edgeroute
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**:
   ```bash
   docker-compose exec web flask db upgrade
   ```

### Heroku Deployment

1. **Create a Heroku app**:
   ```bash
   heroku create edgeroute
   ```

2. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set FLASK_CONFIG=production
   heroku config:set SECRET_KEY=your-secure-secret-key
   # Add other environment variables as needed
   ```

4. **Deploy the application**:
   ```bash
   git push heroku main
   ```

5. **Initialize the database**:
   ```bash
   heroku run flask db upgrade
   ```

### Render Deployment

Render is a unified cloud platform that makes it easy to deploy your applications without managing complex infrastructure.

1. **Create a Render account**:
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub repository

2. **Deploy using the render.yaml file**:
   - The repository includes a `render.yaml` configuration file
   - In the Render dashboard, click "New" and select "Blueprint"
   - Select your repository and click "Apply"
   - Render will automatically set up your web service and database

3. **Manual deployment (alternative)**:
   - In the Render dashboard, click "New" and select "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - Name: `edgeroute`
     - Environment: `Python`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn wsgi:app`
   - Add environment variables:
     - `FLASK_APP`: `wsgi.py`
     - `FLASK_CONFIG`: `production`
     - `SECRET_KEY`: Generate a secure random string
   - Click "Create Web Service"

4. **Set up the database**:
   - In the Render dashboard, click "New" and select "PostgreSQL"
   - Configure the database:
     - Name: `edgeroute-db`
     - Database: `edgeroute`
     - User: `edgeroute_user`
   - After creation, copy the "Internal Database URL"
   - Add it as an environment variable to your web service:
     - `DATABASE_URL`: The internal database URL from Render

5. **Initialize the database**:
   - In the Render dashboard, go to your web service
   - Click "Shell"
   - Run: `python init_db.py`
   - This script will create all tables and set up an admin user

6. **Access your application**:
   - Your application will be available at `https://edgeroute.onrender.com`
   - Render automatically provides SSL certificates

## Database Setup

For production, we recommend using PostgreSQL:

1. **Install PostgreSQL**:
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```

2. **Create a database and user**:
   ```bash
   sudo -u postgres psql
   ```

   ```sql
   CREATE DATABASE edgeroute;
   CREATE USER edgeroute_user WITH PASSWORD 'your-secure-password';
   GRANT ALL PRIVILEGES ON DATABASE edgeroute TO edgeroute_user;
   \q
   ```

3. **Update the DATABASE_URL in your .env file**:
   ```
   DATABASE_URL=postgresql://edgeroute_user:your-secure-password@localhost/edgeroute
   ```

## Environment Variables

Key environment variables for deployment:

- `FLASK_APP`: Set to `wsgi.py`
- `FLASK_CONFIG`: Set to `production`
- `SECRET_KEY`: A secure random string
- `DATABASE_URL`: Your database connection string
- `ADMIN_EMAIL`: Email for the admin account
- `ADMIN_PASSWORD`: Initial password for the admin account

## SSL Configuration

For production, always use HTTPS:

1. **Obtain an SSL certificate**:
   - Use Let's Encrypt for free certificates:
     ```bash
     sudo apt install certbot python3-certbot-nginx
     sudo certbot --nginx -d yourdomain.com
     ```

2. **Update Nginx configuration**:
   - The provided Nginx configuration already includes SSL settings
   - Replace the certificate paths with your actual certificate paths

## Monitoring

Monitor your application using:

1. **Prometheus and Grafana**:
   - The application includes prometheus-flask-exporter
   - Set up Prometheus to scrape metrics from your application
   - Create Grafana dashboards for visualization

2. **Supervisor logs**:
   - Check logs at `/var/log/edgeroute/`

## Troubleshooting

Common issues and solutions:

1. **Application not starting**:
   - Check supervisor logs: `sudo supervisorctl status edgeroute`
   - Check application logs: `tail -f /var/log/edgeroute/edgeroute.err.log`

2. **Database connection issues**:
   - Verify database credentials in .env
   - Check if PostgreSQL is running: `sudo systemctl status postgresql`

3. **Nginx not serving the application**:
   - Check Nginx configuration: `sudo nginx -t`
   - Check Nginx logs: `tail -f /var/log/nginx/error.log`

4. **SSL certificate issues**:
   - Renew certificates: `sudo certbot renew`
   - Check certificate expiration: `sudo certbot certificates`

5. **Render-specific issues**:
   - Check logs in the Render dashboard
   - Verify that the build command completes successfully
   - Ensure the start command is correct: `gunicorn wsgi:app`
   - Check that all required environment variables are set
   - For database issues, verify the connection string format
