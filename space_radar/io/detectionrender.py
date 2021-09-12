from typing import List

import numpy as np

from space_radar.algorithms.detectionstrategy import Detection


class DetectionsTextRenderer:
    @staticmethod
    def render(x: int, y: int, detections: List[Detection]) -> None:
        render = np.full((x, y), '.')

        # inplace sorting - this should improve rendering of most-likely detecions in case of overlaps
        detections.sort(key=lambda d: d.score)

        for d in detections:
            obj_width = d.footprint.shape[0]
            object_height = d.footprint.shape[1]
            footprint = d.footprint.astype(str)
            footprint[footprint == 'True'] = 'o'
            footprint[footprint == 'False'] = '-'

            render[max(d.x, 0):min(d.x + obj_width, y), max(d.y, 0):min(d.y + object_height, y)] = footprint

        DetectionsTextRenderer._print_string_matrix(render)

    @staticmethod
    def _print_string_matrix(matrix: np.ndarray) -> None:
        print("#" * matrix.shape[1])
        print('\n'.join([''.join(row) for row in matrix]))
        print("#" * matrix.shape[1])
