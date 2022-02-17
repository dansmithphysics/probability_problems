#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Coin flip game

Players take turns flipping a coin.
Whoever gets heads first wins.
The 1st player always plays first.
The 2nd always plays 2nd, and so on.

What is the probability that a given player wins?

I answer this question using a Toy MC, by playing
many iterations of the game via the function 'game'

I also double check against an infinite series that
gives the analytical result.

The probability of the ith player winning is
P = Sum_{k=0}^{infty} (1/2)^{n*k + ith_player},
where n = number of players in the game.
"""


import numpy as np
import matplotlib.pyplot as plt


def game(n_players=2):
    """
    One Toy MC iteration of the coin toss game.

    Parameters
    ----------
    n_players : int
        Number of players in the game.

    Returns
    -------
    out : int
        Which player won the game.
        The first player is player number 0
    """

    i = 0
    while True:
        toss = np.random.choice([0, 1])
        if(toss == 1):
            break
        i += 1

    return int(i % n_players)


if __name__ == '__main__':

    n_games = 1000
    n_players = 3

    # Run the toy MC.
    winning_players = np.array([game(n_players) for i in range(n_games)])

    # Post-process the toy MC to make the PDF.
    hist_of_winners, edges_of_winners = np.histogram(winning_players,
                                                     range=(0, n_players),
                                                     bins=n_players)

    centers_of_winners = edges_of_winners[1:]
    err_on_hist_of_winners = np.sqrt(hist_of_winners) / n_games

    # Run the analytical calculation.

    ks = np.arange(1000)  # Take the sum up to k = 999, a fair approximation.
    P_sums = np.array([np.sum(np.power(0.5, n_players*ks + ith_player))
                       for ith_player in np.arange(1, n_players+1)])

    # Plot the results.

    plt.figure()
    for i, P_sums_ in enumerate(P_sums):
        plt.axhline(P_sums_, color='purple')
    plt.axhline(-1, color='purple', label="Analytical Probability")
    plt.scatter(centers_of_winners,
                hist_of_winners / n_games,
                color='black',
                label='Numerical Result')
    plt.errorbar(centers_of_winners,
                 hist_of_winners / n_games,
                 yerr=err_on_hist_of_winners,
                 fmt=' ', color='black')
    plt.xlim(0.5, n_players + 0.5)
    plt.ylim(0.0, 1.0)
    plt.xlabel("Player Ordinal Number")
    plt.ylabel("Probablity density function")
    plt.grid()
    plt.legend()

    plt.savefig("./plots/coin_flip_game_3players.png", dpi=300)

    plt.show()
