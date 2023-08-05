#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mindspore as ms
from msadapter.utils import unsupported_attr
from msadapter.pytorch.common._inner import _out_inplace_assign


def range(start, end, step=1, out=None, dtype=None, layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    if dtype is None:
        dtype = ms.float32
    start = ms.Tensor(start, dtype=dtype)
    end = ms.Tensor(end+0.001, dtype=dtype)
    # TODO This function is deprecated and will be removed in a future release
    # because its behavior is inconsistent with Python’s range builtin. Instead, use torch.arange(),
    # which produces values in [start, end).
    step = ms.Tensor(step, dtype=dtype)
    output = ms.ops.range(start, end, step)
    return _out_inplace_assign(out, output, "range")


def arange(start, end=None, step=1, *, out=None, dtype=None,
        layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    if end is None:
        end = start
        start = 0
    output =  ms.ops.arange(start=start, end=end, step=step, dtype=dtype)
    return _out_inplace_assign(out, output, "arange")
