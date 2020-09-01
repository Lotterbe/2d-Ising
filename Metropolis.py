from numba import jitclass, int64, float64
import numpy as np
from scipy.special import ellipk as elli

spec = [('NX', int64), ('NY', int64), ('total_number_of_points', int64),
        ('itersteps', int64), ('first_skip', int64), ('skip', int64),
        ('inter', float64), ('beta', float64), ('beta_crit', float64),
        ('actual_config', int64[:, :]), ('save_number', int64),
        ('save_lenght', int64), ('all_configs', int64[:, :, :]),
        ('b_ext', float64)]


@jitclass(spec)
class Metropolis:
    def __init__(self, x_lenght, y_lenght, beta=0.20, external_field=0):
        """ Constructor - defines the attributes

        :param x_lenght: x-lenght of lattice
        :param y_lenght: y-lenght of lattice
        :param beta: the inverse temperature
        :param external_field: external magnetic field
        """
        self.NX = x_lenght
        self.NY = y_lenght
        self.total_number_of_points = self.NX * self.NY
        # check if (itersteps - first_skip) % skip == 0
        self.itersteps = 1020 * self.total_number_of_points
        self.first_skip = 20 * self.total_number_of_points
        self.skip = 10 * self.total_number_of_points
        # J = inter
        self.inter = 1
        self.beta = beta
        # ca. 0.4406
        self.beta_crit = np.log(1 + np.sqrt(2)) / 2
        self.actual_config = self._init_config()
        self.save_number = 0
        self.save_lenght = int((self.itersteps - self.first_skip)
                               / self.skip) + \
                           (self.itersteps - self.first_skip) % self.skip
        self.all_configs = np.zeros((self.save_lenght, self.NX, self.NY),
                                    dtype=np.int64)
        self.b_ext = external_field

    def _init_config(self):
        """Initialize start configuration hot or cold.

        :return: the initial config of lattice
        """
        # cold one
        if self.beta >= self.beta_crit:
            return np.ones((self.NX, self.NY), dtype=np.int64)
        # hot one
        else:
            return np.random.choice(np.array((-1, 1)), (self.NX, self.NY))

    def __configurator(self):
        """Choose random spin out of lattice

        :return: The corresponding line and column of the choosen spin
        """
        random_number = np.random.randint(self.total_number_of_points)
        i = int(random_number / self.NY)
        j = random_number % self.NY
        return i, j

    def exponential_delta(self, dE):
        """Calculates the change in the action

        :param dE: change in energy
        :return: change in action
        """
        return np.exp(-self.beta * dE)

    def save(self):
        """Saves actual config in an array """
        # copy is very important here!
        self.all_configs[self.save_number] = np.copy(self.actual_config)
        self.save_number += 1

    def __update_step(self, step):
        """The main update routine:
        - Chooses random spin and flips it
        - Checks how action changes
        - If accepted, then leaves the flipped spin otherwise undoes it
        - Skip a few configs in the saved configs array
        for autocorrelation reasons

        :param step: Number of updates
        """
        nx, ny = self.__configurator()
        neighbours = self.actual_config[nx - 1, ny] \
                     + self.actual_config[nx, ny - 1] \
                     + self.actual_config[(nx + 1) % self.NX, ny] \
                     + self.actual_config[nx, (ny + 1) % self.NY]
        dE = 2 * self.inter * self.actual_config[nx, ny] * neighbours \
             - self.b_ext * self.actual_config[nx, ny] * (-1)
        r = np.random.random(1)[0]
        if self.exponential_delta(dE) >= r:
            self.actual_config[nx, ny] *= (-1)
            # Vermeidung von Autokorrelationen
        if step >= self.first_skip and step % self.skip == 0:
            self.save()
            # Flip Flop
            self.actual_config *= (-1)

    def start_simulation(self):
        """This method starts the whole simulation and updates
        the configs itersteps times.

        :return: The saved configs after itersteps updates.
        """
        print('Starting Simulation..')
        print(self.save_lenght, ' configs will come out.')
        for step in range(0, self.itersteps):
            self.__update_step(step)
        return self.all_configs


