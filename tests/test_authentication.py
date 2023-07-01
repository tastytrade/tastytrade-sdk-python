from unittest import TestCase

from tastytrade_sdk.api import Unauthorized
from tests.utils import get_tasty


class Authentication(TestCase):
    def test_authentication(self):
        tasty = get_tasty()
        tasty.api.post('/sessions/validate')
        tasty.logout()
        with self.assertRaises(Unauthorized):
            tasty.api.post('/sessions/validate')
