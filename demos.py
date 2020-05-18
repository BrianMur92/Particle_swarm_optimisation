# Author:       Brian Murphy
# Date started: 07/05/2020
# Last updated: <06/05/2020 05:49:32 (BrianM)>

import numpy as np
import PSO


def find_the_centre_of_a_circle():
    """
    Find the centre of a circle of the form (x-a)^2 + (y-b)^2 = r^2 where x, y and r equal 3, 4 and 5 respectfully

    Example - how to run:
        import demos
        demos.find_the_centre_of_a_circle()

    """
    # Define the cost function
    def circle_cost(positions, args):
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

