import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


class Task:
    def __init__(self, title, description="", completed=False):
        self.title = title
        self.description = description
        self.completed = completed


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple To-Do List")
        self.geometry("700x450")

        self.tasks = []
        self.filtered_indices = []

        self.create_widgets()

    def create_widgets(self):
        # ---- Top Input ----
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(top, text="Task:").pack(side=tk.LEFT)
        self.title_var = tk.StringVar()
        entry_title = ttk.Entry(top, textvariable=self.title_var)
        entry_title.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        ttk.Button(top, text="Add", command=self.add_task).pack(side=tk.LEFT)
        ttk.Button(top, text="Update", command=self.update_task).pack(side=tk.LEFT, padx=6)

        # ---- Middle ----
        middle = ttk.Frame(self)
        middle.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Left section
        left = ttk.Frame(middle)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Search bar
        search_frame = ttk.Frame(left)
        search_frame.pack(fill=tk.X)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        # Buttons under search
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill=tk.X, pady=6)

        ttk.Button(btn_frame, text="Complete", command=self.mark_complete).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Incomplete", command=self.mark_incomplete).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Delete", command=self.delete_task).pack(side=tk.LEFT)

        # Task listbox
        self.listbox = tk.Listbox(left)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox.bind("<<ListboxSelect>>", lambda e: self.show_details())
        self.listbox.bind("<Double-1>", lambda e: self.load_task())

        scrollbar = ttk.Scrollbar(left, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # ---- Right section ----
        right = ttk.Frame(middle, width=250)
        right.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))

        ttk.Label(right, text="Description:").pack(anchor=tk.W)
        self.txt_desc = ScrolledText(right, height=10)
        self.txt_desc.pack(fill=tk.BOTH, expand=True)

        ttk.Label(right, text="Status:").pack(anchor=tk.W, pady=(8, 0))
        self.lbl_status = ttk.Label(right, text="-")
        self.lbl_status.pack(anchor=tk.W)

    # ---------------- Core Features ----------------

    def add_task(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty.")
            return

        desc = self.txt_desc.get("1.0", tk.END).strip()
        task = Task(title, desc)
        self.tasks.append(task)

        self.clear_inputs()
        self.refresh_list()

    def update_task(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Update", "Select a task to update.")
            return

        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty.")
            return

        desc = self.txt_desc.get("1.0", tk.END).strip()

        task = self.tasks[idx]
        task.title = title
        task.description = desc

        self.refresh_list()

    def delete_task(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Delete", "Select a task to delete.")
            return

        del self.tasks[idx]
        self.clear_inputs()
        self.refresh_list()

    def mark_complete(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        self.tasks[idx].completed = True
        self.refresh_list()

    def mark_incomplete(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        self.tasks[idx].completed = False
        self.refresh_list()

    # ---------------- Helpers ----------------

    def get_selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        visible = sel[0]
        return self.filtered_indices[visible]

    def refresh_list(self):
        query = self.search_var.get().lower()
        visible = []

        for i, t in enumerate(self.tasks):
            if query in t.title.lower() or query in t.description.lower():
                visible.append((i, t))

        self.listbox.delete(0, tk.END)
        self.filtered_indices = []

        for idx, t in visible:
            status = "[✓]" if t.completed else "[ ]"
            self.listbox.insert(tk.END, f"{status} {t.title}")
            self.filtered_indices.append(idx)

        self.show_details()

    def show_details(self):
        idx = self.get_selected_index()
        if idx is None:
            self.lbl_status.config(text="-")
            return

        t = self.tasks[idx]
        self.lbl_status.config(text="Completed" if t.completed else "Pending")

    def load_task(self):
        idx = self.get_selected_index()
        if idx is None:
            return

        t = self.tasks[idx]
        self.title_var.set(t.title)
        self.txt_desc.delete("1.0", tk.END)
        self.txt_desc.insert(tk.END, t.description)

    def clear_inputs(self):
        self.title_var.set("")
        self.txt_desc.delete("1.0", tk.END)
        self.listbox.selection_clear(0, tk.END)


# ---------------- Run App ----------------
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
