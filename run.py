import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Roadmap, RoadmapNode, UserProgress, Comment

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Roadmap=Roadmap,
                RoadmapNode=RoadmapNode, UserProgress=UserProgress,
                Comment=Comment)

# Create necessary directories
def create_directories():
    # Create profile pictures directory
    profile_pics_dir = os.path.join(app.root_path, 'static', 'profile_pics')
    os.makedirs(profile_pics_dir, exist_ok=True)

    # Add default profile picture if it doesn't exist
    default_pic = os.path.join(profile_pics_dir, 'default.jpg')
    if not os.path.exists(default_pic):
        from PIL import Image, ImageDraw

        # Create a new image with a blue background
        img_size = (200, 200)
        background_color = (59, 89, 152)  # Facebook blue
        img = Image.new('RGB', img_size, background_color)

        # Create a drawing context
        draw = ImageDraw.Draw(img)

        # Draw a circle for the avatar
        circle_center = (img_size[0] // 2, img_size[1] // 2)
        circle_radius = min(img_size) // 2 - 10
        circle_color = (255, 255, 255)  # White

        # Draw the circle
        draw.ellipse(
            (
                circle_center[0] - circle_radius,
                circle_center[1] - circle_radius,
                circle_center[0] + circle_radius,
                circle_center[1] + circle_radius
            ),
            fill=circle_color
        )

        # Draw a simple user icon
        icon_color = background_color

        # Head
        head_radius = circle_radius // 3
        head_center = (circle_center[0], circle_center[1] - head_radius // 2)
        draw.ellipse(
            (
                head_center[0] - head_radius,
                head_center[1] - head_radius,
                head_center[0] + head_radius,
                head_center[1] + head_radius
            ),
            fill=icon_color
        )

        # Body
        body_width = circle_radius
        body_height = circle_radius
        body_top_left = (circle_center[0] - body_width // 2, head_center[1] + head_radius)

        # Draw a rounded rectangle for the body
        draw.ellipse(
            (
                body_top_left[0],
                body_top_left[1],
                body_top_left[0] + body_width,
                body_top_left[1] + body_height
            ),
            fill=icon_color
        )

        # Save the image
        img.save(default_pic, 'JPEG', quality=95)
        print(f"Created default profile picture at {default_pic}")

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Create necessary directories
        create_directories()

    app.run(debug=True)