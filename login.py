import tkinter as tk
from tkinter import messagebox
import subprocess  # Import for running student_registration.py

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Screen")
        self.root.geometry("700x500")
        self.root.configure(bg="white")  # Set background color

        # Load Image (Handle missing file)
        try:
            self.img = tk.PhotoImage(file="image1.png")  # Ensure 'image1.png' exists
            self.img_label = tk.Label(root, image=self.img, bg="white")
            self.img_label.place(x=10, y=50, width=400, height=400)  # Adjusted position
        except Exception as e:
            print("Error loading image:", e)
            self.img_label = tk.Label(root, text="Image not found", bg="white", font=("Arial", 12))
            self.img_label.place(x=10, y=50, width=400, height=400)

        # 🔹 Updated Login Frame Size (Bigger)
        self.frame = tk.Frame(root, height=350, width=1000, bg="white", bd=2, relief="ridge")
        self.frame.place(x=450, y=200)  # Adjusted position

        tk.Label(self.frame, text="Login", font=("Arial", 22, "bold"), bg="white").pack(pady=20)

        # Username
        self.username_var = tk.StringVar()
        tk.Label(self.frame, text="Username:", bg="white", font=("Arial", 12)).pack()
        self.entry_username = tk.Entry(self.frame, textvariable=self.username_var, font=("Arial", 12))
        self.entry_username.pack(pady=5)

        # Password
        self.password_var = tk.StringVar()
        tk.Label(self.frame, text="Password:", bg="white", font=("Arial", 12)).pack()
        self.entry_password = tk.Entry(self.frame, textvariable=self.password_var, show="*", font=("Arial", 12))
        self.entry_password.pack(pady=5)

        # Login Button
        tk.Button(self.frame, text="Login", bg="#3498DB", fg="white", font=("Arial", 14, "bold"), command=self.login).pack(pady=15)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username == "admin" and password == "1234":  # Sample credentials
            messagebox.showinfo("Login Successful", "Welcome!")
            self.root.destroy()  # Close login window
            subprocess.run(["python", "student_registration.py"])  # Run student_registration.py
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
