from typing import List

import numpy as np

from space_radar.algorithms.detectionstrategy import Detection
from space_radar.algorithms.detectionstrategy import DetectionStrategy
from space_radar.logutils import LogMixin


class EdgeDetectionStrategy(DetectionStrategy, LogMixin):
    """
    This is the EdgeDetection Algorithm.
    It is very similar to the simple detection algorithm, excel that it tries to find aliens partially visible (i.e.
    partially outside of radar sample edges.
    It accepts a "min_edge_overlapping" parameter, which defines minimum evaluated overlapping. This is needed to limit
    false-positives near edges.
    """

    def __init__(self, detection_threshold: float, min_edge_overlapping: int):
        if detection_threshold > 1 or detection_threshold <= 0:
            raise ValueError("Invalid detection threshold provided %s" % detection_threshold)

        if min_edge_overlapping < 1:
            raise ValueError("Minimum Edge overlapping should be > 0 - %s provided" % min_edge_overlapping)

        self.threshold = detection_threshold
        self.min_edge_overlapping = min_edge_overlapping
        self.logger.info("Initialised EdgeDetectionStrategy with threshold: %s - min_edge_overlapping: %s",
                         detection_threshold, min_edge_overlapping)

    def __str__(self):
        return "{cname}(threshold={threshold}, min_edge_overlapping={min_edge_overlapping})".format(
            cname=self.__class__.__name__,
            threshold=self.threshold,
            min_edge_overlapping=self.min_edge_overlapping
        )

    def detect(self, footprints: List[np.matrix], radar_sample: np.matrix):
        if radar_sample.ndim != 2:
            raise ValueError("You have a non 2D observation")
        if not footprints:
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

        overlap = self.min_edge_overlapping

        for start_x in range(-footprint.shape[0] + overlap,
                             radar_sample.shape[0] - footprint.shape[0] + overlap):

            for start_y in range(-footprint.shape[1] + overlap,
                                 radar_sample.shape[1] - footprint.shape[1] + overlap):
                observation_slice = radar_sample[
                                    max(start_x, 0):min(footprint.shape[0] + start_x, radar_sample.shape[0]),
                                    max(start_y, 0):min(footprint.shape[1] + start_y, radar_sample.shape[1])]

                footprint_slice = footprint[
                                  max(0, -start_x):min(radar_sample.shape[0] - start_x, footprint.shape[0]),
                                  max(0, -start_y):min(radar_sample.shape[1] - start_y, footprint.shape[1])]

                if not footprint_slice.shape == observation_slice.shape:
                    raise RuntimeError("algorithm error - wrong boundary")

                assert footprint_slice.shape == observation_slice.shape

                matching = (observation_slice == footprint_slice).sum() / footprint_slice.size
                if matching >= self.threshold:
                    # score != matching since this is evaluated over the entire footprint, not just the overlapping part
                    score = (observation_slice == footprint_slice).sum() / footprint.size
                    d = Detection(
                        x=max(0, start_x),
                        y=max(0, start_y),
                        score=score,
                        footprint=footprint_slice)
                    self.logger.debug("Detected alien at (%s, %s) with score: %s", d.x, d.y, d.score)
                    matches.append(d)

        return matches
