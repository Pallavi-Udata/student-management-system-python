import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ---------------- Database Setup ----------------
def connect_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT,
            course TEXT,
            marks REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_student(roll_no, name, course, marks):
    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (roll_no, name, course, marks))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "✅ Student added successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "⚠️ Roll No already exists!")

def view_students():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_student(roll_no):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
    row = cur.fetchone()
    conn.close()
    return row

def update_student(roll_no, name, course, marks):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=?, course=?, marks=? WHERE roll_no=?", (name, course, marks, roll_no))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "✅ Student updated successfully!")

def delete_student(roll_no):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "✅ Student deleted successfully!")

# ---------------- GUI Functions ----------------
def add_student_gui():
    if not roll_no_entry.get():
        messagebox.showwarning("Input Error", "Roll No is required!")
        return
    insert_student(int(roll_no_entry.get()), name_entry.get(), course_entry.get(), float(marks_entry.get()))
    clear_entries()
    refresh_list()

def search_student_gui():
    if not roll_no_entry.get():
        messagebox.showwarning("Input Error", "Enter Roll No to search!")
        return
    row = search_student(int(roll_no_entry.get()))
    if row:
        messagebox.showinfo("Found", f"🎓 Roll No: {row[0]}\n👤 Name: {row[1]}\n📚 Course: {row[2]}\n📊 Marks: {row[3]}")
    else:
        messagebox.showwarning("Not Found", "⚠️ No student with this Roll No.")

def update_student_gui():
    update_student(int(roll_no_entry.get()), name_entry.get(), course_entry.get(), float(marks_entry.get()))
    clear_entries()
    refresh_list()

def delete_student_gui():
    if not roll_no_entry.get():
        messagebox.showwarning("Input Error", "Enter Roll No to delete!")
        return
    delete_student(int(roll_no_entry.get()))
    clear_entries()
    refresh_list()

def clear_entries():
    roll_no_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def refresh_list():
    student_list.delete(*student_list.get_children())
    for row in view_students():
        student_list.insert("", tk.END, values=row)

# ---------------- Main Window ----------------
connect_db()
root = tk.Tk()
root.title("🎓 Student Management System (GUI + SQLite)")
root.geometry("600x400")
root.configure(bg="#f5f6fa")

# Frame for inputs
input_frame = tk.Frame(root, bg="#dcdde1", padx=10, pady=10)
input_frame.pack(fill="x", pady=5)

tk.Label(input_frame, text="Roll No", bg="#dcdde1", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Label(input_frame, text="Name", bg="#dcdde1", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
tk.Label(input_frame, text="Course", bg="#dcdde1", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
tk.Label(input_frame, text="Marks", bg="#dcdde1", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)

roll_no_entry = tk.Entry(input_frame)
name_entry = tk.Entry(input_frame)
course_entry = tk.Entry(input_frame)
marks_entry = tk.Entry(input_frame)

roll_no_entry.grid(row=0, column=1, padx=5, pady=5)
name_entry.grid(row=1, column=1, padx=5, pady=5)
course_entry.grid(row=2, column=1, padx=5, pady=5)
marks_entry.grid(row=3, column=1, padx=5, pady=5)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f5f6fa")
button_frame.pack(fill="x", pady=5)

tk.Button(button_frame, text="➕ Add", command=add_student_gui, bg="#4cd137", fg="white", width=12).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="🔍 Search", command=search_student_gui, bg="#487eb0", fg="white", width=12).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="✏️ Update", command=update_student_gui, bg="#e1b12c", fg="white", width=12).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="🗑️ Delete", command=delete_student_gui, bg="#e84118", fg="white", width=12).grid(row=0, column=3, padx=5, pady=5)
tk.Button(button_frame, text="🧹 Clear", command=clear_entries, bg="#718093", fg="white", width=12).grid(row=0, column=4, padx=5, pady=5)

# Student List (Treeview instead of Listbox)
list_frame = tk.Frame(root, bg="#f5f6fa")
list_frame.pack(fill="both", expand=True, pady=10)

columns = ("roll_no", "name", "course", "marks")
student_list = ttk.Treeview(list_frame, columns=columns, show="headings")

for col in columns:
    student_list.heading(col, text=col.capitalize())
    student_list.column(col, width=100)

student_list.pack(fill="both", expand=True)

# Add scrollbar
scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=student_list.yview)
student_list.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

refresh_list()
root.mainloop()
