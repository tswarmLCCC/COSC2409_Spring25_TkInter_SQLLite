import sqlite3

connection = None
db_file_path = './my_db.db'

def toggle_connection():
    global connection
    if connection is None:
        connect_database()
    else:
        disconnect_database()

def connect_database():
    global connection, db_file_path
    try:
        connection = sqlite3.connect(db_file_path)
        show_tables()
    except sqlite3.Error as e:
        print("Connection Error", f"Failed to connect to the database.\nError: {e}")

def disconnect_database():
    global connection
    if connection:
        connection.close()
        connection = None


def show_tables():
    global connection
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            

            # Add table names and record counts
            for idx, table in enumerate(tables):
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                record_count = cursor.fetchone()[0]

                print(table_name, record_count)

        except sqlite3.Error as e:
            print("Error", f"Failed to retrieve tables.\nError: {e}")


def show_students_column(colNum):
    global connection
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM student")
            students_cursor = cursor.fetchall()
            for idx, studentRow in enumerate(students_cursor):
                firstCol = studentRow[colNum]
                print(firstCol)
        except sqlite3.Error as e:
            print("Error", f"Failed to retrieve tables.\nError: {e}")

connect_database()
show_students_column(2)