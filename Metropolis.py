import numpy as np


class Metropolis:
    def __init__(self, x_lenght, y_lenght, iterationsteps, beta = 0.8, interaction = 0.3):
        self.NX = x_lenght
        self.NY = y_lenght
        self.total_number_of_points = self.NX * self.NY
        self.itersteps = iterationsteps
        self.save_number = 1
        self.skip = 1000
        self.inter = interaction
        self.beta = beta
        self.actual_config = self.__init_config()

    def __init_config(self, categ='hot'):
        """Initialize start configuration hot or cold.

        :param categ: value for hot or cold start
        """
        self.all_configs = [None] * (int(self.itersteps/self.skip) + 1)
        if categ == 'cold':
            init = np.ones([self.NX, self.NY]) * 1
        elif categ == 'hot':
            init = np.random.choice([-1, 1], (self.NX, self.NY))
        self.all_configs[0] = np.copy(init)
        return init

    def __configurator(self):
        random_number = np.random.randint(self.total_number_of_points)
        i = int(random_number/self.NX)
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
            self.actual_config[nx, ny] *= (-1)
        # nicht jeder Simulationsschritt, ob change nun akzeptiert
        # oder nicht, soll gespeichert werden
        if step % self.skip == 0:
            self.save()

    def start_simulation(self):
        for step in range(0, self.itersteps):
            self.__update_step(step)





