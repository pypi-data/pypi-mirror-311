#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 19:56
# @Author  : 兵
# @email    : 1747193328@qq.com
import os.path


import numpy as np
from ase.io import read as ase_read




from NepTrain import utils

from .utils import  read_thermo


def plot_md_selected(train_xyz_path,md_xyz_path,selected_xyz_path,descriptor,save_path,decomposition="pca"):
    # 画一下图
    from matplotlib import pyplot as plt

    config = [
        # (文件名,图例,图例颜色)

    ]
    if not utils.is_file_empty(train_xyz_path):
        config.append((train_xyz_path, "base dataset","gray"))

    if not utils.is_file_empty(md_xyz_path):
        config.append((md_xyz_path, 'new dataset', "#07cd66"))

    if not utils.is_file_empty(selected_xyz_path):
        config.append((selected_xyz_path,'selected', "red"))

    fit_data = []




    for info in config:
        atoms_list = ase_read(info[0], ":", format="extxyz", do_not_split_by_at_sign=True)

        # atoms_list_des = np.vstack([get_descriptors(i, nep_txt_path) for i in atoms_list])
        atoms_list_des = np.array([np.mean(descriptor.get_descriptors(i), axis=0) for i in atoms_list])


        fit_data.append(atoms_list_des)
    if decomposition=="pca":
        from sklearn.decomposition import PCA

        reducer = PCA(n_components=2)
    else:
        from umap import UMAP

        reducer = UMAP(n_components=2)

    reducer.fit(np.vstack(fit_data))
    fig = plt.figure()
    for index, array in enumerate(fit_data):
        proj = reducer.transform(array)
        plt.scatter(proj[:, 0], proj[:, 1], label=config[index][1], c=config[index][2])

    plt.legend()
    # plt.axis('off')
    plt.savefig(save_path)
    plt.close(fig)









def plot_energy(thermo_path,natoms=1):
    from matplotlib import pyplot as plt

    potential_energy = read_thermo(thermo_path, natoms)



    fig = plt.figure()
    plt.plot(list(range(len(potential_energy ))), potential_energy)



    plt.savefig(os.path.join(os.path.dirname(thermo_path),"md_energy.png"), dpi=300)
    plt.close(fig)
