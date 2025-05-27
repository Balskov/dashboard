from urllib import request
from flask import Flask, render_template, request, redirect, url_for
import uuid
import json
import os

DATAFIL = "todos.json"

def hent_todos():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r") as f:
            return json.load(f)
    else:
        # Opret en tom JSON-struktur
        tom_data = {}
        with open(DATAFIL, "w") as f:
            json.dump(tom_data, f)
        return tom_data

def gem_todos(todos):
    with open(DATAFIL, "w") as f:
        json.dump(todos, f)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index():
    liste_navn = request.args.get("liste", "privat")  # Standard er 'privat'
    data = hent_todos()
    todos = data.get(liste_navn, [])

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
        return redirect(url_for("index", liste=liste_navn))

    return render_template("index.html", todos=todos, liste=liste_navn, alle_lister=data.keys())

if __name__ == "__main__":
    app.run(debug=True)