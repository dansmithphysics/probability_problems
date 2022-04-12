#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
The company Optiver presents three puzzles
to solve along with their application to
be a quantitative researcher with them.

Below is the solution to the second problem.

An ant starts at the origin. It can take a random
step in any of the cardinal directions every second.
It moves 10 cm / s and is looking for food.

Food is located along a diagonal line passing 
through (10cm, 0cm) and (0cm, 10cm) points. How long 
does it take to get to the food on average?

I deploy a toy MC to solve this problem.
The function `ant_walk` walks the ant until it
reaches the wall and returns how many steps it
took to get there. The number of steps
is equal to the number of seconds there.
With this function, I produce a distribution
of stop times and find the mean.

The mean time is infinite. Increasing the `max_step`
in the function `ant_walk` returns longer and longer
mean time. I am tempted to say that it converges
since diffusion should go as 1/r^2. However,
numerical solutions suggest the mean does not converge.
"""

import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool


def ant_walk(max_step=1000):
    """
    Randomly walks the ant until it reaches food.
    Effectively a markov chain with a stopping condition.

    Parameters
    ----------
    max_step : int
        The maximum number of steps taken until the 
        loop is terminated. 
    """

    step, x, y = 0, 0, 0

    while(y + x - 1.0 != 0.0):
        move_dir = np.random.choice(np.arange(4))

        if(move_dir == 0):
            x += 1.0
        elif(move_dir == 1):
            y += 1.0
        elif(move_dir == 2):
            x -= 1.0
        elif(move_dir == 3):
            y -= 1.0
        
        step += 1

        if(step > max_step):
            break
        
    return step


if __name__ == "__main__":
    nthrows = 10000

    n_cpu = 4
    pool = Pool(n_cpu)
    max_step = 1000
    nsteps_max1000 = pool.map(ant_walk,
                              max_step * np.ones(nthrows))
    max_step = 10000
    nsteps_max10000 = pool.map(ant_walk,
                               max_step * np.ones(nthrows))
    max_step = 100000
    nsteps_max100000 = pool.map(ant_walk,
                                max_step * np.ones(nthrows))
    pool.close()

    print("The mean after max steps of 1000: \t %.2f" % (np.mean(nsteps_max1000)))
    print("The mean after max steps of 10000: \t %.2f" % (np.mean(nsteps_max10000)))
    print("The mean after max steps of 100000: \t %.2f" % (np.mean(nsteps_max100000)))
