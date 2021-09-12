#!/usr/bin/env python3.8
from abc import ABC
from typing import List, Generator

import numpy as np

from space_radar.algorithms.detectionstrategy import DetectionStrategy, Detection


class RadarSampleCruncher:
    def __init__(self,
                 detection_algorithm: DetectionStrategy,
                 footprints: List[np.matrix]):
        self.detection_algorithm = detection_algorithm
        self.footprints = footprints

    def find_aliens(self, radar_sample) -> List[Detection]:
        return self.detection_algorithm.detect(self.footprints, radar_sample)


