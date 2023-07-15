from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session


import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, "src", "templates")

app = Flask(__name__, template_folder=template_dir)


app.config["SESSION_TYPE"] = "filesystem"
PERMANENT_SESSION_LIFETIME = 1800

app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)

if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"
# Rutas de la app


@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    cursor = db.cnxn.cursor()
    email = request.form["email"]
    password = request.form["password"]
    sql = "SELECT * FROM login WHERE email = ?  AND password = ?"
    data = (email, password)
    cursor.execute(sql, data)
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
        session["email"] = email
        session["name"] = user[1]
        session["surname"] = user[2]

        return redirect(url_for("index"))
    else:
        return render_template(
            "login.html", message="Las credenciales no son correctas"
        )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route("/index", methods=["GET"])
def index():
    email = session["email"]
    cursor = db.cnxn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", [email])
    index = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in index:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("index.html", data=insertObject)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/new-user", methods=["GET", "POST"])
def newUser():
    name = request.form["name"]
    surname = request.form["surname"]
    email = request.form["email"]
    password = request.form["password"]

    if name and surname and email and password:
        cursor = db.cnxn.cursor()
        sql = "INSERT INTO login (name, surname, email, password) values (?,?,?,?)"
        data = (name, surname, email, password)
        cursor.execute(sql, data)
        db.cnxn.commit()
    return redirect(url_for("home"))


# Guarda usarios en la base de datos


@app.route("/user", methods=["POST"])
def addUser():
    username = request.form["username"]
    name = request.form["name"]
    password = request.form["password"]
    email = session["email"]

    if username and name and password and email:
        cursor = db.cnxn.cursor()
        sql = "INSERT INTO  users (email,username, name, password) VALUES (?,?,?,?)"
        data = (email, username, name, password)
        cursor.execute(sql, data)
        db.cnxn.commit()
    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def delete(id):
    cursor = db.cnxn.cursor()
    sql = "DELETE FROM  users WHERE id=?"
    data = id
    cursor.execute(sql, data)
    db.cnxn.commit()
    return redirect(url_for("index"))


@app.route("/edit/<string:id>", methods=["POST"])
def edit(id):
    username = request.form["username"]
    name = request.form["name"]
    password = request.form["password"]

    if username and name and password:
        cursor = db.cnxn.cursor()
        sql = "UPDATE  users  SET username=?, name=?, password=? WHERE id=?"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.cnxn.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=4000)
