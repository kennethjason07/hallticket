# Hall Ticket Generator - Web Application

A modern web-based interface for generating professional hall tickets with drag-and-drop file uploads, real-time preview, and batch processing.

## 🌟 Features

### 🎨 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Drag & Drop**: Easy file upload with visual feedback
- **Real-time Preview**: Preview Excel data before processing
- **Progress Indicators**: Loading animations and status updates
- **Beautiful UI**: Modern gradient design with smooth animations

### 📊 Advanced Functionality
- **Excel File Validation**: Automatic column validation and error reporting
- **Live Preview**: See your data before generating tickets
- **Custom Subjects**: Rich text editor for subject entry
- **Logo Upload**: Support for multiple image formats
- **Batch Processing**: Generate tickets for all students at once
- **ZIP Download**: All hall tickets packaged in a single download

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```

Or double-click `start_web.bat` on Windows.

The application will be available at: **http://localhost:5000**

## 📱 How to Use

### 1. Upload Excel File
- Click "📄 Choose Excel File" to select your student data
- Required columns: `Seat No`, `Exam No`, `Name`, `Date`, `Exam Center`
- Optional: `Subjects Applied`, `Photo Path`
- Click "👁️ Preview Data" to verify your file

### 2. Configure Department
- Enter your department name (e.g., "Computer Science Engineering")
- This appears on all generated hall tickets

### 3. Upload Logo (Optional)
- Click "🖼️ Choose Logo Image" to add your college logo
- Supported formats: JPG, PNG, GIF, BMP
- Logo will appear on all hall tickets

### 4. Configure Subjects
Choose one of two options:
- **Excel Subjects**: Use individual subjects from your Excel file
- **Custom Subjects**: Enter uniform subjects for all students
  ```
  21CS81 - Machine Learning
  21CS82 - Software Engineering
  21CS83 - Computer Networks
  21CS84 - Database Management Systems
  ```

### 5. Generate & Download
- Click "🚀 Generate Hall Tickets"
- Wait for processing (progress indicator shows status)
- Click "📥 Download Hall Tickets (ZIP)" to get all PDFs

## 🏗️ Architecture

### Backend (Flask)
- **app.py**: Main Flask application
- **Templates**: HTML templates in `/templates/`
- **Uploads**: Temporary file storage in `/uploads/`
- **Output**: Generated files in `/output/`

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Mobile-first approach
- **Modern CSS**: Gradients, animations, and smooth transitions
- **Interactive JavaScript**: File handling, form validation, AJAX calls
- **Error Handling**: User-friendly error messages

## 🔧 API Endpoints

### `GET /`
Returns the main web interface

### `POST /upload`
Processes hall ticket generation
- **Files**: `excel_file`, `logo_file` (optional)
- **Data**: `department_name`, `subject_option`, `custom_subjects`
- **Response**: Success/error with download link

### `POST /preview`
Previews Excel file data
- **Files**: `excel_file`
- **Response**: Column names, row count, sample data

### `GET /download/<filename>`
Downloads generated ZIP file

## 📂 File Structure

```
mkmk/
├── app.py                 # Flask backend
├── templates/
│   └── index.html        # Main web interface
├── uploads/              # Temporary uploads
├── output/               # Generated files
├── requirements.txt      # Python dependencies
├── start_web.bat        # Windows startup script
└── WEB_README.md        # This documentation
```

## 🎯 Features in Detail

### File Upload & Validation
- **Drag & Drop**: Modern file upload experience
- **File Type Validation**: Only Excel files accepted
- **Size Display**: Shows file size information
- **Error Handling**: Clear error messages for invalid files

### Excel Preview
- **Column Detection**: Automatically identifies available columns
- **Data Preview**: Shows first 3 rows of data
- **Statistics**: Displays row count and column count
- **Missing Column Detection**: Warns about required columns

### Subject Management
- **Flexible Options**: Use Excel data or custom subjects
- **Rich Text Editor**: Monospace font for better formatting
- **Format Guidance**: Clear examples and instructions
- **Real-time Switching**: Toggle between options easily

### Generation Process
- **Progress Indicators**: Spinning loader with status text
- **Error Recovery**: Graceful error handling with user feedback
- **Success Statistics**: Shows generation success rate
- **Automatic ZIP**: Packages all PDFs for easy download

### Mobile Responsive
- **Adaptive Layout**: Optimized for all screen sizes
- **Touch Friendly**: Large buttons and touch targets
- **Readable Text**: Proper font sizes and spacing
- **Simplified Navigation**: Streamlined mobile experience

## 🔒 Security Features

- **File Type Validation**: Only accepted file types allowed
- **Secure Filenames**: Uses werkzeug's secure_filename
- **Temporary Storage**: Files cleaned up after processing
- **Error Sanitization**: Prevents information leakage

## 🚀 Production Deployment

For production use, consider:
- Use a WSGI server like Gunicorn or uWSGI
- Set up reverse proxy with Nginx
- Configure proper logging
- Set up file cleanup routines
- Use environment variables for configuration

```bash
# Example production command
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🎨 Customization

### Styling
Edit the CSS in `templates/index.html` to customize:
- Color scheme
- Fonts and typography
- Layout and spacing
- Animations and transitions

### College Information
Update these fields in `app.py`:
```python
c.drawCentredString(width/2, y_start, "YOUR COLLEGE NAME")
```

### Default Values
Modify default department name and other settings in the HTML template.

## 📱 Browser Support

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**File Upload Errors**
- Check file permissions
- Verify disk space
- Ensure proper file format

**Generation Failures**
- Verify all required columns exist
- Check for special characters in data
- Ensure logo file is valid

### Debug Mode
The application runs in debug mode by default. For production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

Enjoy your modern web-based hall ticket generator! 🎉
