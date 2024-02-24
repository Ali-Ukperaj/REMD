import mdtraj as md
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def REMD_plot(t, paths):
    fig, axs = plt.subplots(nrows=4, ncols=4)
    for i in range(1, 17):
        if i <= 4:
            axs[0, i - 1].plot(t, paths[:, i - 1])
        elif i > 4 and i <= 8:
            axs[1, i - 5].plot(t, paths[:, i - 1])
        elif i > 8 and i <= 12:
            axs[2, i - 9].plot(t, paths[:, i - 1])
        elif i > 12 and i <= 16:
            axs[3, i - 13].plot(t, paths[:, i - 1])
    plt.show()
