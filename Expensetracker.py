import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            amount REAL,
            date TEXT,
            category TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, date, category, description):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, date, category, description) VALUES (?, ?, ?, ?)", 
              (amount, date, category, description))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_category_summary():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = c.fetchall()
    conn.close()
    return rows

# --- Tkinter UI ---
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.description_var = tk.StringVar()
        
        # Entry Form
        tk.Label(root, text="Amount").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.amount_var).grid(row=0, column=1)
        
        tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.date_var).grid(row=1, column=1)
        
        tk.Label(root, text="Category").grid(row=2, column=0)
        self.category_dropdown = ttk.Combobox(root, textvariable=self.category_var, values=["Food", "Transport", "Utilities", "Entertainment"])
        self.category_dropdown.grid(row=2, column=1)
        
        tk.Label(root, text="Description").grid(row=3, column=0)
        tk.Entry(root, textvariable=self.description_var).grid(row=3, column=1)
        
        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="View Expenses", command=self.view_expenses).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Show Category Summary", command=self.show_category_summary).grid(row=6, column=0, columnspan=2)
    
    def add_expense(self):
        try:
            amount = float(self.amount_var.get())
            date = self.date_var.get()
            category = self.category_var.get()
            description = self.description_var.get()
            datetime.strptime(date, "%Y-%m-%d")  # Validate date format
            
            add_expense(amount, date, category, description)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_fields()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data.")
    
    def view_expenses(self):
        expenses = get_expenses()
        view_window = tk.Toplevel(self.root)
        view_window.title("Expense List")
        
        tree = ttk.Treeview(view_window, columns=("Amount", "Date", "Category", "Description"), show="headings")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        for expense in expenses:
            tree.insert("", "end", values=expense[1:])
        tree.pack()
    
    def show_category_summary(self):
        category_summary = get_category_summary()
        categories = [row[0] for row in category_summary]
        amounts = [row[1] for row in category_summary]
        
        plt.figure(figsize=(6,6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title("Expenses by Category")
        plt.show()

    def clear_fields(self):
        self.amount_var.set("")
        self.date_var.set("")
        self.category_var.set("")
        self.description_var.set("")

# Initialize database
init_db()

# Run Tkinter UI
root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()
