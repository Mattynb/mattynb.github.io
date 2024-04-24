from flask import Flask, render_template, redirect, url_for, request
import datetime, time

app = Flask(__name__)

class Task:
    def __init__(self, name, deadline, duration):
        self.name = name
        self.deadline = deadline
        self.duration = duration
        self.completed = False
        self.start_time = None
        self.is_running = False
    
   
    def __repr__(self):
        return (f"{self.name} (Deadline: {self.deadline}, Remaining Duration: {self.duration:.2f}, "
                f"Completed: {self.completed})")

    def start_timer(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def stop_timer(self):
        if self.is_running:
            elapsed_time = (time.time() - self.start_time) / 60  # Convert seconds to minutes
            self.duration = max(0, self.duration - elapsed_time)  # Subtract elapsed time from duration
            self.is_running = False

    def remaining_time(self):
        if not self.start_time:
            return self.duration
        elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds() / 60
        return max(0, self.duration - elapsed_time)
    
    def current_duration(self):
        if self.is_running:
            elapsed_time = (time.time() - self.start_time) / 60  # Convert to minutes
            return max(0, self.duration - elapsed_time)
        return self.duration


# List of tasks
tasks = [
    Task("Task A", datetime.date(2024, 5, 1), 10),
    Task("Task B", datetime.date(2024, 4, 25), 5),
    Task("Task C", datetime.date(2024, 4, 30), 8),
    Task("Task D", datetime.date(2024, 5, 2), 3),
    Task("Task E", datetime.date(2024, 4, 25), 2)
]

@app.route('/', methods=['GET', 'POST'])
def index():
    # Filter out completed tasks and sort by deadline
    available_tasks = sorted([task for task in tasks if not task.completed], key=lambda x: (x.deadline, x.duration))
    next_task = available_tasks[0] if available_tasks else None
    return render_template('index.html', next_task=next_task, tasks=available_tasks)

@app.route('/complete/<task_name>', methods=['GET', 'POST'])
def complete_task(task_name):
    # Mark the task as completed
    for task in tasks:
        if task.name == task_name:
            task.completed = True
            break
    return redirect(url_for('index'))

# add route to add new task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        deadline = datetime.datetime.strptime(request.form['deadline'], '%Y-%m-%d').date()
        duration = int(request.form['duration'])
        tasks.append(Task(name, deadline, duration))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/start_timer/<task_name>', methods=['POST'])
def start_timer(task_name):
    for task in tasks:
        if task.name == task_name:
            task.start_timer()
            break
    return redirect(url_for('index'))

@app.route('/stop_timer/<task_name>', methods=['POST'])
def stop_timer(task_name):
    for task in tasks:
        if task.name == task_name:
            task.stop_timer()
            break
    return redirect(url_for('index'))

@app.route('/get_duration/<task_name>')
def get_duration(task_name):
    for task in tasks:
        if task.name == task_name:
            return {'duration': task.current_duration()}
    return {}, 404

@app.route('/script.js')
def get_js():
    return 

if __name__ == '__main__':
    app.run(debug=True)
