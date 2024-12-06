# Copyright (C) Marlin.2024 Elias Frantar (elias.frantar@ist.ac.at)
# GPTQModel/licences/LICENSE.apache

import numpy as np
import torch
import torch.nn.functional as F
from gptqmodel.nn_modules.qlinear import BaseQuantLinear

from ...utils.logger import setup_logger

marlin_import_exception = None
try:
    import gptqmodel_marlin_cuda
except ImportError as e:
    marlin_import_exception = e

logger = setup_logger()


def mul(A, B, C, s, workspace, thread_k=-1, thread_n=-1, sms=-1, max_par=16):
    """Marlin FP16xINT4 multiply; can be used within `torch.compile`.
    @A: `torch.half` input matrix of shape `(m, k)` in standard row-major layout
    @B: `torch.int` weight matrix of original shape `(k, n)` in Marlin format; see `Layer.pack()`
    @C: `torch.half` out matrix of shape `(m, n)` in standard row-major layout
    @s: `torch.half` scales of shape `(m / group_size, n)`
    @workspace: `torch.int` tensor with at least `n / 128 * max_par` entries that are all zero
    @thread_k: `k` size of a thread_tile in `B` (can usually be left as auto -1)
    @thread_n: `n` size of a thread_tile in `B` (can usually be left as auto -1)
    @sms: number of SMs to use for the kernel (can usually be left as auto -1)
    @max_par: maximum number of batch 64 problems to solve in parallel for large input sizes
    """
    gptqmodel_marlin_cuda.mul(A, B, C, s, workspace, thread_k, thread_n, sms, max_par)


# Precompute permutations for Marlin weight and scale shuffling
def _get_perms():
    perm = []
    for i in range(32):
        perm1 = []
        col = i // 4
        for block in [0, 1]:
            for row in [
                2 * (i % 4),
                2 * (i % 4) + 1,
                2 * (i % 4 + 4),
                2 * (i % 4 + 4) + 1,
            ]:
                perm1.append(16 * row + col + 8 * block)
        for j in range(4):
            perm.extend([p + 256 * j for p in perm1])

    perm = np.array(perm)
    interleave = np.array([0, 2, 4, 6, 1, 3, 5, 7])
    perm = perm.reshape((-1, 8))[:, interleave].ravel()
    perm = torch.from_numpy(perm)
    scale_perm = []
    for i in range(8):
        scale_perm.extend([i + 8 * j for j in range(8)])
    scale_perm_single = []
    for i in range(4):
        scale_perm_single.extend([2 * i + j for j in [0, 1, 8, 9, 16, 17, 24, 25]])
    return perm, scale_perm, scale_perm_single


_perm, _scale_perm, _scale_perm_single = _get_perms()


