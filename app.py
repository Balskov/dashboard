from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import json
import os
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'Angles8-Wanting0-Swear6-Haven4'
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Brugerkonto (dummy)
brugernavn = "admin"
kode_hash = generate_password_hash("Hazily9-Hazing3-Gallon4-Barbell6")

# Todo-data
DATAFIL = "todos.json"
alle_lister = defaultdict(list)

def hent_todos():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r") as f:
            return json.load(f)
    else:
        with open(DATAFIL, "w") as f:
            json.dump({}, f)
        return {}

def gem_todos(todos):
    with open(DATAFIL, "w") as f:
        json.dump(todos, f)

# Kanban-data (dummy)
kanban_data = {
    "Backlog": [],
    "I gang": [],
    "Færdig": []
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        navn = request.form.get("brugernavn", "")
        kode = request.form.get("kode", "") 

        if navn == brugernavn and check_password_hash(kode_hash, kode):
            session["logget_ind"] = True
            return redirect(url_for("todo"))
        else:
            flash("Forkert brugernavn eller kode")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def index():
    return redirect(url_for("todo"))

@app.route("/todo", methods=["GET", "POST"])
def todo():
    if not session.get("logget_ind"):
        return redirect(url_for("login"))

    liste_navn = request.args.get("liste", "privat")
    data = hent_todos()
    todos = data.get(liste_navn, [])

    if liste_navn not in alle_lister:
        alle_lister[liste_navn] = []

    if request.method == "POST":
        if "opgave" in request.form:
            opgave_tekst = request.form.get("opgave")
            if opgave_tekst:
                todos.append({
                    "id": str(uuid.uuid4()),
                    "tekst": opgave_tekst
                })
        elif "slet_id" in request.form:
            slet_id = request.form.get("slet_id")
            todos = [t for t in todos if t["id"] != slet_id]

        data[liste_navn] = todos
        gem_todos(data)
        return redirect(url_for("todo", liste=liste_navn))

    return render_template(
        "todo.html",
        todos=todos,
        liste=liste_navn,
        alle_lister=data.keys(),
        aktiv="todo"
    )

@app.route("/kanban", methods=["GET", "POST"])
def kanban():
    if not session.get("logget_ind"):
        return redirect(url_for("login"))

    if request.method == "POST":
        kolonne = request.form["kolonne"]
        tekst = request.form["tekst"]
        kanban_data[kolonne].append({
            "id": str(uuid.uuid4()),
            "tekst": tekst
        })

    return render_template(
        "kanban.html",
        aktiv="kanban",
        kanban_data=kanban_data
    )

if __name__ == "__main__":
    app.run(debug=True)
