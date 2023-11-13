import sqlite3

# Make temp table if doesn't exist
def create_temp_table(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS temp_data
                (person_id INTEGER, cam_id INTEGER, datetime VARCHAR, floor INTEGER, 
                x_location INTEGER, y_location INTEGER, classification INTEGER)
                """)
    
    conn.commit()
    conn.close()


# Make history table if doesn't exist
def create_history_table(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS history_data
                (person_id INTEGER, cam_id INTEGER, datetime VARCHAR, floor INTEGER, 
                x_location INTEGER, y_location INTEGER, classification INTEGER)
                """)
    
    conn.commit()
    conn.close()


# Query the database and return all records
def show_all(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM temp_data")
    items = cur.fetchall()

    for item in items:
        print(item)

    conn.commit()
    conn.close()


# Add many data to the table
def add_many_temp(db_path, data_list):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executemany("INSERT INTO temp_data (person_id, cam_id, datetime, floor, x_location, y_location, classification)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?)", (data_list))

    conn.commit()
    conn.close()


def add_many_history(db_path, data_list):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executemany("INSERT INTO history_data (person_id, cam_id, datetime, floor, x_location, y_location, classification)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?)", (data_list))

    conn.commit()
    conn.close()


# Delete all data in temp_file
def delete_temp(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DELETE FROM temp_data")

    conn.commit()
    conn.close()