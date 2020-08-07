from Metropolis import Metropolis, Observables
import numpy as np
from Plot import Ising_Plot
from numba import jitclass

beta = 0.48
nx, ny = 100, 100
lattice = (nx, ny)
metro = Metropolis(*lattice, beta=beta)
configs = metro.start_simulation()
observables = Observables(configs, beta=beta)
observables.measure_observables()
print('energy_average', observables.energy_average / (nx*ny))
print(observables.energy_var / (nx*ny))
print(observables.heat_per_lattice)
print(observables.m_average)
print(observables.magnetisation_var)
print(observables.chi)

quit()
#metro = Metropolis(100, 100, 3000000, beta=0.7)


#beta_arr = [0.39, 0.41, 0.42, 0.43, 0.435, 0.44, 0.445, 0.45, 0.46, 0.47, 0.49]
#measure_number = 4
beta_arr = [0.48]
measure_number = 1
for b in beta_arr:
    nx = 100
    ny = 100
    metro = Metropolis(nx, ny, beta=b)
    energy = np.zeros(measure_number)
    energy_var = np.zeros(measure_number)
    heat = np.zeros(measure_number)
    magneti = np.zeros(measure_number)
    magneti_var = np.zeros(measure_number)
    chi = np.zeros(measure_number)
    for m in range(0, measure_number):
        metro.start_simulation()
        metro.measure_observables()
        energy[m] = metro.energy_average / (nx*ny)
        energy_var[m] = metro.energy_var / (nx*ny)
        heat[m] = metro.heat_per_lattice
        magneti[m] = metro.m_average
        magneti_var[m] = metro.magnetisation_var
        chi[m] = metro.chi
        print(energy[m], ' +/- ', energy_var[m])
        print(heat[m])
        print(magneti[m], ' +/- ', magneti_var[m])
        print(chi[m])
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

