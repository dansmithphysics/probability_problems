#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tosses until three heads.

What is the expectation number of tosses
until a fair coin achieves three heads in a row?

Easily done via a Toy MC that simulates
the tosses of the coins.

From the resulting distribution, the mean
is the numerically calculated expectation value
of tosses until three heads.
"""


import numpy as np
import matplotlib.pyplot as plt


def tosses_until_three_heads():
    """
    Tosses until three heads

    Runs a loop until three heads are hit in a row.

    Returns
    -------
    out : int
        The number of tosses until three heads
        in a row was achieved.
    """
    sides = np.random.choice([0, 1], 3)
    n_tosses = 3
    while np.sum(sides) != 3:
        sides = np.roll(sides, -1)
        sides[-1] = np.random.choice([0, 1])
        n_tosses += 1
    return n_tosses


if(__name__ == '__main__'):
    # Number of Toy MC runs, or games until three heads
    nthrows = 10000

    results_tosses_until_three_heads = np.array([tosses_until_three_heads()
                                                 for i in range(nthrows)])

    num_expectation_tosses = np.mean(results_tosses_until_three_heads)

    print('Expectation value to N: %.2f' % num_expectation_tosses)

    plt.hist(results_tosses_until_three_heads,
             range=(1, np.max(results_tosses_until_three_heads)),
             bins=np.max(results_tosses_until_three_heads) - 1,
             weights=np.ones(nthrows) / nthrows,
             log=True,
             label='Numerical Result')

    plt.axvline(14.0,
                label='Analytical Expectation Value: %.2f' % 14,
                color='purple',
                linestyle='-')

    plt.axvline(num_expectation_tosses,
                label=('Numerical Expectation Value: %.2f'
                       % num_expectation_tosses),
                color='red',
                linestyle='--')

    plt.xlabel("Number of Tosses until Three Heads")
    plt.ylabel("Probability Density Function")
    plt.xlim(2, np.max(results_tosses_until_three_heads))
    plt.grid()
    plt.legend()

    plt.savefig("./plots/tosses_until_three_heads.png", dpi=300)

    plt.show()
