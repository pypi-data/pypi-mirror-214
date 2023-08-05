#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mindspore as ms
from msadapter.pytorch.nn import Module
from msadapter.pytorch.tensor import cast_to_adapter_tensor

all = [
    'auto_mixed_precision'
]


class _CastToAdapter(Module):
    """Wrap amp net for msadapter, cast network from ms.nn.Cell to nn.Module."""
    def __init__(self, net):
        super(_CastToAdapter, self).__init__()
        self._ms_amp_net = net

    def forward(self, *inputs):
        output = self._ms_amp_net(*inputs)
        return cast_to_adapter_tensor(output)


def auto_mixed_precision(network, amp_level="O0"):
    """
    This API wraps ms.amp.auto_mixed_precision() for cast adapter type.
    https://www.mindspore.cn/tutorials/zh-CN/r2.0/advanced/mixed_precision.html
    """
    # This is an internal interface, only for debugging.
    # After calling this API, use amp_net.trainable_params() to replace amp_net.parameters().
    amp_net = ms.amp.auto_mixed_precision(network, amp_level)
    return _CastToAdapter(amp_net)
