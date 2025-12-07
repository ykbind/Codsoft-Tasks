import tkinter as tk
from tkinter import ttk, messagebox
import string
import random


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Password Generator")
        self.geometry("500x300") 
        self.resizable(False, False)
        self.length_var = tk.StringVar(value="12")
        self.include_upper = tk.BooleanVar(value=False)
        self.include_lower = tk.BooleanVar(value=False)
        self.include_digits = tk.BooleanVar(value=False)
        self.include_symbols = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar(value="")
        self.create_widgets()

    def create_widgets(self):
        
        title_label = ttk.Label(self, text="Password Generator", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=12)

        
        length_frame = ttk.Frame(self)
        length_frame.pack(pady=5, fill="x", padx=20)

        ttk.Label(length_frame, text="Password length:").pack(side="left")
        length_entry = ttk.Entry(length_frame, textvariable=self.length_var, width=10)
        length_entry.pack(side="left", padx=8)

        
        options_frame = ttk.LabelFrame(self, text="Include characters")
        options_frame.pack(pady=10, fill="x", padx=20)

        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.include_upper).pack(anchor="w", padx=8)
        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.include_lower).pack(anchor="w", padx=8)
        ttk.Checkbutton(options_frame, text="Digits (0-9)", variable=self.include_digits).pack(anchor="w", padx=8)
        ttk.Checkbutton(options_frame, text="Symbols (!@#$...)", variable=self.include_symbols).pack(anchor="w", padx=8)

       
        generate_btn = ttk.Button(self, text="Generate Password", command=self.generate_password)
        generate_btn.pack(pady=12)

        
        result_frame = ttk.Frame(self)
        result_frame.pack(pady=8, fill="x", padx=20)

        ttk.Label(result_frame, text="Password:").pack(side="left")

        
        result_entry = ttk.Entry(result_frame, textvariable=self.password_var, width=40)
        result_entry.pack(side="left", padx=8)

        ttk.Button(result_frame, text="Copy", command=self.copy_to_clipboard).pack(side="left")

    def generate_password(self):
       
        try:
            length = int(self.length_var.get())
            if length <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid length", "Please enter a positive number for length.")
            return

        
        chars = ""
        if self.include_upper.get():
            chars += string.ascii_uppercase
        if self.include_lower.get():
            chars += string.ascii_lowercase
        if self.include_digits.get():
            chars += string.digits
        if self.include_symbols.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("No characters selected", "Please select at least one character type.")
            return

        
        password = "".join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

    def copy_to_clipboard(self):
        pwd = self.password_var.get()
        if not pwd:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return

        self.clipboard_clear()
        self.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
