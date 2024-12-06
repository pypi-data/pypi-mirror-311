#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 14:22
# @Author  : 兵
# @email    : 1747193328@qq.com
import contextlib
import os

import numpy as np

from nep_cpu import NEP3

class Nep3Calculator:

    def __init__(self, model_file="nep.txt"):
        if not isinstance(model_file, str):
            model_file=str(model_file,encoding="utf-8")
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                self.nep3 = NEP3(model_file)
        self.element_list=self.nep3.get_element_list()
        self.type_dict = {e: i for i, e in enumerate(self.element_list)}


    def get_descriptors(self,structure):
        symbols = structure.get_chemical_symbols()
        _type = [self.type_dict[k] for k in symbols]
        _box = structure.cell.transpose(1, 0).reshape(-1).tolist()
        _position = structure.get_positions().transpose(1, 0).reshape(-1).tolist()
        descriptor = self.nep3.find_descriptors(_type, _box, _position)

        descriptors_per_atom = np.array(descriptor).reshape(-1, len(structure)).T

        return descriptors_per_atom
    def get_structure_descriptors(self, structure):
        descriptors_per_atom=self.get_descriptors(structure)
        return descriptors_per_atom.mean(axis=0)
    @classmethod
    def get_structure_descriptors_nep(cls, structure,model_file="nep.txt"):
        nep=cls(model_file)
        return nep.get_structure_descriptors(structure)