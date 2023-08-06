import unittest
import numpy as np
from pyfairsim.sim_algorithm.SIM_Utils import locate_peak

def get_outside_position(distance, shape):
    if distance/2 > np.sqrt(shape[0]**2 + shape[1]**2):  # there is no outside position
        return -1, -1
    return shape[1]//2, shape[0]//2  # choose the outermost position

class TestSIM_Utils(unittest.TestCase):
    
    image_shapes = [[512, 512], [512, 1024], [1024, 512], [2048, 2048], [401, 100]]

    def test_locate_peak(self):
        relative_distances = (0, 0.2, 0.9, 1)
        for image_shape in self.image_shapes:
            test_array = np.zeros(image_shape, dtype=complex)
            for relative_distance in relative_distances:
                min_distance = int(0.5 * relative_distance * np.sqrt(image_shape[0]**2 + image_shape[1]**2))
                self.assertEqual(locate_peak(test_array, min_distance), (-1, -1, 0., 0.))
                test_array_with_max = np.copy(test_array)
                x, y = get_outside_position(min_distance, image_shape)
                if x != -1:
                    test_array_with_max[y][x] = 3 + 4j
                    self.assertEqual(locate_peak(test_array_with_max, min_distance), (x, -y, 5, 0.9272952180016122))

                test_array_with_max_in_radius = np.copy(test_array)
                test_array_with_max_in_radius[0][0] = 1
                self.assertEqual(locate_peak(test_array, min_distance), (-1, -1, 0., 0.))

if __name__ == "__main__":
    unittest.main()