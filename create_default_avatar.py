from PIL import Image, ImageDraw, ImageFont
import os

def create_default_avatar():
    # Create a directory for profile pictures if it doesn't exist
    profile_pics_dir = os.path.join('app', 'static', 'profile_pics')
    os.makedirs(profile_pics_dir, exist_ok=True)
    
    # Path for the default avatar
    default_avatar_path = os.path.join(profile_pics_dir, 'default.jpg')
    
    # Check if default avatar already exists
    if os.path.exists(default_avatar_path):
        print(f"Default avatar already exists at {default_avatar_path}")
        return
    
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
    body_bottom_right = (circle_center[0] + body_width // 2, body_top_left[1] + body_height)
    
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
    img.save(default_avatar_path, 'JPEG', quality=95)
    print(f"Default avatar created at {default_avatar_path}")

if __name__ == "__main__":
    create_default_avatar()
