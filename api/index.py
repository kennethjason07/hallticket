from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import zipfile
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Configuration for Vercel - use /tmp for temporary files
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/output'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def draw_ticket(c, row, y_start, copy_label, department_name, logo_path):
    width, height = A4

    # Draw outer box for ticket (top above logo)
    box_left = 30
    box_right = width - 30
    box_top = y_start + 40
    box_bottom = y_start - 320
    box_width = box_right - box_left
    box_height = box_top - box_bottom
    c.setLineWidth(1)
    c.rect(box_left, box_bottom, box_width, box_height, stroke=1, fill=0)

    # College Logo
    if logo_path and os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, 40, y_start-30, width=60, height=60, mask='auto')
        except:
            pass

    # Header
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width/2, y_start, "GURU NANAK DEV ENGINEERING COLLEGE, BIDAR")
    c.setLineWidth(1)

    # Department name
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, y_start-20, department_name.upper())
    c.setLineWidth(0.8)

    # Exam title
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, y_start-40, "ADMISSION TICKET FOR B.E EXAMINATION JUNE / JULY 2025")
    c.setLineWidth(0.5)
    c.line(40, y_start-50, width-40, y_start-50)

    # Copy Label
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width-40, y_start-40, copy_label)

    # Student details
    c.setFont("Helvetica", 10)
    c.drawString(50, y_start-80, f"1. UNIVERSITY SEAT NO.: {row['Seat No']}     No: {row['Exam No']}     Date: {row['Date']}")
    c.drawString(50, y_start-100, f"2. NAME OF THE CANDIDATE: {row['Name']}")

    # Subjects with signature box
    c.drawString(50, y_start-120, "3. SUBJECTS APPLIED:")
    subjects = str(row['Subjects Applied']).split(",")
    y = y_start - 140
    for sub in subjects:
        sub = sub.strip()
        c.drawString(70, y, sub)
        c.rect(200, y-5, 60, 15)
        y -= 20

    # Note
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(70, y, "Note: Please verify the eligibility of candidate before issuing the admission ticket.")
    y -= 20
    c.drawString(70, y, "This is Electronically Generated Admission Ticket.")

    # Photo - aligned with university seat number line
    photo_path = row.get('Photo Path', '')
    print(f"Photo path for {row.get('Seat No', 'Unknown')}: {photo_path}")
    
    if pd.notna(photo_path) and str(photo_path).strip() != '' and os.path.exists(str(photo_path)):
        try:
            print(f"Drawing image: {photo_path}")
            # Align photo with the university seat number line (y_start-80)
            photo_x = width - 150  # Right side position
            photo_y = y_start - 80 - 100  # Start at same level as university seat no, account for image height
            c.drawImage(photo_path, photo_x, photo_y, 100, 100)
            print(f"Successfully drew image for {row.get('Seat No', 'Unknown')}")
        except Exception as e:
            print(f"Error drawing image for {row.get('Seat No', 'Unknown')}: {e}")
    else:
        print(f"No photo or file doesn't exist for {row.get('Seat No', 'Unknown')}: {photo_path}")

    # Exam Center
    c.setFont("Helvetica", 10)
    c.drawString(50, y-30, f"Exam Center: {row['Exam Center']}")

    # Signature placeholders
    c.drawString(50, y-70, "Signature of the Candidate")
    c.drawString(250, y-70, "Signature of the Principal with seal")
    c.drawString(450, y-70, "Signature of the Hod")

def generate_hallticket(row, department_name, logo_path, output_dir):
    filename = f"hallticket_{row['Seat No']}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    copies = ["STUDENT COPY", "COLLEGE COPY"]
    y_positions = [height-50, height/2-30]

    for label, y in zip(copies, y_positions):
        draw_ticket(c, row, y, label, department_name, logo_path)
        c.setLineWidth(0.5)
        c.line(40, y-280, width-40, y-280)

    # Footer note
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "Candidate must read the instructions provided in the answer booklet before commencement of examination.")

    c.showPage()
    c.save()
    return filename

