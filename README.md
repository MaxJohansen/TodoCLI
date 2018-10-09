# A simple console Todo application

The app is written in Python3 and has no dependencies outside of the standard library.

Run the program with `python todoapp.py` and verify that it meets all requirements.

## Running the automated tests

If you like pretty test output, I recommend `pytest` using the `pytest-spec` plugin.
Simply running `pytest` will find the tests and run them all.

If you just want to verify that the tests pass, you can run `python -m unittest *_test.py`

### Assumptions

- "Do 1" is equivalent to "Do #1"
- Creating duplicate tasks is allowed
