#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Airplane Boarding Problem

Passengers are lined up to board an airplane.
Everyone has pre-determined seat on their ticket.
The first passenger gets to the gate and realizes
that they lost their ticket.
They are instructed to sit in a random seat on the plane.
The remaining passengers are instructed to sit in
their designated spots if possible. If not possible,
they are instructed to sit in a random available seat.

What is the probability that the final passenger
sits in their predetermined seat?

The answer is 50% of the time.
Below is a Toy MC that proves proves it.
"""


import numpy as np
import matplotlib.pyplot as plt


def random_seat(sat_spot):
    """
    Random Seat helper function.
    Returns a random seat out of available seats.

    Parameters
    ----------
    sat_spot : array_like
        Seat map, with -1 in spots that are still open.

    Returns
    -------
    out : int
        Returns the index of a random available
        spot in sat_spot.
    """
    return np.random.choice(np.where(sat_spot == -1)[0])


def board_plane(n_passengers):
    """
    Boarding the Plane Toy MC

    The first passenger gets assigned a random spot.
    The subsequent passengers either sit in
    their ticketed seat if open, or in a random seat if not.

    Returns true if final passenger sat in
    their designated seat.

    Parameters
    ----------
    n_passengers : int
        Number of passengers to board plane, from 2 to infty.

    Returns
    -------
    out : bool
        Returns true if final passenger sat in
        their designated seat.
    """

    # Each passengers id is the number of their bording order, starting at 0.

    # Their seat position is also an integer,
    # the seat number they should sit in.
    ticket_spot = np.arange(n_passengers)
    np.random.shuffle(ticket_spot)

    # Where they actually, array of the seats and, at the end,
    # has the integer of the passenger that sat there.
    sat_spot = -1 * np.ones(n_passengers, dtype='int')  # -1 is a temp. number

    # First passenger (0) sits in a random spot,
    # it could be where he was supposed to sit.
    sat_spot[random_seat(sat_spot)] = 0

    # In order of passengers boarding,
    # check if someone is in your seat, skipping the first spot
    # and, if taken, chose a spot that isn't taken yet.
    for i in range(1, n_passengers):
        if(sat_spot[ticket_spot[i]] == -1):
            sat_spot[ticket_spot[i]] = i
        else:
            sat_spot[random_seat(sat_spot)] = i

    # Return boolean of the last passenger (n_passengers - 1) actually
    # sat in their pre-determined seat (ticket_spot[-1]).
    return sat_spot[ticket_spot[-1]] == (n_passengers - 1)


if(__name__ == "__main__"):
    # Number of toy MC tests, or 1000 boardings.
    n_throws = 10000

    n_passengers = np.arange(2, 103, 10)

    # Vectorize the process to speed it up a bit.
    vfunc_board_plane = np.vectorize(board_plane)

    last_had_seat = np.zeros(len(n_passengers))

    for i, n_passengers_ in enumerate(n_passengers):
        last_had_seat_ = vfunc_board_plane(n_passengers_ * np.ones(n_throws, dtype='int'))
        last_had_seat[i] = np.sum(last_had_seat_)

    last_had_seat_prob = last_had_seat / n_throws
    # Approximate binomial errors using sqrt(counts)
    last_had_seat_prob_yerr = np.sqrt(last_had_seat) / n_throws

    plt.figure()
    plt.scatter(n_passengers,
                last_had_seat_prob,
                color='black')
    plt.errorbar(n_passengers,
                 last_had_seat_prob,
                 yerr=last_had_seat_prob_yerr,
                 fmt=' ', color='black',
                 label="Numerical Result")

    plt.axhline(0.5,
                color='red',
                linestyle='--',
                label="Analytical Result")

    plt.xlabel("Number of Passengers Boarding Plane")
    plt.ylabel("Probability Last Passengers had Their Ticketed Seat")
    plt.xlim(np.min(n_passengers) - 1, np.max(n_passengers) + 1)
    plt.ylim(0.45, 0.55)
    plt.grid()
    plt.legend()

    plt.savefig("./plots/airplane_boarding.png", dpi=300)

    plt.show()
