"""Utilities for testing ADLStream2."""


from ADLStream2.data import BaseStreamGenerator


class FakeContext:
    """Fake ADLStream2 context for testing purposes."""

    def __init__(self):
        self.X = []
        self.y = []

    def set_time_out(self):
        pass

    def log(self, l, s):
        pass

    def add(self, x, y):
        if x is not None:
            self.X.append(x)
        if y is not None:
            self.y.append(y)


class SimpleTestGenerator(BaseStreamGenerator):
    """Simple ADLStream2 generator for testing purposes."""

    def preprocess(self, message):
        x = message
        return x, x
