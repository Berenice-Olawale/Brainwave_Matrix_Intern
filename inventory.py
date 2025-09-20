import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib

def init_db():
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, hash_password(password)))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()

def login_user(username, password):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    result = cursor.fetchone()
    connection.close()
    return result

def add_product(name, description, quantity, price):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products(name, description, quantity, price) VALUES (?, ?, ?, ?)", (name, description, quantity, price))
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    connection.close()
    return data

def edit_product(product_id, name, description, quantity, price):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE products
    SET name = ?, description = ?, quantity = ?, price = ?
    WHERE id = ?
    """, (name, description, quantity, price, product_id))
    connection.commit()
    connection.close()

def delete_product(product_id):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    connection.commit()
    connection.close()

def get_low_stock_products(threshold=5):
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < ?", (threshold,))
    data = cursor.fetchall()
    connection.close()
    return data

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.configure(bg="#2c3e50")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2c3e50')
        style.configure('TLabel', background='#2c3e50', foreground='#ecf0f1')
        style.configure('TEntry', fieldbackground='#34495e', foreground='#ecf0f1')
        style.configure('TButton', background='#34495e', foreground='#ecf0f1', borderwidth=0, focuscolor='#34495e')
        style.map('TButton', background=[('active', '#1abc9c')])

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Username").pack(pady=(0, 5))
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(pady=(0, 10))

        ttk.Label(main_frame, text="Password").pack(pady=(0, 5))
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(pady=(0, 10))

        ttk.Button(main_frame, text="Login", command=self.login).pack(pady=5, ipadx=10)
        ttk.Button(main_frame, text="Register", command=self.register).pack(pady=5, ipadx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login_user(username, password):
            self.root.destroy()
            Dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered!")
        else:
            messagebox.showerror("Error","Username already exists")


class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inventory Dashboard")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2c3e50')
        style.configure('TLabel', background='#2c3e50', foreground='#ecf0f1')
        style.configure('TEntry', fieldbackground='#34495e', foreground='#ecf0f1')
        style.configure('TButton', background='#34495e', foreground='#ecf0f1', borderwidth=0, focuscolor='#34495e')
        style.map('TButton', background=[('active', '#1abc9c')])
        style.configure('Treeview', background='#34495e', foreground='#ecf0f1', fieldbackground='#34495e',
                        borderwidth=0)
        style.configure('Treeview.Heading', background='#2c3e50', foreground='#ecf0f1')
        style.map('Treeview.Heading', background=[('active', '#1abc9c')])

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Product", command=self.open_add_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Low Stock Report", command=self.show_low_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh Data", command=self.refresh_data).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Description", "Quality", "Price"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, padx=10, pady=10)

        tk.Button(self.root, text="Edit Selected", command=self.edit_selected).pack(pady=5, ipadx=10)
        tk.Button(self.root, text="Delete Selected", command=self.delete_selected).pack(pady=5, ipadx=10)

        self.refresh_data()
        self.root.mainloop()

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = get_all_products()
        for product in products:
            self.tree.insert("", "end", values=product)

    def open_add_window(self):
        ProductForm(self, "Add Product")

    def edit_selected(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No product selected!")
            return

        product_data = self.tree.item(selected_item, 'values')
        ProductForm(self, "Edit Product", product_data)

    def delete_selected(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No product selected!")
            return

        product_id = self.tree.item(selected_item, 'values')[0]
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete product ID {product_id}?"):
            delete_product(product_id)
            self.refresh_data()
            messagebox.showinfo("Success", "Product deleted successfully.")

    def show_low_stock(self):
        low_stock_products = get_low_stock_products()

        report_window = tk.Toplevel(self.root)
        report_window.title("Low Stock Report")
        report_window.geometry("600x400")
        report_window.configure(bg="#2c3e50")

        tk.Label(report_window, text="Products with Low Stock (Quantity < 5)").pack(pady=10)

        tree = ttk.Treeview(report_window, columns=("ID", "Name", "Description", "Quantity", "Price"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Description", text="Description")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Price", text="Price")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for product in low_stock_products:
            tree.insert("", "end", values=product)


class ProductForm:
    def __init__(self, dashboard, title, product=None):
        self.dashboard = dashboard
        self.product = product
        self.form_window = tk.Toplevel(dashboard.root)
        self.form_window.title(title)
        self.form_window.geometry("400x300")
        self.form_window.configure(bg="#2c3e50")
        self.form_window.grab_set()

        form_frame = ttk.Frame(self.form_window, padding="15")
        form_frame.pack(expand=True)

        tk.Label(self.form_window, text="Name").pack(pady=(0, 5))
        self.name_entry = tk.Entry(self.form_window)
        self.name_entry.pack(pady=(0, 10))

        tk.Label(self.form_window, text="Description").pack(pady=(0, 5))
        self.description_entry = tk.Entry(self.form_window)
        self.description_entry.pack(pady=(0, 10))

        tk.Label(self.form_window, text="Quantity").pack(pady=(0, 5))
        self.quantity_entry = tk.Entry(self.form_window)
        self.quantity_entry.pack(pady=(0, 10))

        tk.Label(self.form_window, text="Price").pack(pady=(0, 5))
        self.price_entry = tk.Entry(self.form_window)
        self.price_entry.pack(pady=(0, 10))

        if self.product:
            self.name_entry.insert(0, self.product[1])
            self.description_entry.insert(0, self.product[2])
            self.quantity_entry.insert(0, self.product[3])
            self.price_entry.insert(0, self.product[4])

        tk.Button(self.form_window, text="Save", command=self.save).pack(pady=5, ipadx=10)
        tk.Button(self.form_window, text="Cancel", command=self.form_window.destroy).pack(pady=5, ipadx=10)

    def save(self):
        try:
            name = self.name_entry.get()
            description = self.description_entry.get()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())

            if not name or quantity < 0 or price < 0:
                messagebox.showerror("Invalid Input", "Name must be provided. Quantity and price cannot be negative.")
                return

            if self.product:
                product_id = self.product[0]
                edit_product(product_id, name, description, quantity, price)
                messagebox.showinfo("Success", "Product updated successfully.")
            else:
                add_product(name, description, quantity, price)
                messagebox.showinfo("Success", "Product added successfully.")

            self.dashboard.refresh_data()
            self.form_window.destroy()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for Quantity and Price.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = Login(root)
    root.mainloop()
