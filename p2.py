import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

# Initialize main window
my_w = tk.Tk()
my_w.title("SQLite Database Connector")
my_w.geometry("600x600")

connection = None

def toggle_connection():
    global connection
    if connection is None:
        connect_database()
    else:
        disconnect_database()

def connect_database():
    global connection, db_path_label, tables_frame
    db_file = filedialog.askopenfilename(title="Select SQLite Database File", filetypes=[("SQLite Database", "*.sqlite *.db")])
    if db_file:
        try:
            connection = sqlite3.connect(db_file)
            db_path_label.config(text=db_file, fg="green")
            connect_button.config(text="Disconnect")
            show_tables()
        except sqlite3.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the database.\nError: {e}")

def disconnect_database():
    global connection, db_path_label, tables_frame
    if connection:
        connection.close()
        connection = None
        db_path_label.config(text="Not connected", fg="red")
        connect_button.config(text="Connect to SQLite Database")
        for widget in tables_frame.winfo_children():
            widget.destroy()

def show_tables():
    global connection, tables_frame
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for widget in tables_frame.winfo_children():
                widget.destroy()

            # Add headers
            header_name = tk.Label(tables_frame, text="Table Name", font=('times', 12, 'bold'), borderwidth=2, relief='groove', padx=10, pady=5)
            header_count = tk.Label(tables_frame, text="Number of Records", font=('times', 12, 'bold'), borderwidth=2, relief='groove', padx=10, pady=5)
            header_name.grid(row=0, column=0, sticky='nsew')
            header_count.grid(row=0, column=1, sticky='nsew')

            # Add table names and record counts
            for idx, table in enumerate(tables):
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                record_count = cursor.fetchone()[0]
                label_name = tk.Label(tables_frame, text=table_name, font=('times', 12), borderwidth=2, relief='groove', padx=10, pady=5)
                label_count = tk.Label(tables_frame, text=record_count, font=('times', 12), borderwidth=2, relief='groove', padx=10, pady=5)
                label_name.grid(row=idx + 1, column=0, sticky='nsew')
                label_count.grid(row=idx + 1, column=1, sticky='nsew')
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to retrieve tables.\nError: {e}")

# Button to connect/disconnect to SQLite database
connect_button = tk.Button(my_w, text="Connect to SQLite Database", command=toggle_connection, font=('times', 18, 'bold'))
connect_button.grid(row=1, column=1, pady=10, padx=10)

# Label to show database path
db_path_label = tk.Label(my_w, text="Not connected", font=('times', 14, 'bold'), fg="red")
db_path_label.grid(row=2, column=1, pady=5, columnspan=2, padx=10)

# Frame to display tables in the database
tables_frame = tk.Frame(my_w)
tables_frame.grid(row=3, column=1, pady=10, padx=10, columnspan=2, sticky='nsew')

my_w.mainloop()
