import mdtraj as md
import numpy as np
import matplotlib.pyplot as plt



def plot_rg(rg, lentraj, traj, sim_numb):
    time_sim = traj[lentraj-1].time[0]
    x = np.linspace(0, time_sim, lentraj)
    fig, axs = plt.subplots(nrows=4, ncols=4, label='REMD Discontinuous')
    for i in range(1, (sim_numb+1)):
        if i <= 4:
            axs[0, i - 1].plot(x, rg[i - 1][:])
        elif 4 < i <= 8:
            axs[1, i - 5].plot(x, rg[i - 1][:])
        elif 8 < i <= 12:
            axs[2, i - 9].plot(x, rg[i - 1][:])
        elif 12 < i <= 16:
            axs[3, i - 13].plot(x, rg[i - 1][:])
    plt.show()
