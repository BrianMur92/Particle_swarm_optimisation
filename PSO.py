# Author:       Brian Murphy
# Date started: 16/03/2020
# Last updated: <08/05/2020 09:52:57 (BrianM)>

import numpy as np
import time


def default_PSO_params(params):
    """
    This is to set the default PSO parameters. Note by default constriction will be applied over inertia weighting.
    To prevent this, specify the wdamp parameter that isn't 1.

    Will display info by default

    Early stopping is disabled by default
    """
    if 'maxit' not in params:
        params['maxit'] = 30
    if 'n_part' not in params:
        params['n_part'] = 15
    if 'w' not in params:
        params['w'] = 1
    if 'wdamp' not in params:
        params['wdamp'] = 1
    if 'c1' not in params:
        params['c1'] = 2.05
    if 'c2' not in params:
        params['c2'] = 2.05
    if 'con' not in params and params['wdamp'] != 1 and params['w'] != 1:
        params['con'] = 0.7298437881283576
    if 'display_info' not in params:
        params['display_info'] = 1
    if 'early_stopping' not in params:
        params['early_stopping'] = 0
    if 'early_stopping_rounds' not in params:
        params['early_stopping_rounds'] = 10
    if 'BPSO' not in params:
        params['BPSO'] = 0
    if 'velocity_limit_scale' not in params and params['BPSO'] == 0:
        params['velocity_limit_scale'] = 0.2
    elif params['BPSO'] == 1:
        params['velocity_limit_scale'] = 1

    return params


class Particle:
    def __init__(self):
        self.position = 0
        self.velocity = 0
        self.pbest_position = self.position
        self.pbest_value = float('inf')

    def initial_position(self, varmin, varmax, BPSO):
        if not BPSO:
            self.position = np.random.uniform(low=varmin, high=varmax, size=[1, len(varmin)])[0]
        else:
            self.position = np.random.uniform(low=0, high=1, size=[1, len(varmin)])[0]
        self.pbest_position = self.position
        self.velocity = np.random.uniform(low=varmin, high=varmax, size=[1, len(varmin)])[0]

    def update_velocity(self, con, w, c1, c2, gbest_position, min_velocity, max_velocity):
        self.velocity = con * ((w * self.velocity)
                               + (c1 * np.random.rand() * (self.pbest_position - self.position))
                               + (c2 * np.random.rand() * (gbest_position - self.position)))
        # Apply velocity limits
        self.velocity = np.max([self.velocity, min_velocity], axis=0)
        self.velocity = np.min([self.velocity, max_velocity], axis=0)

    def update_position(self, varmin, varmax, BPSO):
        if not BPSO:
            self.position = self.position + self.velocity
            # Apply position limits
            self.position = np.max([self.position, varmin], axis=0)
            self.position = np.min([self.position, varmax], axis=0)
        else:
            sig_velocity = self.sigmoid(self.velocity)
            self.position = np.array([1 if np.random.rand(1) < p else 0 for p in sig_velocity])

    def sigmoid(self, x):
        return 1.0/(1.0 + np.exp(-x))


def examine_particles(particles_vector, gbest_position):
    converged = 0
    ham_dist = []
    for particle in particles_vector:
        if all(particle.position == gbest_position):
            converged += 1
        ham_dist.append(sum(particle.position != gbest_position))
    return {'number_converged': converged, 'particle_hamming_distance': ham_dist}


