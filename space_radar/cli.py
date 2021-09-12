#!/usr/bin/env python3.8

import logging.config
import os

from space_radar.algorithms.edgedetectionstrategy import EdgeDetectionStrategy
from space_radar.io.detectionrender import DetectionsTextRenderer
from space_radar.io.samplereader import FileSampleReader, TextToMatrixConverter
from space_radar.samplecruncher import RadarSampleCruncher


class Cli:
    @staticmethod
    def main():
        # TODO cli can accept sys.args params and be more modular
        Cli._configure_logging()

        converter = TextToMatrixConverter()
        file_sample_reader = FileSampleReader(converter)
        alien_footprints = list(file_sample_reader.load("samples/aliens.txt"))
        radar_samples = file_sample_reader.load("samples/radar-sample-1.txt")
        # detection_strategy = SimpleDetectionStrategy(0.8)
        detection_strategy = EdgeDetectionStrategy(0.8, 4)
        print("Crunching data")
        sample_cruncher = RadarSampleCruncher(detection_strategy, alien_footprints)
        print("Printing detected aliens")
        for sample in radar_samples:
            detected_aliens = sample_cruncher.find_aliens(sample)
            DetectionsTextRenderer.render(x=sample.shape[0],
                                          y=sample.shape[1],
                                          detections=detected_aliens)

    @staticmethod
    def _configure_logging():
        current_folder = os.path.dirname(os.path.abspath(__file__))
        logging_config = os.path.join(current_folder, "logging_config.ini")
        logging.config.fileConfig(logging_config)


def main():
    Cli.main()


if __name__ == '__main__':
    main()
