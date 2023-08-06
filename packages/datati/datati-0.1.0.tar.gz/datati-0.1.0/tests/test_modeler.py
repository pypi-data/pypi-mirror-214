import unittest

from dataset import Dataset
from encoding.quantization import Quantiler
from models.binary import SBRLModeler
from models.modelers.filters import ContinuousModeler
from models.modelers.one_hot import OneHotModeler, BinaryBoolModeler
from models.trees import ContinuousTreeModeler, OneHotTreeModeler

datasets = [
    ("mstz/adult", "income"),
]


class TestLoad(unittest.TestCase):
    def test_load(self):
        for name, config in datasets:
            d = Dataset(name, load_from="huggingface", config=config, split="train")

    def test_onehot_modeler(self):
        for name, config in datasets:
            modeler = OneHotModeler()
            d = Dataset(name, load_from="huggingface", config=config, split="train")
            d1 = modeler.process(d)

            for dtype in d1.dtypes:
                assert dtype.name.startswith("int") or dtype.name.startswith("float") or dtype.name.startswith("bool")

    def test_continuous_modeler(self):
        for name, config in datasets:
            modeler = ContinuousModeler()
            d = Dataset(name, load_from="huggingface", config=config, split="train")
            d1 = modeler.process(d)

            for dtype in d1.dtypes:
                assert dtype.name.startswith("int") or dtype.name.startswith("float")

    def test_continuoustree_modeler(self):
        for name, config in datasets:
            modeler = ContinuousTreeModeler()
            d = Dataset(name, load_from="huggingface", config=config, split="train")
            d.target_feature = d.columns[-1]
            d1 = modeler.process(d)

            for dtype in d1.dtypes:
                assert dtype.name.startswith("int") or dtype.name.startswith("float")

    def test_onehottree_modeler(self):
        for name, config in datasets:
            modeler = OneHotTreeModeler()
            d = Dataset(name, load_from="huggingface", config=config, split="train")
            d1 = modeler.process(d)

            for dtype in d1.dtypes:
                assert dtype.name.startswith("int") or dtype.name.startswith("float")

    def test_binary_modeler(self):
        for name, config in datasets:
            binner = Quantiler(n_quantiles=4)
            modeler = BinaryBoolModeler(binner=binner)
            d = Dataset(name, load_from="huggingface", config=config, split="train")
            d1 = modeler.process(d)

            for dtype in d1.dtypes:
                assert dtype.name == "bool"

    def test_sbrl_modeler(self):
        for name, config in datasets:
            binner = Quantiler(n_quantiles=4)
            modeler = SBRLModeler(binner=binner)
            d = Dataset(name, load_from="huggingface", config=config, split="train")
            d1 = modeler.process(d)

            for dtype in d1.dtypes:
                assert dtype.name == "int8"

            for f in d1.columns:
                assert set(d1[f].unique()) == {0, 1} or set(d1[f].unique()) == {1}


if __name__ == "main":
    unittest.main()
