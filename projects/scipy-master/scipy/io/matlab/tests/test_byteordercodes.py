''' Tests for byteorder module '''

from __future__ import division, print_function, absolute_import

import sys

import scipy.io.matlab.byteordercodes as sibc
from numpy.testing import assert_raises, assert_, run_module_suite


def test_native():
    native_is_le = sys.byteorder == 'little'
    assert_(sibc.sys_is_le == native_is_le)


def test_to_numpy():
    if sys.byteorder == 'little':
        assert_(sibc.to_numpy_code('native') == '<')
        assert_(sibc.to_numpy_code('swapped') == '>')
    else:
        assert_(sibc.to_numpy_code('native') == '>')
        assert_(sibc.to_numpy_code('swapped') == '<')
    assert_(sibc.to_numpy_code('native') == sibc.to_numpy_code('='))
    assert_(sibc.to_numpy_code('big') == '>')
    for code in ('little', '<', 'l', 'L', 'le'):
        assert_(sibc.to_numpy_code(code) == '<')
    for code in ('big', '>', 'b', 'B', 'be'):
        assert_(sibc.to_numpy_code(code) == '>')
    assert_raises(ValueError, sibc.to_numpy_code, 'silly string')


if __name__ == "__main__":
    run_module_suite()
