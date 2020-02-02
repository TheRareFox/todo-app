from flask import *
import sqlite3
import datetime
import os

def db_Init():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    try:
        cur.execute('CREATE TABLE Todo (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT NOT NULL,message text NOT NULL);')
        cur.commit()
    except:
        print("Table already exists")
    conn.close
    return True

def add_Todo(date,message):
    conn  = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Todo (date,message) VALUES (?,?)",(date,message))
    conn.commit()
    conn.close()
    return "Data added"
    


app = Flask(__name__)

@app.route('/')
def index():
    db_Init()
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Todo ORDER BY DATE ASC")
    todos = cur.fetchall()
    conn.close()
    suc = []
    fail = []
    print(datetime.datetime.now().strftime("%x"))
    
    for i in todos:
        a = i[1].split("-")
        date = datetime.datetime(int(a[0]),int(a[1]),int(a[2]))
        if date > datetime.datetime.now():
            suc.append(i)
        else:
            fail.append(i)
    
    return render_template("index.html", suc = suc, fail = fail)

@app.route("/addtodo")
def add():
    return render_template("create_todo.html")

@app.route("/submit")
def submit():
    date = request.args.get("date")
    message = request.args.get("message")
    add_Todo(date,message)
    return redirect("/")

@app.route("/<string:id>")
def todo(id):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Todo WHERE id = ?",id)
    todo = cur.fetchone()
    conn.close()
    a = todo[1].split("-")
    date = datetime.datetime(int(a[0]),int(a[1]),int(a[2]))
    due = False
    if date < datetime.datetime.now():
        due = True
    return render_template("todo.html",todo = todo, due = due)

@app.route("/done/<string:id>")
def done(id):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Todo WHERE id = ?",id)
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
