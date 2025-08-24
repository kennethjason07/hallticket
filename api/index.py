from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

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
        <p><strong>Status:</strong> Frontend loaded successfully!</p>
        <p><strong>Note:</strong> This is a simplified version running on Vercel serverless functions.</p>
        
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
            
            <button type="button" onclick="alert('Backend functionality is being implemented for Vercel deployment!')">🚀 Generate Hall Tickets (Demo)</button>
        </form>
        
        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <h3>🔧 Deployment Status</h3>
            <p>✅ Frontend: Working</p>
            <p>⏳ Backend: In Progress</p>
            <p>📝 This page confirms that the Vercel deployment is successful and the serverless function is responding.</p>
        </div>
    </div>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode())
        return
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'success': False,
            'message': 'POST endpoint working! Backend functionality is being implemented.',
            'path': self.path,
            'method': self.command
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
