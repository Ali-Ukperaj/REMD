# Background
This project was an attempt for me to integrate a few analysis methods for REMD simulations into one tool using python. It is incomplete as it is not generalized as of 2/24/2024. It was developed using a reference REMD of a coarse-grained model of the protein FUS (wild type) with 16 trajectories, each containing: 1001 frames, 163 residues, and an x, y, and z-coordinate. Therefore a 4 dimensional is used for most of the data storage and analysis within this package (traj, frame, residue, position)

# Dependencies
Numpy, Matplotlib, sys, mdtraj, scipy

# Project Outline
For understanding this project, it is important to note that I often interpreted the REMD simulations as a number of rooms with people in them. Each simulation is one room, and each structure simulated is one person. Throughout the simulation, an exchange occurs, where two people simultaneously attempt to switch rooms. There is never more than one person occupying a room. When dealing with a continuous simulation, output data and trajectories follow the perspective of each "person" as they move through different "rooms". However, it is often preferred to analyze simulations with respect to what occurs to different conformations under the same conditions (ie: what each "room's" effect on a person is). For example, if you want to know the generalized effect of a specific temperature on a protein, it is useful to see what happens to it over a range of different starting conformations. Therefore, I started this project by demultiplexing the data into the form of following each simulation, regardless of which structure occupied it. Therefore, it the data is now in discontinuous form, with the procession of frames showing new versions of the same protein being exchanged into it every so often and displaying the manner in which it acts.

# Package Structure
This package is centered around a python class defined in the file "REMD_Class.py" called "Sim". This class takes an input of the REMD's log file (containing which simulation the protein is in), generalized location name of set of trajectories (ie: if inside a folder named "trajectories" with trajectory names of "dump_traj_0.xtc" with trajectories 0-15, you would just input "trajectories/dump_traj_.xtc"), topology file, and number of simulations. This project was used as a tool for my research, so it makes a couple of assumptions:
1. The REMD is Continuous (data follows the specific model moving through exchanges as opposed to the simulation at a set temperature)
2. All trajectory files are labeled exactly the same except for the number identifying which simulation it is (starting at 0 and increasing by 1)
3. Trajectory format is .xtc
4. 

Each python script is developed in a separate file and set as a function. This function is then set as a method within the class (which, when called, will reference the function from the original, separate script). This is true for everything except my "Organize" (REMD_Disc_Tools/REMD_Organize) and "Demultiplex" (REMD_Disc_Tools/REMD_Demultiplex) functions. These are used in almost every method contained within this class, so rather than having them as their own methods and calling them each time I ran a separate method, I decided to just run them with the initialization of the class so and set their outputs as object attributes. Therefore, once an object is created, every method called from that point on will have access to this data. As of this time, I do not have any class attributes defined.

# Object Attributes
Upon initialization, the object will create a number of attributes. These include "log" (input log file), "dump_loc" (name of the trajectory input), "topology", "dump_index" (index of the last point before the ".xtc" is written; used for writing and reading files properly), "lentraj" (number of frames in the trajectory), "n_atoms" (atoms/residues in the structure analyzed), "sim_numb" (number of simulations used in this REMD), "t" (numpy array of all timestep values), "paths" (numpy matrix separated into columns based on the specific protein, with values detailing the temperature/simulation it is in at a specific timestep), "rooms" (4D numpy matrix detailing the discontinuous trajectories; organized by simulation, frame, residue, position), "res_list" (list of residue names in order of the protein), and "new_traj_step" (gives the ratio of the trajectory length to the log length; in other words, frame_interval/exchange_interval).

# Object Methods
1. trajectory_xtc = uses mdtraj to quickly give you the trajectory information of a specific, _discontinuous_ trajectory (original xtc files). Once called, it will ask you which simulation number you'd like to look at
2. subplot = plots the data previously found with the “organize” function to show how well the “people” are moving through each “room”
3. write_xyz = takes the “rooms” output of the “demultiplex” method and use it to create xyz files for each simulation you run. For example, if you ran 16 REMD simulations, you would now create 16 xyz files that correspond to demultiplexed data
4. RG = this will calculate the center of mass and radius of gyration for each “room” and each frame
5. plot_rg = this will take the calculated radius of gyration from “RG” and use it to plot for all simulations through all frames
6. Rij = this will solve for the ensemble and time average Rij
7. plot_scaling_exponent = this will use data from “Rij” in order to fit the given exponential function and graph each simulation on a similar plot. This plot will have the actual Rij data circled, while the fitted curve will be solid. Each fitted line will have its respective scaling exponent displayed on the legend

# Improvements Needed
This package is not generalized. It works well for continuous REMD simulations where there are 16 trajectories given in .xtc format. Possible improvements:
1. Make compatible with non-xtc trajectories.
2. Generalize plotting methods to look better with different overall numbers of simulations (ie: 6, 8, 9, 12).
3. Generalize log and trajectory interval relationship so that my demultiplexing does not rely on the exchange and frames being multiples of each other.
4. Radius of gyration and scaling exponent calculations come into periodic boundary issue that causes it to spike when part of the protein falls too far over the boundary.
