import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Toplevel, Label, Entry, Button, StringVar, Text, Scrollbar, Frame

# Initialize tkinter for file dialogs
root = tk.Tk()
root.withdraw()  # Hide the main window

def select_excel_file():
    """Allow user to select an Excel file"""
    file_path = filedialog.askopenfilename(
        title="Select Excel File with Student Data",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
    )
    return file_path

def get_department_name():
    """Get department name from user input"""
    dept_name = simpledialog.askstring(
        "Department Name", 
        "Enter the department name:",
        initialvalue="INFORMATION SCIENCE ENGINEERING"
    )
    return dept_name if dept_name else "INFORMATION SCIENCE ENGINEERING"

def get_logo_path():
    """Allow user to select logo file or use default"""
    if os.path.exists("logo.jpg"):
        use_existing = messagebox.askyesno(
            "Logo File", 
            "Found 'logo.jpg' in current directory. Use this file?"
        )
        if use_existing:
            return "logo.jpg"
    
    logo_path = filedialog.askopenfilename(
        title="Select Logo Image (optional)",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"), ("All files", "*.*")]
    )
    return logo_path if logo_path else None

def get_subjects_option():
    """Ask user whether to use subjects from Excel or enter manually"""
    return messagebox.askyesno(
        "Subject Selection",
        "Do you want to enter subjects manually?\n\nYes = Enter subjects manually\nNo = Use subjects from Excel file"
    )

def get_custom_subjects():
    """Get custom subjects from user via a dialog"""
    dialog = Toplevel(root)
    dialog.title("Enter Subjects")
    dialog.geometry("500x400")
    dialog.resizable(True, True)
    dialog.grab_set()  # Make dialog modal
    
    # Center the dialog
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    subjects = []
    
    # Main frame
    main_frame = Frame(dialog)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Instructions
    Label(main_frame, text="Enter subjects (one per line):")\
        .pack(anchor='w', pady=(0, 5))
    Label(main_frame, text="Format: Subject Code - Subject Name\nExample: 21CS81 - Machine Learning", 
          fg='gray', justify='left').pack(anchor='w', pady=(0, 10))
    
    # Text area with scrollbar
    text_frame = Frame(main_frame)
    text_frame.pack(fill='both', expand=True, pady=(0, 10))
    
    text_area = Text(text_frame, wrap='word', height=15)
    scrollbar = Scrollbar(text_frame, orient='vertical', command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)
    
    text_area.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Sample text
    sample_text = """21CS81 - Machine Learning
21CS82 - Software Engineering
21CS83 - Computer Networks
21CS84 - Database Management Systems"""
    text_area.insert('1.0', sample_text)
    
    # Button frame
    button_frame = Frame(main_frame)
    button_frame.pack(fill='x', pady=(10, 0))
    
    def on_ok():
        content = text_area.get('1.0', 'end-1c').strip()
        if content:
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            subjects.extend(lines)
        dialog.destroy()
    
    def on_cancel():
        dialog.destroy()
    
    Button(button_frame, text="OK", command=on_ok, width=10).pack(side='right', padx=(5, 0))
    Button(button_frame, text="Cancel", command=on_cancel, width=10).pack(side='right')
    
    # Wait for dialog to close
    root.wait_window(dialog)
    
    return subjects if subjects else None

# Get user inputs
print("🔍 Please select the Excel file containing student data...")
excel_file = select_excel_file()

if not excel_file:
    print("❌ No Excel file selected. Exiting.")
    exit()

print("📝 Please enter the department name...")
department_name = get_department_name()

print("🖼️ Please select the logo file...")
logo_path = get_logo_path()

try:
    # Load Excel
    df = pd.read_excel(excel_file)
    print(f"✅ Loaded Excel file: {os.path.basename(excel_file)}")
    print(f"📊 Found {len(df)} student records")
    print(f"🏫 Department: {department_name}")
    if logo_path:
        print(f"🖼️ Logo: {os.path.basename(logo_path)}")
    else:
        print("🖼️ No logo selected")
except Exception as e:
    print(f"❌ Error loading Excel file: {e}")
    exit()

# Ask for subject option
print("📚 Choose subject option...")
use_custom_subjects = get_subjects_option()
custom_subjects = None

