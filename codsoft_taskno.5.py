import tkinter as tk
from tkinter import ttk, messagebox


class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address


class ContactManager(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Contact Manager")
        self.geometry("650x420")
        self.resizable(False, False)

        self.contacts = []
        self.filtered_indices = []

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Contact Management System", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=5, padx=10, fill="x")

        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5)

        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky="w")
        self.phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, padx=5)

        # Email
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w")
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, padx=5)

        # Address
        ttk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky="w")
        self.address_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.address_var, width=30).grid(row=3, column=1, padx=5)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add Contact", command=self.add_contact).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Update Contact", command=self.update_contact).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Delete Contact", command=self.delete_contact).grid(row=0, column=2, padx=10)

        # Search
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=7)

        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        # Contact List
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, width=60, height=10)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.load_contact())

        scrollbar = ttk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

    # --------------------- CORE FUNCTIONS ---------------------

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required!")
            return

        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        self.contacts.append(Contact(name, phone, email, address))

        self.clear_form()
        self.refresh_list()

    def update_contact(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Update", "Select a contact to update.")
            return

        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required!")
            return

        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        c = self.contacts[idx]
        c.name = name
        c.phone = phone
        c.email = email
        c.address = address

        self.refresh_list()

    def delete_contact(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Delete", "Select a contact to delete.")
            return

        del self.contacts[idx]
        self.clear_form()
        self.refresh_list()

    # ---------------------- SEARCH & DISPLAY ----------------------

    def get_selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        return self.filtered_indices[sel[0]]

    def refresh_list(self):
        query = self.search_var.get().lower()
        visible = []

        for i, c in enumerate(self.contacts):
            if query in c.name.lower() or query in c.phone:
                visible.append((i, c))

        self.listbox.delete(0, tk.END)
        self.filtered_indices = []

        for idx, c in visible:
            self.listbox.insert(tk.END, f"{c.name} - {c.phone}")
            self.filtered_indices.append(idx)

    def load_contact(self):
        idx = self.get_selected_index()
        if idx is None:
            return

        c = self.contacts[idx]
        self.name_var.set(c.name)
        self.phone_var.set(c.phone)
        self.email_var.set(c.email)
        self.address_var.set(c.address)

    def clear_form(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    ContactManager().mainloop()

