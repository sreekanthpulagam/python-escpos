#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import escpos.printer as printer
from escpos.constants import BARCODE_TYPE_A, BARCODE_TYPE_B
from escpos.capabilities import Profile, BARCODE_B
from escpos.exceptions import BarcodeTypeError
import pytest


@pytest.mark.parametrize("bctype,data,expected", [
    ('EAN13', '4006381333931',
        b'\x1ba\x01\x1dh@\x1dw\x03\x1df\x00\x1dH\x02\x1dk\x024006381333931\x00')
])
def test_barcode(bctype, data, expected):
    """should generate different barcode types correctly.
    """
    instance = printer.Dummy()
    instance.barcode(data, bctype)
    assert instance.output == expected


@pytest.mark.parametrize("bctype,supports_b", [
    ('invalid', True),
    ('CODE128', False),
])
def test_lacks_support(bctype, supports_b):
    """should raise an error if the barcode type is not supported.
    """
    profile = Profile(features={BARCODE_B: supports_b})
    instance = printer.Dummy(profile=profile)
    with pytest.raises(BarcodeTypeError):
        instance.barcode('test', bctype)

    assert instance.output == b''