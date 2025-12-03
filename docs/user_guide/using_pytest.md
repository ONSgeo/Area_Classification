# Using pytest

[`pytest`][pytest] has been used to create some of the python-based testing in this repo. Pytest is the most commonly used python module for testing python code. Testing code is vital for following coding best practices and has numerous benefits such as:

* Assisting with debug code
* Helping developers write more efficient code first time
* Encouraging thoughtful consideration of what the code is doing as it is written
* Providing documentation for increased clarity
* Supporting smooth code deployment.

## Structure

There is a `tests` folder in the root directory of this repository containing all the tests relate to this pipeline. The tests are there for contributors to use, so will be available to contributors when cloning the whole repository.

## Writing pytests

All test files and tests must either start with `test_` or finish with `_test.py` for pytest to find them. 


## Running pytest
### In the terminal

There are a few ways to run pytests in the terminal. The easiest is by running
```shell
pytest
```
in the root directory. This will find any existing pytests within the directory and run them.

To run pytests in a specific pytest file run
```shell
pytest tests/test_example_module.py
```

Both of these methods can be tried in the root directory of a new repository.


[pytest]: https://pypi.org/project/pytest/
