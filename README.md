Particle Swarm Optimisation: A python implementation
============================================

Python code that is used to implement particle swarm optimisation (PSO). PSO is an optimisation algorithm based on the flocking patterns of birds. It is a simple optimisation scheme that does not require complex operations. This file will provide details on how to use set up and use the python PSO file. 


---

[Requirements](#requirements) | [Use](#use) | [Files](#files) | [Test computer
setup](#test-computer-setup) | [Licence](#licence) | [References](#references) |
[Contact](#contact)

## Requirements:
Python 3.7 or newer with the following packages installed
| Package       | Version installed  |
| ------------- |:------------------:|
| numpy         | 1.17.1             |


## Use 

Set path `(Particle_swarm_optimisation)` to the folder location of Particle_swarm_optimisation. Then the following will load the main functions:
```
  import sys
  sys.path.append(Particle_swarm_optimisation)
  import PSO
```

As an example, we will use PSO to find the centre of a circle of the form (x-a)^2 + (y-b)^2 = r^2 where x, y and r equal 3, 4 and 5 respectfully:
```
  import numpy as np

  # Define the cost function
  def circle_cost(positions, args):
    return np.abs(25 - ((3 - positions[0])**2 + (4 - positions[1])**2))
  cost_function = circle_cost

  # Set maximum values of a and b
  varmin = [-1000, -1000]  # a min, b min
  varmax = [1000, 1000]    # a max, b max

  # Create problem dictionary
  problem = {'cost_function': cost_function, 'varmin': varmin, 'varmax': varmax}

  # Create PSO parameters dictionary
  params = {'maxit': 15, 'n_part': 30, 'c1': 2, 'c2': 2, 'w': 0.9, 'wdamp': 0.2, 'con': 1, 'display_info': 1,
            'early_stopping': 1, 'early_stopping_rounds': 7}

  # Run PSO and return lowest cost, a,b values and the costs per iteration
  gbest_value, gbest_position, best_costs = PSO.PSO(problem, params)

```

The PSO function takes in 2 arguments and the possibility to add more in the form of *args if the cost function needs them.


The first parameter is the `problem` parameter, it is a dictionary and the following values are needed in the dictionary:
| Value            | Purpose                               |
| ---------------- |:-------------------------------------:|
| 'cost_function'  | Cost function that PSO is to evaluate |
| 'varmin'         | Minimum possible particle locations   |
| 'varmax'         | Maximum possible particle locations   |



The second parameter is the `params` parameter, it is a dictionary and has lots of default parameters so they do not need to be specified all the time:
| Value                   | Purpose                                          | Default  |
| ----------------------- |:------------------------------------------------:|:--------:|
| 'maxit'                 | Max number of PSO iterations                     |30        |
| 'n_part'                | Number of PSO particles                          |15        |
| 'w'                     | Inertia weight                                   |1         |
| 'wdamp'                 | Inertia weight damping factor                    |1         |
| 'c1'                    | Personal constant                                |2.05      |
| 'c2'                    | Social constant                                  |2.05      |
| 'con'                   | Constriction factor                              |0.7298    |
| 'display_info'          | Display information after each iteration         |1         |
| 'early_stopping'        | Use early stopping                               |0         |
| 'early_stopping_rounds' | How many rounds to stop after if no improvement  |10        |
| 'velocity_limit_scale'  | Scaling factor used to set max velocity          |0.2       |




## Files
Some python files (.py files) have a description and an example in the header. To read this
header, type `help(filename)` in the console after importing (`import filename`).  Directory structure is as follows: 
```
├── CHANGELOG.md          # changelog file
├── LICENSE.md            # license file 
├── PSO.py                # PSO file
└── README.md             # readme file describing project
```




## Test computer setup
- hardware:  Intel Core i7-8700K @ 3.2GHz; 32GB memory.
- operating system: Windows 10 64-bit
- software: python 3.7


## Licence

```
Copyright (c) 2020, Brian M. Murphy, University College Cork
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

  Neither the name of the University College Cork nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```


## References

1. Kennedy, James, and Russell Eberhart. "Particle swarm optimization." Proceedings of ICNN'95-International Conference on Neural Networks. Vol. 4. IEEE, 1995.

2. Shi, Yuhui, and Russell Eberhart. "A modified particle swarm optimizer." 1998 IEEE international conference on evolutionary computation proceedings. IEEE world congress on computational intelligence (Cat. No. 98TH8360). IEEE, 1998.

3. Clerc, Maurice, and James Kennedy. "The particle swarm-explosion, stability, and convergence in a multidimensional complex space." IEEE transactions on Evolutionary Computation 6.1 (2002): 58-73.




## Contact

Brian M. Murphy

Neonatal Brain Research Group,  
[INFANT Research Centre](https://www.infantcentre.ie/),  
Department of Paediatrics and Child Health,  
Room 2.18 UCC Academic Paediatric Unit, Cork University Hospital,  
University College Cork,  
Ireland

- email: Brian.M.Murphy AT umail dot ucc dot ie 