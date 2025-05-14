from app import create_app, db
from app.models import Roadmap

app = create_app()
with app.app_context():
    roadmaps = Roadmap.query.all()
    print(f"Number of roadmaps: {len(roadmaps)}")
    
    if len(roadmaps) == 0:
        print("No roadmaps found in the database.")
    else:
        print("First 5 roadmaps:")
        for roadmap in roadmaps[:5]:
            print(f"  - {roadmap.id}: {roadmap.title}")
