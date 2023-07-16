import sys
import unittest
from unittest import IsolatedAsyncioTestCase

sys.path.insert(0, './state_machine/drivers/emulation/lib')
sys.path.insert(0, './state_machine/drivers/emulation/')
sys.path.insert(0, './state_machine/applications/flight')
sys.path.insert(0, './state_machine/applications/flight/lib')
sys.path.insert(0, './state_machine/frame/')

import Tasks.radio as radio
from radio_driver import _Packet as Packet
import radio_utils.commands as cdh
from radio_utils.memory_buffered_message import MemoryBufferedMessage
from pycubed import cubesat
from state_machine import state_machine
from testutils import command_data
import settings

state_machine.state = 'Debug'
settings.TX_ALLOWED = True

# Make radio rx return instantly
cubesat.radio._rx_time_bias = 0.0
cubesat.radio._rx_time_dev = 0.0


class AssertCalled:

    def __init__(self, func):
        self.func = func
        self.called = False

    def command(self, s2, args=None):
        self.called = True
        if args is None:
            self.func(s2)
        else:
            self.func(s2, args)

class RXCommandTest(IsolatedAsyncioTestCase):

    async def test_basic(self):
        """Test that RX of a command with and without args works"""
        cubesat.radio.debug.reset()
        rt = radio.task()

        noop_packet = Packet(command_data(cdh.NO_OP, b''))
        cubesat.radio.debug.push_rx_queue(noop_packet)

        noop = AssertCalled(cdh.noop)
        cdh.commands[cdh.NO_OP]["function"] = noop.command

        await rt.main_task()
        self.assertEqual(noop.called, True, "No-op command was not called")

        query_packet = Packet(command_data(cdh.QUERY, b'5+5'))
        cubesat.radio.debug.push_rx_queue(query_packet)
        query = AssertCalled(cdh.query)
        cdh.commands[cdh.QUERY]["function"] = query.command

        await rt.main_task()
        self.assertEqual(noop.called, True, "Query command was not called")

class TestRxAndTx(IsolatedAsyncioTestCase):

    async def test_query(self):
        """Test that we can send and receive a query"""
        cubesat.radio.debug.reset()
        rt = radio.task()

        query_packet = Packet(command_data(cdh.QUERY, b'5+7'))
        cubesat.radio.debug.push_rx_queue(query_packet)

        for _ in range(3):
            await rt.main_task()

        expect = bytearray(b'\xfd12')
        self.assertEqual(cubesat.radio.debug.last_tx_packet, expect, "Got unexpected packet")


class MemBuffRXTest(IsolatedAsyncioTestCase):

    async def test(self):
        """Test that RX of a command with and without args works"""
        cubesat.radio.debug.reset()
        self.rt = radio.task()

        small_msg = "This is a small test message!"
        await self.rx_string(small_msg)
        await self.rx_string(small_msg * 100)

    async def rx_string(self, str):
        msg = MemoryBufferedMessage(bytearray(str, "ascii"))
        while not msg.done():
            pkt_data, _ = msg.packet()
            small_packet = Packet(pkt_data)
            cubesat.radio.debug.push_rx_queue(small_packet)
            await self.rt.main_task()
            msg.ack()
        self.assertEqual(self.rt.msg, str)


if __name__ == '__main__':
    unittest.main()
