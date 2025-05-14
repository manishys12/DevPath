import os
import json
from app import create_app, db
from app.models import Roadmap, RoadmapNode
from sqlalchemy.exc import IntegrityError

def import_all_roadmaps():
    # Import all roadmap data from JSON files in the roadmap_data directory
    # and store it in the database.
    print("Starting roadmap import process...")

    # Get the path to the roadmap_data directory
    roadmap_data_dir = os.path.join(os.path.dirname(__file__), 'roadmap_data')

    # Load the roadmaps.json file first to get the list of roadmaps
    with open(os.path.join(roadmap_data_dir, 'roadmaps.json'), 'r', encoding='utf-8') as f:
        roadmaps_data = json.load(f)

    imported_count = 0
    skipped_count = 0

    # Process each roadmap
    for roadmap_info in roadmaps_data['roadmaps']:
        roadmap_id = roadmap_info['id']

        # Check if roadmap already exists
        existing_roadmap = db.session.get(Roadmap, roadmap_id)
        if existing_roadmap:
            print(f"Skipping existing roadmap: {roadmap_id}")
            skipped_count += 1
            continue

        print(f"Importing roadmap: {roadmap_id}")

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

        try:
            # Commit the roadmap to avoid integrity errors with nodes
            db.session.commit()

            # Load the detailed roadmap data
            roadmap_file = os.path.join(roadmap_data_dir, f"{roadmap_id}.json")
            if os.path.exists(roadmap_file):
                with open(roadmap_file, 'r', encoding='utf-8') as f:
                    nodes_data = json.load(f)

                    # Process each node
                    node_count = 0
                    for node_id, node_data in nodes_data.items():
                        # Check if node already exists
                        existing_node = db.session.get(RoadmapNode, node_id)
                        if existing_node:
                            print(f"  Skipping existing node: {node_id}")
                            continue

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
                        node_count += 1

                        # Commit every 10 nodes to avoid large transactions
                        if node_count % 10 == 0:
                            try:
                                db.session.commit()
                            except IntegrityError:
                                db.session.rollback()
                                print(f"  Error adding some nodes, continuing...")

                    # Commit any remaining nodes
                    try:
                        db.session.commit()
                        print(f"  Added {node_count} nodes for roadmap: {roadmap_id}")
                    except IntegrityError:
                        db.session.rollback()
                        print(f"  Error adding some nodes, continuing...")
            else:
                print(f"  Warning: No detailed data file found for roadmap: {roadmap_id}")

            imported_count += 1

        except IntegrityError:
            db.session.rollback()
            print(f"  Error importing roadmap: {roadmap_id}")
            skipped_count += 1

    print(f"\nImport completed:")
    print(f"  - {imported_count} roadmaps imported")
    print(f"  - {skipped_count} roadmaps skipped (already exist or error)")

    return imported_count

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        import_all_roadmaps()
