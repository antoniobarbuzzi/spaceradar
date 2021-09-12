from typing import List

import numpy as np

from space_radar.algorithms.detectionstrategy import Detection
from space_radar.algorithms.detectionstrategy import DetectionStrategy
from space_radar.logutils import LogMixin


class SimpleDetectionStrategy(DetectionStrategy, LogMixin):
    """
    This is a simple algorithm.
    For every location, it checks if there's an alien footprint matching a radar sample.
    If matching is > threshold, a detection is provided.
    Aliens partially outside of radar sample are ignored
    """

    def __init__(self, detection_threshold: float):
        if detection_threshold > 1 or detection_threshold <= 0:
            raise ValueError("Invalid detection threshold provided %s" % detection_threshold)

        self.threshold = detection_threshold
        self.logger.info("Initialised SimpleDetectionStrategy with threshold: %s", detection_threshold)

    def __str__(self):
        return "{cname}(threshold={threshold})".format(cname=self.__class__.__name__, threshold=self.threshold)

    def detect(self, footprints: List[np.matrix], radar_sample: np.matrix):
        if radar_sample.ndim != 2:
            raise ValueError("You have a non 2D observation")
        if footprints is None:
            raise ValueError("No footprint has been provided")

        detections = []
        for footprint in footprints:
            detections.extend(self._single_pattern_detection(radar_sample, footprint))

        return detections

    def _single_pattern_detection(self, radar_sample, footprint) -> List[Detection]:
        if radar_sample.ndim != 2:
            raise ValueError("You have a non 2D observation")
        if footprint.ndim != 2:
            raise ValueError("You have a non 2D object to detect")

        matches = []
        if any(diff <= -1 for diff in [x - y for x, y in zip(radar_sample.shape, footprint.shape)]):
            raise ValueError("Input array cannot be smaller than pattern in any dimension")

        for start_x in range(0, radar_sample.shape[0] - footprint.shape[1]):
            for start_y in range(0, radar_sample.shape[1] - footprint.shape[1]):
                observation_slice = radar_sample[start_x:footprint.shape[0] + start_x,
                                    start_y:footprint.shape[1] + start_y]
                matching = (observation_slice == footprint).sum() / footprint.size
                if matching >= self.threshold:
                    d = Detection(x=start_x, y=start_y, score=matching, footprint=footprint)
                    self.logger.debug("Detected %s", d)
                    matches.append(d)

        return matches
