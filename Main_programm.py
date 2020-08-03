from Metropolis import Metropolis
import numpy as np
from Plot import Ising_Plot

#metro = Metropolis(100, 100, 3000000, beta=0.7)


beta_arr = [0.39, 0.41, 0.42, 0.43, 0.435, 0.44, 0.445, 0.45, 0.46, 0.47, 0.49]
measure_number = 4
for b in beta_arr:
    nx = 100
    ny = 100
    metro = Metropolis(nx, ny, beta=b)
    energy = np.zeros(measure_number)
    heat = np.zeros(measure_number)
    magneti = np.zeros(measure_number)
    chi = np.zeros(measure_number)
    for m in range(0, measure_number):
        metro.start_simulation()
        energy[m] = metro.total_energy()
        heat[m] = metro.specific_heat()
        magneti[m] = metro.magnetisation()
        chi[m] = metro.magnetic_susceptibility()
        print(np.mean(energy))
        print(np.mean(heat))
        print(np.mean(magneti))
        print(np.mean(chi))
        filename = 'Analyse/Temperatur/' + str(nx) + 'x' + str(ny) + 'lattice_beta_' \
                   + str(b).replace('.', '') + 'measure_no_' + str(m)
        metro.save_simulation(filename)
        metro._init_config()
    # nun soll ein komplett neues Objekt erzeugt werden
    # (neues beta oder neue Gittergroesse und damit auch
    # andere Variablen etc)
    del metro
#configs = metro.all_configs
#plot_mod = Ising_Plot(configs)

