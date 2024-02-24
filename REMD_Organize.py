import mdtraj as md
import matplotlib.pyplot as plt
import sys
import numpy as np

def organ(log_file, sim_numb):
    f = log_file
    data = np.loadtxt(f, comments=['#', '@'])
    paths = np.empty((len(data), 16))
    t = np.empty((len(data), 1))

    for i in range(0, sim_numb+1):
        if i < 1:
            t = data[:, i]
        elif i >= 1:
            paths[:, i - 1] = data[:, i]
    return t, paths
