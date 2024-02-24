import sys, matplotlib
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import REMD
import REMD.REMD_Organize, REMD.REMD_Paths, REMD.REMD_Demultiplex, REMD.REMD_xyz
import REMD.REMD_RG, REMD.REMD_plot_rg, REMD.REMD_scaling_exponent, REMD.REMD_scaling_exponent_plot

class Sim:
    def __init__(self, log, dump_location, topology, simulation_number):
        # log.lammps file, dump_trajectory.xtc, topology.pdb, how many simulations you're running
        self.log = log
        self.dump_loc = dump_location
        self.topology = topology
        self.dump_index = dump_location.index('.xtc')
        dump_file_name = dump_location[:-4] + '0.xtc'
        traj_ex = md.load(dump_file_name, top=topology)
        self.lentraj = len(traj_ex)
        self.n_atoms = traj_ex[0].n_residues
        self.sim_numb = int(simulation_number)
        self.t, self.paths = REMD.REMD_Organize.organ(self.log, self.sim_numb)
        self.rooms, self.traj, self.res_list, self.new_traj_step = REMD.REMD_Demultiplex.demultiplex(self.log, self.dump_loc, self.topology, self.t, self.paths)

    def trajectory_xtc(self):
        sim_of_interest = int(input('What simulation would you look to observe?\n'))
        if sim_of_interest >= self.sim_numb:
            print('This index is not included in your data.')
        dump_file_name = self.dump_loc[:-4] + str(sim_of_interest) + '.xtc'
        traj = md.load(dump_file_name, top=self.topology)
        return traj

    def subplot(self):
        REMD.REMD_Paths.REMD_plots(self.t, self.paths)

    def write_xyz(self):
        REMD.REMD_xyz.REMD_write(self.dump_loc, self.sim_numb, self.dump_index, self.n_atoms, self.lentraj, self.rooms, self.res_list)

    def RG(self):
        self.COM, rooms = REMD.REMD_RG.Center_of_mass(self.log, self.dump_loc, self.topology, self.lentraj, self.rooms, self.n_atoms)
        self.rg = REMD.REMD_RG.radius_gyration(self.COM, self.rooms, self.lentraj, self.n_atoms)

    def plot_rg(self):
        self.RG()
        REMD.REMD_plot_rg.plot_rg(self.rg, self.lentraj, self.traj, self.sim_numb)

    def Rij(self):
        rooms = self.rooms/10 # convert to angstroms
        lentraj = self.lentraj
        sim_numb = self.sim_numb
        n_atoms = self.n_atoms
        self.ensemble_avg_Rij, self.time_avg_Rij = REMD.REMD_scaling_exponent.radius_ij(rooms, lentraj, sim_numb, n_atoms)

    def plot_scaling_exponent(self):
        self.Rij()
        time_Rij = self.time_avg_Rij
        REMD.REMD_scaling_exponent_plot.plot_scaling(time_Rij)
