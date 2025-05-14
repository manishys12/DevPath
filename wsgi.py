from app import create_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import os

# Initialize Sentry for error tracking
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    environment=os.environ.get('FLASK_ENV', 'production')
)

app = create_app('production')

# This is needed for gunicorn to find the app instance
application = app

if __name__ == '__main__':
    app.run() 