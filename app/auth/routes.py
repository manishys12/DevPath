from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.auth import auth
import os
from PIL import Image

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    from app.models import Roadmap, RoadmapNode, UserProgress
    from sqlalchemy import func

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.avatar.data:
            picture_file = save_picture(form.avatar.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Get progress summary data
    # 1. Count roadmaps with at least one completed topic
    roadmaps_in_progress = db.session.query(UserProgress.roadmap_id) \
        .filter(UserProgress.user_id == current_user.id) \
        .group_by(UserProgress.roadmap_id) \
        .count()

    # 2. Count completed topics
    completed_topics = UserProgress.query \
        .filter(UserProgress.user_id == current_user.id, UserProgress.completed == True) \
        .count()

    # 3. Count total topics across all roadmaps
    total_topics = RoadmapNode.query.count()

    # Get user's recent activity (last 5 completed topics)
    recent_activity = UserProgress.query \
        .filter(UserProgress.user_id == current_user.id, UserProgress.completed == True) \
        .order_by(UserProgress.date_completed.desc()) \
        .limit(5) \
        .all()

    # Get roadmap and node info for recent activity
    activity_details = []
    for progress in recent_activity:
        if progress.date_completed:  # Only include items with a completion date
            roadmap = Roadmap.query.get(progress.roadmap_id)
            node = RoadmapNode.query.get(progress.node_id)
            if roadmap and node:
                activity_details.append({
                    'roadmap': roadmap,
                    'node': node,
                    'date_completed': progress.date_completed
                })

    image_file = url_for('static', filename='profile_pics/' + current_user.avatar)
    return render_template('auth/profile.html', title='Profile',
                           image_file=image_file, form=form,
                           roadmaps_in_progress=roadmaps_in_progress,
                           completed_topics=completed_topics,
                           total_topics=total_topics,
                           activity_details=activity_details)

def save_picture(form_picture):
    # Generate random filename to avoid collisions
    import secrets
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(auth.root_path, '..', 'static', 'profile_pics', picture_fn)

    # Resize image to save space
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Save the picture
    i.save(picture_path)

    return picture_fn

@auth.route("/dashboard")
@login_required
def dashboard():
    """Show a dashboard of user's progress across all roadmaps"""
    from app.models import Roadmap, RoadmapNode, UserProgress
    from sqlalchemy import func, case
    from sqlalchemy.sql import text

    # Get all roadmaps with progress information
    roadmaps_with_progress = db.session.query(
        Roadmap,
        func.count(RoadmapNode.id).label('total_nodes'),
        func.sum(case((UserProgress.completed == True, 1), else_=0)).label('completed_nodes')
    ).outerjoin(
        RoadmapNode, RoadmapNode.roadmap_id == Roadmap.id
    ).outerjoin(
        UserProgress, (UserProgress.node_id == RoadmapNode.id) &
                      (UserProgress.user_id == current_user.id)
    ).group_by(
        Roadmap.id
    ).all()

    # Calculate progress percentage for each roadmap
    roadmap_progress = []
    for roadmap, total_nodes, completed_nodes in roadmaps_with_progress:
        if total_nodes > 0:
            percentage = int((completed_nodes or 0) / total_nodes * 100)
        else:
            percentage = 0

        # Only include roadmaps that have been started or have at least 10 nodes
        if completed_nodes > 0 or total_nodes >= 10:
            roadmap_progress.append({
                'roadmap': roadmap,
                'total_nodes': total_nodes,
                'completed_nodes': completed_nodes or 0,
                'percentage': percentage
            })

    # Sort by progress percentage (descending)
    roadmap_progress.sort(key=lambda x: x['percentage'], reverse=True)

    # Get recent activity (last 10 completed topics)
    recent_activity = UserProgress.query \
        .filter(UserProgress.user_id == current_user.id, UserProgress.completed == True) \
        .order_by(UserProgress.date_completed.desc()) \
        .limit(10) \
        .all()

    # Get roadmap and node info for recent activity
    activity_details = []
    for progress in recent_activity:
        if progress.date_completed:  # Only include items with a completion date
            roadmap = Roadmap.query.get(progress.roadmap_id)
            node = RoadmapNode.query.get(progress.node_id)
            if roadmap and node:
                activity_details.append({
                    'roadmap': roadmap,
                    'node': node,
                    'date_completed': progress.date_completed
                })

    # Get overall statistics
    stats = {
        'roadmaps_started': len([r for r in roadmap_progress if r['completed_nodes'] > 0]),
        'total_completed': sum(r['completed_nodes'] for r in roadmap_progress),
        'total_available': sum(r['total_nodes'] for r in roadmap_progress),
        'overall_percentage': int(sum(r['completed_nodes'] for r in roadmap_progress) /
                               max(sum(r['total_nodes'] for r in roadmap_progress), 1) * 100)
    }

    # Get recommended roadmaps (roadmaps with similar tags to completed ones)
    # This is a simplified recommendation system
    completed_roadmap_ids = [r['roadmap'].id for r in roadmap_progress if r['completed_nodes'] > 0]

    recommended_roadmaps = []
    if completed_roadmap_ids:
        # Get tags from completed roadmaps
        completed_roadmaps = Roadmap.query.filter(Roadmap.id.in_(completed_roadmap_ids)).all()
        all_tags = []
        for r in completed_roadmaps:
            if r.tags:
                all_tags.extend([tag.strip() for tag in r.tags.split(',')])

        # Find roadmaps with similar tags that haven't been started
        if all_tags:
            for tag in set(all_tags):
                similar_roadmaps = Roadmap.query.filter(
                    Roadmap.tags.like(f'%{tag}%'),
                    ~Roadmap.id.in_(completed_roadmap_ids)
                ).limit(3).all()

                for roadmap in similar_roadmaps:
                    if roadmap not in recommended_roadmaps and len(recommended_roadmaps) < 3:
                        recommended_roadmaps.append(roadmap)

    # If we don't have enough recommendations, add some popular roadmaps
    if len(recommended_roadmaps) < 3:
        popular_roadmaps = Roadmap.query.filter(
            ~Roadmap.id.in_([r.id for r in recommended_roadmaps]),
            ~Roadmap.id.in_(completed_roadmap_ids)
        ).limit(3 - len(recommended_roadmaps)).all()

        recommended_roadmaps.extend(popular_roadmaps)

    return render_template('auth/dashboard.html',
                          title='My Learning Dashboard',
                          roadmap_progress=roadmap_progress,
                          activity_details=activity_details,
                          stats=stats,
                          recommended_roadmaps=recommended_roadmaps)
