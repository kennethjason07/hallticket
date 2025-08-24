# Candidate Images Upload Guide

## 📸 Overview

The Hall Ticket Generator now supports uploading individual candidate photos that will appear on their respective hall tickets. This feature allows you to add student photographs for better identification and professional appearance.

## 🚀 How to Use Candidate Images

### Step 1: Prepare Your Images
- **File Format**: JPG, JPEG, PNG, GIF, or BMP
- **File Naming**: **CRITICAL** - Name each image file with the student's seat number
  - ✅ Correct: `3GN21CS021.jpg`, `3GN21AI015.png`, `3GN21ME045.jpeg`
  - ❌ Incorrect: `john.jpg`, `student1.png`, `photo.jpeg`

### Step 2: Upload Images
1. In the web interface, scroll to the "📸 Candidate Photos" section
2. Click "📸 Choose Candidate Images"
3. Select multiple image files (Hold Ctrl/Cmd to select multiple)
4. Click "📤 Upload Images" to process them
5. Wait for confirmation that images were uploaded successfully

### Step 3: Generate Hall Tickets
- After uploading images, proceed with normal hall ticket generation
- Images will automatically be matched to students based on seat numbers
- Students with matching images will have photos on their hall tickets

## 📋 Image Requirements

### File Naming Convention
- **Format**: `[SEAT_NUMBER].[extension]`
- **Examples**:
  - `3GN21CS021.jpg` → matches seat number "3GN21CS021"
  - `3GN21AI015.png` → matches seat number "3GN21AI015" 
  - `3GN21ME045.jpeg` → matches seat number "3GN21ME045"

### Supported Formats
- **JPG/JPEG**: Most common, recommended
- **PNG**: Good quality, larger file size
- **GIF**: Supported but not recommended for photos
- **BMP**: Supported but large file size

### Image Quality
- **Recommended Size**: 200x200 pixels or larger
- **Aspect Ratio**: Square (1:1) or portrait (3:4) works best
- **File Size**: Keep under 2MB per image for faster upload
- **Quality**: Clear, well-lit photographs work best

## 🔧 Technical Details

### Processing
- Images are automatically resized to 200x200 pixels maximum
- Aspect ratio is maintained during resize
- Images are optimized for faster PDF generation
- Original files are stored temporarily and cleaned up after processing

### Storage
- Images are stored in session-specific folders
- Each upload session gets a unique timestamp ID
- Files are automatically linked to students during generation
- Temporary storage is used - files are not permanently stored

### Matching Logic
1. System extracts seat number from filename (before first underscore or dot)
2. Matches extracted seat number with Excel data
3. If match found, associates image with that student's hall ticket
4. If no match, image is ignored (no error generated)

## ⚠️ Important Notes

### File Naming is Critical
- **The seat number in the filename MUST exactly match the seat number in your Excel file**
- Case-sensitive matching (though extensions are case-insensitive)
- Any deviation will result in no photo being added to that student's ticket

### Missing Images
- Students without uploaded photos will have blank photo spaces on their tickets
- This is normal and doesn't cause errors
- You can mix students with and without photos in the same batch

### Multiple Uploads
- You can upload images multiple times in the same session
- Later uploads will overwrite earlier ones if seat numbers match
- Upload images before generating tickets for best results

## 💡 Best Practices

### Preparation
1. **Standardize Naming**: Use a consistent naming convention
2. **Batch Process**: Rename all images before uploading
3. **Quality Check**: Ensure all images are clear and properly oriented
4. **Size Optimization**: Resize large images beforehand if possible

### Workflow
1. Prepare Excel file with student data
2. Organize and name image files correctly
3. Upload Excel file and preview data
4. Upload candidate images and verify count
5. Configure other settings (department, subjects, etc.)
6. Generate hall tickets

### Error Prevention
- **Double-check seat number spelling in filenames**
- **Verify Excel file has correct seat numbers**
- **Test with a small batch first**
- **Keep backup of original images**

## 📊 Example Workflow

### Sample Files Structure
```
Candidate_Photos/
├── 3GN21CS021.jpg  (John Doe)
├── 3GN21CS022.jpg  (Jane Smith) 
├── 3GN21AI015.png  (Mike Johnson)
├── 3GN21ME045.jpg  (Sarah Wilson)
└── 3GN21EC030.jpeg (Tom Brown)
```

### Excel File Sample
| Seat No      | Name        | Exam No  | Date       | Exam Center |
|-------------|-------------|----------|------------|-------------|
| 3GN21CS021  | John Doe    | E001     | 2025-07-01 | GN          |
| 3GN21CS022  | Jane Smith  | E002     | 2025-07-01 | GN          |
| 3GN21AI015  | Mike Johnson| E003     | 2025-07-01 | GN          |

### Result
- John Doe → Gets photo from `3GN21CS021.jpg`
- Jane Smith → Gets photo from `3GN21CS022.jpg`  
- Mike Johnson → Gets photo from `3GN21AI015.png`
- Students without matching images → No photo (blank space)

## 🆘 Troubleshooting

### Common Issues

**Images Not Appearing**
- ✅ Check filename matches seat number exactly
- ✅ Verify image file format is supported
- ✅ Ensure images were uploaded successfully
- ✅ Confirm seat numbers exist in Excel file

**Upload Errors**
- ✅ Check file size (keep under 2MB each)
- ✅ Verify file format is supported
- ✅ Try uploading smaller batches
- ✅ Check available disk space

**Wrong Photos on Tickets**
- ✅ Verify filename matches intended student
- ✅ Check for duplicate seat numbers
- ✅ Ensure no extra characters in filenames

### Getting Help
If you encounter issues:
1. Check this guide first
2. Verify your file naming convention
3. Test with a single image first
4. Contact support with specific error messages

## 🎯 Tips for Success

1. **Use spreadsheet formulas** to generate correct filenames
2. **Batch rename tools** can help standardize filenames
3. **Keep a backup** of original images before renaming
4. **Test with a small group** before processing all students
5. **Document your naming convention** for future reference

This feature makes your hall tickets more professional and helps with student identification during examinations! 📸✨
