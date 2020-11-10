from Metropolis import Metropolis, Observables
import numpy as np
from Plot import Ising_Plot
from numba import jitclass


beta_arr = [0.39, 0.41, 0.42, 0.43, 0.435, 0.44, 0.445, 0.45, 0.46, 0.47, 0.49]
# 2^n Gittergrößen bis 512x512
#nx, ny = 200, 200
lattice_arr = [(2,2), (8,8)]
for lattice in lattice_arr:
    print(lattice)
    quit()
    b_field = 0
    for beta in beta_arr:
        print(r'########################## Starte Simulation mit $\beta = $', str(beta))
        metro = Metropolis(*lattice, beta=beta, external_field=b_field)
        configs = metro.start_simulation()
        observables = Observables(configs, beta=beta)
        observables.measure_observables()
        filename = 'Analyse/Temperatur/' + str(nx) + 'x' + str(ny) + 'lattice_beta_' \
                           + str(b).replace('.', '') + 'external_field' + str(b_field)
        observables.save_simulation(filename)
        del metro
    
"""
Notizen:
    
Hysterese als Alternative zur Überprüfung der einzelnen Observablen in Abh. 
 von b_field 

beta_crit = ca. 0.4406

"""

