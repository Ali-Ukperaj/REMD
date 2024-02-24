import mdtraj as md
import numpy as np
import matplotlib.pyplot as plt

# python <script_name.py> <log.lammps> <dump_file.xtc> <topology_file.pdb>
def Center_of_mass(log, traj_loc, topolog, lentraj, rooms, n_atoms):
    # there will be a center of mass (xyz-coordinate) for each 1001 frames in all 16 simulations
    COM = np.empty(shape=[16, 1001, 3])
    for i in range(0, 16):
        for n in range(0, lentraj):
            COM_x = (sum(rooms[i][n][:][:, 0]))/n_atoms
            COM_y = (sum(rooms[i][n][:][:, 1]))/n_atoms
            COM_z = (sum(rooms[i][n][:][:, 2]))/n_atoms
            COM[i][n][:] = [COM_x, COM_y, COM_z]
    return COM, rooms

def radius_gyration(COM, rooms, lentraj, n_atoms):
    # radius of gyration; will be a single distance for all 1001 frames of each 16 simulations
    rg = np.empty(shape=[16, 1001])
    for i in range(0,16):
        rg_x = 0
        rg_y = 0
        rg_z = 0
        for n in range(0, lentraj):
            rg_x = (sum (( np.power( (rooms[i][n][:][:, 0] -  COM[i][n][0]),2) ) ))
            rg_y = (sum (( np.power( (rooms[i][n][:][:, 1] - COM[i][n][1]),2) ) ))
            rg_z = (sum (( np.power( (rooms[i][n][:][:, 2] - COM[i][n][2]),2) ) ))
            rg[i][n] = ( ( ((rg_x) + (rg_y) + (rg_z)) /n_atoms) ** (1/2) )
    return rg
