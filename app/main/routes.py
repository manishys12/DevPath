from flask import render_template, request, Blueprint
from app.models import Roadmap
from app.main import main

@main.route("/")
@main.route("/home")
def index():
    roadmaps = Roadmap.query.all()
    return render_template('main/index.html', roadmaps=roadmaps)

@main.route("/about")
def about():
    return render_template('main/about.html', title='About')

@main.route("/search")
def search():
    query = request.args.get('q', '')
    if query:
        roadmaps = Roadmap.query.filter(
            (Roadmap.title.contains(query)) | 
            (Roadmap.description.contains(query)) | 
            (Roadmap.tags.contains(query))
        ).all()
    else:
        roadmaps = []
    return render_template('main/search.html', title='Search', roadmaps=roadmaps, query=query)
