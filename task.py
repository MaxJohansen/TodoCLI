class TodoTask:
    def __init__(self, text, id_generator):
        if not text or not isinstance(text, str):
            raise ValueError("Cannot create empty task")
        self.id = id_generator()
        self.text = text
        self.completed = False

    def toggle_completed(self):
        self.completed = not self.completed

    def __str__(self):
        return "#{task.id} {task.text}".format(task=self)

    @classmethod
    def from_dict(cls, dictionary):
        self = cls.__new__(cls)
        default_dict = {"id": -1, "text": "Invalid task", "completed": False}
        self.__dict__ = {**default_dict, **dictionary.copy()}
        return self

    def to_dict(self):
        return self.__dict__

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __lt__(self, other):
        return self.id < other.id