def PSO(problem, params, *args):
    """
    Syntax: gbest_value, gbest_position, best_costs = PSO.PSO(problem, params)

    Inputs:
        problem       - This is a mandatory dictionary that contains the cost function, parameter minimum vales
                        and parameter maximum values
        params        - These are the parameters needed to specify PSO parameters. Ideally specified by the user but
                        default values are available

    Outputs:
        gbest_value     - This is the best performance achieved by PSO
        gbest_position  - This is the set of parameters that gave the best performance
        best_costs      - This is a numpy array containing the costs achieved for each iteration

    Example:
        import numpy as np
        import PSO

        print('Find the centre of a circle of the form (x-a)^2 + (y-b)^2 = r^2 where x, y and r equal 3, 4 and 5.')


        # Define the cost function
        def circle_cost(positions):
            return np.abs(25 - ((3 - positions[0]) ** 2 + (4 - positions[1]) ** 2))


        cost_function = circle_cost

        # Set maximum values of a and b
        varmin = [-1000, -1000]  # a min, b min
        varmax = [1000, 1000]  # a max, b max

        # Create problem dictionary
        problem = {'cost_function': cost_function, 'varmin': varmin, 'varmax': varmax}

        # Create PSO parameters dictionary
        params = {'maxit': 15, 'n_part': 30, 'c1': 2, 'c2': 2, 'w': 0.9, 'wdamp': 0.2, 'con': 1, 'display_info': 1,
                  'early_stopping': 1, 'early_stopping_rounds': 7}

        # Run PSO and return lowest cost, a,b values and the costs per iteration
        gbest_value, gbest_position, best_costs = PSO.PSO(problem, params)

        print('Found the centre of the circle as a = %f and b = %f' % (gbest_position[0], gbest_position[1]))
        print('The error was %f' % gbest_value)

    """
    if not args:
        args = []

    # Setting the random seed based off the current time
    np.random.seed(int(time.time()))

    cost_function = problem['cost_function']  # This tells PSO what the cost function is
    varmin = np.array(problem['varmin'])  # list of minimum lower bound values
    varmax = np.array(problem['varmax'])  # list of maximum upper bound values

    params = default_PSO_params(params)

    maxit = params['maxit']  # maximum number of PSO iterations
    n_part = params['n_part']  # number of PSO particles

    w = params['w']  # inertia coefficient
    wdamp = params['wdamp']  # damping factor for inertia coefficient
    c1 = params['c1']  # personal acceleration coefficient
    c2 = params['c2']  # global acceleration coefficient
    con = params['con']  # constriction value

    display_info = params['display_info']  # flag to show iteration info
    max_velocity = params['velocity_limit_scale'] * (varmax - varmin)
    min_velocity = -max_velocity


    particles_vector = [Particle() for _ in range(n_part)]  # create the particles


    gbest_value = float('inf')
    gbest_position = []

    for particle in particles_vector:  # set particles initial position within confines
        particle.initial_position(varmin, varmax, params['BPSO'])
        particle.pbest_position = particle.position
        particle.pbest_value = cost_function(particle.position, args)
        if particle.pbest_value < gbest_value:
            gbest_value = particle.pbest_value
            gbest_position = particle.pbest_position

    best_costs = np.zeros(maxit+1)
    best_costs[0] = gbest_value  # track best costs
    particle_debug = []
    # Enter main PSO loop
    for it in range(maxit):
        particle_debug.append(examine_particles(particles_vector, gbest_position))
        for particle in particles_vector:
            # Update velocity
            particle.update_velocity(con, w, c1, c2, gbest_position, min_velocity, max_velocity)

            # Update position
            particle.update_position(varmin, varmax, params['BPSO'])

            # Evaluate the cost at the new function
            cost_at_new_position = cost_function(particle.position, args)
            if cost_at_new_position < particle.pbest_value:
                particle.pbest_value = cost_at_new_position
                particle.pbest_position = particle.position
                if cost_at_new_position < gbest_value:
                    gbest_value = cost_at_new_position
                    gbest_position = particle.pbest_position

        best_costs[it+1] = gbest_value

        if display_info:
            print('Iteration: ', str(it), '  Best cost: ', str(gbest_value), '  Best position: ', str(gbest_position))

        w = w * wdamp

        if params['early_stopping'] and it > params['early_stopping_rounds']:
            if np.abs(best_costs[it+1] - best_costs[it+1 - params['early_stopping_rounds']]) < 0.0001:

                if display_info:
                    print('Stopping at round: ', str(it), ' as there was no performnce increase in ',
                          str(params['early_stopping_rounds']), 'rounds')
                    print('Best cost: ', str(gbest_value), '  Best position: ', str(gbest_position))
                return gbest_value, gbest_position, best_costs

    if display_info:
        print('Finished the PSO process')
        print('Best cost: ', str(gbest_value), '  Best position: ', str(gbest_position))
    return gbest_value, gbest_position, best_costs
