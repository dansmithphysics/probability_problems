#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
The company Optiver presents three puzzles
to solve along with their application to
be a quantitative researcher with them.

Below is the solution to the first problem.

An ant starts at the origin. It can take a random
step in any of the cardinal directions every second.
It moves 10 cm / s and is looking for food.

If the ant starts in the middle of a box that is
40 cm in side length, how long does it take to
get to the food on average?

I deploy a toy MC to solve this problem.
The function `ant_walk` walks the ant until it
reaches the wall and returns how many steps it
took to get there. The number of steps
is equal to the number of seconds there.
With this function, I produce a distribution
of stop times and find the mean.

The answer is 4.5 seconds.
"""

import numpy as np
import matplotlib.pyplot as plt


def ant_walk():
    """
    Randomly walks the ant until it reaches food.
    Effectively a markov chain with a stopping condition.
    """

    step, x, y = 0, 0, 0
    while(np.abs(y) != 2.0 and np.abs(x) != 2.0):
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
    return step


if __name__ == "__main__":

    nants = 100000
    nsteps = np.array([ant_walk() for ithrow in range(nants)])

    mean = np.mean(nsteps)

    plt.figure()
    plt.hist(nsteps,
             log=True,
             range=(0.0, np.max(nsteps)),
             bins=int(np.max(nsteps)))
    plt.axvline(mean, color='red', label="Mean = %.2f seconds" % mean)
    plt.legend()
    plt.xlabel("Number of Steps Until Wall")
    plt.xlim(0, 50)
    plt.grid()

    plt.savefig("./plots/optiver_prb1.png", dpi=300)

    plt.show()
