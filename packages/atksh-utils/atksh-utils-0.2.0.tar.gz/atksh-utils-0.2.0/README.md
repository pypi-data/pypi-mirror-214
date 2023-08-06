# atksh-utils

This is my collection of utilities.


## Development

To install this for development, run the following commands in your terminal:

```bash
python -m pip install -e '.[dev]'
pre-commit install
```

## OpenAI

```python
ai = OpenAI(key, "gpt-3.5-turbo-0613")

print(ai("Just answer the value of (5243 + 642) x (5314 - 4231) // 100"))
# The value of the expression (5243 + 642) x (5314 - 4231) // 100 is 7112.


def mul(a: int, b: int) -> int:
    """This is a multiplication function.

    :param a: An integer.
    :type a: int
    :param b: An integer.
    :type b: int
    :return: The sum of a and b.
    :rtype: int
    """
    return a * b


def add(a: int, b: int) -> int:
    """This is an addition function.

    :param a: An integer.
    :type a: int
    :param b: An integer.
    :type b: int
    :return: The sum of a and b.
    :rtype: int
    """
    return a + b


def sub(a: int, b: int) -> int:
    """This is a subtraction function.

    :param a: An integer.
    :type a: int
    :param b: An integer.
    :type b: int
    :return: The sum of a and b.
    :rtype: int
    """
    return a - b


def div(a: int, b: int) -> int:
    """This is a division function.

    :param a: An integer.
    :type a: int
    :param b: An integer.
    :type b: int
    :return: The sum of a and b.
    :rtype: int
    """
    return a // b


def exec_python_code(code: str) -> str:
    """This is a function that executes Python code and returns the stdout. Don't forget to print the result.

    :param code: A string of Python code.
    :type code: str
    :return: The result of the execution of the Python code (stdout by print)
    :rtype: str
    """
    import tempfile
    import subprocess
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
        f.write(code)
        f.flush()
        result = subprocess.check_output(["python", f.name])
    result = result.decode("utf-8").strip()
    if result == "":
        result = "NotPrintedError('The result is not printed.')"
    return result

ai.set_function(mul)
ai.set_function(add)
ai.set_function(sub)
ai.set_function(div)
ai.set_function(exec_python_code)

print(ai("Just answer the value of (5243 + 642) x (5314 - 4231) // 100"))
# The value of (5243 + 642) x (5314 - 4231) // 100 is 63734.
```
