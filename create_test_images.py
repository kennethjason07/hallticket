#!/usr/bin/env python3
"""
Create sample images for testing the candidate image upload feature.
This script creates simple colored rectangles as test images with proper naming.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(seat_no, name, size=(200, 200)):
    """Create a test image with seat number and name"""
    # Create a new image with a light blue background
    img = Image.new('RGB', size, color=(173, 216, 230))  # Light blue
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw seat number
    text = f"Seat: {seat_no}"
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = size[1] // 3
        draw.text((x, y), text, fill=(0, 0, 0), font=font)
    
    # Draw name
    name_text = f"Name: {name}"
    if font:
        bbox = draw.textbbox((0, 0), name_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2
        y = (size[1] // 3) + 30
        draw.text((x, y), name_text, fill=(0, 0, 0), font=font)
    
    # Draw a simple border
    draw.rectangle([5, 5, size[0]-5, size[1]-5], outline=(0, 0, 0), width=2)
    
    return img

# Sample student data from your Excel file
students = [
    ("3GN21AI015", "Mahesh"),
    ("3GN21CS021", "Anjali"), 
    ("3GN21ME045", "Ravi Kumar")
]

# Create test images
test_images_dir = "test_images"
os.makedirs(test_images_dir, exist_ok=True)

print("Creating test candidate images...")

for seat_no, name in students:
    # Create image
    img = create_test_image(seat_no, name)
    
    # Save with seat number as filename
    filename = f"{seat_no}.jpg"
    filepath = os.path.join(test_images_dir, filename)
    img.save(filepath, "JPEG", quality=85)
    
    print(f"✅ Created: {filename}")

print(f"\n🎉 Test images created in '{test_images_dir}' directory")
print(f"📋 Files created:")
for seat_no, name in students:
    print(f"   - {seat_no}.jpg (for {name})")

print(f"\n📖 Instructions:")
print(f"1. Use these images to test the candidate photo upload feature")
print(f"2. In the web interface, upload these images using the '📸 Choose Candidate Images' button")
print(f"3. Click '📤 Upload Images' to process them")
print(f"4. Generate hall tickets - the images should appear on matching students' tickets")
