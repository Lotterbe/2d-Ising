from Metropolis import Observables


beta_arr = [0.39, 0.395, 0.4, 0.405, 0.41, 0.4125, 0.415, 0.4175, 0.42, 0.4225, 0.425, 0.4275, 0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.43894, 0.43896, 0.43898, 0.44, 0.4402, 0.4404, 0.4406, 0.4408, 0.441, 0.4412, 0.44125, 0.4414, 0.4416, 0.4418, 0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45, 0.4525, 0.455, 0.4575, 0.46, 0.4625, 0.465, 0.4675, 0.47, 0.475, 0.48, 0.485, 0.49]


for b in beta_arr:
    filename = 'Analyse/256x256/Observablen/Neu_201229/' +  str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
               + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
    data = np.load(filename)
    observables = Observables(data['configs'], beta=b)
    observables.measure_observables()
    observables.save_simulation(filename)
    del observables