class MarlinQuantLinear(BaseQuantLinear):
    SUPPORTS_BITS = [4]
    SUPPORTS_GROUP_SIZE = [128, -1]
    SUPPORTS_DESC_ACT = [False]
    SUPPORTS_SYM = [True]

    def __init__(self, bits: int, group_size: int, desc_act: bool, sym: bool, infeatures: int, outfeatures: int,
                 bias: bool, **kwargs):
        if marlin_import_exception is not None:
            raise ValueError(
                f"Trying to use the marlin backend, but could not import the C++/CUDA dependencies with the following error: {marlin_import_exception}"
            )

        super().__init__(bits=bits, group_size=group_size, sym=sym, desc_act=desc_act, infeatures=infeatures, outfeatures=outfeatures, **kwargs)
        if not torch.cuda.get_device_capability()[0] >= 8:
            raise ValueError(
                f'Can not use Marlin int4*fp16 kernel with a device of compute capability {torch.cuda.get_device_capability()}, the minimum compute capability is 8.0 for Marlin kernel. Please do not use `backend=Backend.MARLIN`, or please upgrade your GPU ("The more you buy, the more you save." - Taiwanese proverb).'
            )

        # if infeatures % 128 != 0 or outfeatures % 256 != 0:
        #     raise ValueError("`infeatures` must be divisible by 128 and `outfeatures` by 256.")
        if group_size not in [-1, 128] and group_size != infeatures:
            raise ValueError("Only group_size -1 and 128 are supported.")
        # # Marlin groups infeatures according to group_size, so infeatures must be an integer multiple of group_size.
        # if infeatures % group_size != 0:
        #     raise ValueError("`infeatures` must be divisible by `group_size`.")


        self.original_infeatures = infeatures
        self.original_outfeatures = outfeatures

        self.infeatures = infeatures + (-infeatures % 128)
        self.outfeatures = outfeatures + (-outfeatures % 256)

        self.group_size = group_size if group_size != -1 else infeatures

        self.register_buffer(
            "B",
            torch.empty((self.infeatures // 16, self.outfeatures * 16 // 8), dtype=torch.int),
        )
        self.register_buffer(
            "s",
            torch.empty((self.infeatures // self.group_size, self.outfeatures), dtype=torch.half),
        )
        # 128 is currently the minimum `tile_n`, hence it gives the maximum workspace size; 16 is the default `max_par`
        self.register_buffer(
            "workspace",
            torch.zeros(self.outfeatures // 128 * 16, dtype=torch.int),
            persistent=False,
        )
        if bias:
            self.register_buffer("bias", torch.zeros((self.outfeatures), dtype=torch.half))
        else:
            self.bias = None


    def pack(self, linear, scales):
        """Pack a fake-quantized linear layer into this actual Marlin representation.
        @linear: fake-quantized `torch.nn.Linear` layer to convert (must be of type `torch.half`)
        @scales: corresponding quantization scales of shape `(infeatures, groups)`
        """
        # 'linear' is a torch.nn.Linear module
        if linear.weight.dtype != torch.half:
           #logger.warning(
           #    f"Only `torch.half` linear.weights are supported. Converting from {linear.weight.dtype} to torch.half")
           linear.weight.data = linear.weight.data.to(torch.float16)

        tile = 16
        maxq = 2**4 - 1
        s = scales.t()
        w = linear.weight.data.t()

        if self.infeatures != self.original_infeatures or self.outfeatures != self.original_outfeatures:
            padded_w = torch.zeros((self.infeatures, self.outfeatures), dtype=w.dtype, device=w.device)
            padded_w[:w.size(0), :w.size(1)] = w
            w = padded_w

            padded_s = torch.zeros((s.size(0), self.outfeatures), dtype=torch.half, device=s.device)
            padded_s[:s.size(0), :s.size(1)] = s
            s = padded_s

        if self.group_size != self.infeatures:
            w = w.reshape((-1, self.group_size, self.outfeatures))
            w = w.permute(1, 0, 2)
            w = w.reshape((self.group_size, -1))
            s = s.reshape((1, -1))
        w = torch.round(w / s).int()
        w += (maxq + 1) // 2
        w = torch.clamp(w, 0, maxq)
        if self.group_size != self.infeatures:
            w = w.reshape((self.group_size, -1, self.outfeatures))
            w = w.permute(1, 0, 2)
            w = w.reshape((self.infeatures, self.outfeatures)).contiguous()
            s = s.reshape((-1, len(_scale_perm)))[:, _scale_perm]
        else:
            s = s.reshape((-1, len(_scale_perm_single)))[:, _scale_perm_single]
        s = s.reshape((-1, self.outfeatures)).contiguous()
        w = w.reshape((self.infeatures // tile, tile, self.outfeatures // tile, tile))
        w = w.permute((0, 2, 1, 3))
        w = w.reshape((self.infeatures // tile, self.outfeatures * tile))
        res = w
        res = res.reshape((-1, _perm.numel()))[:, _perm].reshape(res.shape)
        q = np.zeros((res.shape[0], res.shape[1] // 8), dtype=np.uint32)
        res = res.cpu().numpy().astype(np.uint32)
        for i in range(8):
            q |= res[:, i::8] << 4 * i
        q = torch.from_numpy(q.astype(np.int32)).to(w.device)

        self.B[:, :] = q.to(self.B.device)
        self.s[:, :] = s.to(self.s.device)

        if linear.bias is not None:
            if self.bias is not None:
                self.bias[:] = linear.bias.data.to(self.bias.device)
            else:
                self.bias = linear.bias.clone()

    def forward(self, A):
        A = A.half()

        # padding
        if A.size(-1) != self.infeatures:
            A = F.pad(A, (0, self.infeatures - self.original_infeatures))

        C = torch.empty(A.shape[:-1] + (self.s.shape[1],), dtype=A.dtype, device=A.device)
        mul(
            A.view((-1, A.shape[-1])),
            self.B,
            C.view((-1, C.shape[-1])),
            self.s,
            self.workspace,
        )
        C = C + self.bias if self.bias is not None else C

        # revert padding
        if self.outfeatures != self.original_outfeatures:
            return C[:, :, :self.original_outfeatures]
        else:
            return C

    def post_init(self):
        self.validate_device(self.B.device.type)

# Copied from https://github.com/IST-DASLab/marlin/pull/1
@torch.no_grad()
def unpack_4bit_to_32bit_signed(qweight, qzeros):
    # Unpack 4-bit values and interpret them as signed integers
    unpacked_weights = torch.zeros(
        (qweight.shape[0] * 8, qweight.shape[1]),
        dtype=torch.int8,
        device=qweight.device,
        requires_grad=False,
    )

    unpacked_zeros = torch.zeros(
        (qzeros.shape[0], qzeros.shape[1] * 8),
        dtype=torch.int8,
        device=qzeros.device,
        requires_grad=False,
    )

    for row in range(unpacked_weights.shape[0]):
        i = row % 8
        unpacked_weights[row, :] = (qweight[row // 8, :] >> (4 * i)) & 0xF

    for col in range(unpacked_zeros.shape[1]):
        i = col % 8
        unpacked_zeros[:, col] = (qzeros[:, col // 8] >> (4 * i)) & 0xF

    return unpacked_weights, unpacked_zeros


def unpack_qzeros(qzeros):
    unpacked_zeros = torch.zeros(
        (qzeros.shape[0], qzeros.shape[1] * 8),
        dtype=torch.int8,
        device=qzeros.device,
        requires_grad=False,
    )

    for col in range(unpacked_zeros.shape[1]):
        i = col % 8
        unpacked_zeros[:, col] = (qzeros[:, col // 8] >> (4 * i)) & 0xF

    return unpacked_zeros


# Copied from https://github.com/IST-DASLab/marlin/pull/1
@torch.no_grad()
def dequantize_weight(layer):
    qweight, qzeros, scales = layer.qweight, layer.qzeros, layer.scales
    unpacked_qweight, unpacked_qzeros = unpack_4bit_to_32bit_signed(qweight, qzeros)
    unpacked_qzeros = torch.clamp(unpacked_qzeros, min=0, max=15)
    group_size = unpacked_qweight.shape[0] // scales.shape[0]
    scales = scales.repeat_interleave(group_size, dim=0)
    unpacked_qzeros = unpacked_qzeros.repeat_interleave(group_size, dim=0)
    unpacked_qweight = (unpacked_qweight - unpacked_qzeros) * scales

    return unpacked_qweight.T, unpacked_qzeros


def dequantize_qzeros(layer):
    qzeros = layer.qzeros
    unpacked_qzeros = unpack_qzeros(qzeros)
    group_size = layer.group_size
    unpacked_qzeros = unpacked_qzeros.repeat_interleave(group_size, dim=0)

    return unpacked_qzeros


__all__ = ["MarlinQuantLinear", "dequantize_weight"]
