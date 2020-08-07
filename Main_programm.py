from Metropolis import Metropolis
import numpy as np
from Plot import Ising_Plot

#metro = Metropolis(100, 100, 3000000, beta=0.7)


#beta_arr = [0.39, 0.41, 0.42, 0.43, 0.435, 0.44, 0.445, 0.45, 0.46, 0.47, 0.49]
beta_arr = [0.39, 0.49]
measure_number = 2

for b in beta_arr:
    nx = 10
    ny = 10
    metro = Metropolis(nx, ny, beta=b)
    energy = np.zeros(measure_number)
    heat = np.zeros(measure_number)
    magneti = np.zeros(measure_number)
    chi = np.zeros(measure_number)
    counter = 0
    for m in range(0, measure_number):
        metro.start_simulation()
        #metro.measure_observables()
        print('############################### \n Measurement ' + str(counter + 1))
        energy[m] = metro.total_energy()
        heat[m] = metro.specific_heat()
        magneti[m] = metro.magnetisation()
        chi[m] = metro.magnetic_susceptibility()
        print('Onsager energy Cark: '+ str(metro.OnsagerEnergy()))
        print('Onsager energy Book: '+ str(metro.OnsagerEnergy2()))
        print('Energy per lattice point: ' + str(metro.EnergyPerLatticePoint()))
        print('Delta Energy: ' + str(metro.DeltaEnergy()))
        print('Beta: ' + str(metro.beta))
        print('Beta_critical: ' + str(metro.beta_crit))
        print('Onsager magnetisation: '+ str(metro.OnsagerMagn()))
        print('Averaged Magnetisation: ' + str(metro.magnetisation()))
        print('Delta Magnetisation: ' + str(metro.DeltaMagnetisation()))
        filename = 'Analyse/Temperatur/' + str(nx) + 'x' + str(ny) + 'lattice_beta_' \
                   + str(b).replace('.', '') + 'measure_no_' + str(m)
        metro.save_simulation(filename)
        metro._init_config()
        counter += 1
    # nun soll ein komplett neues Objekt erzeugt werden
    # (neues beta oder neue Gittergroesse und damit auch
    # andere Variablen etc)
    print('############################### \n Mean of the observables after '+ str(measure_number) + ' measurements')
    print('Mean energy: ' + str(np.mean(energy)))
    print('Mean specific heat: ' + str(np.mean(heat)))
    print('Mean magnetisation: ' + str(np.mean(magneti)))
    print('Mean magnetic susceptibility: ' + str(np.mean(chi)))
    del metro
#configs = metro.all_configs
#plot_mod = Ising_Plot(configs)
    
"""
b = 0.39
nx = 100
ny = 100
metro = Metropolis(nx, ny, beta = b)
metro.start_simulation()
print(metro.OnsagerEnergy())
print(metro.EnergyPerLatticePoint())
print(metro.Control())
    
"""

