from unittest import IsolatedAsyncioTestCase
from universe import Universe

class EstablishContact(IsolatedAsyncioTestCase):

    async def test(self):
        universe = Universe()
        print('hi')
        universe.terminate()
        pass
