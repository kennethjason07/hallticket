# Hall Ticket Generator

A Python application to generate professional hall tickets for college examinations with customizable options.

## ✨ Features

### 📁 File Management
- **Excel File Selection**: Choose any Excel file with student data
- **Logo Integration**: Add college logo (supports JPG, PNG, GIF, BMP)
- **PDF Generation**: Creates professional PDF hall tickets

### 🎯 Customization Options
- **Department Name**: Enter custom department name
- **Subject Selection**: 
  - Use subjects from Excel file, OR
  - Enter custom subjects manually with codes and names
- **Flexible Layout**: Professional formatting with signature boxes

### 🖥️ User Interface Options
- **GUI Version** (`index.py`): User-friendly dialogs and file browsers
- **CLI Version** (`index_cli.py`): Command-line interface for terminal users

## 📋 Required Excel Format

Your Excel file should contain these columns:
- `Seat No`: Student seat number
- `Exam No`: Examination number
- `Name`: Student name
- `Date`: Examination date
- `Subjects Applied`: Subject codes (only used if custom subjects not selected)
- `Exam Center`: Examination center
- `Photo Path`: Path to student photo (optional)

## 🚀 Installation

```bash
pip install pandas reportlab
```

## 💻 Usage

### GUI Version (Recommended)
```bash
python index.py
```
- File dialogs guide you through the process
- Easy subject entry with text editor
- Visual confirmation before generation

### CLI Version
```bash
python index_cli.py [excel_file]
```
- Terminal-based prompts
- Perfect for automation or server environments
- All features available via command line

## 🎓 Subject Entry Format

When entering custom subjects, use this format:
```
21CS81 - Machine Learning
21CS82 - Software Engineering  
21CS83 - Computer Networks
21CS84 - Database Management Systems
```

## 📄 Output

- Generates individual PDF files: `hallticket_[SEAT_NO].pdf`
- Each PDF contains:
  - Student copy
  - College copy
- Professional formatting with college header
- Signature boxes for verification
- Student photo (if provided)

## 🔧 Customization

### Modify College Details
Edit these lines in the code to change college information:
```python
c.drawCentredString(width/2, y_start, "YOUR COLLEGE NAME HERE")
```

### Change Examination Details
Update the exam title:
```python
c.drawCentredString(width/2, y_start-40, "YOUR EXAM TITLE HERE")
```

## 📁 File Structure

```
mkmk/
├── index.py           # GUI version
├── index_cli.py       # CLI version
├── dummy_students.xlsx # Sample data
├── logo.jpg           # College logo
├── README.md          # This file
└── hallticket_*.pdf   # Generated files
```

## ⚡ Quick Start

1. Prepare your Excel file with student data
2. Add your college logo as `logo.jpg` (optional)
3. Run the application:
   ```bash
   python index.py
   ```
4. Follow the prompts to:
   - Select Excel file
   - Enter department name
   - Choose logo
   - Select subject option (Excel or custom)
   - Generate hall tickets

## 🎯 Example Workflow

### Using Custom Subjects
1. Select your Excel file
2. Enter "Computer Science Engineering" as department
3. Choose custom subjects option
4. Enter subjects:
   ```
   21CS701 - Advanced Algorithms
   21CS702 - Machine Learning
   21CS703 - Computer Networks
   ```
5. Generate hall tickets with your custom subjects

### Using Excel Subjects
1. Select Excel file with subject data
2. Choose "Use subjects from Excel file"
3. All student records will use their individual subjects from Excel

## 🛠️ Troubleshooting

- **Missing tkinter**: Install with `pip install tk`
- **PDF generation errors**: Check reportlab installation
- **Logo not showing**: Verify image file path and format
- **Excel errors**: Ensure all required columns exist

## 📸 Screenshots

The application generates professional hall tickets with:
- College header and logo
- Department name
- Student details
- Subject list with signature boxes
- Examination center information
- Footer notes and instructions

Enjoy generating professional hall tickets! 🎉
"# hallticket" 
