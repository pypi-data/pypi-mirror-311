# -- do not touch
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# -- end do not touch

import random  # noqa: E402
import unittest  # noqa: E402

import numpy  # noqa: E402
import torch  # noqa: E402
from gptqmodel import GPTQModel  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402


class TestLmHead(unittest.TestCase):
    MODEL_ID = "/monster/data/model/TinyLlama-1.1B-intermediate-step-1341k-3T-autoround-lm_head-symFalse" # "LnL-AI/TinyLlama-1.1B-intermediate-step-1341k-3T-autoround-lm_head-symFalse"
    DEVICE = "cuda:0"

    @classmethod
    def setUpClass(cls):
        seed = 898
       # stabilize generation
        torch.manual_seed(seed)
        numpy.random.seed(seed)
        random.seed(seed)
        torch.cuda.manual_seed_all(seed)

    def test_load(self):
        prompt = "My name is Lewis and I like to"

        tokenizer = AutoTokenizer.from_pretrained(self.MODEL_ID)
        inputs = tokenizer(prompt, return_tensors="pt").to(device=self.DEVICE)

        model = GPTQModel.load(self.MODEL_ID, device=self.DEVICE)

       # validate lm_head is loaded as quantized layer
        assert model.model.lm_head.__class__.__name__ == "ExllamaV2QuantLinear"

        res = model.model.generate(
            **inputs, num_beams=1, min_new_tokens=1, max_new_tokens=128, repetition_penalty=1.25
        )
        res_str = tokenizer.decode(res[0])

        print(f"prompt: {prompt}")
        print(f"result: {res_str}")

       # validated on 4090 and a100 + cuda 12.4 + torch 2.2.2 + transformers 4.40.1
        assert "My name is Lewis and I like to play football." in res_str
