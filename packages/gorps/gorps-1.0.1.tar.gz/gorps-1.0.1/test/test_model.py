"""Unit tests for model module."""

import unittest

from gorps.model import Image


class TestImage(unittest.TestCase):
    """Tests for the image class."""

    def test_as_b64(self) -> None:
        self.assertEqual(
            Image(
                fmt="image/png",
                data=b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82",
            ).as_b64(),
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4//8/AAX+Av7czFnn"
            "AAAAAElFTkSuQmCC",
        )
