from flask import jsonify, request, Blueprint
from app.models import Roadmap, RoadmapNode, UserProgress
from app.api import api
from flask_login import current_user, login_required
import json

@api.route('/roadmaps')
def get_roadmaps():
    roadmaps = Roadmap.query.all()
    result = []
    
    for roadmap in roadmaps:
        tags = roadmap.tags.split(',') if roadmap.tags else []
        result.append({
            'id': roadmap.id,
            'title': roadmap.title,
            'description': roadmap.description,
            'category': roadmap.category,
            'difficulty': roadmap.difficulty,
            'tags': tags
        })
    
    return jsonify({'roadmaps': result})

@api.route('/roadmaps/<string:roadmap_id>')
def get_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).all()
    
    # Format the roadmap data
    tags = roadmap.tags.split(',') if roadmap.tags else []
    roadmap_data = {
        'id': roadmap.id,
        'title': roadmap.title,
        'description': roadmap.description,
        'category': roadmap.category,
        'difficulty': roadmap.difficulty,
        'tags': tags,
        'nodes': {}
    }
    
    # Add nodes data
    for node in nodes:
        links = json.loads(node.links) if node.links else []
        roadmap_data['nodes'][node.id] = {
            'title': node.title,
            'description': node.description,
            'links': links
        }
    
    return jsonify(roadmap_data)

@api.route('/user/progress')
@login_required
def get_user_progress():
    progress_entries = UserProgress.query.filter_by(user_id=current_user.id).all()
    result = {}
    
    for entry in progress_entries:
        if entry.roadmap_id not in result:
            result[entry.roadmap_id] = {}
        
        result[entry.roadmap_id][entry.node_id] = {
            'completed': entry.completed,
            'date_completed': entry.date_completed.isoformat() if entry.date_completed else None
        }
    
    return jsonify({'progress': result})

@api.route('/user/progress/<string:roadmap_id>')
@login_required
def get_roadmap_progress(roadmap_id):
    progress_entries = UserProgress.query.filter_by(
        user_id=current_user.id,
        roadmap_id=roadmap_id
    ).all()
    
    result = {}
    for entry in progress_entries:
        result[entry.node_id] = {
            'completed': entry.completed,
            'date_completed': entry.date_completed.isoformat() if entry.date_completed else None
        }
    
    return jsonify({'roadmap_id': roadmap_id, 'progress': result})
