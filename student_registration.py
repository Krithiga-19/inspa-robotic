import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import openpyxl
import os
import re
import shutil
import subprocess

# Global variable to store the photo path
photo_filename = ""
admin_access = False  # Track admin login status

# Function to upload a photo
def upload_photo():
    global photo_filename
    file_path = filedialog.askopenfilename(title="Select a Photo", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        if not os.path.exists("photos"):
            os.makedirs("photos")

        filename = os.path.basename(file_path)
        destination = os.path.join("photos", filename)
        shutil.copy(file_path, destination)
        photo_filename = filename
        messagebox.showinfo("Success", "Photo uploaded successfully!")

# Function to validate input data
def validate_data():
    phone_pattern = r"^\d{10}$"
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not entries[0].get():
        messagebox.showerror("Error", "Full Name is required.")
        return False
    if not entries[4].get().isdigit() or not re.match(phone_pattern, entries[4].get()):
        messagebox.showerror("Error", "Enter a valid 10-digit Phone Number.")
        return False
    if not re.match(email_pattern, entries[5].get()):
        messagebox.showerror("Error", "Enter a valid Email Address.")
        return False
    if not photo_filename:
        messagebox.showerror("Error", "Please upload a photo.")
        return False
    return True

# Function to save student data
def save_data():
    if not validate_data():
        return
    
    data = [
        entries[0].get(), entries[1].get(), gender_var.get(), class_var.get(),
        entries[2].get(), entries[3].get(), entries[4].get(), entries[5].get(),
        entries[6].get(), entries[7].get(), entries[8].get(), entries[9].get(),
        entries[10].get(), photo_filename
    ]

    filename = "student_data.xlsx"

    if not os.path.exists(filename):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Student Details"
        headers = ["Full Name", "Date of Birth", "Gender", "Class", "Religion",
                   "Address", "Phone Number", "Email", "Nationality",
                   "Guardian's Name", "Guardian's Contact", "Previous School", "Admission Date", "Photo"]
        sheet.append(headers)
        workbook.save(filename)

    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active
    sheet.append(data)
    workbook.save(filename)
    workbook.close()

    messagebox.showinfo("Success", "Student details saved successfully!")
    reset_fields()

# Function to reset fields
def reset_fields():
    global photo_filename
    for entry in entries:
        entry.delete(0, tk.END)
    gender_var.set()
    class_var.set("Select class")
    photo_filename = ""

# Function to authenticate admin and enable the search button
def admin_login():
    global admin_access
    password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show="*")
    if password == "admin123":  # Change this password as needed
        messagebox.showinfo("Access Granted", "Admin Access Enabled!")
        admin_access = True
        search_button.config(state=tk.NORMAL)  # Enable search button
    else:
        messagebox.showerror("Access Denied", "Incorrect Password!")

# Function to open search.py using subprocess
def open_search_window():
    if admin_access:
        subprocess.Popen(["python", "search.py"])
    else:
        messagebox.showerror("Access Denied", "Admin login required!")

# Create main window
root = tk.Tk()
root.title("Student Registration System")
root.geometry("750x700")
root.configure(bg="purple")

# Header
tk.Label(root, text="STUDENT REGISTRATION", font=("Arial", 16, "bold"), bg="violet", fg="white").pack(pady=10)

# Form Frame
form_frame = tk.Frame(root, bg="purple")
form_frame.pack(pady=10)

# Labels & Entry Fields
fields = [
    ("Full Name:", 0, 0), ("Date of Birth:", 1, 0), ("Gender:", 2, 0), ("Class:", 3, 0),
    ("Religion:", 4, 0), ("Address:", 5, 0), ("Phone Number:", 6, 0), ("Email ID:", 7, 0),
    ("Nationality:", 8, 0), ("Guardian's Name:", 9, 0), ("Guardian's Contact:", 10, 0),
    ("Previous School:", 11, 0), ("Admission Date:", 12, 0), ("Upload Photo:", 13, 0)
]

entries = []
gender_var = tk.StringVar(value="None")
class_var = tk.StringVar(value="Select class")

for text, row, col in fields:
    tk.Label(form_frame, text=text, fg="white", bg="purple", font=("Arial", 10, "bold")).grid(row=row, column=col, padx=10, pady=5, sticky="w")
    
    if text == "Gender:":
        tk.Radiobutton(form_frame, text="Male", variable=gender_var, value="Male", bg="purple", fg="white").grid(row=row, column=col+1, sticky="w")
        tk.Radiobutton(form_frame, text="Female", variable=gender_var, value="Female", bg="purple", fg="white").grid(row=row, column=col+2, sticky="w")
    elif text == "Class:":
        class_dropdown = tk.OptionMenu(form_frame, class_var, "B.Tech", "B.Com", "Arts and Science", "Agricultural Science")
        class_dropdown.grid(row=row, column=col+1, padx=10, pady=5)
    elif text == "Upload Photo:":
        upload_button = tk.Button(form_frame, text="Choose File", command=upload_photo, bg="blue", fg="white")
        upload_button.grid(row=row, column=col+1, padx=10, pady=5)
    else:
        entry = tk.Entry(form_frame, width=30)
        entry.grid(row=row, column=col+1, padx=10, pady=5)
        entries.append(entry)

# Buttons
button_frame = tk.Frame(root, bg="purple")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Save & Next", command=save_data, bg="green", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Reset", command=reset_fields, bg="red", fg="white", width=10).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Exit", command=root.destroy, bg="gray", fg="white", width=10).grid(row=0, column=2, padx=5)

# Admin Login Button
tk.Button(button_frame, text="Admin Login", command=admin_login, bg="orange", fg="white", width=12).grid(row=1, column=0, padx=5, pady=5)

# Search Button (Initially Disabled)
search_button = tk.Button(button_frame, text="Search", command=open_search_window, bg="blue", fg="white", width=10, state=tk.DISABLED)
search_button.grid(row=1, column=1, padx=5, pady=5)

# Run the application
root.mainloop()