class Observables:
    def __init__(self, configs, beta, inter=1, external_field=0):
        """Constructor - defines some attributes

        :param configs: the simulated configs of lattice
        :param beta: inverse temperature
        :param inter: interaction
        :param external_field: external magnetic field
        """
        self.all_configs = configs
        self.total_number_of_points = len(self.all_configs[0]) \
                                      * len(self.all_configs[0][0])
        self.beta = beta
        self.beta_crit = np.log(1 + np.sqrt(2)) / 2
        self.inter = inter
        self.b_ext = external_field
        self.save_lenght = len(configs)
        self.energy_per_config = np.zeros(self.save_lenght,
                                          dtype=np.float64)
        self.energy_average = 0
        self.m_per_config = np.zeros(self.save_lenght,
                                     dtype=np.float64)
        self.m_average = 0
        self.chi = 0
        self.heat_per_lattice = 0
        self.energy_var = 0
        self.magnetisation_var = 0
        self.heat_var = 0
        self.chi_var = 0

    def magnetisation(self):
        """Calculates the magnetisation of lattice

        """
        self.m_per_config = np.abs(np.sum(np.sum(self.all_configs, axis=2),
                                          axis=1)) \
                            / self.total_number_of_points
        self.m_average = np.mean(self.m_per_config)

    def total_energy(self):
        """Calculates the energy of the lattice

        """
        self.energy_per_config = - self.beta * self.inter * np.sum(np.sum((
                self.all_configs * (np.roll(self.all_configs, shift=1,
                                            axis=1)
                                    + np.roll(self.all_configs, shift=1,
                                              axis=2))), axis=2), axis=1) \
                                 - self.b_ext * np.sum(self.all_configs)
        self.energy_average = np.mean(self.energy_per_config)

    def specific_heat(self):
        """Calculates the specific heat, the variance of energy

        """
        squared_energy_average = np.mean(self.energy_per_config ** 2)
        self.heat_per_lattice = self.beta ** 2 * (
                squared_energy_average - self.energy_average ** 2
        ) / self.total_number_of_points

    def magnetic_susceptibility(self):
        """Calculates the magnetic susceptibility,
        the variance of magnetisation

        """
        squared_magnetisation_average = np.mean(self.m_per_config ** 2)
        self.chi = self.beta * (
                squared_magnetisation_average - self.m_average ** 2
        ) * self.total_number_of_points

    def measure_observables(self):
        """This method starts the whole measuring of the observables
         for the simulated lattice

        """
        print('Start Measuring...')
        self.total_energy()
        self.specific_heat()
        self.magnetisation()
        self.magnetic_susceptibility()
        self.energy_var = self.jackknife(self.energy_per_config,
                                         del_number=10)
        self.magnetisation_var = self.jackknife(self.m_per_config,
                                                del_number=10)
        self.heat_var = self.beta * self.jackknife_for_var(
            self.energy_per_config, del_number=10
        ) / self.total_number_of_points
        self.chi_var = np.sqrt(self.beta) * self.jackknife_for_var(
            self.m_per_config, del_number=10
        ) * self.total_number_of_points

    def save_simulation(self, filename):
        """Saves the configs and measured observables in a compressed file.
        Measure_observables method must be called before otherwise
        there will be zeros as values.

        :param filename: Name for the file in which values will be saved.
        """
        array_list = ['#' + str(len(self.all_configs)) + ' configs',
                      '#' + str(self.total_number_of_points) +
                      ' lattice points', '#' + ' beta = ' +
                      str(self.beta), '#' + ' interaction = ' +
                      str(self.inter), '#' +
                      ' external magnetic field = ' + str(self.b_ext)]
        np.savez_compressed(
            filename, infos=array_list, configs=self.all_configs,
            magnetisation=self.m_average,
            magnetisation_var=self.magnetisation_var,
            energy=self.energy_average / self.total_number_of_points,
            energy_var=self.energy_var / self.total_number_of_points,
            specific_heat=self.heat_per_lattice, heat_var=self.heat_var,
            chi=self.chi, chi_var=self.chi_var
        )

    def jackknife(self, observable_per_config, del_number=1):
        """Calculates the error with jackknife for primary observables.

        :param observable_per_config: The observable for which
        error will be calculated
        :param del_number: How big the blocks are and therefore
        how much values are 'deleted' for creating new data set
        :return: estimator for standard deviation for the observable
        """
        observable = observable_per_config
        number_of_configs = len(observable)
        obs_part = [np.mean(np.roll(observable, shift=-part * del_number,
                                    axis=0)[:- del_number])
                    for part in range(number_of_configs)]
        obs_part_mean = np.mean(obs_part)
        obs_var = (number_of_configs - del_number) / number_of_configs * \
                  np.sum((np.array(obs_part) - obs_part_mean) ** 2)
        return np.sqrt(obs_var)

    def jackknife_for_var(self, observable_per_config, del_number=10):
        """Calculates the error with jackknife for secundary observables.

        :param observable_per_config: The primary observable
        :param del_number: How big the blocks are and therefore
        how much values are 'deleted' for creating new data set
        :return: estimator for standard deviation
        for the secundary observable
        """
        base_observable = observable_per_config
        number_of_configs = len(base_observable)
        obs_base_part_squared = np.array([np.mean(
            np.roll(base_observable, shift=-part * del_number,
                    axis=0)[:- del_number]
        ) ** 2 for part in range(number_of_configs)])
        obs_base_square_part = np.array([np.mean(
            np.roll(base_observable ** 2, shift=-part * del_number,
                    axis=0)[:- del_number]
        ) for part in range(number_of_configs)])
        obs_part = obs_base_square_part - obs_base_part_squared
        obs_part_mean = np.mean(obs_part)
        obs_var = (number_of_configs - del_number) / number_of_configs * \
                  np.sum((obs_part - obs_part_mean) ** 2)
        return np.sqrt(obs_var)

    def OnsagerEnergy(self):
        # Some variables for simpler calculating
        k = 1 / ((np.sinh(2 * self.beta * self.inter)) ** 2)
        l = 4 * k * (1 + k) ** -2
        integral = elli(l)
        self.onsager_energy = - self.beta * self.inter / np.tanh(
            2 * self.beta * self.inter
        ) * (1 + 2 / np.pi * (2 * np.tanh(
            2 * self.beta * self.inter
        ) ** 2 - 1) * integral)
        return self.onsager_energy

    def OnsagerEnergy2(self):
        # Some variables for simpler calculating
        k = 2 * np.tanh(2 * self.beta * self.inter) ** 2 - 1
        l = (2 * np.sinh(2 * self.beta * self.inter)) \
            / (np.cosh(2 * self.beta * self.inter) ** 2)
        integral = elli(l)
        self.onsager_energy = (-(self.beta * self.inter)
                               / (np.tanh(2 * self.beta * self.inter))) *\
                              (1 + 2 / np.pi * k * integral)
        return self.onsager_energy

    def EnergyPerLatticePoint(self):
        if self.energy_average == 0:
            self.total_energy()
        self.energy_per_lattice_point = self.energy_average / \
                                        self.total_number_of_points
        return self.energy_per_lattice_point

    def DeltaEnergy(self):
        delta_energy = np.abs(
            self.onsager_energy - self.energy_per_lattice_point
        )
        return delta_energy

    def OnsagerMagn(self):
        # Is only for T < T_c not equal to zero => beta > beta_c 
        if self.beta > self.beta_crit:
            self.onsager_magnetisation = (1 - np.sinh(
                np.log(1 + np.sqrt(2) * self.beta / self.beta_crit)
            ) ** (-4)) ** (1 / 8)
        else:
            self.onsager_magnetisation = 0
        return self.onsager_magnetisation

    def DeltaMagnetisation(self):
        delta_magnetisation = np.abs(
            self.onsager_magnetisation - self.m_average
        )
        return delta_magnetisation
