#!/usr/bin/env python
import warnings
import numbers
# from functools import lru_cache
from copy import deepcopy
import numpy as np
from scipy import signal
import mindspore as ms
from mindspore import ops
from mindspore.common import dtype as mstype
from mindspore.ops.primitive import _primexpr
from mindspore.ops._primitive_cache import _get_cache_prim

from msadapter.pytorch.tensor import tensor, cast_to_ms_tensor, cast_to_adapter_tensor, custom_matmul
from msadapter.utils import unsupported_attr, get_backend, pynative_mode_condition, is_under_gpu_context, \
                             is_under_ascend_context, _infer_size, \
                             set_name_tuple, set_multiple_name_tuple, _get_ms_type
from msadapter.pytorch.tensor import Tensor as adapter_tensor
from msadapter.pytorch.common._inner import _out_inplace_assign, _out_limit_pynative, \
                                             _out_inplace_assign_with_adapter_tensor
from msadapter.pytorch.common.dtype import _TypeDict, all_int_type, all_float_type, all_complex_type
from msadapter.pytorch.common.device import Device
from msadapter.pytorch.linalg import lu_solve as linalg_lu_solve
from msadapter.pytorch.linalg import matrix_power as linalg_matrix_power
from msadapter.pytorch._register_numpy_primitive import poisson_op

def empty(*size, out=None, dtype=None, layout=None, \
          device=None, requires_grad=False, pin_memory=False, \
          memory_format=None):
    # TODO: ms.numpy.empty will create a tensor fill with zeros, not uninitialized numbers.
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(pin_memory)
    unsupported_attr(memory_format)
    if dtype is None:
        dtype = ms.float32

    _size = size
    if isinstance(size[0], (tuple, list)):
        _size = size[0]
    output = ms.numpy.empty(_size, dtype)
    return _out_inplace_assign(out, output, "empty")


def eye(n, m=None, *, out=None, dtype=None, layout=None, \
        device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)

    if m is None:
        m = n
    if dtype is None:
        dtype = ms.float32

    output = ms.ops.eye(n, m, dtype)
    return _out_inplace_assign(out, output, "eye")


def cat(tensors, dim=0, *, out=None):
    if tensors is None:
        raise ValueError('`tensors` in `{}` should not be None'.format(cat.__name__))

    if not isinstance(tensors, (tuple, list)):
        raise TypeError('`tensors` in `{}` should be tuple or list'.format(cat.__name__))

    if is_under_ascend_context():
        _rank = len(tensors[0].shape)
        dim = dim if dim >= 0 else dim + _rank

    inputs = cast_to_ms_tensor(tensors)
    output = ops.concat(inputs, dim)
    return _out_inplace_assign(out, output, "cat")

def concat(tensors, dim=0, *, out=None):
    if tensors is None:
        raise ValueError('`tensors` in `{}` should not be None'.format(concat.__name__))

    if not isinstance(tensors, (tuple, list)):
        raise TypeError('`tensors` in `{}` should be tuple or list'.format(concat.__name__))

    if is_under_ascend_context():
        _rank = len(tensors[0].shape)
        dim = dim if dim >= 0 else dim + _rank

    inputs = cast_to_ms_tensor(tensors)
    output = ops.concat(inputs, dim)
    return _out_inplace_assign(out, output, "concat")

def ones(*size, out=None, dtype=None, layout=None,
        device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)

    if isinstance(size[0], (tuple, list)):
        size = tuple(size[0])
    output = ms.ops.ones(size, dtype)
    return _out_inplace_assign(out, output, "ones")


def stack(tensors, dim = 0, *, out=None):
    tensors = cast_to_ms_tensor(tensors)
    output = ops.stack(tensors, dim)
    return _out_inplace_assign(out, output, "stack")


def meshgrid(*tensors, indexing='ij'):
    if isinstance(tensors[0], (list, tuple)):
        input_tensor = tuple(*tensors)
    else:
        input_tensor = tensors

    input_tensor = cast_to_ms_tensor(input_tensor)
    output = ops.meshgrid(*input_tensor, indexing=indexing)
    return cast_to_adapter_tensor(output)


def log(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ops.log(input)
    return _out_inplace_assign(out, output, "log")


def chunk(input, chunks, dim=0):
    input = cast_to_ms_tensor(input)
    output = ops.chunk(input, chunks, dim)
    return cast_to_adapter_tensor(output)


def diag(input, diagonal=0, *, out=None):
    # TODO
    # May be use mindspore.ops.diag instead. Nowadays, this operator do not support CPU.
    input = cast_to_ms_tensor(input)
    output =  ms.numpy.diag(input, diagonal)
    return _out_inplace_assign(out, output, "diag")


def sqrt(input, *, out=None):
    # TODO: ms.ops.sqrt do not support int input
    if input.dtype == mstype.int32 or input.dtype == mstype.int64:
        input = input.astype(mstype.float32)

    input = cast_to_ms_tensor(input)
    output = ops.sqrt(input)
    return _out_inplace_assign(out, output, "sqrt")


def mm(input, mat2, *, out=None):
    output = input.mm(mat2)
    return _out_inplace_assign_with_adapter_tensor(out, output, "mm")


def zeros(*size, out=None, dtype=None, device=None, requires_grad=False):
    unsupported_attr(device)
    unsupported_attr(requires_grad)

    if isinstance(size[0], (tuple, list)):
        size = size[0]

    output = ms.ops.zeros(size, dtype)
    return _out_inplace_assign(out, output, "zeros")


def div(input, other, *, rounding_mode=None, out=None):
    input = cast_to_ms_tensor(input)
    value = cast_to_ms_tensor(other)
    if not isinstance(input, ms.Tensor):
        input = ms.ops.scalar_to_tensor(input)
    if not isinstance(value, ms.Tensor):
        value = ms.ops.scalar_to_tensor(value)
    if rounding_mode is None:
        if input.dtype in all_int_type:
            input = ms.ops.cast(input, mstype.float32)
    output = ms.ops.div(input, value, rounding_mode=rounding_mode)
    return _out_inplace_assign(out, output, "div")


def divide(input, other, *, rounding_mode=None, out=None):
    output = div(input, other, rounding_mode=rounding_mode)
    return _out_inplace_assign(out, output, "divide")


def flatten(input, start_dim=0, end_dim=-1):
    return input.flatten(start_dim, end_dim)


def unflatten(input, dim, sizes):
    return input.unflatten(dim, sizes)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE)
def _check_transpose_dim(dim, rank):
    if dim >= rank or dim < -rank:
        raise ValueError("dim is out of bound, should be in range [{}, {})"
                .format(-rank, rank))


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE)
def _get_transpose_perm(input_shape, dim0, dim1):
    rank = len(input_shape)
    _check_transpose_dim(dim0, rank)
    _check_transpose_dim(dim1, rank)
    _perm = list(range(rank))
    _perm[dim0] = dim1
    _perm[dim1] = dim0
    return tuple(_perm)


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE)
def _get_transpose_perm_ascend(input_shape, dim0, dim1):
    rank = len(input_shape)
    _check_transpose_dim(dim0, rank)
    _check_transpose_dim(dim1, rank)
    _perm = list(range(rank))
    _dim0 = dim0 if dim0 >=0 else dim0 + rank
    _dim1 = dim1 if dim1 >=0 else dim1 + rank
    _perm[_dim0] = _dim1
    _perm[_dim1] = _dim0
    return tuple(_perm)


def transpose(input, dim0, dim1):
    if is_under_ascend_context():
        input_ms = cast_to_ms_tensor(input)
        out = ms.ops.transpose(input_ms, _get_transpose_perm_ascend(input.shape, dim0, dim1))
        return cast_to_adapter_tensor(out)

    input_ms = cast_to_ms_tensor(input)
    if input.nelement() == 0:
        out_shape = list(input.shape)
        out_shape[dim0], out_shape[dim1] = out_shape[dim1], out_shape[dim0]
        out = input.reshape(tuple(out_shape))
    else:
        out = ops.transpose(input_ms, _get_transpose_perm(input.shape, dim0, dim1))
    return cast_to_adapter_tensor(out)


def multinomial(input, num_samples, replacement=False, *, generator=None, out=None):
    unsupported_attr(generator)
    if generator is not None:
        warnings.warn("torch.multinomal don't support generator now.")
    input_tensor = cast_to_ms_tensor(input).astype(mstype.float32)
    output = ms.ops.multinomial(input_tensor, num_samples, replacement)
    return _out_inplace_assign(out, output, "multinomial")


def randperm(n, *, generator=None, out=None, dtype=mstype.int64, layout=None, device=None,
             requires_grad=False, pin_memory=False):
    unsupported_attr(generator)
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(pin_memory)

    if generator is not None:
        warnings.warn("torch.randperm don't support generator now.")
    if layout is not None:
        warnings.warn("torch.randperm don't support layout now.")

    output = np.random.permutation(n)
    output = tensor(output, dtype=dtype)
    return _out_inplace_assign(out, output, "randperm")


def randint(low, high, size, *, generator=None, out=None, dtype=None, layout=None,
            device=None, requires_grad=False):
    unsupported_attr(generator)
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)

    if generator is not None:
        warnings.warn("torch.randint don't support generator now.")
    if layout is not None:
        warnings.warn("torch.randint don't support layout now.")

    # TODO: input low can be optional
    # TODO: ms.ops.randint to support non-int types
    _dtype = mstype.int64 if dtype not in all_int_type or dtype == mstype.uint8 else dtype
    output = ms.ops.randint(low, high, size, dtype=_dtype)
    if dtype is not None:
        output = output.astype(dtype)
    return _out_inplace_assign(out, output, "randint")


def as_tensor(data, dtype=None, device=None):
    unsupported_attr(device)

    if isinstance(data, (tuple, list)):
        data = [i.data.item() if isinstance(i, adapter_tensor) else i for i in data ]

    output = ms.Tensor(data, dtype=dtype)
    return cast_to_adapter_tensor(output)


