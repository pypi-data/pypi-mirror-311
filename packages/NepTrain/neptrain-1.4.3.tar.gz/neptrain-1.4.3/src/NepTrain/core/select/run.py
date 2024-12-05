#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/13 19:36
# @Author  : 兵
# @email    : 1747193328@qq.com
import os.path

from NepTrain import utils

from ase.io import read as ase_read
from ase.io import write as ase_write
from .select import select_structures, filter_by_bonds
from ..gpumd.plot import plot_md_selected
from ..nep.utils import read_symbols_from_file
from dscribe.descriptors import SOAP

def run_select(argparse):

    if utils.is_file_empty(argparse.trajectory_path):
        raise FileNotFoundError(f"An invalid file path was provided: {argparse.trajectory_path}.")
    utils.print_msg("Reading the file, please wait...")

    trajectory=ase_read(argparse.trajectory_path,":",format="extxyz")

    # if argparse.filter:
    # #转移到gpumd的模块
    #     atoms=ase_read(argparse.base_structure,)
    #     good, bad = filter_by_bonds(trajectory, model=atoms)
    #     directory=os.path.dirname(argparse.trajectory_path)
    #     trajectory=good
    #     ase_write(os.path.join(directory, "good_structures.xyz"), good,append=False)
    #     ase_write(os.path.join(directory, "remove_by_bond_structures.xyz"), bad,append=False)
    #     utils.print_msg(f"Bond length filtering activated, {len(bad)} structures filtered out, saved to {os.path.join(directory, 'remove_by_bond_structures.xyz')}.")


    if utils.is_file_empty(argparse.base):
        base_train=[]
    else:
        base_train=ase_read(argparse.base,":",format="extxyz")
    if utils.is_file_empty(argparse.nep):
        utils.print_msg("An invalid path for nep.txt was provided, using SOAP descriptors instead.")
        species=set()
        for atoms in trajectory+base_train:
            for i in atoms.get_chemical_symbols():
                species.add(i)

        species = list(species)
        r_cut = argparse.r_cut
        n_max = argparse.n_max
        l_max = argparse.l_max
        descriptor = SOAP(
            species=species,
            periodic=False,
            r_cut=r_cut,
            n_max=n_max,
            l_max=l_max,
        )

    else:
        descriptor=argparse.nep
    utils.print_msg("Starting to select points, please wait...")

    selected_structures = select_structures(base_train,
                                            trajectory,
                                            descriptor,
                      max_selected=argparse.max_selected,
                      min_distance=argparse.min_distance,
                      )

    utils.print_msg(f"Obtained {len(selected_structures)} structures." )

    ase_write(argparse.out_file_path, selected_structures)
    png_path=os.path.join(os.path.dirname(argparse.out_file_path),"selected.png")
    plot_md_selected(argparse.base,
                     argparse.trajectory_path,

                     argparse.out_file_path,
                     descriptor,
                       png_path ,

                     )
    utils.print_msg(f"The point selection distribution chart is saved to {png_path}." )
    utils.print_msg(f"The selected structures are saved to {argparse.out_file_path}." )

