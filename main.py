from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="webpages")

tasks = []
habits = []

task_id_counter = 1
habit_id_counter = 1

@app.route("/")
def home():
    return render_template("index.html", tasks=tasks, habits=habits)

#new task
@app.route("/add_task", methods=["POST"])
def add_task():
    global task_id_counter
    title = request.form.get("title")
    if title:
        tasks.append({
            "id": task_id_counter,
            "title": title,
            "done": False
        })
        task_id_counter += 1
    return redirect(url_for("home"))

#check-off tasks
@app.route("/toggle_task/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("home"))

#reset tasks
@app.route("/reset_tasks",methods=["POST"])
def reset_tasks():
    global tasks
    tasks = []
    task_id_counter = 1
    return redirect(url_for("home"))

#new habit
@app.route("/add_habit", methods=["POST"])
def add_habit():
    global habit_id_counter
    name = request.form.get("name")
    if name:
        habits.append({
            "id": habit_id_counter,
            "name": name,
            "history": []
        })
        habit_id_counter += 1
    return redirect(url_for("home"))

#habit pages
@app.route("/habit/<int:habit_id>")
def habit_detail(habit_id):
    habit = next((h for h in habits if h["id"] == habit_id), None)
    if habit is None:
        return "Habit not found", 404
    return render_template("habit_detail.html", habit=habit)

#main programme
if __name__ == "__main__":
    app.run(debug=True)
