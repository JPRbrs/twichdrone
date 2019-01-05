import pytest

from ..nonlinearinterp import NonLinearInterpolator


class TestInterpolator:

    TEST_CURVE = [[(0, 10), (0, 5)],
                  [(10, 20), (5, 15)],
                  [(20, 30), (15, 16)]]

    def test_create_interpolator_no_curve(self):
        with pytest.raises(Exception):
            NonLinearInterpolator()

    @pytest.mark.parametrize('in_value, range_index', [
        (0, 0),
        (2, 0),
        (10, 0),
        (20, 1),
        (30, 2),
    ])
    def test_find_range(self, in_value, range_index):
        nli = NonLinearInterpolator(self.TEST_CURVE)
        assert range_index == nli.find_range(in_value)
