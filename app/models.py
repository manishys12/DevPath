from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(60), nullable=False)  # Hashed password
    avatar = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_text_password):
        self._password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        if not self._password:
            return False
        try:
            # Try to verify the password
            return bcrypt.check_password_hash(self._password, attempted_password)
        except Exception as e:
            # Log any errors that occur during password verification
            import logging
            logging.error(f"Error checking password: {str(e)}")
            return False

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Roadmap(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(200), nullable=True)

    # Relationships
    nodes = db.relationship('RoadmapNode', backref='roadmap', lazy=True, cascade="all, delete-orphan")
    progress = db.relationship('UserProgress', backref='roadmap', lazy=True)
    comments = db.relationship('Comment', backref='roadmap', lazy=True)

    def __repr__(self):
        return f"Roadmap('{self.id}', '{self.title}')"

class RoadmapNode(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    roadmap_id = db.Column(db.String(50), db.ForeignKey('roadmap.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    links = db.Column(db.Text, nullable=True)  # Stored as JSON

    # Relationships
    progress = db.relationship('UserProgress', backref='node', lazy=True)

    def get_links(self):
        """Parse and return the links JSON as a Python list"""
        if not self.links:
            return []
        try:
            return json.loads(self.links)
        except:
            return []

    def __repr__(self):
        return f"RoadmapNode('{self.id}', '{self.title}')"

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    roadmap_id = db.Column(db.String(50), db.ForeignKey('roadmap.id'), nullable=False)
    node_id = db.Column(db.String(50), db.ForeignKey('roadmap_node.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_completed = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"UserProgress(User: {self.user_id}, Node: {self.node_id}, Completed: {self.completed})"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    roadmap_id = db.Column(db.String(50), db.ForeignKey('roadmap.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"

class RoadmapVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.String(50), db.ForeignKey('roadmap.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Text, nullable=False)  # JSON data of the roadmap and nodes
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    description = db.Column(db.String(200), nullable=True)

    # Relationships
    roadmap = db.relationship('Roadmap', backref='versions')
    creator = db.relationship('User', backref='created_versions')

    def __repr__(self):
        return f"RoadmapVersion('{self.roadmap_id}', v{self.version_number}, '{self.created_at}')"