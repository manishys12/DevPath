from flask import render_template, request, jsonify, flash, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Roadmap, RoadmapNode, UserProgress, Comment
from app.forms import CommentForm
from app.roadmap import roadmap
from app.roadmap.utils import load_roadmap_data
from app.roadmap.version_utils import create_roadmap_version, get_roadmap_versions, get_roadmap_version, restore_roadmap_version
import json
import sys
import os

# AI Roadmap Generator imports - commented out until module is available
# try:
#     # Add the project root directory to the Python path
#     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
#     from ai_roadmap_generator import RoadmapAnalyzer, AIRoadmapGenerator, RoadmapImporter
# except ImportError:
#     # Define placeholder classes if the module is not available
#     class RoadmapAnalyzer: pass
#     class AIRoadmapGenerator: pass
#     class RoadmapImporter: pass

@roadmap.route("/list")
def list_roadmaps():
    roadmaps = Roadmap.query.all()
    return render_template('roadmap/list.html', title='Roadmaps', roadmaps=roadmaps)

@roadmap.route("/<string:roadmap_id>")
def view_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)

    # Get all nodes for the table of contents
    all_nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).all()

    # For initial load, only get the first 5 nodes
    nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).limit(5).all()

    # Get total node count for pagination
    total_nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).count()

    # Get user progress if logged in
    user_progress = {}
    if current_user.is_authenticated:
        progress_entries = UserProgress.query.filter_by(
            user_id=current_user.id,
            roadmap_id=roadmap_id
        ).all()
        for entry in progress_entries:
            user_progress[entry.node_id] = entry.completed

    # Get comments
    form = CommentForm()
    comments = Comment.query.filter_by(roadmap_id=roadmap_id).order_by(Comment.date_posted.desc()).all()

    # Get related roadmaps based on category and tags
    related_roadmaps = []

    # First, try to find roadmaps with the same category
    category_matches = Roadmap.query.filter(
        Roadmap.category == roadmap.category,
        Roadmap.id != roadmap_id
    ).limit(5).all()
    related_roadmaps.extend(category_matches)

    # If we need more, look for tag matches
    if len(related_roadmaps) < 5 and roadmap.tags:
        current_tags = roadmap.tags.split(',')
        for tag in current_tags:
            tag = tag.strip()
            if len(related_roadmaps) >= 5:
                break

            # Find roadmaps that have this tag but aren't already in our list
            tag_matches = Roadmap.query.filter(
                Roadmap.tags.like(f'%{tag}%'),
                Roadmap.id != roadmap_id
            ).all()

            for match in tag_matches:
                if match not in related_roadmaps and len(related_roadmaps) < 5:
                    related_roadmaps.append(match)

    # If we still need more, just add some popular roadmaps
    if len(related_roadmaps) < 3:
        popular_roadmaps = Roadmap.query.filter(
            Roadmap.id != roadmap_id
        ).limit(5 - len(related_roadmaps)).all()

        for roadmap in popular_roadmaps:
            if roadmap not in related_roadmaps:
                related_roadmaps.append(roadmap)

    return render_template('roadmap/view.html',
                          title=roadmap.title,
                          roadmap=roadmap,
                          nodes=nodes,
                          all_nodes=all_nodes,
                          total_nodes=total_nodes,
                          user_progress=user_progress,
                          form=form,
                          comments=comments,
                          related_roadmaps=related_roadmaps)

@roadmap.route("/<string:roadmap_id>/comment", methods=['POST'])
@login_required
def add_comment(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            roadmap_id=roadmap_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('roadmap.view_roadmap', roadmap_id=roadmap_id))

@roadmap.route("/<string:roadmap_id>/progress/<string:node_id>", methods=['POST'])
@login_required
def update_progress(roadmap_id, node_id):
    # Check if roadmap and node exist
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    node = RoadmapNode.query.get_or_404(node_id)

    # Get the completed status from the request
    data = request.get_json()
    completed = data.get('completed', False)

    # Find existing progress or create new one
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        roadmap_id=roadmap_id,
        node_id=node_id
    ).first()

    if progress:
        progress.completed = completed
        if completed:
            from datetime import datetime, timezone
            progress.date_completed = datetime.now(timezone.utc)
        else:
            progress.date_completed = None
    else:
        from datetime import datetime, timezone
        progress = UserProgress(
            user_id=current_user.id,
            roadmap_id=roadmap_id,
            node_id=node_id,
            completed=completed,
            date_completed=datetime.now(timezone.utc) if completed else None
        )
        db.session.add(progress)

    db.session.commit()

    return jsonify({'success': True, 'completed': completed})

