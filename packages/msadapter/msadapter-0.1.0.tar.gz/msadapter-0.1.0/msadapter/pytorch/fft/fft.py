#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mindspore as ms
from msadapter.pytorch.common._inner import _out_inplace_assign
from msadapter.pytorch._register_numpy_primitive import fft_op, rfft_op


def fft(input, n=None, dim=-1, norm=None, out=None):
    # TODO: To use ms.ops.fft after it support
    output = fft_op(input, n, dim, norm)
    return _out_inplace_assign(out, output, "fft")


def rfft(input, n=None, dim=-1, norm=None, *, out=None):
    # TODO: To use ms.ops.rfft after it support
    output = rfft_op(input, n, dim, norm)
    return _out_inplace_assign(out, ms.Tensor(output), "rfft")
