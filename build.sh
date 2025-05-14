#!/usr/bin/env bash
# build.sh - Build script for Render deployment

set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p app/static/profile_pics

# Create default profile picture if it doesn't exist
if [ ! -f "app/static/profile_pics/default.jpg" ]; then
    echo "Creating default profile picture..."
    python -c "
from PIL import Image, ImageDraw
img_size = (200, 200)
background_color = (59, 89, 152)
img = Image.new('RGB', img_size, background_color)
draw = ImageDraw.Draw(img)
circle_center = (img_size[0] // 2, img_size[1] // 2)
circle_radius = min(img_size) // 2 - 10
circle_color = (255, 255, 255)
draw.ellipse(
    (
        circle_center[0] - circle_radius,
        circle_center[1] - circle_radius,
        circle_center[0] + circle_radius,
        circle_center[1] + circle_radius
    ),
    fill=circle_color
)
img.save('app/static/profile_pics/default.jpg')
"
fi

echo "Build completed successfully!"
