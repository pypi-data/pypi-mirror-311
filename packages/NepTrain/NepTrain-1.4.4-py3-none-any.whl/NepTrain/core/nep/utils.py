#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/14 14:34
# @Author  : 兵
# @email    : 1747193328@qq.com
from pathlib import Path

from ase.data import chemical_symbols, atomic_numbers
import re
import os
from calorine.nep import get_descriptors as get_nep_descriptors
def read_symbols_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding="utf8") as f:
            trainxyz = f.read()
        groups = re.findall("^([A-Z][a-z]?)\s+", trainxyz, re.MULTILINE)
        groups = set(groups)
        symbols = []
        for symbol in groups:
            if symbol in chemical_symbols:
                symbols.append(symbol)

        symbols = sorted(symbols, key=lambda x: atomic_numbers[x])
    else:
        symbols = []
    return symbols


def get_soap_descriptors(atoms,soap):
    return  soap.create(atoms)

def get_descriptor_function(model):


    if isinstance(model, (str,Path)) and os.path.exists(model):
        return get_nep_descriptors

    return get_soap_descriptors
