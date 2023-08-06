import tkinter as tk
from tkinter import messagebox

def add_task():
    task = task_entry.get()
    if task:
        task_list.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def delete_task():
    try:
        selected_index = task_list.curselection()
        task_list.delete(selected_index)
    except tk.TclError:
        messagebox.showwarning("Warning", "No task selected.")

def run_task_manager():
    root = tk.Tk()
    root.title("Task Manager")

    global task_list
    task_list = tk.Listbox(root)
    task_list.pack(pady=10)

    global task_entry
    task_entry = tk.Entry(root, font=("Helvetica", 12))
    task_entry.pack(pady=10)

    add_button = tk.Button(root, text="Add Task", command=add_task)
    add_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Task", command=delete_task)
    delete_button.pack(pady=5)

    root.mainloop()

