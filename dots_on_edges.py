"""
Dots on the edges of a shape.

Given n_dots placed randomly on the n_edges
of a shape, what is the probability that all
n_dots are on the same edge?

The analytical result is straight forward:

P = (1.0 / n_edges)**(n_dots - 1)

I compare this result with a probability
calculated from a Toy MC

"""


import numpy as np
import matplotlib.pyplot as plt


def place_dots(n_dots, n_edges):
    """
    Toy MC of placing the dots

    Parameters
    ----------
    n_dots : int
        Number of dots to place.
    n_edges : int
        Number of edges of shape.

    Returns
    -------
    out : bool
        Returns true if all dots are on
        the same side. False otherwise.
    """

    spots = np.random.choice(np.arange(n_edges), n_dots)
    return len(np.unique(spots)) == 1


if __name__ == "__main__":
    n_throws = 10000

    n_dots = 3
    n_edges = np.arange(2, 51)
    probs = np.zeros(len(n_edges))

    for i, n_edges_ in enumerate(n_edges):

        vfunc_place_dots = np.vectorize(place_dots)

        results = vfunc_place_dots(n_dots * np.ones(n_throws, dtype='int'),
                                   n_edges_ * np.ones(n_throws, dtype='int'))

        probs[i] = float(np.sum(results) / n_throws)

    plt.figure()
    plt.title(r"Probability that $N_{dots} = 3$ are all on one edge of shape.")
    plt.semilogy(n_edges, probs,
                 label="Numerical Result", color="black")
    plt.semilogy(n_edges, np.power(1/n_edges, n_dots-1),
                 label="Analytical Result", color="red", alpha=0.5)
    plt.xlabel(r"$N_{edges}$")
    plt.ylabel("Probability")
    plt.ylim(1e-4, 1.0)
    plt.xlim(1, 50)
    plt.grid()
    plt.legend()

    plt.savefig("./plots/dots_on_edge.png", dpi=300)

    plt.show()
