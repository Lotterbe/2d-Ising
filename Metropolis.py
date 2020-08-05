#from numba import jit
#from numba.experimental import jitclass
import numpy as np

#@jitclass
class Metropolis:

    def __init__(self, x_lenght, y_lenght, beta=0.8, interaction=1):
        self.NX = x_lenght
        self.NY = y_lenght
        self.total_number_of_points = self.NX * self.NY
        # check if (itersteps - first_skip) % skip == 0
        self.itersteps = 1020 * self.total_number_of_points
        self.first_skip = 20*self.total_number_of_points
        self.skip = 10*self.total_number_of_points
        # J = inter
        self.inter = interaction
        self.beta = beta
        # ca. 0.4406
        self.beta_crit = np.log(1+np.sqrt(2))/2
        self.actual_config = self._init_config()
        self.save_number = 0
        self.save_lenght = int((self.itersteps - self.first_skip) / self.skip) \
                           + (self.itersteps - self.first_skip) % self.skip
        self.all_configs = [None] * self.save_lenght
        self.energy_per_config = None
        self.energy_average = None
        self.m_per_config = None
        self.chi = None
        self.m_average = None
        self.heat_per_lattice = None

    #@jit(nopython=True)
    def _init_config(self):
        """Initialize start configuration hot or cold.

        """
        # cold one
        if self.beta >= self.beta_crit:
            init = np.ones([self.NX, self.NY]) * 1
        # hot one
        else:
            init = np.random.choice([-1, 1], (self.NX, self.NY))
        return init

    #@jit
    def __configurator(self):
        random_number = np.random.randint(self.total_number_of_points)
        i = int(random_number / self.NY)
        j = random_number % self.NY
        return i, j

    #@jit
    def exponential_delta(self, dE):
        return np.exp(-self.beta * dE)

    #@jit
    def save(self):
        # copy ist hier sehr sehr wichtig!
        self.all_configs[self.save_number] = np.copy(self.actual_config)
        self.save_number += 1

    #@jit
    def __update_step(self, step):
        nx, ny = self.__configurator()
        neighbours = self.actual_config[nx - 1, ny] \
                     + self.actual_config[nx, ny - 1] \
                     + self.actual_config[(nx + 1) % self.NX, ny] \
                     + self.actual_config[nx, (ny + 1) % self.NY]
        dE = 2 * self.inter * self.actual_config[nx, ny] * neighbours
        r = np.random.random(1)
        #r_arr = np.random.random(10)
        #changer_arr = np.where(r_arr <= self.exponential_delta(dE), -1, 1)
        #changer = np.prod(np.where(r_arr <= self.exponential_delta(dE), -1, 1))
        #self.actual_config[nx, ny] *= changer
        if self.exponential_delta(dE) >= r:
            self.actual_config[nx, ny] *= (-1)
            # nicht jeder Simulationsschritt, ob change nun akzeptiert
            # oder nicht, soll gespeichert werden
        if step >= self.first_skip and step % self.skip == 0:
            self.save()
            # Flip Flop
            self.actual_config *= (-1)

    #@jit
    def start_simulation(self):
        print('Starting Simulation..')
        print(self.save_lenght, ' configs will come out.')
        for step in range(0, self.itersteps):
            self.__update_step(step)

    def measure_observables(self):
        self.total_energy()
        self.specific_heat()
        self.magnetisation()
        self.magnetic_susceptibility()
        self.energy_var = self.jackknife(self.energy_per_config)
        self.magnetisation_var = self.jackknife(self.m_per_config)



    def magnetisation(self):
        self.m_per_config = np.abs(np.sum(np.sum(self.all_configs, axis=2), axis=1))\
                       / self.total_number_of_points
        self.m_average = np.mean(self.m_per_config)
        #return self.m_average

    def total_energy(self):
        self.energy_per_config = - self.beta * self.inter * np.sum(
            np.sum((self.all_configs * (np.roll(self.all_configs, shift=1, axis=1)
                                        + np.roll(self.all_configs, shift=1, axis=2)
                                        )), axis=2), axis=1)
        # per lattice? or not?
        self.energy_average = np.mean(self.energy_per_config)

        #return self.energy_average

    def specific_heat(self):
        # variance of energy
        squared_energy_average = np.mean(self.energy_per_config ** 2)
        self.heat_per_lattice = self.beta ** 2 * (squared_energy_average
                                                  - self.energy_average ** 2) \
                                / self.total_number_of_points
        #return self.heat_per_lattice

    def magnetic_susceptibility(self):
        # variance of magnetisation
        squared_magnetisation_average = np.mean(self.m_per_config ** 2)
        self.chi = self.beta * (squared_magnetisation_average
                                - (self.m_average) ** 2) * self.total_number_of_points
        #return self.chi


    def save_simulation(self, filename):
        array_list = ['#' + str(len(self.all_configs)) + ' configs',
                      '#' + str(self.total_number_of_points) + ' lattice points',
                      '#' + str(self.beta) + ' beta',
                      '#' + str(self.inter) + ' interaction']
        np.savez(filename, infos=array_list, configs=self.all_configs,
                 magnetisation=self.m_average, energy=self.energy_average,
                 specific_heat=self.heat_per_lattice, chi=self.chi)


    def jackknife(self, observable_per_config, block_number=10):
        blocks = block_number
        observable = observable_per_config
        if len(observable) % blocks == 0:
            obs_part = np.array([np.mean(np.roll(observable, shift=-part*blocks, axis=0)[:-blocks])
                        for part in range(blocks)])
            obs_part_mean = np.mean(obs_part)
            obs_var = (block_number - 1) / block_number * np.sum((obs_part - obs_part_mean)**2)
            return obs_var
        else:
            raise ValueError('Please choose a number of blocks in which the number of configs could be divided.')






