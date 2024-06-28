"""The Image Queue is a max heap of filepaths to be transmitted.

Messages must support the `__lt__`, `__le__`, `__eq__`, `__ge__`, and `__gt__` operators.
This enables to the max heap to compare messages based on their priority.
"""
# from . import priority_queue as pq
from .priority_queue import PriorityQueue

image_queue = PriorityQueue([], 5)
