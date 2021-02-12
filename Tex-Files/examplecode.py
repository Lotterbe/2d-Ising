from Metropolis import Metropolis, Observables
from Ising_Visualizing import Ising_Ani

for beta in beta_arr:
    metro = Metropolis(*lat, beta)
    configs = metro.start_simulation()
    observables = Observables(configs, beta)
    observables.measuring_observables()
    observables.save_simulation(filename)

ani = Ising_Ani(ising_data=config_arr,
                    slider_data=beta_arr)
ani.start_animation()
