from os import stat
import sqlite3
from flask import Flask, redirect, render_template, url_for, request, jsonify

app = Flask(__name__)

# 404 Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# DB Connection
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get ToDos Function
def getTodo():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("select * from todo")
   
    todos = cur.fetchall(); 
    return render_template("index.html",todos = todos)


# Routes & Request
@app.route('/')
@app.route('/home')
@app.route('/index')
def homepage():
    return getTodo()

@app.route('/index')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todo').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/addtodo', methods=['POST'])
def addtodo():
    #sql = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO todo(title, content, status) VALUES(?, ?, ?)',(title, content, 1))
        conn.commit()
        conn.close()
        return getTodo()
    else:
        return "Bad request method",400
            
@app.route('/deleteTodo/<int:id>', methods=['GET'])
def deletetodo(id):
    if request.method == 'GET':
        conn = get_db_connection()
        conn.execute('DELETE  FROM todo WHERE id=?',(id,))
        conn.commit()
        conn.close()
        return getTodo()
    else:
        return "Bad Request Method",400

@app.route('/updateStatus', methods=['POST'])
def updateStatus():
    if request.method == "POST":
        updateId = int(request.form['id'])
        status = int(request.form['status'])
        print(status)
        if status == 1:
            status = 0
            conn = get_db_connection()
            conn.execute('UPDATE todo SET status=? WHERE id=?',(status, updateId))
            conn.commit()
            conn.close()
            return getTodo()
        else:
            status = 1
            conn = get_db_connection()
            conn.execute('UPDATE todo SET status=? WHERE id=?',(status, updateId))
            conn.commit()
            conn.close()
            return getTodo()
    else:
        return "Bad request method",400
    
        

if __name__ == '__main__':
    app.run(debug=True)



