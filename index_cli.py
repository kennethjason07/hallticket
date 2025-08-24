import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import sys

def get_user_inputs():
    """Get user inputs via command line"""
    print("🎓 Hall Ticket Generator - Command Line Version")
    print("=" * 50)
    
    # Get Excel file path
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        excel_file = input("📄 Enter the path to Excel file (or press Enter for 'dummy_students.xlsx'): ").strip()
        if not excel_file:
            excel_file = "dummy_students.xlsx"
    
    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"❌ Error: File '{excel_file}' not found!")
        return None, None, None, None, None
    
    # Get department name
    department_name = input("🏫 Enter department name (or press Enter for default): ").strip()
    if not department_name:
        department_name = "INFORMATION SCIENCE ENGINEERING"
    
    # Get logo path
    logo_path = input("🖼️ Enter logo file path (or press Enter to skip): ").strip()
    if logo_path and not os.path.exists(logo_path):
        print(f"⚠️ Warning: Logo file '{logo_path}' not found. Continuing without logo.")
        logo_path = None
    elif not logo_path and os.path.exists("logo.jpg"):
        logo_path = "logo.jpg"
        print("✅ Found 'logo.jpg' in current directory. Using this file.")
    
    # Ask for subject option
    print("\n📚 Subject Options:")
    print("1. Use subjects from Excel file")
    print("2. Enter subjects manually")
    
    while True:
        choice = input("Choose option (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Please enter 1 or 2")
    
    use_custom_subjects = choice == '2'
    custom_subjects = None
    
    if use_custom_subjects:
        print("\n📝 Enter subjects (one per line). Press Enter twice when done:")
        print("Format: Subject Code - Subject Name")
        print("Example: 21CS81 - Machine Learning")
        print()
        
        subjects = []
        while True:
            subject = input().strip()
            if not subject:
                break
            subjects.append(subject)
        
        if subjects:
            custom_subjects = subjects
            print(f"✅ Received {len(custom_subjects)} subjects")
        else:
            print("❌ No subjects entered. Will use subjects from Excel file.")
            use_custom_subjects = False
    
    return excel_file, department_name, logo_path, use_custom_subjects, custom_subjects

def draw_ticket(c, row, y_start, copy_label, department_name, logo_path):
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
    if logo_path:
        try:
            c.drawImage(logo_path, 40, y_start-30, width=60, height=60, mask='auto')
        except:
            pass

    # Header
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width/2, y_start, "GURU NANAK DEV ENGINEERING COLLEGE, BIDAR")
    c.setLineWidth(1)

    # Department name (dynamically set by user)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, y_start-20, department_name.upper())
    c.setLineWidth(0.8)

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

def generate_hallticket(row, department_name, logo_path):
    filename = f"hallticket_{row['Seat No']}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Only two copies now
    copies = ["STUDENT COPY", "COLLEGE COPY"]
    y_positions = [height-50, height/2-30]  # spaced nicely

    for label, y in zip(copies, y_positions):
        draw_ticket(c, row, y, label, department_name, logo_path)

        # Horizontal line separator
        c.setLineWidth(0.5)
        c.line(40, y-280, width-40, y-280)

    # Footer note
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30, "Candidate must read the instructions provided in the answer booklet before commencement of examination.")

    c.showPage()
    c.save()
    print(f"✅ Generated {filename}")

def main():
    # Get user inputs
    excel_file, department_name, logo_path, use_custom_subjects, custom_subjects = get_user_inputs()
    
    if excel_file is None:
        return

    try:
        # Load Excel
        df = pd.read_excel(excel_file)
        print(f"\n✅ Loaded Excel file: {os.path.basename(excel_file)}")
        print(f"📊 Found {len(df)} student records")
        print(f"🏫 Department: {department_name}")
        if logo_path:
            print(f"🖼️ Logo: {os.path.basename(logo_path)}")
        else:
            print("🖼️ No logo selected")
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return

    # Handle custom subjects
    if use_custom_subjects and custom_subjects:
        subjects_string = ", ".join(custom_subjects)
        df['Subjects Applied'] = subjects_string
        print(f"⚙️ Updated all records with custom subjects")
        print(f"📚 Using {len(custom_subjects)} custom subjects")
    else:
        print(f"📊 Using subjects from Excel file")

    # Display summary
    print(f"\n📋 Summary:")
    print(f"   Excel File: {os.path.basename(excel_file)}")
    print(f"   Department: {department_name}")
    print(f"   Students: {len(df)}")
    if logo_path:
        print(f"   Logo: {os.path.basename(logo_path)}")
    if use_custom_subjects and custom_subjects:
        print(f"   Subjects: {len(custom_subjects)} custom subjects")
        for i, subject in enumerate(custom_subjects[:2], 1):
            print(f"      {i}. {subject}")
        if len(custom_subjects) > 2:
            print(f"      ... and {len(custom_subjects) - 2} more")
    else:
        print(f"   Subjects: From Excel file")

    # Confirm generation
    confirm = input(f"\n🔄 Generate hall tickets for {len(df)} students? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Operation cancelled by user.")
        return

    # Generate hall tickets
    print("\n🔄 Generating hall tickets...")
    generated_count = 0

    for _, row in df.iterrows():
        try:
            generate_hallticket(row, department_name, logo_path)
            generated_count += 1
        except Exception as e:
            print(f"❌ Error generating ticket for {row.get('Name', 'Unknown')}: {e}")

    print(f"\n🎉 Successfully generated {generated_count} out of {len(df)} hall tickets!")
    print(f"📁 Files saved in: {os.getcwd()}")

if __name__ == "__main__":
    main()
