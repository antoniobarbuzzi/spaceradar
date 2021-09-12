from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import numpy


@dataclass(frozen=True)
class Detection:
    x: int
    y: int
    score: int
    footprint: numpy.matrix


class DetectionStrategy(ABC):
    @abstractmethod
    def detect(self, footprints: List[numpy.matrix], sample: numpy.matrix) -> List[Detection]:
        pass
