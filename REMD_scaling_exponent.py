import mdtraj as md
import numpy as np
import matplotlib.pyplot as plt

def radius_ij(rooms, lentraj, sim_numb, n_atoms):
    ensemble_avg_Rij = np.empty(shape=[16, 1001, 163])
    time_avg_Rij = np.empty(shape=[16, 163])
    for r in range(0, sim_numb):
        for fr in range(0, lentraj):
                # loop for each residue in sequence
            for j in range(1, (n_atoms-1)):
                # interval between residues: i - j (ie: step_size)
                # can find the scalar magnitude of the distance between two residues by taking
                # the matrix norm of the difference between the two position vectors
                # structure = (mean_by_interval (norm (diff_vect)))
                # column will be interval (i - j), row will be frame, value will be Rij
                ensemble_avg_Rij[r][fr, j] = np.mean(np.linalg.norm(rooms[r][fr][:-j][:] - rooms[r][fr][j:][:], axis=1))
        # Rij averaged across all frames, so that there will be 163 data point for 16 simulations
        # Thus, there is 16 lines that can be graphed across all data
        time_avg_Rij[r] = np.mean(ensemble_avg_Rij[r][:, :], axis=0)
    return ensemble_avg_Rij, time_avg_Rij
