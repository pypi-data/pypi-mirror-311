# Standard Library Imports
import unittest

# External Imports
import numpy as np

# Local Imports
from pepitatools.imageops import _get_bit_depth


class TestBitDepth(unittest.TestCase):
    def test_get_bit_depth(self):
        self.assertTupleEqual(
            _get_bit_depth(np.array([1, 2, 3, 4, 5])), (np.uint8, 255)
        )
        self.assertTupleEqual(
            _get_bit_depth(np.array([1, 2, 3, 4, 255])), (np.uint8, 255)
        )
        self.assertTupleEqual(
            _get_bit_depth(np.array([1, 2, 3, 4, 256])), (np.uint16, 65_535)
        )
        self.assertTupleEqual(
            _get_bit_depth(np.array([1, 2, 3, 4, 65_536])), (np.int32, 2_147_483_647)
        )


if __name__ == "__main__":
    unittest.main()
