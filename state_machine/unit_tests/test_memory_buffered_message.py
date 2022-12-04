import unittest
import sys

sys.path.insert(0, './state_machine/applications/flight/lib/')

from radio_utils.memory_buffered_message import MemoryBufferedMessage
import radio_utils.headers as headers

packet_len = MemoryBufferedMessage.packet_len
data_len = MemoryBufferedMessage.data_len

class MemoryBufferedMessageTests(unittest.TestCase):

    def test_short_message(self):
        """Tests that a 1 packet message has the correct headers"""

        p = MemoryBufferedMessage(0, 'x' * data_len)
        res, _ = p.packet()
        self.assertEqual(res[0], headers.MEMORY_BUFFERED_END)
        p.ack()
        self.assertTrue(p.done())

    def test_medium_message(self):
        """Tests that a 2 packet message has the correct headers for each packet"""

        p = MemoryBufferedMessage(0, 'x' * (data_len + 1))
        res, _ = p.packet()
        self.assertEqual(res[0], headers.MEMORY_BUFFERED_START)
        p.ack()
        res, _ = p.packet()
        self.assertEqual(res[0], headers.MEMORY_BUFFERED_END)
        p.ack()
        self.assertTrue(p.done())

    def test_long_message(self):
        """Tests that a 3 packet message has the correct headers for each packet"""
        p = MemoryBufferedMessage(0, 'x' * (data_len * 2 + 1))

        res, _ = p.packet()
        self.assertEqual(res[0], headers.MEMORY_BUFFERED_START)
        self.assertEqual(len(res), packet_len)
        p.ack()

        res, _ = p.packet()
        self.assertEqual(len(res), packet_len)
        self.assertEqual(res[0], headers.MEMORY_BUFFERED_MID)
        p.ack()
        self.assertFalse(p.done())

        res, _ = p.packet()
        self.assertEqual(len(res), 4)  # 1 header + 1 data + 2 checksum
        self.assertEqual(res[0], headers.MEMORY_BUFFERED_END)
        p.ack()
        self.assertTrue(p.done())
