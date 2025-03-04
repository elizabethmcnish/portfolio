import numpy as np


class santas_lights:
    """
    New class for santas lights grid, with properties below. When initated, a NumPy array is created.

    Each item in the array represents one light in the grid.

    All lights are off to start with, taking the value "0". When lights are turned on, the value is changed to "1".
    """

    def __init__(self, no_of_rows, no_of_cols):
        self.no_of_rows = no_of_rows
        self.no_of_cols = no_of_cols
        self.two_d_array = np.zeros((self.no_of_rows, self.no_of_cols), dtype=int)

    def turn_on_off(self, new_start_light: tuple[int], new_stop_light: tuple[int], on=True):
        """

        This method is used to "turn on/off" a light in the grid of lights. In other words, this method will toggle
        an item in the NumPy array from 0 to 1 or vice versa, representing a light turning on / off.

        All lights that were previously on will remain on.

        """
        # Destructuring the coordinate tuples
        a, b = new_start_light
        c, d = new_stop_light

        assert 0 <= a <= self.no_of_rows, f"Row coordinate {a} out of range"
        assert 0 <= c <= self.no_of_rows, f"Row coordinate {c} out of range"

        assert 0 <= b <= self.no_of_cols, f"Column coordinate {b} out of range"
        assert 0 <= d <= self.no_of_cols, f"Column coordinate {d} out of range"

        if on is True:
            x = 1
        else:
            x = 0

        self.two_d_array[new_start_light[0] : new_stop_light[0] + 1, new_start_light[1] : new_stop_light[1] + 1] = x

        no_lights_on = np.count_nonzero(self.two_d_array == 1)

        no_lights_off = np.count_nonzero(self.two_d_array == 0)

        print(
            f"Shape of new 'on' pattern: {(self.two_d_array[new_start_light[0]:new_stop_light[0],new_start_light[1]:new_stop_light[1]]).shape}"
        )

        print(f"Count no. of 'on' lights in grid {no_lights_on}")

        print(f"Count no. of 'off' lights in grid {no_lights_off}")
        return self.two_d_array

    def toggle(self, new_start_light: tuple[int], new_stop_light: tuple[int]):
        """
        If "0", change to "1"
        If "1", change to "0"

        """

        sliced_array = self.two_d_array[
            new_start_light[0] : new_stop_light[0] + 1, new_start_light[1] : new_stop_light[1] + 1
        ]

        # Toggling 1s and 0s using Logical Not operator
        array = ~sliced_array & 1

        no_lights_on = np.count_nonzero(array == 1)

        no_lights_off = np.count_nonzero(array == 0)

        print(f"Count no. of 'on' lights in grid {no_lights_on}")

        print(f"Count no. of 'off' lights in grid {no_lights_off}")

        return array
