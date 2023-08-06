import time
from scinode.core.executor import Executor


def test_float(t=0, value=0.0):
    """Float node."""
    time.sleep(t)
    return value


def test_string(t=0, value=""):
    """String node."""
    time.sleep(t)
    return value


def test_enum(t=0, value=""):
    """Enum node."""
    time.sleep(t)
    return value


def test_add(t=0, x=0, y=0):
    """Add node."""
    time.sleep(t)
    return x + y


def test_minus(t=0, x=0, y=0):
    """Minus node."""
    time.sleep(t)
    return x - y


def test_power(t=0, x=0, y=0):
    """Power node."""
    from math import pow

    time.sleep(t)
    return pow(x, y)


def test_greater(t=0, x=0, y=0):
    """Greater than node"""
    time.sleep(t)
    return x > y


def test_less(t=0, x=0, y=0):
    """Less than node"""
    time.sleep(t)
    return x < y


def test_sqrt(t=0, x=1):
    """sqrt node"""
    from math import sqrt

    time.sleep(t)
    return sqrt(x)


def test_range(start=0, stop=5, step=1):
    """Range node"""
    return list(range(start, stop, step))


class TestWriteFile(Executor):
    """Test write a file to a path.

    Args:
        Executor (_type_): _description_
    """

    def run(self):
        """"""
        import os

        print("    TestWriteFile job")
        workdir = os.path.join(
            self.worker_workdir,
            self.kwargs["directory"],
        )
        if not os.path.exists(workdir):
            os.mkdir(workdir)
        filepath = os.path.join(
            workdir,
            self.kwargs["filename"],
        )
        with open(filepath, "w") as f:
            f.write(self.kwargs["content"])
        return (filepath,)


class Person:
    name = "Bob"
    age = 5

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def run(self):
        return self

    def __repr__(self) -> str:
        s = "Person(name={}, age={})".format(self.name, self.age)
        return s


def person(name, age):
    return Person(name, age)
