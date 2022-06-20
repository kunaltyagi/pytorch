

# Owner(s): ["oncall: quantization"]

import torch
from torch import quantize_per_tensor
from torch.ao.quantization.experimental.APoT_tensor import TensorAPoT
import unittest
import random
quantize_APoT = TensorAPoT.quantize_APoT
dequantize = TensorAPoT.dequantize

class TestQuantizedTensor(unittest.TestCase):
    r""" Tests quantize_APoT result (int representation) on random 1-dim tensor
        and hardcoded values for b, k by comparing to uniform quantization
        (non-uniform quantization reduces to uniform for k = 1)
        quantized tensor (https://pytorch.org/docs/stable/generated/torch.quantize_per_tensor.html)
        * tensor2quantize: Tensor
        * b: 4
        * k: 1
    """
    def test_quantize_APoT_rand_1d(self):
        # generate random size of tensor2dequantize between 1 -> 20
        size = random.randint(1, 20)

        # generate tensor with random fp values
        tensor2quantize = torch.rand(size, dtype=torch.float)

        qtensor = TensorAPoT(4, 1, False)

        # get apot quantized tensor result
        qtensor = qtensor.quantize_APoT(tensor2quantize=tensor2quantize, use_int_repr=True)

        # get uniform quantization quantized tensor result
        uniform_quantized = quantize_per_tensor(input=tensor2quantize, scale=1.0, zero_point=0, dtype=torch.quint8).int_repr()

        qtensor_data = torch.tensor(qtensor.data).type(torch.uint8)
        uniform_quantized_tensor = uniform_quantized.data

        self.assertTrue(torch.equal(qtensor_data, uniform_quantized_tensor))

    r""" Tests quantize_APoT result (int representation) on random 2-dim tensor
        and hardcoded values for b, k by comparing to uniform quantization
        (non-uniform quantization reduces to uniform for k = 1)
        quantized tensor (https://pytorch.org/docs/stable/generated/torch.quantize_per_tensor.html)
        * tensor2quantize: Tensor
        * b: 4
        * k: 1
    """
    def test_quantize_APoT_rand_2d(self):
        # generate random size of tensor2dequantize between 1 -> 20
        size = random.randint(1, 20)

        # generate tensor with random fp values
        tensor2quantize = torch.rand((size, size), dtype=torch.float)

        qtensor = TensorAPoT(4, 1, False)

        # get apot quantized tensor result
        qtensor = qtensor.quantize_APoT(tensor2quantize=tensor2quantize, use_int_repr=True)

        # get uniform quantization quantized tensor result
        uniform_quantized = quantize_per_tensor(input=tensor2quantize, scale=1.0, zero_point=0, dtype=torch.quint8).int_repr()

        qtensor_data = torch.tensor(qtensor.data).type(torch.uint8)
        uniform_quantized_tensor = uniform_quantized.data

        self.assertTrue(torch.equal(qtensor_data, uniform_quantized_tensor))

    r""" Tests quantize_APoT result (reduced precision fp representation) on random 1-dim tensor
        and hardcoded values for b, k by comparing to int representation
        * tensor2quantize: Tensor
        * b: 4
        * k: 2
    """
    def test_quantize_APoT_reduced_precision(self):
        # generate random size of tensor2dequantize between 1 -> 20
        size = random.randint(1, 20)

        # generate tensor with random fp values
        tensor2quantize = torch.rand(size, dtype=torch.float)

        qtensor = TensorAPoT(4, 2, False)

        # get apot reduced precision fp quantized tensor result
        qtensor_red_prec = torch.clone(qtensor.quantize_APoT(tensor2quantize=tensor2quantize,
                                                             use_int_repr=False))
        reduced_precision_lst = list(qtensor_red_prec)

        # get apot int representation quantized tensor result
        qtensor_int_rep = torch.clone(qtensor.quantize_APoT(tensor2quantize=tensor2quantize, use_int_repr=True))
        int_rep_lst = list(qtensor_int_rep)

        # get quantization levels and level indices
        quant_levels_lst = list(qtensor.quantization_levels)
        level_indices_lst = list(qtensor.level_indices)

        # compare with quantized int representation to verify result
        expectedResult = True
        for ele, i in zip(reduced_precision_lst, int_rep_lst):
            reduced_prec_idx = quant_levels_lst.index(ele)
            int_rep_idx = level_indices_lst.index(i)
            if int_rep_idx != reduced_prec_idx:
                expectedResult = False

        self.assertTrue(expectedResult)

    def test_dequantize(self):
        with self.assertRaises(NotImplementedError):
            TensorAPoT.dequantize(self)


    def test_q_apot_alpha(self):
        with self.assertRaises(NotImplementedError):
            TensorAPoT.q_apot_alpha(self)

if __name__ == '__main__':
    unittest.main()
