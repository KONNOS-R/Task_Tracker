from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime


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

    total_time_spent = 0

    x = [i["time_spent"] for i in habit["history"]]
    for i in x:
        hour, minute, second = i.split(":")
        total_time_spent += int(hour)*3600 + int(minute)*60 + int(second)

    if habit is None:
        return "Habit not found", 404
    return render_template("habit_detail.html", habit=habit, total_time_spent=format_time(total_time_spent))

#delete habits
@app.route("/delete_habit/<int:habit_id>", methods=["POST"])
def delete_habit(habit_id):
    global habits
    habits = [h for h in habits if h["id"] != habit_id]
    return redirect(url_for("home"))

#habit timer
@app.route("/save_session/<int:habit_id>", methods=["POST"])
def save_session(habit_id):
    #global habit
    habit = next((h for h in habits if h["id"] == habit_id), None)
    if habit:
        time_spent = int(request.form.get("time") or 0)
        habit["history"].append({
            "date":datetime.now().strftime("%Y-%m-%d"),
            "time_spent": format_time(time_spent)
        }
        )
        return redirect(url_for("habit_detail", habit_id = habit_id))
def format_time(sec):
    hrs = sec//3600
    mins = (sec %3600)// 60
    secs = (sec % 3600) % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

#main programme
if __name__ == "__main__":
    app.run(debug=True)
