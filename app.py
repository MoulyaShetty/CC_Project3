from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'ccproj.cmvks4aqjsy6.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'ccproj1234'
app.config['MYSQL_DB'] = 'todo'
mysql = MySQL(app)

# Read operation (display all tasks)
@app.route('/')
def tasks():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), due_date DATE)''')
    mysql.connection.commit()
    cur.execute('''SELECT * FROM tasks ORDER BY due_date ASC''')
    tasks = cur.fetchall()
    cur.close()
    return render_template('tasks.html', tasks=tasks)

# Create operation (add a new task)
@app.route('/add', methods=['POST'])
def add_task():
    name = request.form['name']
    due_date = request.form['due_date']
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO tasks (name, due_date) VALUES (%s, %s)''', (name, due_date))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

# Update operation (edit an existing task)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM tasks WHERE id=%s''', (id,))
    task = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        name = request.form['name']
        due_date = request.form['due_date']
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE tasks SET name=%s, due_date=%s WHERE id=%s''', (name, due_date, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('edit.html', task=task)

# Delete operation (remove an existing task)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM tasks WHERE id=%s''', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
