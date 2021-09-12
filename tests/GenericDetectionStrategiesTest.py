import unittest

import numpy as np

from space_radar.algorithms.edgedetectionstrategy import EdgeDetectionStrategy
from space_radar.algorithms.simpledetectionstrategy import SimpleDetectionStrategy
from space_radar.logutils import LogMixin


class GenericDetectionStrategiesTest(unittest.TestCase, LogMixin):
    def test_run_subtests(self):
        simple_alg_08 = SimpleDetectionStrategy(0.8)
        simple_alg_10 = SimpleDetectionStrategy(1)
        edge_alg_08 = EdgeDetectionStrategy(0.8, 2)
        edge_alg_10 = EdgeDetectionStrategy(1, 2)

        all_tests = {
            self.subtest_fail_on_smaller_sample: {
                simple_alg_08: True,
                simple_alg_10: True,
                edge_alg_08: True,
                edge_alg_10: True
            },

            self.subtest_no_match_if_all_different: {
                simple_alg_08: True,
                simple_alg_10: True,
                edge_alg_08: True,
                edge_alg_10: True
            },

            self.subtest_find_match_with_no_noise: {
                simple_alg_08: True,
                simple_alg_10: True,
                edge_alg_08: True,
                edge_alg_10: False
            },

            self.subtest_find_match_with_0_1_noise: {
                simple_alg_08: True,
                simple_alg_10: False,
                edge_alg_08: True,
                edge_alg_10: False
            },

            self.subtest_edge_detection: {
                simple_alg_08: False,
                simple_alg_10: False,
                edge_alg_08: True,
                edge_alg_10: True
            }

        }

        for test_to_run, params in all_tests.items():
            for algorithm, should_succeed in params.items():
                test_name = test_to_run.__name__ + " --> (" + str(algorithm) + ")"
                if should_succeed:
                    with self.subTest(test_name):
                        test_to_run(algorithm)
                else:
                    self.logger.info("Skipping test %s - not suitable")

    def subtest_fail_on_smaller_sample(self, alg):
        test_footprint = np.matrix([
            [True, True, True],
            [True, True, True],
            [True, True, True]
        ])

        sample = np.matrix([
            [False, False],
            [False, False],
            [False, False]
        ])

        with self.assertRaises(ValueError):
            alg.detect(test_footprint, sample)

    def subtest_no_match_if_all_different(self, alg):
        test_footprint = np.matrix([
            [True, True, True],
            [True, True, True],
            [True, True, True]
        ])

        sample = np.matrix([
            [False, False, False],
            [False, False, False],
            [False, False, False]
        ])
        detections = alg.detect([test_footprint], sample)
        self.assertEmpty(detections)

    def subtest_find_match_with_no_noise(self, alg):
        return self.subtest_find_match_with_noise(alg, 0)

    def subtest_find_match_with_0_1_noise(self, alg):
        return self.subtest_find_match_with_noise(alg, 0.1)

    def subtest_find_match_with_noise(self, alg, noise_probability):
        # build random input/output
        expected_x = 3
        expected_y = 5
        test_footprint = np.random.choice(a=[True, False], size=(5, 4), p=[0.5, 0.5])
        sample = np.random.choice(a=[True, False], size=(10, 10), p=[0.5, 0.5])
        sample[3:3 + test_footprint.shape[0], 3:3 + test_footprint.shape[1]] = test_footprint

        noise = np.random.choice(a=[True, False], size=sample.shape, p=[noise_probability, 1 - noise_probability])

        sample = np.logical_or(sample, noise)

        # run test
        detections = alg.detect([test_footprint], sample)

        # verify
        self.assertNotEmpty(detections)
        detected_position = filter(lambda d: d.x == expected_x and d.y == expected_y, detections)
        self.assertNotEmpty(detected_position)

    def subtest_edge_detection(self, alg):
        test_footprint = np.matrix([
            [True, True, False],
            [True, True, False],
            [False, False, False]
        ])

        sample = np.matrix([
            [True, True, True],
            [True, True, True],
            [True, True, True]
        ])
        detections = alg.detect([test_footprint], sample)
        self.assertNotEmpty(detections)
        self.assertEquals(len(detections), 1)
        self.assertEquals((detections[0].x, detections[0].y), (1, 1))

    def assertEmpty(self, obj):
        self.assertFalse(obj)

    def assertNotEmpty(self, obj):
        self.assertTrue(obj)


if __name__ == '__main__':
    unittest.main()
