import sqlite3
import json

def insert_handler_data(handler_name, ip_address, hostname, location, username, port):
    # Connect to the database
    conn = sqlite3.connect('data.db')

    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()

    # Define an SQL query to insert the data into a table
    query = '''
            INSERT INTO handlers (handler_name, ip_address, hostname, location, username, port)
            VALUES (?, ?, ?, ?, ?, ?);
            '''

    # Execute the SQL query, passing in the data as parameters
    cursor.execute(query, (handler_name, ip_address, hostname, location, username, port))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()


def read_connections():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT handler_name FROM handlers')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[0])
    cursor.close()
    conn.close()
    return json.dumps(result)
    

def read_connection_data(handler_name):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ip_address, hostname, location, username, port FROM handlers WHERE handler_name=?', (handler_name,))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({'ip_address': row[0], 'hostname': row[1], 'location': row[2], 'username': row[3], 'port': row[4]})
    cursor.close()
    conn.close()
    return json.dumps(result)

def read_tasks(handler_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT taskid, handler_name, cmd, output, status FROM tasks WHERE handler_name = ?',(handler_name,))
    rows = c.fetchall()
    result = []
    for row in rows:
        result.append({'taskid': row[0], 'handler_name': row[1], 'cmd': row[2], 'output': row[3], 'status': row[4]})
    c.close()
    conn.close()
    return json.dumps(result)

def write_tasks(handler_name,cmd):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("INSERT INTO tasks (handler_name, cmd) VALUES (?, ?)", (handler_name, cmd))

    conn.commit()
    conn.close()

def get_task_c2(handler_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT taskid, handler_name, cmd, output, status FROM table WHERE handler_name = ? AND status != ? ORDER BY taskid ASC LIMIT 1',(handler_name,'pending'))
    row = c.fetchone()
    conn.close()
    return json.dumps({'taskid': row[0], 'handler_name': row[1], 'cmd': row[2], 'output': row[3], 'status': row[4]})

def update_task_c2(taskid,output):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Update the output for the given taskid
    c.execute("UPDATE tasks SET output = ?, status = 'done' WHERE taskid = ?", (output, taskid))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()