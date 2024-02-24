def REMD_write(dump_name, simulation_number, dump_index, n_atoms, lentraj, rooms, res_list):
    simulation_number = int(simulation_number)
    for i in range(0, simulation_number):
        n = str(i)
        dump_index = int(dump_index)
        new_name_xyz = dump_name[0:dump_index] + n + '.xyz'

        # writes a new file (will automatically overwrite data)
        with open(new_name_xyz, "w") as xyz_file_init:
            xyz_file_init.write(str(n_atoms) + "\nFUS_WT Timestep: " + "0" + "\n")
            xyz_file_init.close()

        # will append additional data
        with open(new_name_xyz, "a") as xyz_file:
            for fr in range(0, lentraj):
                fr = int(fr)
                if fr != 0:
                    xyz_file.write(str(n_atoms) + "\n")
                for rs in range(0, n_atoms):
                    rs = int(rs)
                    x = str(rooms[i][fr][rs][0])
                    y = str(rooms[i][fr][rs][1])
                    z = str(rooms[i][fr][rs][2])
                    xyz_file.write(res_list[rs] + " " + x + " " + y + " " + z + "\n")
                xyz_file.write("\n")
            xyz_file.close()