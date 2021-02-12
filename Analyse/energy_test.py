import matplotlib.pyplot as plt
import numpy as np
from Metropolis import Metropolis, Observables


all_up = [1, 1, 1, 1] # 1
all_down = [-1, -1, -1, -1] # 1
half_by_half = [1, 1, -1, -1] # 2
half_diag = [1, -1, -1, 1] # 2
anti_pairs = [1, -1, 1, -1] # 2
one_down = [1, 1, 1, -1] #4
one_up = [1, -1, -1, -1] #4

config_list = [all_up, all_down, half_by_half, half_by_half, half_diag, half_diag,
                anti_pairs, anti_pairs, one_down, one_down, one_down, one_down, one_up,
                one_up, one_up, one_up]

def part_sum(part):
    ret = part[0]*part[1] + part[0]*part[2] + part[1]*part[3] + part[2]*part[3]
    #print(4*ret)
    return 4*ret

sum = 0
for conf in config_list:
    sum = sum + part_sum(conf)
    #print(sum)

#print(sum/16)


def debug_energy(beta):
    return -16 * np.sinh(8*beta)/(12+2*np.cosh(8*beta))/4

#beta_arr = [0.39, 0.395, 0.4, 0.405, 0.41, 0.4125, 0.415, 0.4175, 0.42, 0.4225, 0.425, 0.4275, 0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.43894, 0.43896, 0.43898, 0.44, 0.4402, 0.4404, 0.4406, 0.4408, 0.441, 0.4412, 0.44125, 0.4414, 0.4416, 0.4418, 0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45, 0.4525, 0.455, 0.4575, 0.46, 0.4625, 0.465, 0.4675, 0.47, 0.475, 0.48, 0.485, 0.49]


#beta_arr = np.arange(0.1, 0.6, 0.025)
beta_arr = np.arange(0, 1, 0.05)

energy_arr = []
for bet in beta_arr:
    energy_arr.append(debug_energy(beta=bet))


np.savez_compressed('Analyse/Testing/2x2/energyandbetavalues', energy=energy_arr, beta=beta_arr)


#lat = (64,64)
#lat = (128,128)
lat = (2, 2)
#lat = (256,256)
#lat = (64,64)
b_field=0

#beta_arr_short = [beta_arr[0], beta_arr[-1]] #beta_arr[26], beta_arr[27],
#[0.1]
#beta_arr_short = [0.0, 0.1, 0.2, 0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
#[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
#print(debug_energy(np.array(beta_arr_short)))
#print(beta_arr_short)
meas_energy_arr = []
y_err = []
y_err_compare = []
config_energy_arr = []
y_err_mag = []
y_err_mag_std = []
y_err_mag_boot = []
heat = []
y_err_heat_boot = []
mag = []
chi = []
y_err_chi_boot = []
obs = []
obs_std = []
#for b in beta_arr_short:
for b in beta_arr:
    #print(r'Measuring $\beta$ = ' + str(b))
    #metro = Metropolis(*lat, beta=b, external_field=b_field)#, flip=False)
    #metro.itersteps = 2010000 * metro.total_number_of_points # 20010000
    #metro.first_skip = 10000 * metro.total_number_of_points #10000
    #metro.skip = 1 * metro.total_number_of_points #2000
    #metro.itersteps = 500500 * metro.total_number_of_points
    #metro.first_skip = 500 * metro.total_number_of_points
    #metro.skip = 500 * metro.total_number_of_points
    #metro.reset()


    #configs = metro.start_simulation()
    filename = 'Analyse/Testing/2x2/' +  str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
               + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
    data = np.load(filename)
    obs.append(data['energy'])
    obs_std.append(data['energy_var'])
    #observables = Observables(data['configs'], beta=b)
    #observables = Observables(configs, beta=b)
    #observables.measure_observables()
    #observables.save_simulation(filename)


    #observables = Observables(configs, beta=b)
    #observables.measure_observables()
    #observables.total_energy()

    #observables.magnetisation()
    # y_err_mag_std.append(np.std(observables.m_per_config))
    # y_err_mag_boot.append(observables.bootstrap(100, observable='magnetisation'))
    # y_err_mag.append(observables.jackknife_onedel(observables.m_per_config))
    # mag.append(observables.m_average)

    #observables.specific_heat()
    #observables.magnetic_susceptibility()
    #heat.append(observables.heat_per_lattice)
    #chi.append(observables.chi)
    #y_err_heat_boot.append(observables.bootstrap(100, observable='heat'))
    #y_err_heat_boot.append(observables.jackknife_onedel_for_var(observables.energy_per_config)/(lat[0]*lat[1]))
    #y_err_chi_boot.append(observables.bootstrap(100, observable='chi'))
    #y_err_chi_boot.append(observables.jackknife_onedel_for_var(observables.m_per_config))
    #y_err_compare.append(observables.jackknife(observables.energy_per_config,
    #                                  del_number=40)/(lat[0]*lat[1]))
    #y_err_compare.append(observables.jackknife_onedel(observables.energy_per_config)/(lat[0]*lat[1]))
    #y_err_compare.append(observables.bootstrap_energy(100)/(lat[0]*lat[1]))
    # filename = 'Analyse/DEBUG/' +  str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
    #            + str(b).replace('.', '') + 'external_field_' + str(b_field) #+ '.npz'

    #observables.measure_observables()
    #observables.save_simulation(filename)
    #config_energy_arr.append(observables.energy_per_config/(lat[0]*lat[1]))
    #meas_energy_arr.append(observables.energy_average/(lat[0]*lat[1]))
    #y_err.append(np.std(observables.energy_per_config)/(lat[0]*lat[1]))
    #np.savez_compressed(filename, observables.energy_per_config/(lat[0]*lat[1]))
    #y_err.append(observables.energy_var/(lat[0]*lat[1]))
    #del metro, observables
    #del observables

