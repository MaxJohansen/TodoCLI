from collections import defaultdict
from itertools import count

from task import TodoTask
from persistence import DiskPersistence


class ConsoleApp:
    def __init__(self, storage, outputter, inputter):
        self.storage = storage
        self.outputter = outputter
        self.inputter = inputter
        raw_tasks = self.storage.load() or {}
        self.tasks = {int(k): TodoTask.from_dict(v) for k, v in raw_tasks.items()}
        highest_id = max(self.tasks.keys(), default=0) + 1
        self.id_generator = count(highest_id).__next__
        self.commands = defaultdict(lambda: lambda x: outputter("Unknown command, type 'help' for a list of valid commands"))
        self.commands.update(
            {
                "add": self.add_task,
                "help": self.print_usage,
                "print": self.print_tasks,
                "do": self.complete_task,
                "quit": self.quit,
            }
        )

    @property
    def incomplete_tasks(self):
        return [t for t in self.tasks.values() if not t.completed]

    @property
    def serializable_tasks(self):
        return {t.id: t.to_dict() for t in self.incomplete_tasks}

    def print_tasks(self, args):
        tasks = "\n".join(str(t) for t in self.incomplete_tasks) or "No notes"
        self.outputter(tasks)

    def add_task(self, args):
        task_text = " ".join(args).strip('"')
        try:
            new_task = TodoTask(task_text, self.id_generator)
            self.outputter(str(new_task))
            self.tasks[new_task.id] = new_task
            self.storage.store(self.serializable_tasks)
        except ValueError:
            self.outputter("Missing description for task")

    def complete_task(self, args):
        id_number = int(args[0].strip("#"))
        if id_number not in self.tasks:
            self.outputter("Cannot find task #{}".format(id_number))
            return

        task = self.tasks[id_number]
        self.outputter("Completed {}".format(task))
        task.toggle_completed()
        self.storage.store(self.serializable_tasks)

    def quit(self, args):
        self.running = False

    def print_usage(self, args=None):
        self.outputter(
            """
    Add <text> - Add a new todo task
    Do #<id> - Complete the task with <id>
    Print - Print all pending tasks
    Quit - Exit the program
"""
        )

    def run_loop(self):
        self.print_usage()
        self.running = True
        while self.running:
            text = self.inputter("> ")
            if text:
                cmd, *args = text.split()
                self.commands[cmd.lower()](args)


if __name__ == "__main__":
    ConsoleApp(DiskPersistence("tasks.json"), print, input).run_loop()
