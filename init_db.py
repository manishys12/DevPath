"""
Database initialization script for Render deployment.
Run this script after deploying to Render to set up the database.
"""
import os
from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt

# Create the application
app = create_app(os.getenv('FLASK_CONFIG') or 'production')
bcrypt = Bcrypt(app)

def init_db():
    """Initialize the database with tables and initial data."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            # Create admin user
            admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
            hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            
            admin = User(
                username='admin',
                email=admin_email,
                password=hashed_password,
                is_admin=True
            )
            
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created with email: {admin_email}")
        else:
            print(f"Admin user already exists with email: {admin_email}")
        
        print("Database initialization completed successfully!")

if __name__ == '__main__':
    init_db()
