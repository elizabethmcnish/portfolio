# Unit tests for Christmas Kata project using PyTest module

from kata_projects.christmas_lights.client import santas_lights
import numpy as np


def test():
    # Initiate 4x4 NumPy array of zeros
    array = santas_lights(4, 4)

    # Test for turning lights on
    on_method_result = array.turn_on_off((0, 0), (2, 2), on=True)

    on_expected_result = np.array([[1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]])

    np.testing.assert_array_equal(on_method_result, on_expected_result)

    # Test for turning lights off
    off_method_result = array.turn_on_off((0, 2), (2, 2), on=False)

    off_expected_result = np.array([[1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]])

    np.testing.assert_array_equal(off_method_result, off_expected_result)

    # Test for toggling lights
    toggle_method_result = array.toggle((0, 0), (3, 3))

    toggle_expected_result = np.array([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 1, 1]])

    np.testing.assert_array_equal(toggle_method_result, toggle_expected_result)

    # return "Tests Passing!"
