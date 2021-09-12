from typing import Iterator

import numpy as np

from space_radar.io.markerreader import MarkerTextReader
from space_radar.logutils import LogMixin



class TextToMatrixConverter(LogMixin):
    """
    Convert a textual text representation to a matrix
    """
    default_translate_map = {'o': True, '-': False}

    def __init__(self, translate_map=None):
        if not translate_map:
            translate_map = TextToMatrixConverter.default_translate_map
        self._translate_map = translate_map

    def convert(self, text):
        return np.matrix([[self._translate_map.get(ch) for ch in line] for line in text.splitlines()])


class FileSampleReader(LogMixin):
    """
    Read files
    """

    def __init__(self, text_converter: TextToMatrixConverter):
        self._text_converter = text_converter

    def load(self, filename: str) -> Iterator[np.matrix]:
        reader = MarkerTextReader(filename)
        for text in reader.iter():
            yield self._text_converter.convert(text)