#print(y_err)
#print(y_err_compare)
# up = 0
# down = 0
# for conf in config_energy_arr[0]:
#     if conf >= 0.1:
#         up +=1
#     elif conf <= -0.1:
#         down +=1
#
# print('up', up)
# print('down', down)
# print('bolz', up/down)

#up = np.isclose(config_energy_arr, 0.2, atol=0.002)

#down = np.isclose(config_energy_arr, -0.2, atol=0.002)
#down = np.where(config_energy_arr==-0.2, 1, 0)
#print('Boltzmann', np.sum(up)/np.sum(down))

plt.plot(beta_arr, energy_arr*beta_arr, marker='+')
#plt.plot(beta_arr, meas_energy_arr, marker='o')
plt.errorbar(x=beta_arr, y=obs, yerr=obs_std, fmt='o')
# for i in range(0,len(config_energy_arr)):
#    plt.plot(config_energy_arr[i], marker='+', ls='')
#    filename= 'Analyse/DEBUG/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + str(beta_arr_short[i]) + 'alt.png'
#    plt.savefig(filename)
#    plt.close()
plt.show()



#plt.errorbar(beta_arr, meas_energy_arr, y_err, fmt='x')
# plt.errorbar(beta_arr, mag, y_err_mag_std, fmt='x')
# #plt.plot(beta_arr_short, debug_energy(np.array(beta_arr_short)), marker='o')
# #filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'energy_std.pdf'
# filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'magneti_std.pdf'
# plt.savefig(filename)
# plt.close()
#plt.errorbar(beta_arr, meas_energy_arr, y_err_compare, fmt='x')
# plt.errorbar(beta_arr, mag, y_err_mag, fmt='x')
# #filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'energy_bootstrap100.pdf'
# filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'magneti_jackonedel.pdf'
# plt.savefig(filename)
# plt.close()


# plt.errorbar(beta_arr, mag, y_err_mag_boot, fmt='x')
# #filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'energy_bootstrap100.pdf'
# filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'magneti_bootstrap100.pdf'
# plt.savefig(filename)
# plt.close()


# plt.errorbar(beta_arr, heat, y_err_heat_boot, fmt='x')
# #filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'energy_bootstrap100.pdf'
# filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'heat_bootstrap100.pdf'
# plt.savefig(filename)
# plt.close()
#plt.show()


#plt.errorbar(beta_arr, chi, y_err_chi_boot, fmt='x')
#filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'energy_bootstrap100.pdf'
#filename= 'Analyse/DEBUG/Jack/' + 'lattice' + str(lat[0]) + 'x' + str(lat[1]) + 'chi_jack.pdf'
#plt.savefig(filename)
#plt.close()