@roadmap.route("/<string:roadmap_id>/load-more", methods=['GET'])
def load_more_nodes(roadmap_id):
    """Load more nodes for lazy loading"""
    # Get the offset from the request
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 5, type=int)

    # Get the nodes
    nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).offset(offset).limit(limit).all()

    # Get user progress if logged in
    user_progress = {}
    if current_user.is_authenticated:
        node_ids = [node.id for node in nodes]
        if node_ids:
            progress_entries = UserProgress.query.filter(
                UserProgress.user_id == current_user.id,
                UserProgress.roadmap_id == roadmap_id,
                UserProgress.node_id.in_(node_ids)
            ).all()
            for entry in progress_entries:
                user_progress[entry.node_id] = entry.completed

    # Prepare the response
    nodes_data = []
    for node in nodes:
        links = node.get_links()
        node_data = {
            'id': node.id,
            'title': node.title,
            'description': node.description,
            'links': links,
            'completed': user_progress.get(node.id, False)
        }
        nodes_data.append(node_data)

    return jsonify({
        'success': True,
        'nodes': nodes_data,
        'has_more': len(nodes) == limit
    })

@roadmap.route("/import", methods=['GET', 'POST'])
@login_required
def import_roadmaps():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        try:
            # Import roadmaps from JSON files
            imported_count = load_roadmap_data()
            flash(f'Successfully imported {imported_count} roadmaps!', 'success')
            return redirect(url_for('roadmap.list_roadmaps'))
        except Exception as e:
            flash(f'Error importing roadmaps: {str(e)}', 'danger')

    return render_template('roadmap/import.html', title='Import Roadmaps')

@roadmap.route("/<string:roadmap_id>/versions")
@login_required
def roadmap_versions(roadmap_id):
    """View all versions of a roadmap"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    roadmap = Roadmap.query.get_or_404(roadmap_id)
    versions = get_roadmap_versions(roadmap_id)

    return render_template('roadmap/versions.html',
                          title=f'Versions of {roadmap.title}',
                          roadmap=roadmap,
                          versions=versions)

@roadmap.route("/<string:roadmap_id>/versions/create", methods=['POST'])
@login_required
def create_version(roadmap_id):
    """Create a new version of a roadmap"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    description = request.form.get('description', '')

    version = create_roadmap_version(roadmap_id, description)
    if version:
        flash(f'Version {version.version_number} created successfully!', 'success')
    else:
        flash('Failed to create version.', 'danger')

    return redirect(url_for('roadmap.roadmap_versions', roadmap_id=roadmap_id))

@roadmap.route("/<string:roadmap_id>/versions/<int:version_number>/view")
@login_required
def view_version(roadmap_id, version_number):
    """View a specific version of a roadmap"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    roadmap = Roadmap.query.get_or_404(roadmap_id)
    version_data = get_roadmap_version(roadmap_id, version_number)

    if not version_data:
        flash('Version not found.', 'danger')
        return redirect(url_for('roadmap.roadmap_versions', roadmap_id=roadmap_id))

    return render_template('roadmap/view_version.html',
                          title=f'Version {version_number} of {roadmap.title}',
                          roadmap=roadmap,
                          version_number=version_number,
                          version_data=version_data)

@roadmap.route("/<string:roadmap_id>/versions/<int:version_number>/restore", methods=['POST'])
@login_required
def restore_version(roadmap_id, version_number):
    """Restore a roadmap to a previous version"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    success = restore_roadmap_version(roadmap_id, version_number)

    if success:
        flash(f'Roadmap restored to version {version_number} successfully!', 'success')
    else:
        flash('Failed to restore version.', 'danger')

    return redirect(url_for('roadmap.view_roadmap', roadmap_id=roadmap_id))
