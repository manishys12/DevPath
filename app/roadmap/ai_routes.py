from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.roadmap import roadmap

@roadmap.route("/ai-generator", methods=['GET', 'POST'])
@login_required
def ai_generator():
    """AI Roadmap Generator (placeholder)"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))
        
    # This is a placeholder until the AI generator module is implemented
    if request.method == 'POST':
        flash('AI Roadmap Generator is not yet implemented.', 'info')
        
    return render_template('roadmap/ai_generator_placeholder.html', title='AI Roadmap Generator')
