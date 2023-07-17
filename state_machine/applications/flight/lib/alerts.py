class BaseAlert:

    def __init__(self, name):
        self.name = name

    def set(self, value):
        self.state = value
