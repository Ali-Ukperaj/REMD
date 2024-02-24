import numpy as np
import scipy
import matplotlib.pyplot as plt
import mdtraj as md

def plot_scaling(time_Rij):

    def exp_func(ij, v):
        Rij_func = 0.55*((abs(ij))**v)
        return Rij_func

    # curve_fit for data points of all 16 simulations ("rooms")
    ij = np.linspace(0, 163, 163)
    # parameter matrix to save scaling exponent data
    param = np.empty(shape=[16])
    fit_y = np.empty(shape=[163])

    colors = ['b', 'g', 'k', 'r', 'c', 'm', 'y', 'k']
    colors += colors
    for r in range(0, 16):
        parameters = scipy.optimize.curve_fit(exp_func, ij, time_Rij[r, :])
        fit_y = exp_func(ij, parameters[0])
        plt.plot(ij[:-1], time_Rij[r][:-1], fillstyle='none', marker='o', linewidth=1, alpha=0.3, color=colors[r])
        plt.plot(ij, fit_y, '-', linewidth=3, label=parameters[0], color=colors[r])
        plt.legend(parameters[0])
    scal_ref = [.33, .5, .6]
    #for i in range(0, length(ij)):
        #Rij_ref_1 = exp_func(ij[i], scale_ref[0])
        #Rij_ref_2 = exp_func(ij[i], scale_ref[1])
       # Rij_ref_3 = exp_func(ij[i], scale_ref[2])
    #plt.plot(ij, Rij_ref_1)
    #plt.plot(ij, Rij_ref_2)
    #plt.plot(ij, Rij_ref_3)
    plt.xlabel('Residue Interval (|i - j|)')
    plt.ylabel('Rij (nm)')
    plt.legend()
    plt.show()
