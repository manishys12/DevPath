from flask import render_template, request, jsonify, flash, redirect, url_for, Blueprint, abort
from flask_login import current_user, login_required
from app import db
from app.models import Roadmap, RoadmapNode
from app.forms import CustomRoadmapForm, RoadmapNodeForm
from app.roadmap import roadmap
import json
import uuid
from datetime import datetime, timezone

@roadmap.route("/custom/create", methods=['GET', 'POST'])
@login_required
def create_custom_roadmap():
    """Create a new custom roadmap"""
    form = CustomRoadmapForm()
    
    if form.validate_on_submit():
        # Generate a unique ID for the roadmap
        roadmap_id = f"custom-{uuid.uuid4().hex[:8]}"
        
        # Create the roadmap
        new_roadmap = Roadmap(
            id=roadmap_id,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            difficulty=form.difficulty.data,
            tags=form.tags.data,
            is_custom=True,
            creator_id=current_user.id,
            is_public=form.is_public.data,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.session.add(new_roadmap)
        db.session.commit()
        
        flash('Your roadmap has been created! Now add some nodes to it.', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))
    
    return render_template('roadmap/create_custom.html', title='Create Custom Roadmap', form=form)

@roadmap.route("/custom/<string:roadmap_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_custom_roadmap(roadmap_id):
    """Edit a custom roadmap"""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    
    # Check if user is the creator or an admin
    if roadmap.creator_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # Get all nodes for this roadmap
    nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).all()
    
    # Create a form for the roadmap
    form = CustomRoadmapForm(obj=roadmap)
    
    if form.validate_on_submit():
        roadmap.title = form.title.data
        roadmap.description = form.description.data
        roadmap.category = form.category.data
        roadmap.difficulty = form.difficulty.data
        roadmap.tags = form.tags.data
        roadmap.is_public = form.is_public.data
        roadmap.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        flash('Your roadmap has been updated!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))
    
    return render_template('roadmap/edit_custom.html', 
                          title=f'Edit {roadmap.title}', 
                          form=form, 
                          roadmap=roadmap, 
                          nodes=nodes)

@roadmap.route("/custom/<string:roadmap_id>/nodes/add", methods=['GET', 'POST'])
@login_required
def add_roadmap_node(roadmap_id):
    """Add a node to a custom roadmap"""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    
    # Check if user is the creator or an admin
    if roadmap.creator_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    form = RoadmapNodeForm()
    
    if form.validate_on_submit():
        # Generate a unique ID for the node
        node_id = f"node-{uuid.uuid4().hex[:8]}"
        
        # Process links - convert from textarea to JSON
        links_text = form.links.data
        links_list = []
        
        if links_text:
            for line in links_text.strip().split('\n'):
                line = line.strip()
                if line:
                    links_list.append({
                        "title": line,
                        "url": line
                    })
        
        # Create the node
        new_node = RoadmapNode(
            id=node_id,
            roadmap_id=roadmap_id,
            title=form.title.data,
            description=form.description.data,
            links=json.dumps(links_list) if links_list else None
        )
        
        db.session.add(new_node)
        db.session.commit()
        
        flash('Node added successfully!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))
    
    return render_template('roadmap/add_node.html', 
                          title='Add Node', 
                          form=form, 
                          roadmap=roadmap)

@roadmap.route("/custom/<string:roadmap_id>/nodes/<string:node_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_roadmap_node(roadmap_id, node_id):
    """Edit a node in a custom roadmap"""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    node = RoadmapNode.query.get_or_404(node_id)
    
    # Check if user is the creator or an admin
    if roadmap.creator_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # Check if node belongs to this roadmap
    if node.roadmap_id != roadmap_id:
        abort(404)
    
    # Create a form and populate it with node data
    form = RoadmapNodeForm(obj=node)
    
    # Convert JSON links to text format for the form
    links = node.get_links()
    links_text = '\n'.join([link.get('url', '') for link in links])
    form.links.data = links_text
    
    if form.validate_on_submit():
        # Process links - convert from textarea to JSON
        links_text = form.links.data
        links_list = []
        
        if links_text:
            for line in links_text.strip().split('\n'):
                line = line.strip()
                if line:
                    links_list.append({
                        "title": line,
                        "url": line
                    })
        
        # Update the node
        node.title = form.title.data
        node.description = form.description.data
        node.links = json.dumps(links_list) if links_list else None
        
        db.session.commit()
        
        flash('Node updated successfully!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))
    
    return render_template('roadmap/edit_node.html', 
                          title='Edit Node', 
                          form=form, 
                          roadmap=roadmap,
                          node=node)

@roadmap.route("/custom/<string:roadmap_id>/nodes/<string:node_id>/delete", methods=['POST'])
@login_required
def delete_roadmap_node(roadmap_id, node_id):
    """Delete a node from a custom roadmap"""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    node = RoadmapNode.query.get_or_404(node_id)
    
    # Check if user is the creator or an admin
    if roadmap.creator_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # Check if node belongs to this roadmap
    if node.roadmap_id != roadmap_id:
        abort(404)
    
    db.session.delete(node)
    db.session.commit()
    
    flash('Node deleted successfully!', 'success')
    return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))

@roadmap.route("/custom/my-roadmaps")
@login_required
def my_roadmaps():
    """View all roadmaps created by the current user"""
    roadmaps = Roadmap.query.filter_by(creator_id=current_user.id).all()
    return render_template('roadmap/my_roadmaps.html', title='My Roadmaps', roadmaps=roadmaps)

@roadmap.route("/custom/<string:roadmap_id>/delete", methods=['POST'])
@login_required
def delete_custom_roadmap(roadmap_id):
    """Delete a custom roadmap"""
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    
    # Check if user is the creator or an admin
    if roadmap.creator_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # Delete all nodes first (should cascade, but just to be safe)
    RoadmapNode.query.filter_by(roadmap_id=roadmap_id).delete()
    
    # Delete the roadmap
    db.session.delete(roadmap)
    db.session.commit()
    
    flash('Roadmap deleted successfully!', 'success')
    return redirect(url_for('roadmap.my_roadmaps'))
