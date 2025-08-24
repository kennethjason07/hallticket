#!/usr/bin/env python3
"""
Debug script to check the candidate images workflow
"""

import pandas as pd
import os
from pathlib import Path

def check_excel_data():
    """Check Excel file data"""
    print("🔍 Checking Excel file...")
    try:
        df = pd.read_excel('dummy_students.xlsx')
        print(f"✅ Excel file loaded successfully")
        print(f"📊 Columns: {list(df.columns)}")
        print(f"📋 Student data:")
        for _, row in df.iterrows():
            print(f"   - Seat No: {row['Seat No']}, Name: {row['Name']}")
        return df
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return None

def check_test_images():
    """Check if test images exist"""
    print("\n🖼️ Checking test images...")
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        print(f"❌ Test images directory '{test_dir}' doesn't exist")
        return []
    
    images = []
    for file in os.listdir(test_dir):
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            seat_no = file.split('.')[0]
            filepath = os.path.join(test_dir, file)
            size = os.path.getsize(filepath)
            images.append((seat_no, file, filepath, size))
            print(f"   ✅ Found: {file} (Seat: {seat_no}, Size: {size} bytes)")
    
    return images

def check_upload_directories():
    """Check upload directories"""
    print("\n📁 Checking upload directories...")
    upload_dir = "uploads"
    
    if not os.path.exists(upload_dir):
        print(f"❌ Upload directory '{upload_dir}' doesn't exist")
        return
    
    print(f"✅ Upload directory exists")
    
    # Check for image session directories
    image_dirs = []
    for item in os.listdir(upload_dir):
        item_path = os.path.join(upload_dir, item)
        if os.path.isdir(item_path) and item.startswith('images_'):
            image_dirs.append(item)
            print(f"   📂 Found image session: {item}")
            
            # List images in this directory
            for img_file in os.listdir(item_path):
                if img_file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    img_path = os.path.join(item_path, img_file)
                    size = os.path.getsize(img_path)
                    print(f"      🖼️ {img_file} ({size} bytes)")
    
    if not image_dirs:
        print("   ⚠️ No image session directories found")
        print("   💡 This means images haven't been uploaded through the web interface yet")
    
    return image_dirs

def simulate_matching(df, image_dirs):
    """Simulate the image matching process"""
    print("\n🔗 Simulating image matching...")
    
    if not df is None and image_dirs:
        latest_dir = max(image_dirs)  # Get most recent session
        images_path = os.path.join("uploads", latest_dir)
        
        print(f"   Using image directory: {images_path}")
        
        for _, row in df.iterrows():
            seat_no = str(row['Seat No'])
            matched = False
            
            for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                img_path = os.path.join(images_path, f"{seat_no}.{ext}")
                if os.path.exists(img_path):
                    print(f"   ✅ Match found: {seat_no} → {img_path}")
                    matched = True
                    break
            
            if not matched:
                print(f"   ❌ No image found for seat number: {seat_no}")
    
    else:
        print("   ⚠️ Cannot simulate matching - missing Excel data or image directories")

def main():
    """Main debug function"""
    print("🐛 Hall Ticket Generator - Image Debug Script")
    print("=" * 50)
    
    # Check Excel data
    df = check_excel_data()
    
    # Check test images
    test_images = check_test_images()
    
    # Check upload directories  
    image_dirs = check_upload_directories()
    
    # Simulate matching
    simulate_matching(df, image_dirs)
    
    print("\n💡 Troubleshooting Tips:")
    print("1. Make sure you've uploaded images through the web interface")
    print("2. Click '📤 Upload Images' button after selecting files")
    print("3. Verify image filenames exactly match seat numbers from Excel")
    print("4. Check that images were processed into uploads/images_* directories")
    print("5. Run the Flask app with debug=True to see console output")
    
    print("\n🚀 Quick Test Steps:")
    print("1. Start the web app: python app.py")
    print("2. Go to: http://localhost:5000")
    print("3. Upload dummy_students.xlsx")
    print("4. Upload test images from test_images/ directory")
    print("5. Generate hall tickets and check for photos")

if __name__ == "__main__":
    main()
