from Metropolis import Metropolis
import numpy as np
from Plot import Ising_Plot

metro = Metropolis(10, 10, 1000000)
metro.start_simulation()
configs = metro.all_configs
plot_mod = Ising_Plot(configs)

