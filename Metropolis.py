import numpy as np


class Metropolis:
    def __init__(self, x_lenght, y_lenght, iterationsteps, beta = 1, interaction = 1):
        self.NX = x_lenght
        self.NY = y_lenght
        self.total_number_of_points = self.NX * self.NY
        self.itersteps = iterationsteps
        self.actual_config = self.__init_config()
        self.save_number = 1
        self.skip = 100
        self.inter = interaction
        self.beta = beta

    def __init_config(self, categ='cold'):
        """Initialize start configuration hot or cold.

        :param categ: value for hot or cold start
        """
        self.all_configs = [None] * self.itersteps
        if categ == 'cold':
            init = np.ones([self.NX, self.NY]) * 1
        elif categ == 'hot':
            init = np.random.choice([-1, 1], (self.NX, self.NY))
        self.all_configs[0] = init
        return init

    def __configurator(self):
        random_number = np.random.randint(self.total_number_of_points)
        i = int(random_number/self.NX)
        j = random_number % self.NX
        return i, j

    def exponential_delta(self, dE):
        return np.exp(self.beta * dE)

    def save(self):
        self.all_configs[self.save_number] = self.actual_config
        self.save_number += 1

    def __update_step(self, step):
        nx, ny = self.__configurator()
        neighbours = self.actual_config[nx - 1, ny] \
                     + self.actual_config[nx, ny - 1] \
                     + self.actual_config[(nx + 1) % self.NX, ny] \
                     + self.actual_config[nx, (ny + 1) % self.NY]
        dE = self.inter * self.actual_config[nx, ny] * neighbours
        r = np.random.random(1)
        if self.exponential_delta(dE) >= r:
            if step % self.skip == 0:
                self.save()
            self.actual_config[nx, ny] *= (-1)

    def start_simulation(self):
        for step in range(0, self.itersteps):
            self.__update_step(step)





