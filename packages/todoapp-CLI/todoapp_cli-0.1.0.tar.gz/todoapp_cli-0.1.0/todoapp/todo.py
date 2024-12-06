# todoapp/todo.py

import os
import json

class TodoApp:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append({'task': task, 'done': False})
        self.save_tasks()

    def list_tasks(self, show_completed=False):
        if not self.tasks:
            print("No tasks found!")
            return

        filtered_tasks = [task for task in self.tasks if task['done'] == show_completed]

        if not filtered_tasks:
            print("No tasks to display!")
        else:
            status = "✓" if show_completed else "✗"
            print("\nYour Tasks:")
            for idx, task in enumerate(filtered_tasks):
                print(f"{idx + 1}. {task['task']} [{status}]")

    def mark_done(self, task_number):
        if task_number <= 0 or task_number > len(self.tasks):
            print("Invalid task number!")
        else:
            self.tasks[task_number - 1]['done'] = True
            self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)

def display_menu():
    print("\n=== To-Do List CLI ===")
    print("Commands:")
    print("Press Enter to add a new task")
    print("Press 'S' to show tasks")
    print("Press 'C' to show completed tasks")
    print("Press 'I' to show incompleted tasks")
    print("Press 'M' to mark a task as completed")
    print("Press 'E' to exit")

def main():
    app = TodoApp()
    print("Welcome to your To-Do List CLI App!")

    while True:
        user_input = input().strip().upper()

        if user_input == "HELP":
            display_menu()
        elif user_input == "":
            task = input("Enter the task: ")
            app.add_task(task)
        elif user_input == "S":
            app.list_tasks()
        elif user_input == "C":
            app.list_tasks(show_completed=True)
        elif user_input == "I":
            app.list_tasks(show_completed=False)
        elif user_input == "M":
            try:
                task_number = int(input("Enter the task number to mark as done: "))
                app.mark_done(task_number)
            except ValueError:
                print("Please enter a valid number.")
        elif user_input == "E":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Type 'HELP' for a list of commands.")

if __name__ == "__main__":
    main()
