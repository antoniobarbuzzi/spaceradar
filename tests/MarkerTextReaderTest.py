import os
import unittest

from space_radar.io.markerreader import MarkerTextReader
from space_radar.logutils import LogMixin


class MarkerTextReaderTest(unittest.TestCase, LogMixin):
    resource_path = os.path.dirname(os.path.realpath(__file__))
    sample_test_file = os.path.join(resource_path, "resources", "test_sample_file.txt")

    def test_read_file(self):
        expected_item_0 = """--o-----o--
---o---o---
--ooooooo--
-oo-ooo-oo-
ooooooooooo
o-ooooooo-o
o-o-----o-o
---oo-oo---
"""

        expected_item_1 = """---oo---
--oooo--
-oooooo-
oo-oo-oo
oooooooo
--o--o--
-o-oo-o-
o-o--o-o
"""
        reader = MarkerTextReader(MarkerTextReaderTest.sample_test_file)
        item = [item for item in reader.iter()]

        self.assertEquals(item[0], expected_item_0)
        self.assertEquals(item[1], expected_item_1)

