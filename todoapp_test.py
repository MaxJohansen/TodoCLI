from unittest import TestCase
from todoapp import ConsoleApp
from persistence import Persistence


class MockPersistence(Persistence):
    def __init__(self, data):
        self.data = data
        self.stored = []

    def store(self, data):
        self.data.clear()
        self.data.update(data)
        self.stored.append(data.copy())

    def load(self):
        return self.data


class ConsoleAppTest(TestCase):
    def setUp(self):
        self.outputs = []
        self.inputs = []

        def outputter(format, *args):
            self.outputs.append(format % args)

        def inputter(args):
            if self.inputs:
                return self.inputs.pop(0)
            return "quit"

        self.data = {}
        self.persistence = MockPersistence(self.data)
        self.app = lambda: ConsoleApp(self.persistence, outputter, inputter)

    def test_adds_tasks_and_persists(self):
        self.inputs = ["print", "add Write integration tests", "print"]
        expected_outputs = [
            "No notes",
            "#1 Write integration tests",
            "#1 Write integration tests",
        ]

        self.assertEqual(0, len(self.data))

        self.app().run_loop()

        self.assertEqual(1, len(self.data))
        self.assertEqual(expected_outputs, self.outputs)

    def test_completes_task(self):
        self.data.update({"2": {"id": 2, "text": "First", "completed": False}})
        self.inputs = ["print", "do 2", "print"]
        expected_outputs = ["#2 First", "Completed #2 First", "No notes"]

        self.assertEqual(1, len(self.data))

        self.app().run_loop()

        self.assertEqual(0, len(self.data))
        self.assertEqual(expected_outputs, self.outputs)

    def test_loads_tasks_and_adds_new_tasks_with_unique_ids(self):
        self.data.update({"2": {"id": 2, "text": "First", "completed": False}})
        self.inputs = ["print", "add Write integration tests", "print"]
        expected_outputs = [
            "#2 First",
            "#3 Write integration tests",
            "#2 First\n#3 Write integration tests",
        ]

        self.app().run_loop()

        self.assertEqual(2, len(self.data))
        self.assertEqual(expected_outputs, self.outputs)

    def test_has_sensible_error_messages(self):
        self.inputs = ["prant", "add", "do #7"]
        expected_outputs = [
            "Unknown command",
            "Missing description for task",
            "Cannot find task #7",
        ]

        self.app().run_loop()

        self.assertEqual(expected_outputs, self.outputs)
