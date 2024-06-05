import unittest
import sys

sys.path.insert(0, 'applications/flight/lib')
sys.path.insert(1, 'applications/flight/lib/radio_utils')

from radio_utils.transmission_queue import transmission_queue as tq  # noqa: E402

class Test(unittest.TestCase):

    def test(self):
        for i in range(tq.limit):
            tq.push(i)
        self.assertRaises(Exception, tq.push, 101)
        self.assertEqual(tq.limit - 1, tq.pop())
        self.assertEqual(99, len(tq.queue))
        tq.clear()
