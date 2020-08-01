import numpy as np


class Metropolis:
    def __init__(self, x_lenght, y_lenght, iterationsteps, beta=0.8, interaction=1):
        self.NX = x_lenght
        self.NY = y_lenght
        self.total_number_of_points = self.NX * self.NY
        #self.itersteps = iterationsteps
        self.itersteps = 200 * self.total_number_of_points
        self.save_number = 0
        self.first_skip = 100*self.total_number_of_points
        self.skip = self.total_number_of_points
        self.inter = interaction
        self.beta = beta
        self.actual_config = self.__init_config()
        self.energy_per_config = None
        self.energy_average = None
        self.m_per_config = None
        self.chi = None
        self.m_average = None
        self.heat_per_lattice = None

    def __init_config(self, categ='hot'):
        """Initialize start configuration hot or cold.

        :param categ: value for hot or cold start
        """
        self.all_configs = [None] * (int((self.itersteps - self.first_skip)
                                         / self.skip) +
                                     (self.itersteps - self.first_skip) % self.skip)
        if categ == 'cold':
            init = np.ones([self.NX, self.NY]) * 1
        elif categ == 'hot':
            init = np.random.choice([-1, 1], (self.NX, self.NY))
        #self.all_configs[0] = np.copy(init)
        return init

    def __configurator(self):
        random_number = np.random.randint(self.total_number_of_points)
        i = int(random_number / self.NX)
        j = random_number % self.NX
        return i, j

    def exponential_delta(self, dE):
        return np.exp(-self.beta * dE)

    def save(self):
        # copy ist hier sehr sehr wichtig!
        self.all_configs[self.save_number] = np.copy(self.actual_config)
        self.save_number += 1

    def __update_step(self, step):
        nx, ny = self.__configurator()
        neighbours = self.actual_config[nx - 1, ny] \
                     + self.actual_config[nx, ny - 1] \
                     + self.actual_config[(nx + 1) % self.NX, ny] \
                     + self.actual_config[nx, (ny + 1) % self.NY]
        dE = 2 * self.inter * self.actual_config[nx, ny] * neighbours
        r = np.random.random(1)
        if self.exponential_delta(dE) >= r:
            # nicht jeder Simulationsschritt, ob change nun akzeptiert
            # oder nicht, soll gespeichert werden
            if step >= self.first_skip and step % self.skip == 0:
                self.save()
            self.actual_config[nx, ny] *= (-1)

    def start_simulation(self):
        for step in range(0, self.itersteps):
            self.__update_step(step)


    def magnetisation(self):
        self.m_per_config = np.abs(np.sum(np.sum(self.all_configs, axis=2), axis=1))\
                       / self.total_number_of_points
        print(len(self.m_per_config))
        self.m_average = np.mean(self.m_per_config)
        return self.m_average

    def total_energy(self):
        self.energy_per_config = self.inter * np.sum(
            np.sum((self.all_configs * (np.roll(self.all_configs, shift=1, axis=1)
                                        + np.roll(self.all_configs, shift=1, axis=2)
                                        )), axis=2), axis=1)
        # per lattice? or not?
        self.energy_average = np.mean(self.energy_per_config)
        return self.energy_average

    def specific_heat(self):
        # variance of energy
        # check if division by volume is neaded
        squared_energy_average = np.mean(self.energy_per_config ** 2)
        self.heat_per_lattice = self.beta ** 2 * (squared_energy_average
                                                  - self.energy_average ** 2) \
                                / self.total_number_of_points
        return self.heat_per_lattice

    def magnetic_susceptibility(self):
        # variance of magnetisation
        squared_magnetisation_average = np.mean(self.m_per_config ** 2)
        self.chi = self.beta * (squared_magnetisation_average
                                - (self.m_average) ** 2) * self.total_number_of_points
        return self.chi, self.beta * np.std(self.m_per_config)


    def save_simulation(self, filename):
        #from tempfile import TemporaryFile
        #outfile = TemporaryFile()
        array_list = ['#' + str(len(self.all_configs)) + ' configs',
                      '#' + str(self.total_number_of_points) + ' lattice points',
                      '#' + str(self.beta) + ' beta',
                      '#' + str(self.inter) + ' interaction']
        #name = str(outfile + '/' + filename)
        #name = outfile
        np.savez(filename, infos=array_list, configs=self.all_configs,
                 magnetisation=self.m_average, energy=self.energy_average,
                 specific_heat=self.heat_per_lattice, chi=self.chi)
