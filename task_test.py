from unittest import TestCase
from task import TodoTask


class TodoTaskTest(TestCase):
    def test_can_be_created_from_dict(self):
        task_dict = {"id": 1, "text": "Write tests", "completed": False}
        todo = TodoTask.from_dict(task_dict)

        self.assertEqual(todo.id, 1)
        self.assertEqual(todo.text, "Write tests")
        self.assertFalse(todo.completed)

    def test_can_turn_itself_into_a_dict(self):
        todo = TodoTask("Write tests", lambda: 1)
        expected_dict = {"id": 1, "text": todo.text, "completed": todo.completed}

        self.assertDictEqual(todo.to_dict(), expected_dict)
        self.assertEqual(TodoTask.from_dict(todo.to_dict()), todo)

    def test_has_a_positive_integer_id(self):
        todo = TodoTask("Write tests", lambda: 1)

        self.assertGreaterEqual(todo.id, 1)

    def test_knows_if_it_is_equal_to_another_task(self):
        original = TodoTask("Original", lambda: 1)
        copy = TodoTask.from_dict(original.to_dict())
        other = TodoTask("Unrelated task", lambda: 2)

        self.assertEqual(original, copy)
        self.assertNotEqual(original, other)

    def test_comparable_on_id(self):
        first = TodoTask("Write test", lambda: 1)
        second = TodoTask("Ensure that test fails", lambda: 2)
        third = TodoTask("Write just enough code to make the past pass", lambda: 3)

        self.assertLess(first, second)
        self.assertLess(second, third)

    def test_must_have_title_text(self):
        with self.assertRaises(ValueError):
            TodoTask(None, lambda: 1)

    def test_remembers_the_title_text(self):
        todo_text = "Write tests"
        todo = TodoTask(todo_text, lambda: 1)

        self.assertEqual(todo.text, todo_text)

    def test_a_new_task_is_not_completed(self):
        todo = TodoTask("Write tests", lambda: 1)

        self.assertFalse(todo.completed)

    def test_a_task_can_be_marked_as_completed(self):
        todo = TodoTask("Write tests", lambda: 1)
        todo.toggle_completed()

        self.assertTrue(todo.completed)

    def test_converts_to_formatted_string(self):
        todo_string = str(TodoTask("Write tests", lambda: 1))

        self.assertEqual(todo_string, "#1 Write tests")
