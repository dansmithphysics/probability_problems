#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
German Tank Problem

During WW2, Germany was producing tanks with a serial number.
The first tank had a serial number of 0, the second of 1, and so on.

The allies forces were capturing tanks, with
uniform likely of capturing any given tank.

Given the serial number of captured tanks, what is the
expected number of total tanks produced?

To answer this question, I compute the probability mass function of the
total number of produced tanks, given the serial numbers of captured tanks.
"""


import numpy as np
import matplotlib.pyplot as plt


def ratio_of_n_tanks(serial_numbers, n_tanks, n_throws=1000):
    """
    Toy MC
    Number of times captured N serial numbers
    are as small as given serial numbers

    Parameters
    ----------
    serial_numbers : array_like
        Serial numbers of captured tanks
    n_tanks : int
        Number of produced tanks to check against
    n_throws : int
        Number of Toy MC tests. Larger the number,
        the longer the run time and more precise the result

    Returns
    -------
    out : float
        The ratio of toy MC that had captured tanks
        with serial numbers lower than or equal to
        the given captured serial numbers
    """
    possible_serial_numbers = np.arange(n_tanks)
    results = np.zeros((n_throws, len(serial_numbers)))
    for i in np.arange(n_throws):
        results[i] = np.random.choice(possible_serial_numbers,
                                      size=len(serial_numbers),
                                      replace=False)
    num_of_captured_less = np.sum(results < np.max(serial_numbers), axis=1)
    num_of_matches = np.sum(num_of_captured_less == len(serial_numbers))

    return num_of_matches / n_throws


if(__name__ == '__main__'):

    # Serial numbers from Wikipedia example, but could be random
    serial_numbers = np.array([60, 19, 40, 42])
    n_tanks = np.arange(np.max(serial_numbers), 1000)

    ratio_matches = np.array([ratio_of_n_tanks(serial_numbers, n_tanks_)
                              for n_tanks_ in n_tanks])
    ratio_matches /= np.sum(ratio_matches)

    k = len(serial_numbers)
    N = n_tanks
    m = np.max(serial_numbers)
    stirling_approx_of_bayes = (k - 1) * np.power(m, float(k - 1)) * np.power(N, -float(k))

    # The expectation values.
    # 89.0 from German Tank Problem Wikipedia page
    print("Numerical Expectation value: \t\t\t %f"
          % (np.sum(n_tanks * ratio_matches)))
    print("Analytical Bayesian Expectation value: \t\t %f"
          % (89.0))
    print("Analytical Bay., Stirling Approx., Exp. value: \t %f"
          % (np.sum(n_tanks * stirling_approx_of_bayes)))

    residual = (ratio_matches - stirling_approx_of_bayes)

    fig, axs = plt.subplots(2)
    fig.suptitle("German Tank Problem Probability Mass Function \n Numerical Result compared with Bayesian Analytical Result")

    axs[0].semilogy(n_tanks, ratio_matches,
                    label="Numerical Result",
                    color="red")
    axs[0].semilogy(n_tanks, stirling_approx_of_bayes,
                    label="Stirling Approx. of Bayesian Probability",
                    color='blue')
    axs[0].set_ylabel(r"Probability Mass Function (PMF)")
    axs[0].set_xlim(np.min(n_tanks), np.max(n_tanks))
    axs[0].set_ylim(1e-6, 1.1e0)
    axs[0].grid()
    axs[0].legend()

    axs[1].plot(n_tanks[ratio_matches != 0], residual[ratio_matches != 0])
    axs[1].set_xlabel(r"$n_{tanks}$, the total number of tanks produced")
    axs[1].set_ylabel(r"Residual")
    axs[1].set_xlim(np.min(n_tanks), np.max(n_tanks))
    axs[1].set_ylim(-0.004, 0.004)
    axs[1].grid()
    fig.savefig("./plots/tank_problem_pmf.png", dpi=300)

    # Numerical CMF (cumulative mass function) from PMF
    cmf = np.cumsum(ratio_matches) / np.cumsum(ratio_matches)[-1]
    median = n_tanks[np.argmin(np.abs(cmf - 0.5))]

    plt.figure()
    plt.title("German Tank Problem Culmulative Mass Function")
    plt.semilogx(n_tanks, cmf, label="CMF")
    plt.axvline(median, color='red', label="Median = %.2f" % median)
    plt.xlim(np.min(n_tanks), np.max(n_tanks))
    plt.grid()
    plt.legend()
    plt.savefig("./plots/tank_problem_cmf.png", dpi=300)

    plt.show()
