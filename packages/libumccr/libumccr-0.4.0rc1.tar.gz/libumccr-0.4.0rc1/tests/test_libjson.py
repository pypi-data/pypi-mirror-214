import logging
from datetime import datetime
from unittest import TestCase

from libumccr import libjson

# FIXME centralise test case logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LibJsonUnitTests(TestCase):

    def test_loads_str(self):
        """
        python -m unittest tests.test_libjson.LibJsonUnitTests.test_loads_str
        """
        json_str = """{"json": "this is json string"}"""
        self.assertIsInstance(json_str, str)
        result = libjson.loads(json_str)
        logger.info(result)
        self.assertIsInstance(result, dict)

    def test_loads_bytes(self):
        """
        python -m unittest tests.test_libjson.LibJsonUnitTests.test_loads_bytes
        """
        json_bytes = b'[{"sample":"SBJ123456","SNV8":0.079}]\n'
        self.assertIsInstance(json_bytes, bytes)
        result = libjson.loads(json_bytes)
        logger.info(result)
        self.assertIsInstance(result, list)

    def test_dumps_fallback(self):
        """
        python -m unittest tests.test_libjson.LibJsonUnitTests.test_dumps_fallback
        """
        result = libjson.dumps({
            'date': datetime.now(),
            'id': 1,
            'name': "Some string",
            'bool': True,
        })
        logger.info(result)
        self.assertIsInstance(result, str)


class LibJsonIntegrationTests(TestCase):
    pass