if use_custom_subjects:
    print("📝 Please enter the subjects...")
    custom_subjects = get_custom_subjects()
    if custom_subjects:
        print(f"✅ Received {len(custom_subjects)} subjects")
        for i, subject in enumerate(custom_subjects[:3], 1):  # Show first 3
            print(f"   {i}. {subject}")
        if len(custom_subjects) > 3:
            print(f"   ... and {len(custom_subjects) - 3} more")
    else:
        print("❌ No subjects entered. Using subjects from Excel file.")
        use_custom_subjects = False
else:
    print("📊 Will use subjects from Excel file")

# Prepare data with custom subjects if needed
if use_custom_subjects and custom_subjects:
    # Replace subjects in dataframe with custom subjects
    subjects_string = ", ".join(custom_subjects)
    df['Subjects Applied'] = subjects_string
    print(f"⚙️ Updated all records with custom subjects")

def draw_ticket(c, row, y_start, copy_label):
    width, height = A4

    # Draw outer box for ticket (top above logo)
    box_left = 30
    box_right = width - 30
    box_top = y_start + 40  # move box top above logo
    box_bottom = y_start - 320  # enough to cover all content including signatures
    box_width = box_right - box_left
    box_height = box_top - box_bottom
    c.setLineWidth(1)
    c.rect(box_left, box_bottom, box_width, box_height, stroke=1, fill=0)

    # College Logo
    try:
        c.drawImage(logo_path, 40, y_start-30, width=60, height=60, mask='auto')
    except:
        pass

    # Header
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width/2, y_start, "GURU NANAK DEV ENGINEERING COLLEGE, BIDAR")
    c.setLineWidth(1)
    # c.line(40, y_start-10, width-40, y_start-10)  # horizontal line after co

    # Department name (dynamically set by user)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, y_start-20, department_name.upper())
    c.setLineWidth(0.8)
    # c.line(40, y_start-30, width-40, y_start-30)  # horizontal line after department name

    # Exam title
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, y_start-40, "ADMISSION TICKET FOR B.E EXAMINATION JUNE / JULY 2025")
    c.setLineWidth(0.5)
    c.line(40, y_start-50, width-40, y_start-50)  # horizontal line after admission ticket text

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
        c.rect(200, y-5, 60, 15)   # box for signature
        y -= 20

    # Note
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(70, y, "Note: Please verify the eligibility of candidate before issuing the admission ticket.")
    y -= 20
    c.drawString(70, y, "This is Electronically Generated Admission Ticket.")

    # Photo
    if pd.notna(row['Photo Path']):
        try:
            c.drawImage(row['Photo Path'], width-150, y_start-130, 100, 100)
        except:
            pass

    # Exam Center
    c.setFont("Helvetica", 10)
    c.drawString(50, y-30, f"Exam Center: {row['Exam Center']}")

    # Signature placeholders
    c.drawString(50, y-70, "Signature of the Candidate")
    c.drawString(250, y-70, "Signature of the Principal with seal")
    c.drawString(450, y-70, "Signature of the Hod")

def generate_hallticket(row):
    filename = f"hallticket_{row['Seat No']}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Only two copies now
    copies = ["STUDENT COPY", "COLLEGE COPY"]
    y_positions = [height-50, height/2-30]  # spaced nicely

    for label, y in zip(copies, y_positions):
        draw_ticket(c, row, y, label)

        # Horizontal line separator
        c.setLineWidth(0.5)
        c.line(40, y-280, width-40, y-280)

    # Footer note
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "Candidate must read the instructions provided in the answer booklet before commencement of examination.")

    c.showPage()
    c.save()
    print(f"✅ Generated {filename}")

# Confirmation before generating
print(f"\n📋 Summary:")
print(f"   Excel File: {os.path.basename(excel_file)}")
print(f"   Department: {department_name}")
print(f"   Students: {len(df)}")
if logo_path:
    print(f"   Logo: {os.path.basename(logo_path)}")

confirm = messagebox.askyesno(
    "Generate Hall Tickets",
    f"Generate hall tickets for {len(df)} students from {department_name}?"
)

if not confirm:
    print("❌ Operation cancelled by user.")
    exit()

# Generate hall tickets
print("\n🔄 Generating hall tickets...")
generated_count = 0

for _, row in df.iterrows():
    try:
        generate_hallticket(row)
        generated_count += 1
    except Exception as e:
        print(f"❌ Error generating ticket for {row.get('Name', 'Unknown')}: {e}")

print(f"\n🎉 Successfully generated {generated_count} out of {len(df)} hall tickets!")
print(f"📁 Files saved in: {os.getcwd()}")

# Close tkinter root
root.destroy()