# HTML Template embedded
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hall Ticket Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input, select, textarea { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; box-sizing: border-box; }
        input:focus, select:focus, textarea:focus { border-color: #4CAF50; outline: none; }
        button { background-color: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background-color: #45a049; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .success { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .error { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        .download-btn { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }
        .download-btn:hover { background-color: #0056b3; }
        .radio-group { display: flex; gap: 15px; margin-top: 10px; }
        .radio-item { display: flex; align-items: center; }
        .radio-item input { width: auto; margin-right: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Hall Ticket Generator</h1>
        <form id="hallTicketForm" enctype="multipart/form-data">
            <div class="form-group">
                <label for="excel_file">Excel File (Required):</label>
                <input type="file" id="excel_file" name="excel_file" accept=".xlsx,.xls" required>
                <small>Required columns: Seat No, Exam No, Name, Date, Exam Center</small>
            </div>
            
            <div class="form-group">
                <label for="department_name">Department Name:</label>
                <input type="text" id="department_name" name="department_name" value="INFORMATION SCIENCE ENGINEERING">
            </div>
            
            <div class="form-group">
                <label for="logo_file">Logo Image (Optional):</label>
                <input type="file" id="logo_file" name="logo_file" accept=".jpg,.jpeg,.png,.gif,.bmp">
            </div>
            
            <div class="form-group">
                <label>Subject Configuration:</label>
                <div class="radio-group">
                    <div class="radio-item">
                        <input type="radio" id="subject_excel" name="subject_option" value="excel" checked>
                        <label for="subject_excel">Use subjects from Excel file</label>
                    </div>
                    <div class="radio-item">
                        <input type="radio" id="subject_custom" name="subject_option" value="custom">
                        <label for="subject_custom">Enter custom subjects</label>
                    </div>
                </div>
                <textarea id="custom_subjects" name="custom_subjects" placeholder="21CS81 - Machine Learning\n21CS82 - Software Engineering" style="margin-top: 10px; display: none; height: 100px;"></textarea>
            </div>
            
            <button type="submit">🚀 Generate Hall Tickets</button>
        </form>
        
        <div id="result" style="display: none;"></div>
    </div>

    <script>
        document.querySelectorAll('input[name="subject_option"]').forEach(radio => {
            radio.addEventListener('change', function() {
                const customTextarea = document.getElementById('custom_subjects');
                if (this.value === 'custom') {
                    customTextarea.style.display = 'block';
                } else {
                    customTextarea.style.display = 'none';
                }
            });
        });

        document.getElementById('hallTicketForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultDiv = document.getElementById('result');
            const submitBtn = document.querySelector('button[type="submit"]');
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Generating...';
            resultDiv.style.display = 'none';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                resultDiv.style.display = 'block';
                
                if (data.success) {
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = `
                        <h3>✅ Success!</h3>
                        <p>${data.message}</p>
                        <p>Total Students: ${data.total_students} | Generated: ${data.generated_count}</p>
                        <a href="${data.download_url}" class="download-btn">📥 Download Hall Tickets (ZIP)</a>
                    `;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `<h3>❌ Error</h3><p>${data.error}</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.style.display = 'block';
                resultDiv.className = 'result error';
                resultDiv.innerHTML = '<h3>❌ Error</h3><p>An unexpected error occurred. Please try again.</p>';
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = '🚀 Generate Hall Tickets';
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/upload_images', methods=['POST'])
def upload_candidate_images():
    try:
        uploaded_files = request.files.getlist('candidate_images')
        
        if not uploaded_files or uploaded_files[0].filename == '':
            return jsonify({'error': 'No images uploaded'}), 400
        
        # Create images directory for this session
        session_id = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        images_dir = os.path.join(UPLOAD_FOLDER, f'images_{session_id}')
        os.makedirs(images_dir, exist_ok=True)
        
        uploaded_images = []
        for file in uploaded_files:
            if file and file.filename != '':
                if allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                    # Extract seat number from filename (expected format: SeatNo_Name.ext or SeatNo.ext)
                    filename = secure_filename(file.filename)
                    seat_no = filename.split('_')[0].split('.')[0]  # Get seat number from filename
                    
                    # Save with seat number as filename
                    ext = filename.rsplit('.', 1)[1].lower()
                    new_filename = f"{seat_no}.{ext}"
                    file_path = os.path.join(images_dir, new_filename)
                    file.save(file_path)
                    
                    # Resize image for better performance
                    try:
                        with Image.open(file_path) as img:
                            # Resize to max 200x200 while maintaining aspect ratio
                            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                            img.save(file_path, optimize=True)
                    except Exception as e:
                        print(f"Error resizing image {filename}: {e}")
                    
                    uploaded_images.append({
                        'seat_no': seat_no,
                        'filename': new_filename,
                        'path': file_path
                    })
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'uploaded_count': len(uploaded_images),
            'images': uploaded_images
        })
    
    except Exception as e:
        return jsonify({'error': f'Error uploading images: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if files are present
        if 'excel_file' not in request.files:
            return jsonify({'error': 'No Excel file uploaded'}), 400
        
        excel_file = request.files['excel_file']
        logo_file = request.files.get('logo_file')
        department_name = request.form.get('department_name', 'INFORMATION SCIENCE ENGINEERING')
        subject_option = request.form.get('subject_option', 'excel')
        custom_subjects = request.form.get('custom_subjects', '')
        images_session_id = request.form.get('images_session_id', '')

        if excel_file.filename == '':
            return jsonify({'error': 'No Excel file selected'}), 400

        if not allowed_file(excel_file.filename, ALLOWED_EXTENSIONS):
            return jsonify({'error': 'Invalid Excel file format. Please use .xlsx or .xls'}), 400

        # Save Excel file
        excel_filename = secure_filename(excel_file.filename)
        excel_path = os.path.join(UPLOAD_FOLDER, excel_filename)
        excel_file.save(excel_path)

        # Save logo file if provided
        logo_path = None
        if logo_file and logo_file.filename != '':
            if allowed_file(logo_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                logo_filename = secure_filename(logo_file.filename)
                logo_path = os.path.join(UPLOAD_FOLDER, logo_filename)
                logo_file.save(logo_path)

        # Load Excel data
        try:
            df = pd.read_excel(excel_path)
        except Exception as e:
            return jsonify({'error': f'Error reading Excel file: {str(e)}'}), 400

        # Validate required columns
        required_columns = ['Seat No', 'Exam No', 'Name', 'Date', 'Exam Center']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Missing required columns: {", ".join(missing_columns)}'}), 400

        # Handle subjects
        if subject_option == 'custom' and custom_subjects.strip():
            subjects_list = [s.strip() for s in custom_subjects.split('\n') if s.strip()]
            if subjects_list:
                subjects_string = ", ".join(subjects_list)
                df['Subjects Applied'] = subjects_string
        elif 'Subjects Applied' not in df.columns:
            return jsonify({'error': 'No subjects found. Either select Excel subjects or provide custom subjects.'}), 400

        # Handle candidate images
        if images_session_id:
            images_dir = os.path.join(UPLOAD_FOLDER, f'images_{images_session_id}')
            if os.path.exists(images_dir):
                # Map seat numbers to image paths
                for index, row in df.iterrows():
                    seat_no = str(row['Seat No'])
                    # Look for image files with this seat number
                    for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                        img_path = os.path.join(images_dir, f"{seat_no}.{ext}")
                        if os.path.exists(img_path):
                            df.at[index, 'Photo Path'] = img_path
                            print(f"Matched image for {seat_no}: {img_path}")
                            break
                    else:
                        print(f"No image found for seat number: {seat_no}")

        # Create output directory for this session
        session_dir = os.path.join(OUTPUT_FOLDER, f"session_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(session_dir, exist_ok=True)

        # Generate hall tickets
        generated_files = []
        for _, row in df.iterrows():
            try:
                filename = generate_hallticket(row, department_name, logo_path, session_dir)
                generated_files.append(filename)
            except Exception as e:
                print(f"Error generating ticket for {row.get('Name', 'Unknown')}: {e}")

        # Create ZIP file
        zip_filename = f"hall_tickets_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(OUTPUT_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for filename in generated_files:
                file_path = os.path.join(session_dir, filename)
                if os.path.exists(file_path):
                    zipf.write(file_path, filename)

        return jsonify({
            'success': True,
            'message': f'Successfully generated {len(generated_files)} hall tickets',
            'download_url': f'/download/{zip_filename}',
            'total_students': len(df),
            'generated_count': len(generated_files)
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/preview', methods=['POST'])
def preview_excel():
    try:
        if 'excel_file' not in request.files:
            return jsonify({'error': 'No Excel file uploaded'}), 400
        
        excel_file = request.files['excel_file']
        if excel_file.filename == '':
            return jsonify({'error': 'No Excel file selected'}), 400

        # Save temporary file
        temp_filename = secure_filename(excel_file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, f"temp_{temp_filename}")
        excel_file.save(temp_path)

        # Read Excel file
        df = pd.read_excel(temp_path)
        
        # Clean up temp file
        os.remove(temp_path)

        # Return preview data
        preview_data = {
            'columns': list(df.columns),
            'row_count': len(df),
            'sample_data': df.head(3).to_dict('records')
        }

        return jsonify(preview_data)

    except Exception as e:
        return jsonify({'error': f'Error previewing Excel file: {str(e)}'}), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True)
