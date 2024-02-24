import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt

# python <script_name.py> <log.lammps> <dump_file.xtc> <topology_file.pdb>
# for dump file, include every part of file name except for the number, and the
# script will automatically use 16 versions of the file (0-15)
# ie: if directory of 16 dump files called "dump_traj", input "dump_traj/dump_traj_.xtc"

def demultiplex(log_file, trajectory_location, topology_file, t, paths):
    # Organizes log.lammps file into each column (what "room" "person" 0-15 is in).
    # This is calculated on a separate python file "volume/NFS/aiu8/scripts/REMD_Class.py".
    # Also takes the timestep of each piece of data.
    lenx, leny = np.shape(paths)

    # Now want to use path data to organize by "room" instead of "person".
    # Have data show what person is in the room at each timestep.
    # Each column has the identity of the "person" occupying the "room"
    # ie: output_array[0][:,0] will be every "person" at every timestep that is in that "room".
    output_array = np.empty(shape=[lenx, leny], dtype=int)
    for k in range(0, leny):
        output_array[:, k] = np.where(paths == k)[1]

    dump = trajectory_location
    dump_index = dump.index('.xtc')
    topfile = topology_file

    # Create array that saves "person", frame, residue, and xyz location
    people = np.empty(shape=[16, 1001, 163, 3])

    # define residue names in an array
    traj_for_res = md.load(dump[:dump_index] + "0.xtc", top=topfile)
    n_atoms = int(traj_for_res[0].n_atoms)
    res_list = []
    for i in range(0,n_atoms):
        res_list.append(str(traj_for_res[0].topology.residue(i)))


    # this will go through 16 trajectory files (dump_traj{0:15}.xtc) to save all xyz data
    for i in range(0, 16):

        # Create naming system that will loop through trajectories of all simulations
        i1 = str(i)
        trajfile = dump[0:dump_index] + i1 + '.xtc'
        log = log_file
        traj = md.load(trajfile, top=topfile)
        time_values = traj.time

        # determine relationship between length of trajectory and log to relate info
        # assume that trajectory is always shorter and is related by some common factor to the log
        lentraj = len(traj)
        log_diff = t[-1] - t[0]
        # gets time range of log file
        log_step = log_diff / (lenx - 1)
        # determines step size (time interval) of log file
        traj_diff = traj[-1].time[0] - traj[0].time[0]
        # gets time range of trajectory
        traj_step = traj_diff / (lentraj - 1)
        # determines step size (time interval) of trajectory
        new_traj_step = traj_step / log_step
        # relates trajectory and log step sizes to determine how to relate exchanges and trajectories

        for j in range(0, lentraj):
            people[i][j][:][:] = (traj[j].xyz[0][:][:])*10

    # create 4D array that stores values for: "rooms", frame, residue, and xyz location (respectively)
    # initialize array and add to it throughout loop
    rooms = np.empty(shape=[16, 1001, 163, 3])
    for i in range(0, 16):
        # loop through log.lammps info
        curr_person = i
        if (new_traj_step) <= 1 and (log_step % traj_step == 0):
            # Checks that trajectory intervals are larger than exchange attempts and
            # that they are multiples of each other.
            # If this condition is true, you can just take the person in the output_array at
            # every trajectory step and organize in that way.
            # make a new output array that only stores values at exchange steps that coincide with trajectory data

            # create step size value to match files
            new_step_size = int(1/new_traj_step)
            new_output_array = output_array[::new_step_size, :]
            for s in range(0, lentraj):
                # create conditional to check "person" every exchange interval
                curr_person = new_output_array[s, i]
                rooms[i][s][:][:] = people[curr_person][s][:][:]

        elif (new_traj_step > 1) and (traj_step % log_step == 0):
            # Checks if trajectory intervals are smaller than exchange attempts and
            # that they are multiples of each other.

            # For this condition, you can take the trajectory data at every step, changing the person
            # you are reading from every time an exchange occurs (index_position = new_traj_step).
            # ie: if trajectory steps are 10x less than exchange (10x as many traj values), you would
            # take the trajectories for 9 steps, then check the output_array on the 10th step. This output
            # value would be kept until the next exchange attempt (another 10 steps).
            new_traj_step = int(new_traj_step)
            for s in range(0, new_traj_step):
                if s % new_traj_step == 0:
                    curr_person = output_array[s, i]
                rooms[i][s][:][:] = people[curr_person][s][:][:]
        else:
            print('Exchange and Trajectory intervals are not multiples!')

    return rooms, traj, res_list, new_traj_step
