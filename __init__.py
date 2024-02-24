# Attempting REMD Modules filled with useful scripts/methods.
# Version: 1.0
# Date: February 1, 2024

import sys
import numpy as np
import mdtraj as md
import matplotlib
import matplotlib.pyplot as plt
import scipy
import REMD
from REMD import REMD_Class, REMD_Organize, REMD_Paths, REMD_Demultiplex, REMD_xyz
from REMD import REMD_RG, REMD_plot_rg, REMD_scaling_exponent, REMD_scaling_exponent_plot
from REMD.REMD_Class import Sim
from REMD.REMD_Organize import organ
from REMD.REMD_Paths import REMD_plot
from REMD.REMD_Demultiplex import demultiplex
from REMD.REMD_xyz import REMD_write
from REMD.REMD_RG import Center_of_mass
from REMD.REMD_RG import radius_gyration
from REMD.REMD_plot_rg import plot_rg
from REMD.REMD_scaling_exponent import radius_ij
from REMD.REMD_scaling_exponent_plot import plot_scaling