def zeros_like(input, dtype=None, layout=None, device=None, requires_grad=False, memory_format=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(memory_format)
    input_x = cast_to_ms_tensor(input)
    output = ms.ops.zeros_like(input_x, dtype=dtype)
    return cast_to_adapter_tensor(output)


def ones_like(input, dtype=None, layout=None, device=None, requires_grad=False, memory_format=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(memory_format)
    input_x = cast_to_ms_tensor(input)
    dtype = _get_ms_type(dtype)
    output = ms.ops.ones_like(input_x, dtype=dtype)
    return cast_to_adapter_tensor(output)


def empty_like(input, dtype=None, layout=None, device=None, requires_grad=False, memory_format=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(memory_format)
    if dtype is None:
        dtype = ms.float32
    #TODO:replace whith mindspore.ops.empty_like
    output = ms.numpy.empty_like(input, dtype=dtype)
    return cast_to_adapter_tensor(output)


def full(size, fill_value, out=None, dtype=None, layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    if dtype is None:
        dtype = ms.float32
    output = ms.ops.full(size, fill_value, dtype=dtype)
    return _out_inplace_assign(out, output, "full")


def full_like(input, fill_value, dtype=None, layout=None, device=None, requires_grad=False, memory_format=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(memory_format)
    output = ms.ops.full_like(input, fill_value=fill_value, dtype=dtype)
    return cast_to_adapter_tensor(output)


def where(condition, x=None, y=None):
    if x is None and y is None:
        return nonzero(condition, as_tuple=True)
    x = cast_to_ms_tensor(x)
    y = cast_to_ms_tensor(y)
    output = ms.ops.where(condition, x, y)
    return cast_to_adapter_tensor(output)


def rand(*size, out=None, dtype=None, layout=None, device=None, requires_grad=False, pin_memory=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(pin_memory)
    if dtype is None:
        dtype = ms.float32
    output = from_numpy(np.random.rand(*size)).to(dtype)
    if not out:
        return output
    return _out_inplace_assign(out, output, "rand")


def randn(*size, out=None, dtype=None, layout=None,
    device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)

    if isinstance(size[0], (tuple, list)):
        _size = size[0]
    elif isinstance(size[0], int):
        _size = size
    else:
        raise TypeError("`size` type in `randn` only support int, tuple and list")

    if dtype is None:
        dtype = ms.float32

    output = from_numpy(np.random.randn(*_size)).to(dtype)
    if not out:
        return output
    return _out_inplace_assign(out, output, "randn")


def linspace(start, end, steps, *, out=None, dtype=None, device=None, requires_grad=False):
    # TODO: ms.ops.linspace not support complex, not support int dtype tensor.
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    if isinstance(start, adapter_tensor):
        start = cast_to_ms_tensor(start)
        if start.dtype not in (ms.float32, ms.float64):
            start = start.astype(ms.float32)

    if isinstance(end, adapter_tensor):
        end = cast_to_ms_tensor(end)
        if end.dtype not in (ms.float32, ms.float64):
            end = end.astype(ms.float32)

    output = ms.ops.linspace(start, end, steps)
    if dtype is not None:
        output = output.astype(dtype)
    return _out_inplace_assign(out, output, "linspace")


def take(input, index):
    input = cast_to_ms_tensor(input)
    index = cast_to_ms_tensor(index)
    output = input.take(index)
    return cast_to_adapter_tensor(output)


def abs(input, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.abs(input)
    return _out_inplace_assign(out, output, "abs")


def atan2(input, other, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.atan2(input, other)
    return _out_inplace_assign(out, output, "atan2")


def clamp(input, min=None, max=None, out=None):
    input_ms = cast_to_ms_tensor(input)
    if is_under_ascend_context() and input_ms.dtype == ms.float64:
        input_ms = input_ms.astype(ms.float32)
        output = ms.ops.clamp(input_ms, min, max)
        output = output.astype(ms.float64)
    else:
        output = ms.ops.clamp(input_ms, min, max)
    return _out_inplace_assign(out, output, "clamp")


def cos(input, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.cos(input)
    return _out_inplace_assign(out, output, "cos")


@_primexpr
def device(type=None, index=None):
    if type is not None:
        if isinstance(type, str):
            if ':' in type:
                if index is not None:
                    raise ValueError(f"`type` must not include an index because index was passed explicitly: {type}")
                _target, _id = type.split(':')
                _id = int(_id)
            else:
                _target = type
                _id = index
            return Device(_target, _id)

        if isinstance(type, int):
            return Device(get_backend(), type)

        if isinstance(type, Device):
            if index is not None:
                raise ValueError("torch.device(): When input is torch.device, `index` can not be set.")
            return Device(type.type, type.index)

        raise TypeError("torch.device(): `type` must be type of 'str' or 'torch.device'.")

    raise ValueError("torch.device(): `type` can not be None")


def fmod(input, other, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.fmod(input, other)
    return _out_inplace_assign(out, output, "fmod")


def frac(input, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.frac(input)
    return _out_inplace_assign(out, output, "frac")


def log10(input, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.log10(input)
    return _out_inplace_assign(out, output, "log10")


def log1p(input, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.log1p(input)
    return _out_inplace_assign(out, output, "log1p")


def log2(input, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.log2(input)
    return _out_inplace_assign(out, output, "log2")


def sin(input, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.sin(input)
    return _out_inplace_assign(out, output, "sin")


def max(input, dim=None, keepdim=False, *, out=None):
    #TODO: not supper max(input, other)
    input = cast_to_ms_tensor(input)
    type = input.dtype
    input = input.astype(ms.float32)
    if dim is None:
        output = input.max(axis=dim, keepdims=keepdim).astype(type)
        return _out_inplace_assign(out, output, "max")
    value, indice = ms.ops.max(input, dim, keepdim)
    value = value.astype(type)
    if pynative_mode_condition():
        point = set_name_tuple('max')
        rlt = point(cast_to_adapter_tensor(value), cast_to_adapter_tensor(indice))
        if out is not None:
            if len(out) != 2 or not isinstance(out[0], adapter_tensor) or not isinstance(out[1], adapter_tensor):
                raise TypeError("In msadapter.torch.max(), `out` should be tuple of Tensors.")
            out[0].assign_value(value)
            out[1].assign_value(indice)
            return out
        return rlt

    if out is not None:
        raise ValueError('In MindSpore static graph mode, `out` in `max` shoud be None, '
            'please set out=None and use return value instead of `out`.')
    return cast_to_adapter_tensor(value), cast_to_adapter_tensor(indice)


def min(input, dim=None, keepdim=False, *, out=None):
    # TODO: Right Now, not support 'min(input, other, *, out=None)'
    input = cast_to_ms_tensor(input)
    type = input.dtype
    input = input.astype(ms.float32)
    if dim is None:
        output = input.min(dim, keepdim).astype(type)
        return _out_inplace_assign(out, output, "min")
    result, indices = ms.ops.min(input, dim, keepdim)
    result = result.astype(type)
    if pynative_mode_condition():
        point = set_name_tuple('min')
        rlt = point(cast_to_adapter_tensor(result), cast_to_adapter_tensor(indices))
        if out is not None:
            if len(out) != 2 or not isinstance(out[0], adapter_tensor) or not isinstance(out[1], adapter_tensor):
                raise TypeError("In msadapter.torch.min(), `out` should be tuple of Tensors.")
            out[0].assign_value(result)
            out[1].assign_value(indices)
            return out
        return rlt

    if out is not None:
        raise ValueError('In MindSpore static graph mode, `out` in `min` shoud be None, '
                            'please set out=None and use return value instead of `out`.')
    return cast_to_adapter_tensor(result), cast_to_adapter_tensor(indices)

def fmax(input, other, *, out=None):
    output = input.fmax(other)
    return _out_inplace_assign_with_adapter_tensor(out, output, "fmax")


def fmin(input, other, *, out=None):
    output = input.fmin(other)
    return _out_inplace_assign_with_adapter_tensor(out, output, "fmin")


def mean(input, dim=None, keepdim=False, *, dtype=None, out=None):
    input = cast_to_ms_tensor(input)
    if dtype is not None:
        input = input.astype(dtype)

    output = ms.ops.mean(input, axis=dim, keep_dims=keepdim)
    return _out_inplace_assign(out, output, "mean")


def round(input, *, decimals=0, out=None):
    input = cast_to_ms_tensor(input)
    if decimals == 0:
        output = ms.ops.round(input)
    else:
        p = 10**decimals
        input = input*p
        output = ms.ops.round(input)/p
    return _out_inplace_assign(out, output, "round")


def floor(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.floor(input)
    return _out_inplace_assign(out, output, "floor")


def ceil(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.ceil(input)
    return _out_inplace_assign(out, output, "ceil")


def sign(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.sign(input)
    return _out_inplace_assign(out, output, "sign")


def pow(input, exponent, *, out=None):
    # TODO: not support input that is above 7-dimention on GPU and Ascend
    input = cast_to_ms_tensor(input)
    exponent = cast_to_ms_tensor(exponent)
    output = ms.ops.pow(input, exponent)
    return _out_inplace_assign(out, output, "pow")


def exp(input, *, out=None):
    # TODO: after ms.ops.exp support over 7-dimentions input and int-dtype input, finetune the code.
    input = cast_to_ms_tensor(input)
    shape = input.shape
    if len(shape) > 7:
        input = input.flatten()
    if input.dtype != ms.float64:
        input = input.astype(ms.float32)
    output = ms.ops.exp(input)
    if len(shape) > 7:
        output = output.reshape(shape)
    return _out_inplace_assign(out, output, "exp")


def ge(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.ge(input, other)
    return _out_inplace_assign(out, output, "ge")


def gt(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.gt(input, other)
    return _out_inplace_assign(out, output, "gt")


def le(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.le(input, other)
    return _out_inplace_assign(out, output, "le")


def lt(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.less(input, other)
    return _out_inplace_assign(out, output, "lt")


def sum(input, dim=None, keepdim=False, *, dtype=None, out=None):
    output = input.sum(dim=dim, dtype=dtype, keepdim=keepdim)
    return _out_inplace_assign(out, output, "sum")

def median(input, dim=None, keepdim=False, *, out=None):
    output = input.median(dim, keepdim)
    return _out_inplace_assign_with_adapter_tensor(out, output, "median")

def matmul(input, other, *, out=None):
    # TODO: ms.ops.matmul not support int-dtype input on GPU, only support float dtype input
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    # TODO: repalce with output = ms.ops.matmul(input, other)
    output = custom_matmul(input, other)
    return _out_inplace_assign(out, output, "matmul")


def norm(input, p='fro', dim=None, keepdim=False, out=None, dtype=None):
    output = input.norm(p=p, dim=dim, keepdim=keepdim, dtype=dtype)
    return _out_inplace_assign_with_adapter_tensor(out, output, "norm")


def stft(input, n_fft, hop_length=None, win_length=None, window=None, center=True,
         pad_mode='reflect', normalized=False, onesided=None, return_complex=None):
    # TODO: to use ms.ops.stft after it support.
    unsupported_attr(normalized)
    unsupported_attr(onesided)
    unsupported_attr(return_complex)
    input = cast_to_ms_tensor(input)
    input = input.asnumpy()
    if pad_mode == 'reflect':
        pad_mode = 'even'
    if window is None:
        window = 'hann'
    if hop_length is None:
        hop_length = floor(n_fft / 4)
    if win_length is None:
        win_length = n_fft
    output = signal.stft(input, window=window, nperseg=win_length, noverlap=hop_length, padded=center,
                         boundary=pad_mode)
    return output


def istft():
    # TODO: implement istft after ms.ops.istft support.
    raise NotImplementedError


def bartlett_window(window_length, periodic=True, *, dtype=None, layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    input = tensor(window_length)
    output = ms.ops.bartlett_window(input, periodic=periodic, dtype=dtype)
    return cast_to_adapter_tensor(output)


def hamming_window(window_length, periodic=True, alpha=0.54, beta=0.46, dtype=None,
                   layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    output = ms.ops.hamming_window(window_length, periodic, alpha, beta, dtype=dtype)
    return cast_to_adapter_tensor(output)


def hann_window(window_length, periodic=True, *, dtype=None, layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)

    output = ms.ops.hann_window(window_length, periodic=periodic, dtype=dtype)
    return cast_to_adapter_tensor(output)


def cumsum(input, dim, *, dtype=None, out=None):
    output = input.cumsum(dim, dtype)
    return _out_inplace_assign_with_adapter_tensor(out, output, "cumsum")


def einsum(equation, *operands):
    output = _get_cache_prim(ms.ops.Einsum)(equation=equation)(operands)
    return cast_to_adapter_tensor(output)


def histc(input, bins=100, min=0, max=0, *, out=None):
    output = input.histc(bins, min, max)
    return _out_inplace_assign_with_adapter_tensor(out, output, "histc")


def histogram(input, bins, *, range=None, weight=None, density=False, out=None):
    output = input.histogram(bins, range=range, weight=weight, density=density)
    return _out_inplace_assign_with_adapter_tensor(out, output, "histogram")


def triu(input, diagonal=0, out=None):
    input = cast_to_ms_tensor(input)
    input = ms.numpy.array(input)
    output = ms.numpy.triu(input, diagonal)
    output = cast_to_adapter_tensor(output)
    return _out_inplace_assign(out, output, "triu")

def unbind(input, dim=0):
    input = cast_to_ms_tensor(input)
    output = ms.ops.unbind(input, dim)
    return cast_to_adapter_tensor(output)


def unsqueeze(input, dim):
    input = cast_to_ms_tensor(input)
    output = ms.ops.unsqueeze(input, dim)
    return cast_to_adapter_tensor(output)

def reshape(input, shape):
    input = cast_to_ms_tensor(input)
    input_size = input.shape
    if input_size[0] == 0:  # only support first element is 0
        numel = ms.ops.size(input)
        shape = _infer_size(shape, numel)
        output = ms.ops.zeros(shape, input.dtype)
    else:
        shape = tuple(shape)
        output = ms.ops.reshape(input, shape)
    return cast_to_adapter_tensor(output)

def isfinite(input):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.isfinite(input_ms)
    return cast_to_adapter_tensor(output)


def isnan(input):
    input_ms = cast_to_ms_tensor(input)
    return cast_to_adapter_tensor(input_ms.isnan())


def view_as_real(input):
    #Todo: not view
    warnings.warn("not support output as a view.")
    input = cast_to_ms_tensor(input)
    real = ms.ops.expand_dims(ms.ops.real(input), axis=-1)
    imag = ms.ops.expand_dims(ms.ops.imag(input), axis=-1)
    output = ms.ops.cat((real, imag), axis=-1)
    return cast_to_adapter_tensor(output)


def bincount(input, weights=None, minlength=0):
    input = cast_to_ms_tensor(input)
    type = 'int64'
    if input.dtype == ms.uint8:
        input = input.astype(ms.int16)
    if weights is not None:
        weights = cast_to_ms_tensor(weights)
        type = weights.dtype
    output = ms.ops.bincount(input, weights, minlength).astype(type)
    return cast_to_adapter_tensor(output)

def mul(input, other, *, out=None):
    if not isinstance(input, (int, adapter_tensor)):
        raise TypeError(f"mul(): argument 'input' (position 1) must be Tensor, not {type(input)}")
    if not isinstance(other, (int, adapter_tensor)):
        raise TypeError(f"mul(): argument 'other' (position 2) must be Tensor, not {type(other)}")

    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.mul(input, other)
    return _out_inplace_assign(out, output, "mul")


def index_select(input, dim, index, *, out=None):
    _input_params = cast_to_ms_tensor(input)
    _axis = dim
    _input_indices = cast_to_ms_tensor(index)

    output = ms.ops.gather(_input_params, _input_indices, _axis)
    return _out_inplace_assign(out, output, "index_select")

def sort(input, dim=-1, descending=False, stable=False, *, out=None):
    unsupported_attr(stable)
    input = cast_to_ms_tensor(input)
    output = ms.ops.sort(input, dim, descending)
    return _out_inplace_assign(out, output, "sort")


def msort(input, *, out=None):
    output = input.msort()
    return _out_inplace_assign(out, output, "msort")


def argsort(input, dim=-1, descending=False, stable=False):
    unsupported_attr(stable)
    return input.argsort(dim, descending)


def t(input):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.t(input_ms)
    return cast_to_adapter_tensor(output)

def squeeze(input, dim=None):
    input_ms = cast_to_ms_tensor(input)
    if dim is not None:
        if input_ms.shape[dim] != 1:
            output = input
        else:
            output = ms.ops.squeeze(input_ms, dim)
    else:
        output = ms.ops.squeeze(input_ms)
    return cast_to_adapter_tensor(output)

def from_numpy(np_data):
    # TODO: from_numpy can not share memory between tensor and nparray yet.
    return cast_to_adapter_tensor(ms.Tensor.from_numpy(np_data))

def absolute(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.absolute(input)
    return _out_inplace_assign(out, output, "absolute")


def acos(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.acos(input)
    return _out_inplace_assign(out, output, "acos")


def arccos(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.arccos(input)
    return _out_inplace_assign(out, output, "arccos")


def acosh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    shape = input.shape
    if len(shape) > 7:
        input = input.flatten()
    output = ms.ops.acosh(input)
    if len(shape) > 7:
        output = output.reshape(shape)
    return _out_inplace_assign(out, output, "acosh")

def arccosh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    shape = input.shape
    if len(shape) > 7:
        input = input.flatten()
    output = ms.ops.acosh(input)
    if len(shape) > 7:
        output = output.reshape(shape)
    return _out_inplace_assign(out, output, "arccosh")


def add(input, other, *, alpha=1, out=None):
    # TODO: ms.ops.add when add both bool Tensor, return int tensor instead of bool tensor.
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.add(input, other*alpha)
    return _out_inplace_assign(out, output, "add")


def addcdiv(input, tensor1, tensor2, *, value=1, out=None):
    input = cast_to_ms_tensor(input)
    tensor1 = cast_to_ms_tensor(tensor1)
    tensor2 = cast_to_ms_tensor(tensor2)
    value = ms.Tensor(value)
    output = ms.ops.addcdiv(input, tensor1, tensor2, value)
    return _out_inplace_assign(out, output, "addcdiv")


def addcmul(input, tensor1, tensor2, *, value=1, out=None):
    #Todo: use ms.ops.addcmul after it has been fixed
    input = cast_to_ms_tensor(input)
    tensor1 = cast_to_ms_tensor(tensor1)
    tensor2 = cast_to_ms_tensor(tensor2)
    value = ms.ops.scalar_to_tensor(value)
    mul = ms.ops.mul(tensor1, tensor2) * value
    output = ms.ops.add(input, mul)
    return _out_inplace_assign(out, output, "addcmul")


def angle(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.angle(input)
    return _out_inplace_assign(out, output, "angle")


def asin(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if input.dtype in all_int_type:
        input = input.astype(mstype.float32)
    output = ms.ops.asin(input)
    return _out_inplace_assign(out, output, "asin")


def arcsin(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.asin(input)
    return _out_inplace_assign(out, output, "arcsin")


def asinh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    shape = input.shape
    if len(shape) > 7:
        input = input.flatten()
    output = ms.ops.asinh(input)
    if len(shape) > 7:
        output = output.reshape(shape)
    return _out_inplace_assign(out, output, "asinh")


def arcsinh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    shape = input.shape
    if len(shape) > 7:
        input = input.flatten()
    output = ms.ops.asinh(input)
    if len(shape) > 7:
        output = output.reshape(shape)
    return _out_inplace_assign(out, output, "arcsinh")


def atan(input, *, out=None):
    shape = input.shape
    if len(shape) > 7:
        input = input.flatten()
    input = cast_to_ms_tensor(input)
    output = ms.ops.atan(input)
    if len(shape) > 7:
        output = output.reshape(shape)
    return _out_inplace_assign(out, output, "atan")


def arctan(input, *, out=None):
    shape = input.shape
    if len(shape) > 7:
        input = input.flatten()
    input = cast_to_ms_tensor(input)
    output = ms.ops.atan(input)
    if len(shape) > 7:
        output = output.reshape(shape)
    return _out_inplace_assign(out, output, "arctan")


def atanh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.atanh(input)
    return _out_inplace_assign(out, output, "atanh")


def arctanh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.atanh(input)
    return _out_inplace_assign(out, output, "arctanh")


def arctan2(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.atan2(input, other)
    return _out_inplace_assign(out, output, "arctan2")


def bitwise_not(input, *, out=None):
    input = cast_to_ms_tensor(input)
    type = input.dtype
    if str(type) != 'Bool':
        output = 0 - input - 1
    else:
        output = 1 - input
        output = output.astype(ms.bool_)
    return _out_inplace_assign(out, output, "bitwise_not")


def bitwise_and(input, other, *, out=None):
    if isinstance(input, adapter_tensor):
        input = cast_to_ms_tensor(input)
        input_is_bool = str(input.dtype) == 'Bool'
    else:
        input_is_bool = isinstance(input, bool)
    if isinstance(other, adapter_tensor):
        other = cast_to_ms_tensor(other)
        other_is_bool = str(other.dtype) == 'Bool'
    else:
        other_is_bool = isinstance(other, bool)
    if input_is_bool and other_is_bool:
        if isinstance(input, adapter_tensor):
            input = input.astype(ms.int8)
        else:
            other = other.astype(ms.int8)
    output = ms.ops.bitwise_and(input, other)
    if input_is_bool and other_is_bool:
        output = output.astype(ms.bool_)
    return _out_inplace_assign(out, output, "bitwise_and")


def bitwise_or(input, other, *, out=None):
    if isinstance(input, adapter_tensor):
        input = cast_to_ms_tensor(input)
        input_is_bool = str(input.dtype) == 'Bool'
    else:
        input_is_bool = isinstance(input, bool)
    if isinstance(other, adapter_tensor):
        other = cast_to_ms_tensor(other)
        other_is_bool = str(other.dtype) == 'Bool'
    else:
        other_is_bool = isinstance(other, bool)
    if input_is_bool and other_is_bool:
        if isinstance(input, adapter_tensor):
            input = input.astype(ms.int8)
        else:
            other = other.astype(ms.int8)
    output = ms.ops.bitwise_or(input, other)
    if input_is_bool and other_is_bool:
        output = output.astype(ms.bool_)
    return _out_inplace_assign(out, output, "bitwise_or")


def bitwise_xor(input, other, *, out=None):
    if isinstance(input, adapter_tensor):
        input = cast_to_ms_tensor(input)
        input_is_bool = str(input.dtype) == 'Bool'
    else:
        input_is_bool = isinstance(input, bool)
    if isinstance(other, adapter_tensor):
        other = cast_to_ms_tensor(other)
        other_is_bool = str(other.dtype) == 'Bool'
    else:
        other_is_bool = isinstance(other, bool)
    if input_is_bool and other_is_bool:
        if isinstance(input, adapter_tensor):
            input = input.astype(ms.int8)
        else:
            other = other.astype(ms.int8)
    output = ms.ops.bitwise_xor(input, other)
    if input_is_bool and other_is_bool:
        output = output.astype(ms.bool_)
    return _out_inplace_assign(out, output, "bitwise_xor")


def bitwise_left_shift(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.bitwise_left_shift(input, other)
    return _out_inplace_assign(out, output, "bitwise_left_shift")


def bitwise_right_shift(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.bitwise_right_shift(input, other)
    return _out_inplace_assign(out, output, "bitwise_right_shift")


def split(tensor, split_size_or_sections, dim=0):
    tensor = cast_to_ms_tensor(tensor)
    output = ms.ops.split(tensor, split_size_or_sections, dim)
    return cast_to_adapter_tensor(output)

def nonzero(input, *, out=None, as_tuple=False):
    input = cast_to_ms_tensor(input)
    if as_tuple:
        if input.ndim == 1:
            res = ms.ops.nonzero(input)
            output = (cast_to_adapter_tensor(res.flatten()), )
        elif input.ndim > 1:
            output = []
            res = ms.ops.nonzero(input)
            if len(res) != 0:
                res = res.transpose(1,0)
                res = ms.ops.split(res, 1, axis=0)
                output = cast_to_adapter_tensor(res)
        elif input.ndim == 0:
            raise ValueError("Do not support input ndim == 0.")
    else:
        output = ms.ops.nonzero(input)
    return _out_inplace_assign(out, output, "nonzero")

def clip(input, min=None, max=None, *, out=None):
    input = cast_to_ms_tensor(input)
    output = input.clip(min, max)
    return _out_inplace_assign(out, output, "clip")


def conj_physical(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.conj(input)
    return _out_inplace_assign(out, output, "conj_physical")

def copysign(input, other, *, out=None):
    output = input.copysign(other)
    return _out_inplace_assign(out, output, "copysign")


def cosh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.cosh(input)
    return _out_inplace_assign(out, output, "cosh")


def deg2rad(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if input.dtype not in (ms.float16, ms.float32, ms.float64):
        input = input.astype(ms.float32)
    output = ms.ops.deg2rad(input)
    return _out_inplace_assign(out, output, "deg2rad")


def devide(input, other, *, rounding_mode=None, out=None):
    _out_limit_pynative(out, "devide")
    return div(input, other, rounding_mode=rounding_mode, out=out)


def erf(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.erf(input)
    return _out_inplace_assign(out, output, "erf")


def erfc(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.erfc(input)
    return _out_inplace_assign(out, output, "erfc")


def erfinv(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.erfinv(input)
    return _out_inplace_assign(out, output, "erfinv")


def exp2(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.exp2(input)
    return _out_inplace_assign(out, output, "exp2")


def expm1(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.expm1(input)
    return _out_inplace_assign(out, output, "expm1")


def fake_quantize_per_channel_affine(input, scale, zero_point, axis, quant_min, quant_max):
    input = cast_to_ms_tensor(input)
    scale = cast_to_ms_tensor(scale)
    zero_point = cast_to_ms_tensor(zero_point)
    if axis not in range(0, input.ndim):
        raise IndexError("`axis` must be between 0 and number of dimensions of input")
    if input.shape[axis] != scale.shape[0] or input.shape[axis] != zero_point.shape[0]:
        raise RuntimeError("dimensions of scale or zero-point are not consistent with input tensor")
    i = axis + 1
    while i < input.ndim:
        scale = scale.expand_dims(-1)
        zero_point = zero_point.expand_dims(-1)
        i += 1
    output = ms.ops.round(input/scale + zero_point)
    output = ms.ops.clip_by_value(output, quant_min, quant_max) - zero_point
    output = output * scale
    return cast_to_adapter_tensor(output)


def fake_quantize_per_tensor_affine(input, scale, zero_point, quant_min, quant_max):
    input = cast_to_ms_tensor(input)
    scale = cast_to_ms_tensor(scale)
    zero_point = cast_to_ms_tensor(zero_point)

    output = ms.ops.round(input/scale + zero_point)
    output = ms.ops.clip_by_value(output, quant_min, quant_max) - zero_point
    output = output * scale
    return cast_to_adapter_tensor(output)


def fix(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.trunc(input)
    return _out_inplace_assign(out, output, "fix")


def float_power(input, exponent, *, out=None):
    # TODO: not support complex input and exponent now
    output = ms.ops.float_power(input, exponent)
    return _out_inplace_assign(out, output, "float_power")


def floor_divide(input, other, *, out=None):
    # ms.ops.floor_divide doesn't round the quotient towards 0
    # same behavior as torch version lower than 1.13
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.div(input, other, rounding_mode='trunc')
    return _out_inplace_assign(out, output, "floor_divide")


def frexp(input, *, out=None):
    # TODO: to use ms.ops.frexp
    input = cast_to_ms_tensor(input)
    sign = ms.ops.sign(input)
    input = ms.ops.abs(input)
    exp = ms.ops.floor(ms.ops.log2(input)) + 1
    mantissa = input * sign / (2 ** exp)
    output = (mantissa, exp.astype(ms.int32))
    return _out_inplace_assign(out, output, "frexp")

def gradient(input, *, spacing=1, dim=None, edge_order=1):
    input = cast_to_ms_tensor(input)
    if isinstance(spacing, adapter_tensor):
        spacing = cast_to_ms_tensor(spacing)
    elif isinstance(spacing, tuple) and isinstance(spacing[0], adapter_tensor):
        spacing = cast_to_ms_tensor(spacing)
    output = ms.numpy.gradient(input, spacing, axis=dim, edge_order=edge_order)
    output = cast_to_adapter_tensor(output)
    if not isinstance(output, tuple):
        return (output,)
    else:
        return output


def imag(input):
    input = cast_to_ms_tensor(input)
    output = ms.ops.imag(input)
    output = cast_to_adapter_tensor(output)
    output.neg_bit = True
    return output


def ldexp(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.ldexp(input, other)
    return _out_inplace_assign(out, output, "ldexp")


def lerp(input, end, weight, *, out=None):
    input = cast_to_ms_tensor(input)
    end = cast_to_ms_tensor(end)
    if isinstance(weight, adapter_tensor):
        weight = cast_to_ms_tensor(weight)
    elif not isinstance(weight, float):
        weight = float(weight)
    output = ms.ops.lerp(input, end, weight)
    return _out_inplace_assign(out, output, "lerp")


def logaddexp(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.logaddexp(input, other)
    return _out_inplace_assign(out, output, "logaddexp")


def logaddexp2(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.logaddexp2(input, other)
    return _out_inplace_assign(out, output, "logaddexp2")


def logical_and(input, other, *, out=None):
    if isinstance(input, adapter_tensor):
        input = cast_to_ms_tensor(input).astype(ms.bool_)
    if isinstance(other, adapter_tensor):
        other = cast_to_ms_tensor(other).astype(ms.bool_)
    output = ms.ops.logical_and(input, other)
    return _out_inplace_assign(out, output, "logical_and")


def logical_not(input, *, out=None):
    if isinstance(input, adapter_tensor):
        input = cast_to_ms_tensor(input).astype(ms.bool_)
    output = ms.ops.logical_not(input)
    return _out_inplace_assign(out, output, "logical_not")


def logical_or(input, other, *, out=None):
    if isinstance(input, adapter_tensor):
        input = cast_to_ms_tensor(input).astype(ms.bool_)
    if isinstance(other, adapter_tensor):
        other = cast_to_ms_tensor(other).astype(ms.bool_)
    output = ms.ops.logical_or(input, other)
    return _out_inplace_assign(out, output, "logical_or")


def logical_xor(input, other, *, out=None):
    if isinstance(input, adapter_tensor):
        input = cast_to_ms_tensor(input).astype(ms.bool_)
    if isinstance(other, adapter_tensor):
        other = cast_to_ms_tensor(other).astype(ms.bool_)

    # TODO: ms.ops.logical_xor to supported GPU
    if is_under_gpu_context():
        output = ms.numpy.logical_xor(input, other)
    else:
        output = ms.ops.logical_xor(input, other)
    return _out_inplace_assign(out, output, "logical_xor")


def logit(input, eps=None, *, out=None):
    output = input.logit(eps)
    return _out_inplace_assign_with_adapter_tensor(out, output, "logit")


def lu(input, get_infos=False, pivot=True, *, out=None):
    output = input.lu(pivot=pivot, get_infos=get_infos)
    return _out_inplace_assign_with_adapter_tensor(out, output, "lu")


def lu_unpack(LU_data, LU_pivots, unpack_data=True, unpack_pivots=True, *, out=None):
    LU_data = cast_to_ms_tensor(LU_data)
    LU_pivots = cast_to_ms_tensor(LU_pivots)
    #TODO: ms.ops.lu_unpack is only for GPU and CPU now.
    output = ms.ops.lu_unpack(LU_data, LU_pivots, unpack_data=unpack_data, unpack_pivots=unpack_pivots)
    return _out_inplace_assign(out, output, "lu_unpack")

# TODO: currently not support return qr as second result
def lstsq(A, x, *, out=None):
    #TODO: ms.ops.lstsq not support GPU and Ascend, currently use numpy func
    output = A.lstsq(x)
    return _out_inplace_assign_with_adapter_tensor(out, output, "lstsq")

def frombuffer(buffer, *, dtype = None, count=- 1, offset=0, requires_grad=False):
    unsupported_attr(requires_grad)
    np_dtype = _TypeDict[dtype]
    output = np.frombuffer(buffer=buffer, dtype=np_dtype, count=count, offset=offset)
    return adapter_tensor(output, dtype=dtype)

def as_strided(input, size, stride, storage_offset=None):
    warnings.warn("not support output as a view.")
    input_ms = cast_to_ms_tensor(input)
    if len(size) != len(stride):
        raise RuntimeError("mismatch in length of strides and shape.")
    index = np.arange(0, size[0] * stride[0], stride[0])
    for i in range(1, len(size)):
        tmp = np.arange(0, size[i] * stride[i], stride[i])
        index = np.expand_dims(index, -1)
        index = index + tmp
    if storage_offset is not None:
        index = index + storage_offset
    input_indices = ms.Tensor(index)
    out = ms.ops.gather(input_ms.reshape(-1), input_indices, 0)
    return cast_to_adapter_tensor(out)

def ne(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.ne(input, other)
    return _out_inplace_assign(out, output, "ne")


def tanh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if not input.is_floating_point():
        input = input.astype(ms.float32)
    output = ms.ops.tanh(input)
    return _out_inplace_assign(out, output, "tanh")


def maximum(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.maximum(input, other)
    return _out_inplace_assign(out, output, "maximum")


def minimum(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.minimum(input, other)
    return _out_inplace_assign(out, output, "minimum")

def polygamma(n, input, *, out=None):
    n = ms.Tensor(n)
    input_ms = cast_to_ms_tensor(input)
    # TODO: ms.ops.polygamma unsupport on Ascend
    # TODO: when n is 0, the result of ms.ops.polygamma may be wrong.
    output = ms.ops.polygamma(n, input_ms)
    return _out_inplace_assign(out, output, "polygamma")

def searchsorted(sorted_sequence, value, *, out_int32=False, right=False, side='left', out=None, sorter=None):
    if sorter is not None:
        warnings.warn("torch.searchsorted don't support sorter now.")
    #TODO:right and side has the same usage, thus set the side to unable
    if side == 'right':
        right = True
    sorted_sequence = cast_to_ms_tensor(sorted_sequence)
    value = cast_to_ms_tensor(value)
    if sorted_sequence.dtype not in (ms.int64, ms.int32) or value.dtype not in (ms.int64, ms.int32):
        value = value.astype(ms.int64)
        sorted_sequence = sorted_sequence.astype(ms.int64)
    output = ms.ops.searchsorted(sorted_sequence, value, out_int32=out_int32, right=right)
    return _out_inplace_assign(out, output, "searchsorted")

def sigmoid(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if is_under_ascend_context() and input.dtype == ms.float64:
        input = input.astype(ms.float32)
        output = ms.ops.sigmoid(input)
        output = output.astype(ms.float64)
    else:
        output = ms.ops.sigmoid(input)
    return _out_inplace_assign(out, output, "sigmoid")


def softmax(input, dim, dtype=None, *, out=None):
    input = cast_to_ms_tensor(input)
    if dtype is not None:
        input = input.astype(dtype)
    output = ms.ops.softmax(input, dim)
    return _out_inplace_assign(out, output, "softmax")


def prod(input, dim=None, keepdim=False, *, dtype=None, out=None):
    input = cast_to_ms_tensor(input)
    if dtype is not None:
        input = input.astype(dtype)
    if dim is None:
        output = ms.ops.prod(input)
    else:
        output = ms.ops.prod(input, axis=dim, keep_dims=keepdim)
    return _out_inplace_assign(out, output, "prod")


def eq(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.equal(input, other)
    return _out_inplace_assign(out, output, "eq")


def hypot(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.hypot(input, other)
    return _out_inplace_assign(out, output, "hypot")


def i0(input, *, out=None):
    output = input.i0()
    return _out_inplace_assign_with_adapter_tensor(out, output, "i0")

def igamma(input, other, *, out=None):
    output = input.igamma(other)
    return _out_inplace_assign_with_adapter_tensor(out, output, "igamma")

def igammac(input, other, *, out=None):
    output = input.igammac(other)
    return _out_inplace_assign_with_adapter_tensor(out, output, "igammac")


def multiply(input, other, *, out=None):
    if not isinstance(input, (int, adapter_tensor)):
        raise TypeError(f"multiply(): argument 'input' (position 1) must be Tensor, not {type(input)}")
    if not isinstance(other, (int, adapter_tensor)):
        raise TypeError(f"multiply(): argument 'other' (position 2) must be Tensor, not {type(other)}")

    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.mul(input, other)
    return _out_inplace_assign(out, output, "multiply")


def mvlgamma(input, p, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.mvlgamma(input, p)
    return _out_inplace_assign(out, output, "mvlgamma")


def nan_to_num(input, nan=0.0, posinf=None, neginf=None, *, out=None):
    output = input.nan_to_num(nan, posinf, neginf)
    return _out_inplace_assign_with_adapter_tensor(out, output, "nan_to_num")


def neg(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if 'Complex' in str(input.dtype):
        output = input-input-input
    else:
        output = 0 - input
    return _out_inplace_assign(out, output, "neg")


def negative(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if 'Complex' in str(input.dtype):
        output = input-input-input
    else:
        output = 0 - input
    return _out_inplace_assign(out, output, "negative")


def nextafter(input, other, *, out=None):
    output = input.nextafter(other)
    return _out_inplace_assign_with_adapter_tensor(out, output, "nextafter")


def positive(input):
    return input

def qr(input, some=True, *, out=None):
    output = input.qr(some)
    return _out_inplace_assign_with_adapter_tensor(out, output, "qr")

def rad2deg(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if not input.is_floating_point():
        input = input.astype(ms.float32)
    output = ms.ops.rad2deg(input)
    return _out_inplace_assign(out, output, "rad2deg")


def real(input):
    input = cast_to_ms_tensor(input)
    output = ms.ops.real(input)
    return cast_to_adapter_tensor(output)


def reciprocal(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.reciprocal(input)
    return _out_inplace_assign(out, output, "reciprocal")


def remainder(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.remainder(input, other)
    return _out_inplace_assign(out, output, "remainder")


def rsqrt(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if 'Bool' in str(input.dtype) or 'Int' in str(input.dtype):
        input = input.astype(ms.float32)
    output = ms.ops.rsqrt(input)
    return _out_inplace_assign(out, output, "rsqrt")

def roll(input, shifts, dims=None, *, out=None):
    output = input.roll(shifts, dims=dims)
    return _out_inplace_assign_with_adapter_tensor(out, output, "roll")

def rot90(input, k, dims, *, out=None):
    output = input.rot90(k, dims)
    return _out_inplace_assign_with_adapter_tensor(out, output, "rot90")

def sgn(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if 'Bool' in str(input.dtype) or 'Int' in str(input.dtype):
        type = input.dtype
        input = input.astype(ms.float32)
        output = ms.ops.sgn(input).astype(type)
    else:
        output = ms.ops.sgn(input)
    return _out_inplace_assign(out, output, "sgn")

def take_along_dim(input, indices, dim=None, out=None):
    input = cast_to_ms_tensor(input)
    indices = cast_to_ms_tensor(indices)

    if not dim:
        input = input.reshape(-1)
        dim = 0

    output = ms.ops.gather_d(input, dim, indices)
    return _out_inplace_assign(out, output, "take_along_dim")

def signbit(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.signbit(input)
    return _out_inplace_assign(out, output, "signbit")


def sinc(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.sinc(input)
    return _out_inplace_assign(out, output, "sinc")


def sinh(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.sinh(input)
    return _out_inplace_assign(out, output, "sinh")


def square(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.square(input)
    return _out_inplace_assign(out, output, "square")


def sub(input, other, *, alpha=1, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.sub(input, other * alpha)
    return _out_inplace_assign(out, output, "sub")


def subtract(input, other, *, alpha=1, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.subtract(input, other, alpha=alpha)
    return _out_inplace_assign(out, output, "subtract")

def trace(input):
    input = cast_to_ms_tensor(input)
    output = input.trace()
    return cast_to_adapter_tensor(output)

def tril(input, diagonal=0, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.tril(input, diagonal)
    return _out_inplace_assign(out, output, "tril")

def conj(input):
    input = cast_to_ms_tensor(input)
    output = input.conj()
    output = cast_to_adapter_tensor(output)
    output.conj_bit = True
    return output

def is_conj(input):
    if not hasattr(input, "conj_bit"):
        return False
    else:
        return input.conj_bit

def resolve_conj(input):
    output = deepcopy(input)
    output.conj_bit = False
    return output

def tan(input, *, out=None):
    input = cast_to_ms_tensor(input)
    if not input.is_floating_point():
        input = input.astype(ms.float32)
    output = ms.ops.tan(input)
    return _out_inplace_assign(out, output, "tan")


def _check_isint(input):
    if isinstance(input, int):
        return True
    if isinstance(input, (adapter_tensor, ms.Tensor)) and 'Int' in str(input.dtype):
        return True
    return False

def _int_to_float(input):
    if isinstance(input, int):
        return float(input)
    return input.astype(ms.float32)


def true_divide(dividend, divisor, *, out=None):
    input = cast_to_ms_tensor(dividend)
    other = cast_to_ms_tensor(divisor)

    is_input_int = _check_isint(input)
    is_other_int = _check_isint(other)

    if is_input_int and is_other_int:
        input = _int_to_float(input)
        other = _int_to_float(other)
    if isinstance(input, float) and isinstance(other, float):
        input = ms.Tensor(input)
    output = ms.ops.true_divide(input, other)
    return _out_inplace_assign(out, output, "true_divide")


def trunc(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.trunc(input)
    return _out_inplace_assign(out, output, "trunc")


def xlogy(input, other, *, out=None):
    if not isinstance(input, adapter_tensor) and not isinstance(other, adapter_tensor):
        raise TypeError("For xlogy: one of the input must be Tensor.")

    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.xlogy(input, other)
    return _out_inplace_assign(out, output, "xlogy")


def cov(input, *, correction=1, fweights=None, aweights=None, out=None):
    #TODO： need be replaced with mindspore.ops.cov
    input = cast_to_ms_tensor(input)
    if fweights is not None:
        fweights = cast_to_ms_tensor(fweights)
    if aweights is not None:
        aweights = cast_to_ms_tensor(aweights)
    output = input.cov(correction=correction, fweights=fweights, aweights=aweights)
    return _out_inplace_assign(out, output, "cov")


def corrcoef(input, *, out=None):
    output = input.corrcoef()
    return _out_inplace_assign(out, output, "corrcoef")


def cross(input, other, dim=None, *, out=None):
    output = input.cross(other, dim)
    return _out_inplace_assign_with_adapter_tensor(out, output, "cross")


def cummax(input, dim, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.cummax(input, axis=dim)
    return _out_inplace_assign(out, output, "cummax")


def cummin(input, dim, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.cummin(input, dim)
    # the output dtype in ms.ops.cummin is different with ms.ops.cummax
    output[1] = output[1].astype(ms.common.dtype.int64)
    return _out_inplace_assign(out, output, "cummin")


def cumprod(input, dim, *, dtype=None, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.cumprod(input, dim, dtype=dtype)
    return _out_inplace_assign(out, output, "cumprod")

def diagflat(input, offset=0, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.diagflat(input, offset)
    return _out_inplace_assign(out, output, "diagflat")

def diagonal(input, offset=0, dim1=0, dim2=1):
    input = cast_to_ms_tensor(input)
    #TODO float64 not support if offset != 0
    if offset != 0:
        input = input.astype(mstype.float32)
    output = ms.ops.diagonal(input, offset, dim1, dim2)
    return cast_to_adapter_tensor(output)

def diff(input, n=1, dim=-1, prepend=None, append=None):
    input = cast_to_ms_tensor(input)
    #TODO: ms.ops.diff only support n=1
    output = ms.numpy.diff(input, n, dim, prepend, append)
    return cast_to_adapter_tensor(output)

def flip(input, dims):
    input = cast_to_ms_tensor(input)
    if isinstance(dims, list):
        dims = tuple(dims)
    output = ms.ops.flip(input, dims)
    return cast_to_adapter_tensor(output)

def fliplr(input):
    input = cast_to_ms_tensor(input)
    output = ms.ops.fliplr(input)
    return cast_to_adapter_tensor(output)


def gather(input, dim, index, *, sparse_grad=False, out=None):
    if sparse_grad:
        raise ValueError("`sparse_grad` in `sparse_grad` can not be True.")

    input = cast_to_ms_tensor(input)
    index = cast_to_ms_tensor(index)
    output = ms.ops.gather_elements(input, dim, index)
    return _out_inplace_assign(out, output, "gather")

def bmm(input, mat2, *, out=None) :
    input_x = cast_to_ms_tensor(input)
    mat2 = cast_to_ms_tensor(mat2)
    output = ms.ops.bmm(input_x, mat2)
    return _out_inplace_assign(out, output, "bmm")

def equal(input, other):
    if not isinstance(input, adapter_tensor) or not isinstance(other, adapter_tensor):
        raise ValueError("`input` and `other` must be Tensor")
    x = cast_to_ms_tensor(input)
    y = cast_to_ms_tensor(other)

    if x.dtype != y.dtype:
        return False
    if x.shape == y.shape:
        size = x.size
        output = ms.ops.equal(x, y)
        output = output.sum()
        if output == size:
            return True
    return False

def greater_equal(input, other, *, out=None):
    x = cast_to_ms_tensor(input)
    y = cast_to_ms_tensor(other)
    output = ms.ops.greater_equal(x, y)
    return _out_inplace_assign(out, output, "greater_equal")

def greater(input, other, *, out=None):
    x = cast_to_ms_tensor(input)
    y = cast_to_ms_tensor(other)
    output = ms.ops.greater(x, y)
    return _out_inplace_assign(out, output, "greater")

def less_equal(input, other, *, out=None):
    x = cast_to_ms_tensor(input)
    y = cast_to_ms_tensor(other)
    output = ms.ops.less_equal(x, y)
    return _out_inplace_assign(out, output, "less_equal")

def less(input, other, *, out=None):
    x = cast_to_ms_tensor(input)
    y = cast_to_ms_tensor(other)
    output = ms.ops.less(x, y)
    return _out_inplace_assign(out, output, "less")

def not_equal(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.ne(input, other)
    return _out_inplace_assign(out, output, "not_equal")

def baddbmm(input, batch1, batch2, *, beta=1, alpha=1, out=None):
    x = cast_to_ms_tensor(input)
    batch1 = cast_to_ms_tensor(batch1)
    batch2 = cast_to_ms_tensor(batch2)
    output = ms.ops.baddbmm(x, batch1, batch2, beta, alpha)
    return _out_inplace_assign(out, output, "baddbmm")

def masked_select(input, mask, *, out=None):
    x = cast_to_ms_tensor(input)
    mask = cast_to_ms_tensor(mask)
    output = ms.ops.masked_select(x, mask)
    return _out_inplace_assign(out, output, "masked_select")


@_primexpr
# @lru_cache(_GLOBAL_LRU_CACHE_SIZE)
def _get_select_out_shape(input_shape, dim):
    shape = [input_shape[i] for i in range(len(input_shape)) if i != dim]
    return tuple(shape)


def select(input, dim, index):
    return input.select(dim, index)

def argmin(input, dim=None, keepdim=False):
    input = cast_to_ms_tensor(input)
    output = ms.ops.argmin(input, axis=dim, keepdims=keepdim)
    return cast_to_adapter_tensor(output)

def argmax(input, dim=None, keepdim=False):
    input = cast_to_ms_tensor(input)
    output = ms.ops.argmax(input, dim, keepdim)
    return cast_to_adapter_tensor(output)

def broadcast_to(input, shape):
    input = cast_to_ms_tensor(input)
    output = ms.ops.broadcast_to(input, shape)
    return cast_to_adapter_tensor(output)

def ravel(input):
    x = cast_to_ms_tensor(input)
    output = ms.ops.reshape(x, (-1,))
    return cast_to_adapter_tensor(output)

def unique(input, sorted=True, return_inverse=False, return_counts=False, dim=None):
    unsupported_attr(dim)
    unsupported_attr(return_counts)
    input = cast_to_ms_tensor(input)
    data_type = input.dtype
    if sorted and return_inverse:
        raise ValueError("Don't support sorted=True and return_inverse=True.")

    res, idx = ms.ops.unique(input)
    if sorted:
        res = ms.ops.cast(res, ms.float32)
        res, _ = ms.ops.sort(res)
        res = ms.ops.cast(res, data_type)
    if return_inverse:
        res = cast_to_adapter_tensor(res)
        idx = cast_to_adapter_tensor(idx)
        return (res, idx)
    else:
        res = cast_to_adapter_tensor(res)
        return res

def permute(input, dims):
    ms_input = cast_to_ms_tensor(input)
    output = ms.ops.permute(ms_input, dims)
    return cast_to_adapter_tensor(output)

def numel(input):
    input = cast_to_ms_tensor(input)
    output = ms.ops.numel(input)
    return cast_to_adapter_tensor(output)

def logsumexp(input, dim, keepdim=False, *, out=None):
    ms_input = cast_to_ms_tensor(input)
    if ms_input.dtype != mstype.float32:
        ms_input = ms_input.astype(mstype.float32)
    output = ms.ops.logsumexp(ms_input, dim, keepdim)
    return _out_inplace_assign(out, output, "logsumexp")

def addmv(input, mat, vec, *, beta=1, alpha=1, out=None):
    input = cast_to_ms_tensor(input)
    mat = cast_to_ms_tensor(mat)
    vec = cast_to_ms_tensor(vec)
    output = ms.ops.addmv(input, mat, vec, beta=beta, alpha=alpha)
    return _out_inplace_assign(out, output, "addmv")

def dot(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    #TODO: ms.ops.tensor_dot only supports float16/float32
    input_dtype = input.dtype
    if input_dtype in (mstype.float32, mstype.float16):
        output = ms.ops.tensor_dot(input, other, 1)
    else:
        input = input.astype(ms.float32)
        other = other.astype(ms.float32)
        output = ms.ops.tensor_dot(input, other, 1)
        output = output.astype(input_dtype)
    return _out_inplace_assign(out, output, "dot")

def inverse(input, *, out=None):
    input = cast_to_ms_tensor(input)
    #TODO: Ascend has no ms.ops.inverse
    # output = ms.ops.inverse(input)  # ops.inverse is not ready at 11-13
    if input.dtype in all_int_type:
        input = input.astype(mstype.float32)
    output = _get_cache_prim(ms.ops.MatrixInverse)()(input)
    return _out_inplace_assign(out, output, "inverse")

def count_nonzero(input, dim=None):
    input = cast_to_ms_tensor(input)
    if dim is None:
        dim = ()
    output = ms.ops.count_nonzero(input, axis=dim)
    return cast_to_adapter_tensor(output)

def all(input, dim=(), keepdim=False, *, out=None):
    input = cast_to_ms_tensor(input)
    if input.dtype != ms.bool_:
        input = input.astype(ms.bool_)
    output = input.all(axis=dim, keep_dims=keepdim)
    return _out_inplace_assign(out, output, "all")

def scatter(input, dim, index, src):
    return input.scatter(dim, index, src)

def topk(input, k, dim=None, largest=True, sorted=True, *, out=None):
    input_x = cast_to_ms_tensor(input)
    output = ms.ops.topk(input_x, k, dim, largest, sorted)
    return _out_inplace_assign(out, output, "topk")

def addbmm(input, batch1, batch2, *, beta=1, alpha=1, out=None):
    _input, _batch1, _batch2 = cast_to_ms_tensor((input, batch1, batch2))
    output = ms.ops.addbmm(_input, _batch1, _batch2, beta=beta, alpha=alpha)
    return _out_inplace_assign(out, output, "addbmm")

def addmm(input, mat1, mat2, *, beta=1, alpha=1, out=None):
    _input, _mat1, _mat2 = cast_to_ms_tensor((input, mat1, mat2))
    output = ms.ops.addmm(_input, _mat1, _mat2, beta=beta, alpha=alpha)
    return _out_inplace_assign(out, output, "addbmm")

def addr(input, vec1, vec2, *, beta=1, alpha=1, out=None):
    _input, _vec1, _vec2 = cast_to_ms_tensor((input, vec1, vec2))
    output = ms.ops.addr(_input, _vec1, _vec2, beta=beta, alpha=alpha)
    return _out_inplace_assign(out, output, "addr")

def isclose(input, other, rtol=1e-05, atol=1e-08, equal_nan=False):
    _input, _other = cast_to_ms_tensor((input, other))
    output = ms.ops.isclose(_input, _other, rtol=rtol, atol=atol, equal_nan=equal_nan)
    return cast_to_adapter_tensor(output)

def allclose(input, other, rtol=1e-05, atol=1e-08, equal_nan=False):
    output = all(isclose(input, other, rtol=rtol, atol=atol, equal_nan=equal_nan)).item()
    return output

def cholesky(input, upper=False, *, out=None):
    input = cast_to_ms_tensor(input)
    output = input.cholesky(upper)
    return _out_inplace_assign(out, output, "cholesky")

def cholesky_inverse(input, upper=False, *, out=None):
    input = cast_to_ms_tensor(input)
    # TODO: ms.tensor.cholesky_inverse not support GPU.
    output = input.cholesky_inverse(upper)
    return _out_inplace_assign(out, output, "cholesky_inverse")

def dist(input, other, p=2):
    _input = cast_to_ms_tensor(input)
    _other = cast_to_ms_tensor(other)

    _input_dtype = _input.dtype
    if _input_dtype in (ms.float16, ms.float32):
        _other.astype(_input_dtype)
        output = ms.ops.dist(_input, _other, p=p)
    elif _input_dtype == ms.float64:
        _input = _input.astype(ms.float32)
        _other = _other.astype(_input.dtype)
        output = ms.ops.dist(_input, _other, p=p)
        output = output.astype(ms.float64)
    else:
        raise ValueError(f"For torch.dist, input should be floating Tensor, but got {_input_dtype}.")

    return cast_to_adapter_tensor(output)

def aminmax(input, *, dim=None, keepdim=False, out=None):
    _input = cast_to_ms_tensor(input)
    _min = _input.min(axis=dim, keepdims=keepdim)
    _max = _input.max(axis=dim, keepdims=keepdim)
    return _out_inplace_assign(out, (_min, _max), "aminmax")

def any(input, dim=(), keepdim=False, *, out=None):
    input = cast_to_ms_tensor(input)
    if input.dtype != ms.bool_:
        input = input.astype(ms.bool_)
    output = input.any(axis=dim, keep_dims=keepdim)
    return _out_inplace_assign(out, output, "any")

def is_complex(input):
    input = cast_to_ms_tensor(input)
    return input.is_complex()

def isinf(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.isinf(input)
    return _out_inplace_assign(out, output, "isinf")

def isneginf(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.isneginf(input)
    return _out_inplace_assign(out, output, "isneginf")

def isposinf(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.isposinf(input)
    return _out_inplace_assign(out, output, "isposinf")

def isreal(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.isreal(input)
    return _out_inplace_assign(out, output, "isreal")

def lgamma(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.lgamma(input)
    return _out_inplace_assign(out, output, "lgamma")

def digamma(input, *, out=None):
    output = input.digamma()
    return _out_inplace_assign_with_adapter_tensor(out, output, "digamma")

def heaviside(input, values, *, out=None):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.heaviside(input_ms, values)
    return _out_inplace_assign(out, output, "heaviside")

def adjoint(input):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.adjoint(input_ms)
    return cast_to_adapter_tensor(output)

def hsplit(input, indices_or_sections):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.hsplit(input_ms, indices_or_sections)
    return cast_to_adapter_tensor(output)

def dsplit(input, indices_or_sections):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.dsplit(input_ms, indices_or_sections)
    return cast_to_adapter_tensor(output)

def tensor_split(input, indices_or_sections, dim=0):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.tensor_split(input_ms, indices_or_sections, axis=dim)
    return cast_to_adapter_tensor(output)

def vsplit(input, indices_or_sections):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.vsplit(input_ms, indices_or_sections)
    return cast_to_adapter_tensor(output)

def logdet(input):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.logdet(input_ms)
    return cast_to_adapter_tensor(output)

def polar(abs, angle, *, out=None):
    abs = cast_to_ms_tensor(abs)
    angle = cast_to_ms_tensor(angle)
    output = _get_cache_prim(ops.operations.math_ops.Polar)()(abs, angle) #TODO polar don't support Ascend now!
    return _out_inplace_assign(out, output, "polar")

def var(input, dim=None, unbiased=True, keepdim=False, *, out=None):
    input_ms = cast_to_ms_tensor(input)
    ddof = 1 if unbiased is True else 0
    output = input_ms.var(axis=dim, ddof=ddof, keepdims=keepdim)
    return _out_inplace_assign(out, output, "var")

def cdist(x1, x2, p=2.0, compute_mode='use_mm_for_euclid_dist_if_necessary'):
    unsupported_attr(compute_mode)
    x1_ms = cast_to_ms_tensor(x1)
    x2_ms = cast_to_ms_tensor(x2)
    output = ms.ops.cdist(x1_ms, x2_ms, p)
    return cast_to_adapter_tensor(output)

def atleast_1d(*tensors):
    tensors_ms = cast_to_ms_tensor(*tensors)
    outputs = ms.ops.atleast_1d(tensors_ms)
    return cast_to_adapter_tensor(outputs)

def atleast_2d(*tensors):
    tensors_ms = cast_to_ms_tensor(*tensors)
    outputs = ms.ops.atleast_2d(tensors_ms)
    return cast_to_adapter_tensor(outputs)

def atleast_3d(*tensors):
    tensors_ms = cast_to_ms_tensor(*tensors)
    outputs = ms.ops.atleast_3d(tensors_ms)
    return cast_to_adapter_tensor(outputs)

def narrow(input, dim, start, length):
    return input.narrow(dim, start, length)

def vdot(input, other, *, out=None):
    if not isinstance(input, adapter_tensor) or not isinstance(other, adapter_tensor):
        raise TypeError(f"For Tensor.vdot, input must be tensor, but got {type(input)} {type(other)}")
    if input.dtype != other.dtype:
        raise RuntimeError(f"For Tensor.vdot, expected both vectors to have same dtype, but found {input.dtype}"
                           f" and {other.dtype}")
    if input.ndim != 1 or other.ndim != 1:
        raise RuntimeError(f"For Tensor.vdot, 1D tensors expected, but got {input.ndim}D and {other.ndim}D tensors")
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    if input.is_complex():
        input = ms.ops.conj(input)
    output = ms.ops.inner(input, other)
    return _out_inplace_assign(out, output, "vdot")

def inner(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    # TODO: ms.ops.inner(ms.Tensor(2), ms.Tensor([3.2, 4.1])) will not return float type, but int type.
    output = ms.ops.inner(input, other)
    return _out_inplace_assign(out, output, "inner")

def repeat_interleave(input, repeats, dim=None, *, output_size=None):
    # TODO: replace with ms.ops.repeat_interleave. It do not support `output_size` and tensor type `repeats` yet.
    unsupported_attr(output_size)
    input_ms = cast_to_ms_tensor(input)
    if isinstance(repeats, adapter_tensor):
        repeats = cast_to_ms_tensor(repeats)
        new_repeats = []
        if repeats.ndim == 0:
            repeats = int(repeats)
        else:
            for index in repeats:
                new_repeats.append(int(index))
            repeats = new_repeats
    output = input_ms.repeat(repeats, dim)
    return cast_to_adapter_tensor(output)

def amax(input, dim, keepdim=False, *, out=None):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.amax(input_ms, dim, keepdim)
    return _out_inplace_assign(out, output, "amax")

def amin(input, dim, keepdim=False, *, out=None):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.amin(input_ms, dim, keepdim)
    return _out_inplace_assign(out, output, "amin")

def nanmean(input, dim=None, keepdim=False, *, dtype=None, out=None):
    #TODO: replace with ms.ops.nanmean
    sum_out = input.nansum(dim, keepdim, dtype=dtype)
    input_ms = cast_to_ms_tensor(input)
    not_nan = input_ms.isnan().logical_not().sum(dim, dtype, keepdim)
    output =  ms.ops.div(sum_out, not_nan)
    return _out_inplace_assign(out, output, "nanmean")

def nansum(input, dim=None, keepdim=False, *, dtype=None):
    input_ms = cast_to_ms_tensor(input)
    if dim is None:
        dim = ()
    output = ms.ops.function.math_func.nansum(input_ms, dim, keepdim, dtype=dtype)
    return cast_to_adapter_tensor(output)

def std(input, dim=None, unbiased=True, keepdim=False, *, out=None):
    output = input.std(dim, unbiased, keepdim)
    return _out_inplace_assign_with_adapter_tensor(out, output, "std")

def tile(input, dims):
    return input.tile(dims)

def vstack(tensors, *, out=None):
    tensors = cast_to_ms_tensor(tensors)
    output = ms.ops.vstack(tensors)
    return _out_inplace_assign(out, output, "vstack")

def flipud(input):
    input = cast_to_ms_tensor(input)
    output = ms.ops.flipud(input)
    return cast_to_adapter_tensor(output)

def det(input):
    input = cast_to_ms_tensor(input)
    output = ms.ops.det(input)
    return cast_to_adapter_tensor(output)

def outer(input, vec2, *, out=None):
    input = cast_to_ms_tensor(input)
    vec2 = cast_to_ms_tensor(vec2)
    output = ms.ops.outer(input, vec2)
    return _out_inplace_assign(out, output, "outer")

def ger(input, vec2, *, out=None):
    input = cast_to_ms_tensor(input)
    vec2 = cast_to_ms_tensor(vec2)
    if input.dtype != vec2.dtype:
        raise TypeError("For torch.ger(), input and vec2 dtype must be the same")
    if not input.is_floating_point():
        _out_dtype = input.dtype
        input = input.astype(ms.float32)
        vec2 = vec2.astype(ms.float32)
        output = ms.ops.ger(input, vec2)
        output = output.astype(_out_dtype)
    else:
        output = ms.ops.ger(input, vec2)
    return _out_inplace_assign(out, output, "ger")

def svd(input, some=True, compute_uv=True, *, out=None):
    output = input.svd(some, compute_uv)
    return _out_inplace_assign_with_adapter_tensor(out, output, "svd")

def unique_consecutive(input, return_inverse=False, return_counts=False, dim=None) :
    input = cast_to_ms_tensor(input)
    output = ms.ops.unique_consecutive(input, return_idx=return_inverse, return_counts=return_counts, axis=dim)
    return cast_to_adapter_tensor(output)

def block_diag(*tensors):
    inputs = cast_to_ms_tensor(tensors)
    output = ms.ops.block_diag(*inputs)
    return cast_to_adapter_tensor(output)

def logspace(start, end, steps, base=10.0, *, out=None, dtype=None, layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    start = ms.Tensor(start, dtype=dtype)
    end = ms.Tensor(end, dtype=dtype)
    # TODO: ms.ops.logspace only support base is int type
    if base % 1 != 0:
        raise ValueError("For logspace, base only support integer")
    base = int(base)
    if dtype is None:
        dtype = ms.float32
    _dtype = dtype

    if start.dtype in all_int_type or end.dtype in all_int_type or dtype in all_int_type:
        start = start.astype(mstype.float32)
        end = end.astype(mstype.float32)
        _dtype = mstype.float32
    output = ms.ops.logspace(start, end, steps, base, dtype=_dtype)
    output = output.astype(dtype)
    return _out_inplace_assign(out, output, "logspace")

def column_stack(tensors, *, out=None):
    tensors = cast_to_ms_tensor(tensors)
    output = ms.ops.column_stack(tensors)
    return _out_inplace_assign(out, output, "column_stack")

def hstack(tensors, *, out=None):
    tensors = cast_to_ms_tensor(tensors)
    output = ms.ops.hstack(tensors)
    return _out_inplace_assign(out, output, "hstack")

def movedim(input, source, destination):
    input = cast_to_ms_tensor(input)
    output = ms.ops.movedim(input, source,destination)
    return cast_to_adapter_tensor(output)

def moveaxis(input, source, destination):
    input = cast_to_ms_tensor(input)
    output = ms.ops.moveaxis(input, source,destination)
    return cast_to_adapter_tensor(output)

def swapdims(input, dim0, dim1):
    input = cast_to_ms_tensor(input)
    output = ms.ops.swapdims(input, dim0, dim1)
    return cast_to_adapter_tensor(output)

def swapaxes(input, axis0, axis1):
    input = cast_to_ms_tensor(input)
    if input.nelement() == 0:
        out_shape = list(input.shape)
        out_shape[axis0], out_shape[axis1] = out_shape[axis1], out_shape[axis0]
        output = input.reshape(tuple(out_shape))
    else:
        output = ms.ops.swapaxes(input, axis0, axis1)
    return cast_to_adapter_tensor(output)

def row_stack(tensors, *, out=None):
    tensors = cast_to_ms_tensor(tensors)
    output = ms.ops.vstack(tensors)
    return _out_inplace_assign(out, output, "row_stack")

def matrix_exp(A):
    input = cast_to_ms_tensor(A)
    # TODO: ms.ops.matrix_exp to supported GPU
    output = ms.ops.matrix_exp(input)
    return cast_to_adapter_tensor(output)

def argwhere(input):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.argwhere(input_ms)
    return cast_to_adapter_tensor(output)

def mv(input, vec, *, out=None):
    # TODO: On Ascend, ms.ops.mv not support float64 and int16 input
    input = cast_to_ms_tensor(input)
    vec = cast_to_ms_tensor(vec)
    output = ms.ops.mv(input, vec)
    return _out_inplace_assign(out, output, "mv")

def blackman_window(window_length, periodic=True, *, dtype=None, layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    input = ms.Tensor(window_length)
    output = ms.ops.blackman_window(input, periodic=periodic, dtype=dtype)
    return cast_to_adapter_tensor(output)

def tril_indices(row, col, offset=0, *, dtype=mstype.int64, device=None, layout=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    # 'dtype' in ms.ops.tril_indices only support {int32, int64}
    output = ms.ops.tril_indices(row, col, offset=offset).astype(dtype)
    return cast_to_adapter_tensor(output)

def triu_indices(row, col, offset=0, *, dtype=mstype.int64, device=None, layout=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    # 'dtype' in ms.ops.triu_indices only support {int32, int64}
    output = ms.ops.triu_indices(row, col, offset=offset).astype(dtype)
    return cast_to_adapter_tensor(output)

def geqrf(input, *, out=None):
    input = cast_to_ms_tensor(input)
    output = ms.ops.geqrf(input)
    return _out_inplace_assign(out, output, "geqrf")

def _set_trapz_dtype(y, x):
    if x is None:
        if y.is_floating_point():
            return y.dtype
    else:
        if y.dtype == ms.float32 or x.dtype == ms.float32:
            return ms.float32
        if y.dtype == ms.float16 or x.dtype == ms.float16:
            return ms.float16
    return ms.float32

def trapz(y, x=None, *, dim=-1):
    y = cast_to_ms_tensor(y)
    dtype = _set_trapz_dtype(y, x)
    output = ms.ops.trapz(y, x=x, dx=1.0, dim=dim).astype(dtype)
    return cast_to_adapter_tensor(output)

def trapezoid(y, x=None, *, dx=None, dim=-1):
    y = cast_to_ms_tensor(y)
    if dx is None:
        dx = 1.
    dtype = _set_trapz_dtype(y, x)
    output = ms.ops.trapz(y, x=x, dx=float(dx), dim=dim).astype(dtype)
    return cast_to_adapter_tensor(output)

def bucketize(input, boundaries, *, out_int32=False, right=False, out=None):
    input = cast_to_ms_tensor(input)
    boundaries = cast_to_ms_tensor(boundaries).astype(ms.float32).numpy()
    if right is False:
        boundaries += 1
    boundaries = boundaries.tolist()
    net = ms.ops.Bucketize(boundaries)
    output = net(input)
    if out_int32 is True:
        output = output.astype(ms.int32)
    else:
        output = output.astype(ms.int64)
    return _out_inplace_assign(out, output, "bucketize")

def lcm(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.lcm(input, other)
    return _out_inplace_assign(out, output, "lcm")

def renorm(input, p, dim, maxnorm, *, out=None):
    # TODO: ms.ops.renorm not support `p` as float number
    input = cast_to_ms_tensor(input)
    output = ms.ops.renorm(input, int(p), dim, float(maxnorm))
    return _out_inplace_assign(out, output, "renorm")

def tensordot(a, b, dims=2, out=None):
    a = cast_to_ms_tensor(a)
    b = cast_to_ms_tensor(b)
    output = ms.ops.tensor_dot(a, b, dims)
    return _out_inplace_assign(out, output, "tensordot")

def randn_like(input, *, dtype=None, layout=None, device=None, requires_grad=False, memory_format=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(memory_format)
    input = cast_to_ms_tensor(input)
    input_shape = input.shape
    if not dtype:
        dtype = input.dtype
    output = from_numpy(np.random.randn(*input_shape)).to(dtype)
    return output

def rand_like(input, *, dtype=None, layout=None, device=None, requires_grad=False, memory_format=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(memory_format)
    input = cast_to_ms_tensor(input)
    input_shape = input.shape
    if not dtype:
        dtype = input.dtype
    output = from_numpy(np.random.rand(*input_shape)).to(dtype)
    return output

def kron(input, other, *, out=None):
    # TODO: support inputs of different complex type
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.kron(input, other)
    return _out_inplace_assign(out, output, "kron")

def gcd(input, other, *, out=None):
    input = cast_to_ms_tensor(input)
    other = cast_to_ms_tensor(other)
    output = ms.ops.gcd(input, other)
    return _out_inplace_assign(out, output, "gcd")

def index_add(input, dim, index, source, *, alpha=1, out=None):
    # TODO: support input of more than 2-D & dim >= 1
    output = input.index_add(dim, index, source, alpha=alpha)
    return _out_inplace_assign(out, output, "index_add")

def index_copy(input, dim, index, source, *, out=None):
    output = input.index_copy(dim, index, source)
    return _out_inplace_assign(out, output, "index_copy")

def scatter_add(input, dim, index, src):
    # TODO: support src and index of different shape
    # ms.ops.scatter_add has more restrictions on the shape of inputs
    return input.scatter_add(dim, index, src)

def scatter_reduce(input, dim, index, src, reduce, *, include_self=True):
    # TODO: to support reduce='mean'
    return input.scatter_reduce(dim, index, src, reduce, include_self=include_self)

def std_mean(input, dim=None, unbiased=None, keepdim=False, *, out=None):
    # TODO: replace with ms.ops.std_mean()
    input = cast_to_ms_tensor(input)
    _dim = dim if dim is not None else ()
    _ddof = unbiased if unbiased is not None else True
    if is_under_ascend_context() and input.dtype == ms.float64:
        input1 = input.astype(ms.float32)
        std = input1.std(_dim, _ddof, keepdim)
        std = std.astype(ms.float64)
    else:
        std = input.std(_dim, _ddof, keepdim)

    if dim is not None:
        mean = ms.ops.mean(input, axis=dim, keep_dims=keepdim)
    else:
        mean = ms.ops.mean(input, keep_dims=keepdim)
    output = (std, mean)
    return _out_inplace_assign(out, output, "std_mean")

def clone(input, *, memory_format=None):
    unsupported_attr(memory_format)
    input = cast_to_ms_tensor(input)
    output = input.copy()
    return cast_to_adapter_tensor(output)

def slice_scatter(input, src, dim=0, start=None, end=None, step=1):
    return input.slice_scatter(src, dim, start, end, step)

def select_scatter(input, src, dim, index):
    return input.select_scatter(src, dim, index)

def dstack(tensors, *, out=None):
    # TODO: set output dtype to the dtype of tensor with higher accuracy
    tensors = cast_to_ms_tensor(tensors)
    output = ms.ops.dstack(tensors)
    return _out_inplace_assign(out, output, "dstack")

def randint_like(input, low=None, high=None, *, dtype=None,
                 layout=None, device=None, requires_grad=False, memory_format=None):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(memory_format)
    input = cast_to_ms_tensor(input)

    input_type = input.dtype
    if input_type not in all_int_type:
        input = input.round().int()

    output_type = input_type
    if dtype is not None:
        output_type = dtype

    if dtype not in all_int_type:
        _dtype = None
    else:
        _dtype = dtype

    if low is None and high is None:
        raise ValueError('`low` and `high` in `randint_like` shoud not both be None.')
    elif high is None:
        output = ms.ops.randint_like(input, low=0, high=low, dtype=_dtype)
    elif low is None:
        output = ms.ops.randint_like(input, low=0, high=high, dtype=_dtype)
    else:
        output = ms.ops.randint_like(input, low=low, high=high, dtype=_dtype)

    output = output.astype(output_type)
    return cast_to_adapter_tensor(output)

def kaiser_window(window_length, periodic=True, beta=12.0, *, dtype=None,
                  layout=None, device=None, requires_grad=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    output = ms.ops.kaiser_window(window_length, periodic=periodic, beta=beta)
    # TODO: ms.ops.kaiser_window will raise error when dtype=ms.float32
    if dtype is not None:
        output = output.astype(dtype)
    else:
        # TODO: use global default set by ms.ops.set_default_tensor_type
        output = output.astype(ms.float32)
    return cast_to_adapter_tensor(output)

def cartesian_prod(*tensors):
    input_tensor = cast_to_ms_tensor(tensors)
    output = ms.ops.cartesian_prod(*input_tensor)
    return cast_to_adapter_tensor(output)

def combinations(input, r=2, with_replacement=False):
    input_ms = cast_to_ms_tensor(input)
    output = ms.ops.combinations(input_ms, r=r, with_replacement=with_replacement)
    return cast_to_adapter_tensor(output)

def var_mean(input, dim=None, unbiased=True, keepdim=False, *, out=None):
    input_ms = cast_to_ms_tensor(input)
    ddof = 1 if unbiased is True else 0
    var = input_ms.var(axis=dim, ddof=ddof, keepdims=keepdim)

    # TODO: not supprt GRAPH_MODE
    if dim is not None:
        mean = ms.ops.mean(input, axis=dim, keep_dims=keepdim)
    else:
        mean = ms.ops.mean(input, keep_dims=keepdim)
    output = (var, mean)
    return _out_inplace_assign(out, output, "var_mean")

def poisson(input, generator=None):
    # TODO: when call ms.set_seed(), ms.ops.random_poisson will generate the same value in every call.
    if generator is not None:
        raise NotImplementedError("adapter not support generator.")
    if is_under_ascend_context():
        output = poisson_op(input)
    else:
        input_ms = cast_to_ms_tensor(input)
        shape = ms.Tensor([], mstype.int32)
        output = ms.ops.random_poisson(shape, input_ms, dtype=input_ms.dtype)
    return cast_to_adapter_tensor(output)

#TODO: eig currently not support on GPU
def eig(input, *, out=None):
    if is_under_gpu_context():
        raise NotImplementedError("for adapter, eig not supported on GPU")
    output = input.eig()
    return _out_inplace_assign_with_adapter_tensor(out, output, "eig")

def is_nonzero(input):
    input = cast_to_ms_tensor(input)
    if input.numel() != 1:
        raise RuntimeError("`input` of `is_nonzero` must be a single element tensor")
    return bool(input != ms.Tensor(0))

def isin(elements, test_elements, *, assume_unique=False, invert=False):
    if assume_unique is True:
        raise NotImplementedError("Numpy argument `assume_unique` is not supported since the implementation does:",
                                  "not rely on the uniqueness of the input arrays.")
    elements = cast_to_ms_tensor(elements)
    test_elements = cast_to_ms_tensor(test_elements)
    output = ms.numpy.isin(elements, test_elements, invert=invert)
    return cast_to_adapter_tensor(output)

def normal(mean, std=1.0, size=None, *, generator=None, out=None):
    # TODO: ms.ops.normal doesn't take float64 inputs
    unsupported_attr(generator)
    mean = cast_to_ms_tensor(mean)
    std = cast_to_ms_tensor(std)
    if isinstance(mean, numbers.Number):
        if isinstance(std, numbers.Number):
            if size is None:
                raise ValueError('`size` should not be None when `mean` and `std` are both float types.')
            else:
                shape = tuple(size)
                dtype = ms.float32
        else:
            shape = std.shape
            dtype = std.dtype
    else:
        shape = mean.shape
        dtype = mean.dtype
    output = ms.ops.normal(shape, mean, std).astype(dtype)
    return _out_inplace_assign(out, output, "normal")

def orgqr(input, tau):
    return input.orgqr(tau)

def vander(x, N=None, increasing=False, *, out=None):
    x = cast_to_ms_tensor(x)
    #TODO: need to use ops func
    output = ms.numpy.vander(x, N, increasing)
    return _out_inplace_assign(out, output, "vander")

def bernoulli(input, *, generator=None, out=None):
    output = input.bernoulli(generator=generator)
    return _out_inplace_assign(out, output, "bernoulli")

#TODO: Currently not support float64 dtype
def histogramdd(input, bins=10, *, range=None, weight=None, density=False, out=None):
    input = cast_to_ms_tensor(input)
    #TODO: Currently not support ops func
    if range is not None:
        range = ms.ops.reshape(ms.Tensor(range), (-1, input.shape[1]))
        range = cast_to_adapter_tensor(range).tolist()
    hist, bin_edges = ms.numpy.histogramdd(input, bins=bins, range=range, weights=weight, density=density)
    output = (hist, bin_edges)
    if pynative_mode_condition():
        svd_namedtuple = set_multiple_name_tuple('histogramdd', 'hist, bin_edges')
        output = svd_namedtuple(cast_to_adapter_tensor(hist), cast_to_adapter_tensor(bin_edges))
        return output
    return _out_inplace_assign(out, output, "histogramdd")

def diag_embed(input, offset=0, dim1=-2, dim2=-1, *, out=None):
    output = input.diag_embed(offset=offset, dim1=dim1, dim2=dim2)
    return _out_inplace_assign(out, output, "diag_embed")

def is_neg(input):
    if not hasattr(input, "neg_bit"):
        return False
    else:
        return input.neg_bit

def resolve_neg(input):
    output = deepcopy(input)
    output.neg_bit = False
    return output

#TODO: pinv currently not support on Ascend
def pinverse(input, rcond=1e-15, *, out=None):
    if is_under_ascend_context():
        raise NotImplementedError("pinverse currently not supported on Ascend")
    output = input.pinverse(rcond=rcond)
    return _out_inplace_assign_with_adapter_tensor(out, output, "pinverse")

#TODO: use ops func
def asarray(obj, *, dtype=None, device=None, copy=None, requires_grad=False):
    unsupported_attr(device)
    unsupported_attr(copy)
    unsupported_attr(requires_grad)
    return cast_to_adapter_tensor(ms.numpy.asarray(obj, dtype=dtype))

def symeig(input, eigenvectors=False, upper=True, *, out=None):
    output = input.symeig(eigenvectors=eigenvectors, upper=upper)
    if pynative_mode_condition():
        if out is not None:
            if len(out) != 2 or not isinstance(out[0], adapter_tensor) or not isinstance(out[1], adapter_tensor):
                raise TypeError("In msadapter.torch.symeig(), `out` should be tuple of Tensors.")
            out[0].assign_value(ms.Tensor(output[0].asnumpy(), dtype=out[0].dtype))
            out[1].assign_value(output[1])
            return out
        return output
    return _out_inplace_assign_with_adapter_tensor(out, output, "symeig")

#TODO: currently numpy.result_type not support complex
def result_type(tensor1, tensor2):
    type_index = [ms.bool_, ms.uint8, ms.uint16, ms.uint32, ms.uint64, ms.int8, ms.int16, ms.int32, \
                  ms.int64, ms.float16, float, ms.float32, ms.float64, ms.complex64, ms.complex128]
    tensor1 = cast_to_ms_tensor(tensor1)
    tensor2 = cast_to_ms_tensor(tensor2)
    if isinstance(tensor1, ms.Tensor):
        tensor1_type = tensor1.dtype
    else:
        tensor1_type = type(tensor1)
    if isinstance(tensor2, ms.Tensor):
        tensor2_type = tensor2.dtype
    else:
        tensor2_type = type(tensor2)
    if not tensor1_type in [complex, ms.complex64, ms.complex128] \
       and not tensor2_type in [complex, ms.complex64, ms.complex128]:
        output = ms.numpy.result_type(tensor1, tensor2)
    else:
        tensor1_index = type_index.index(tensor1_type)
        tensor2_index = type_index.index(tensor2_type)
        float64_index = type_index.index(ms.float64)
        high = tensor1_index if tensor1_index > tensor2_index else tensor2_index
        low = tensor1_index if tensor1_index < tensor2_index else tensor2_index
        if high > float64_index and low != float64_index:
            output = type_index[high]
        else:
            output =  ms.complex128
    return output

#TODO: currently not support float16 input
def complex(real, imag, *, out=None):
    real = cast_to_ms_tensor(real)
    imag = cast_to_ms_tensor(imag)
    output = _get_cache_prim(ms.ops.Complex)()(real, imag)
    return _out_inplace_assign(out, output, "complex")

def logcumsumexp(input, dim, *, out=None):
    output = input.logcumsumexp(dim=dim)
    return _out_inplace_assign_with_adapter_tensor(out, output, "logcumsumexp")

def kthvalue(input, k, dim=None, keepdim=False, *, out=None):
    output = input.kthvalue(k, dim, keepdim)
    if pynative_mode_condition():
        if out is not None:
            if len(out) != 2 or not isinstance(out[0], adapter_tensor) or not isinstance(out[1], adapter_tensor):
                raise TypeError("In msadapter.torch.kthvalue(), `out` should be tuple of Tensors.")
            out[0].assign_value(output[0])
            out[1].assign_value(output[1])
            return out
        return output
    return _out_inplace_assign_with_adapter_tensor(out, output, "kthvalue")

def broadcast_shapes(*shapes):
    max_len = 0
    for shape in shapes:
        if isinstance(shape, int):
            max_len = max_len if max_len > 1 else 1
        elif isinstance(shape, (tuple, list)):
            s = len(shape)
            max_len = max_len if max_len > s else s
    result = [1] * max_len
    for shape in shapes:
        if isinstance(shape, int):
            shape = (shape,)
        if isinstance(shape, (tuple, list)):
            for i in range(-1, -1 - len(shape), -1):
                if shape[i] < 0:
                    raise RuntimeError("Trying to create tensor with negative dimension ({}): ({})"
                                        .format(shape[i], shape[i]))
                if shape[i] == 1 or shape[i] == result[i]:
                    continue
                if result[i] != 1:
                    raise RuntimeError("Shape mismatch: objects cannot be broadcast to a single shape")
                result[i] = shape[i]
        else:
            raise RuntimeError("Input shapes should be of type ints, a tuple of ints, or a list of ints, got ", shape)
    return result

def broadcast_tensors(*tensors):
    tensor_shape = []
    for tensor in tensors:
        tensor_shape.append(tensor.shape)
    shape = broadcast_shapes(*tensor_shape)
    shape = tuple(shape)
    output = []
    for tensor in tensors:
        tensor = cast_to_ms_tensor(tensor)
        output.append(ms.ops.broadcast_to(tensor, shape))
    return output

def index_reduce(input, dim, index, source, reduce, *, include_self=True, out=None):
    output = input.index_reduce(dim, index, source, reduce, include_self=include_self)
    return _out_inplace_assign(out, output, "index_reduce")

def view_as_complex(input):
    input_ms = cast_to_ms_tensor(input)
    real = input_ms[..., 0]
    imag = input_ms[..., 1]
    output = complex(real, imag)
    return cast_to_adapter_tensor(output)

def chain_matmul(*matrices, out=None):
    input_ms = cast_to_ms_tensor(matrices)
    output = ms.numpy.multi_dot(input_ms)
    return _out_inplace_assign(out, output, "chain_matmul")

def empty_strided(size, stride, *, dtype=None, layout=None, device=None, requires_grad=False, pin_memory=False):
    unsupported_attr(layout)
    unsupported_attr(device)
    unsupported_attr(requires_grad)
    unsupported_attr(pin_memory)
    size = cast_to_ms_tensor(size)
    stride = cast_to_ms_tensor(stride)
    output = ms.numpy.empty(size, dtype)
    output = cast_to_adapter_tensor(output)
    output = output.as_strided(size, stride)
    return output

def cumulative_trapezoid(y, x=None, *, dx=None, dim=-1):
    y = cast_to_ms_tensor(y)
    if y.dtype in (ms.int32, ms.int64):
        y = y.astype(ms.float32)
    if dx is None:
        dx = 1
    if x is not None:
        x = cast_to_ms_tensor(x)
        if x.ndim > 1:
            while x.ndim < y.ndim:
                x = x.unsqueeze(0)
        dx_high = x.index_select(dim, ms.ops.arange(1, x.shape[dim]))
        dx_low = x.index_select(dim, ms.ops.arange(0, x.shape[dim] - 1))
        dx = dx_high - dx_low
    y_high = y.index_select(dim, ms.ops.arange(1, y.shape[dim]))
    y_low = y.index_select(dim, ms.ops.arange(0, y.shape[dim] - 1))
    height = (y_high + y_low) / 2
    areas = height * dx
    cum_areas = areas.cumsum(dim)
    output = ms.ops.cat([cum_areas], dim)
    if y.dtype == ms.float64:
        output = output.astype(ms.float64)
    return cast_to_adapter_tensor(output)

@_primexpr
def _bit_index(x):
    index = 0
    if x == ms.bool_:
        index = 1
    elif x in all_int_type:
        index = 2
    elif x in all_float_type:
        index = 3
    elif x in all_complex_type:
        index = 4
    else:
        raise ValueError('input dtype `{x}` is not legal torch dtype')
    return index

def can_cast(from_dtype, to_dtype):
    from_index =_bit_index(from_dtype)
    to_index =_bit_index(to_dtype)
    output = from_index <= to_index
    return output

def _warn_msg_for_deterministic_apis(func_name):
    if is_under_ascend_context():
        warnings.warn(f"Interface '{func_name}' on Ascend behaves differently than torch. "
                      f"It can not change the actual behavior of nondeterministic operations, "
                      f"but can only get or set the global variable."
                      f"For more details, please go to"
                      f"https://www.mindspore.cn/docs/zh-CN/master/api_python/mindspore/mindspore.set_context.html"
                      f"?highlight=deterministic")
    else:
        raise RuntimeError(f"interface '{func_name}' is not supported on GPU or CPU")

def set_deterministic_debug_mode(debug_mode):
    _warn_msg_for_deterministic_apis("set_deterministic_debug_mode")
    if debug_mode in ["default", 0]:
        ms.context.set_context(deterministic='OFF')
    elif debug_mode in ["warn", "error", 1, 2]:
        ms.context.set_context(deterministic='ON')
    else:
        ValueError(f"set_deterministic_debug_mode(): argument 'debug_mode' must be 'default', 'warn', 'error', "
                   f"0, 1, or 2 , but got {debug_mode}")

def get_deterministic_debug_mode():
    _warn_msg_for_deterministic_apis("get_deterministic_debug_mode")
    flag = ms.context.get_context("deterministic")
    if flag == 'OFF':
        return 0
    else:
        return 1

def are_deterministic_algorithms_enabled():
    _warn_msg_for_deterministic_apis("are_deterministic_algorithms_enabled")
    flag = ms.context.get_context("deterministic")
    if flag == 'OFF':
        return False
    else:
        return True

def is_deterministic_algorithms_warn_only_enabled():
    _warn_msg_for_deterministic_apis("is_deterministic_algorithms_warn_only_enabled")
    return False

def use_deterministic_algorithms(mode, *, warn_only=False):
    unsupported_attr(warn_only)
    _warn_msg_for_deterministic_apis("use_deterministic_algorithms")
    if mode is False:
        ms.context.set_context(deterministic='OFF')
    else:
        ms.context.set_context(deterministic='ON')

def diagonal_scatter(input, src, offset=0, dim1=0, dim2=1):
    return input.diagonal_scatter(src, offset, dim1, dim2)

lu_solve = linalg_lu_solve
matrix_power = linalg_matrix_power
