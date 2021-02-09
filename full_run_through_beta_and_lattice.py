from Metropolis import Metropolis, Observables
from Ising_Visualizing import Ising_Ani
import numpy as np
import matplotlib.pyplot as plt


beta_array = [0.39, 0.395, 0.4, 0.405, 0.41, 0.4125, 0.415, 0.4175, 0.42, 0.4225, 0.425, 0.4275, 0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.43894, 0.43896, 0.43898, 0.44, 0.4402, 0.4404, 0.4406, 0.4408, 0.441, 0.4412, 0.44125, 0.4414, 0.4416, 0.4418, 0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45, 0.4525, 0.455, 0.4575, 0.46, 0.4625, 0.465, 0.4675, 0.47, 0.475, 0.48, 0.485, 0.49]
beta_array = np.array(beta_array)
beta_array[::-1].sort()

lat = (256,256)
b_field = 0
filepart = 'Analyse/256x256/Visualize/Reverserun/'


# print('beta_vals:', len(beta_array))
#
# metro = Metropolis(*lat, beta_array[0])
# configs = metro.start_simulation()
# observables = Observables(configs, beta_array[0])
# #observables.measuring_observables()
# filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
#       + str(beta_array[0]).replace('.', '') + 'external_field_' + str(b_field)
# observables.save_simulation(filename)
# del observables
#
# i = 2
#
# for beta in beta_array[1:]:
#     print('beta_val no.', i)
#     metro.reset()
#     metro.beta = beta
#     configsneu = metro.start_simulation()
#     observables = Observables(configsneu, beta)
#     #observables.measuring_observables()
#     filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
#           + str(beta).replace('.', '') + 'external_field_' + str(b_field)
#     observables.save_simulation(filename)
#     del observables
#     i +=1


for bet in beta_array:
    filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
          + str(bet).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
    newdata = np.load(filename)
    #if bet > 0.39:
    if bet < 0.49:
        data_array = np.append(data_array, newdata['configs'][::2], axis=0)
    else:
        data_array = newdata['configs'][::2]

#lat = (128, 128)
#b_field = 0.1
#bet = 0.49

#b_fields_visual = [0, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075,
#                    0.08, 0.085, 0.09, 0.095, 0.1, 0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
#            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045,
#            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06,
#            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
#            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085,
#            0.09, 0.095, 0.1]

#filepart = 'Analyse/256x256/Visualize/Reverserun/'
#filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
#          + str(bet).replace('.', '') + 'external_field_' + str(b_field) + 'new' + '.npz'
#data = np.load(filename)
#print(len(data['configs'][int(40*20):])/20)
#print(len(b_fields_visual))
#quit()
ising = Ising_Ani(ising_data=data_array, name_data='beta', slider_data=beta_array, configs_per_value=int(200/2))
#ising = Ising_Ani(ising_data=data_array, name_data='beta', slider_data=beta_array, configs_per_value=int(200/2))
#ising = Ising_Ani(ising_data=data['configs'][int(40*20):], name_data='b_field', slider_data=b_fields_visual[40:], configs_per_value=20)

#plt.show()

#ani = Ising_Ani(ising_data=config_arr,
#                    slider_data=beta_arr)
ising.start_animation()
#plt.show()
ising.save('isingvisuwholerunreverse')
