import json
from app import db
from app.models import Roadmap, RoadmapNode, RoadmapVersion
from flask_login import current_user

def create_roadmap_version(roadmap_id, description=None):
    """
    Create a new version of a roadmap

    Args:
        roadmap_id (str): The ID of the roadmap
        description (str, optional): A description of the changes

    Returns:
        RoadmapVersion: The newly created version
    """
    # Get the roadmap and its nodes
    roadmap = Roadmap.query.get(roadmap_id)
    if not roadmap:
        return None

    nodes = RoadmapNode.query.filter_by(roadmap_id=roadmap_id).all()

    # Create a JSON representation of the roadmap and nodes
    roadmap_data = {
        'roadmap': {
            'id': roadmap.id,
            'title': roadmap.title,
            'description': roadmap.description,
            'category': roadmap.category,
            'difficulty': roadmap.difficulty,
            'tags': roadmap.tags
        },
        'nodes': []
    }

    for node in nodes:
        node_data = {
            'id': node.id,
            'title': node.title,
            'description': node.description,
            'links': node.get_links()
        }
        roadmap_data['nodes'].append(node_data)

    # Get the next version number
    latest_version = RoadmapVersion.query.filter_by(roadmap_id=roadmap_id).order_by(
        RoadmapVersion.version_number.desc()
    ).first()

    version_number = 1
    if latest_version:
        version_number = latest_version.version_number + 1

    # Create the new version
    try:
        created_by = current_user.id if current_user.is_authenticated else None
    except:
        # Handle case where current_user is not available (e.g., in scripts)
        created_by = None

    version = RoadmapVersion(
        roadmap_id=roadmap_id,
        version_number=version_number,
        data=json.dumps(roadmap_data),
        created_by=created_by,
        description=description
    )

    db.session.add(version)
    db.session.commit()

    return version

def get_roadmap_versions(roadmap_id):
    """
    Get all versions of a roadmap

    Args:
        roadmap_id (str): The ID of the roadmap

    Returns:
        list: A list of RoadmapVersion objects
    """
    versions = RoadmapVersion.query.filter_by(roadmap_id=roadmap_id).order_by(
        RoadmapVersion.version_number.desc()
    ).all()

    return versions

def get_roadmap_version(roadmap_id, version_number):
    """
    Get a specific version of a roadmap

    Args:
        roadmap_id (str): The ID of the roadmap
        version_number (int): The version number

    Returns:
        dict: The roadmap data for the specified version
    """
    version = RoadmapVersion.query.filter_by(
        roadmap_id=roadmap_id,
        version_number=version_number
    ).first()

    if not version:
        return None

    return json.loads(version.data)

def restore_roadmap_version(roadmap_id, version_number):
    """
    Restore a roadmap to a previous version

    Args:
        roadmap_id (str): The ID of the roadmap
        version_number (int): The version number to restore

    Returns:
        bool: True if successful, False otherwise
    """
    # Get the version data
    version_data = get_roadmap_version(roadmap_id, version_number)
    if not version_data:
        return False

    # Create a new version before restoring (backup)
    create_roadmap_version(roadmap_id, f"Backup before restoring to version {version_number}")

    # Update the roadmap
    roadmap = Roadmap.query.get(roadmap_id)
    roadmap.title = version_data['roadmap']['title']
    roadmap.description = version_data['roadmap']['description']
    roadmap.category = version_data['roadmap']['category']
    roadmap.difficulty = version_data['roadmap']['difficulty']
    roadmap.tags = version_data['roadmap']['tags']

    # Delete existing nodes
    RoadmapNode.query.filter_by(roadmap_id=roadmap_id).delete()

    # Create new nodes from the version data
    for node_data in version_data['nodes']:
        node = RoadmapNode(
            id=node_data['id'],
            roadmap_id=roadmap_id,
            title=node_data['title'],
            description=node_data['description'],
            links=json.dumps(node_data['links'])
        )
        db.session.add(node)

    # Commit changes
    db.session.commit()

    # Create a new version after restoring
    create_roadmap_version(roadmap_id, f"Restored from version {version_number}")

    return True
