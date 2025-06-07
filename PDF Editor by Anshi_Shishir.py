import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import pikepdf
import os

def merge_pdfs():
    # Let user select multiple PDF files
    files = filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF Files", "*.pdf")])
    
    # Check if at least 2 files were selected
    if not files or len(files) < 2:
        if files:
            messagebox.showerror("Error", "Please select at least 2 PDF files to merge!")
        return
        
    # Create PDF merger object
    merger = PdfMerger()
    
    # Add each selected file to merger
    for file in files:
        try:
            merger.append(file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add {file}: {str(e)}")
            merger.close()
            return
            
    # Let user choose where to save merged PDF
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Merged PDF")
    
    if save_path:
        try:
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Success", f"Successfully merged {len(files)} PDFs!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save merged PDF: {str(e)}")

def split_pdf():
    # Let user select a PDF file to split
    file = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
        
    # Open the PDF and check it has enough pages
    reader = PdfReader(file)
    if len(reader.pages) < 2:
        messagebox.showerror("Error", "PDF must have at least 2 pages to split!")
        return
        
    # Get start and end page numbers from user
    start = simple_input(f"Start Page (1-{len(reader.pages)}):")
    end = simple_input(f"End Page (1-{len(reader.pages)}):")
    
    if not start or not end:
        messagebox.showerror("Error", "Page numbers required!")
        return
        
    # Convert page numbers to integers
    try:
        start_page = int(start)
        end_page = int(end)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")
        return
        
    # Validate page range
    if start_page < 1 or end_page > len(reader.pages) or start_page > end_page:
        messagebox.showerror("Error", f"Invalid page range! Please enter numbers between 1 and {len(reader.pages)}")
        return
        
    # Create new PDF with selected pages
    writer = PdfWriter()
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])
        
    # Let user choose where to save split PDF
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Split PDF")
    
    if save_path:
        try:
            with open(save_path, 'wb') as output_file:
                writer.write(output_file)
            messagebox.showinfo("Success", f"Successfully split pages {start_page} to {end_page}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save split PDF: {str(e)}")

def get_compression_level():
    # Create popup window for compression selection
    popup = tk.Toplevel(root)
    result = [pikepdf.CompressionLevel.default]  # Default compression level
    
    popup.title("Select Compression Level")
    popup.geometry("300x200")
    
    tk.Label(popup, text="Select Compression Level:").pack(pady=10)
    
    # Create buttons for each compression level
    compression_options = [
        ("Low (Better Quality)", pikepdf.CompressionLevel.none),
        ("Medium (Balanced)", pikepdf.CompressionLevel.default),
        ("High (Smaller Size)", pikepdf.CompressionLevel.maximum)
    ]
    
    for text, level in compression_options:
        tk.Button(
            popup,
            text=text,
            command=lambda l=level: (result.__setitem__(0, l), popup.destroy())
        ).pack(pady=5)
    
    # Center the popup window
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry(f'{width}x{height}+{x}+{y}')
    
    popup.grab_set()
    root.wait_window(popup)
    return result[0]

def compress_pdf():
    # Let user select PDF to compress
    file = filedialog.askopenfilename(title="Select PDF to Compress", filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
        
    # Get compression level from user
    compression_level = get_compression_level()
    
    # Let user choose where to save compressed PDF
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Compressed PDF")
    
    if save_path:
        try:
            # Open and compress PDF
            pdf = pikepdf.open(file)
            pdf.save(save_path, optimize_pdf=True, compression=compression_level)
            pdf.close()
            
            # Calculate and show compression results
            original_size = os.path.getsize(file) / (1024 * 1024)  # Convert to MB
            compressed_size = os.path.getsize(save_path) / (1024 * 1024)
            reduction_percent = ((original_size - compressed_size) / original_size) * 100
            
            messagebox.showinfo(
                "Success",
                f"PDF compressed successfully!\n\n"
                f"Original size: {original_size:.2f} MB\n"
                f"Compressed size: {compressed_size:.2f} MB\n"
                f"Size reduction: {reduction_percent:.1f}%"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed: {str(e)}")

def simple_input(prompt_text):
    # Create popup window for text input
    popup = tk.Toplevel(root)
    popup.title("Input Required")
    popup.geometry("300x100")
    
    # Add label and entry field
    tk.Label(popup, text=prompt_text).pack(padx=10, pady=5)
    entry = tk.Entry(popup)
    entry.pack(pady=5)
    
    # Store result and create submit button
    result = []
    tk.Button(
        popup,
        text="Submit",
        command=lambda: (result.append(entry.get()), popup.destroy())
    ).pack(pady=5)
    
    # Center the popup window
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry(f'{width}x{height}+{x}+{y}')
    
    popup.grab_set()
    root.wait_window(popup)
    return result[0] if result else None

# Create main window
root = tk.Tk()
root.title("PDF Editor by Anshi_Shishir")
root.geometry("320x320")

# Center the main window
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Add title label
tk.Label(root, text="📄 PDF Editor", font=("Arial", 18)).pack(pady=15)

# Add buttons for each function
buttons = [
    ("Merge PDFs", merge_pdfs),
    ("Split PDF", split_pdf),
    ("Compress PDF", compress_pdf)
]

for text, command in buttons:
    tk.Button(root, text=text, width=30, command=command).pack(pady=10)

# Add footer
tk.Label(root, text="Made with ❤️ by Anshi_Shishir", font=("Arial", 10)).pack(side="bottom", pady=15)

# Start the application
root.mainloop()