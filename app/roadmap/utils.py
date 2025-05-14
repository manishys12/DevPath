import os
import json
from app import db
from app.models import Roadmap, RoadmapNode

def load_roadmap_data():
    # Load roadmap data from JSON files in the roadmap_data directory
    # and store it in the database.
    #
    # Returns:
    #     int: Number of roadmaps imported
    # Get the path to the roadmap_data directory
    roadmap_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'roadmap_data')

    # Load the roadmaps.json file first to get the list of roadmaps
    with open(os.path.join(roadmap_data_dir, 'roadmaps.json'), 'r', encoding='utf-8') as f:
        roadmaps_data = json.load(f)

    imported_count = 0

    # Process each roadmap
    for roadmap_info in roadmaps_data['roadmaps']:
        roadmap_id = roadmap_info['id']

        # Check if roadmap already exists
        existing_roadmap = Roadmap.query.get(roadmap_id)
        if existing_roadmap:
            # Skip if already exists
            continue

        # Create new roadmap
        tags_str = ','.join(roadmap_info['tags']) if 'tags' in roadmap_info else ''
        new_roadmap = Roadmap(
            id=roadmap_id,
            title=roadmap_info['title'],
            description=roadmap_info['description'],
            category=roadmap_info['category'],
            difficulty=roadmap_info['difficulty'],
            tags=tags_str
        )
        db.session.add(new_roadmap)

        # Load the detailed roadmap data
        roadmap_file = os.path.join(roadmap_data_dir, f"{roadmap_id}.json")
        if os.path.exists(roadmap_file):
            with open(roadmap_file, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)

                # Process each node
                for node_id, node_data in nodes_data.items():
                    # Convert links to JSON string
                    links_json = json.dumps(node_data.get('links', []))

                    # Create new node
                    new_node = RoadmapNode(
                        id=node_id,
                        roadmap_id=roadmap_id,
                        title=node_data['title'],
                        description=node_data['description'],
                        links=links_json
                    )
                    db.session.add(new_node)

        imported_count += 1

    # Commit all changes
    db.session.commit()

    return imported_count
