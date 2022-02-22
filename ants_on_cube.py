"""
Ants walking on edges of cube

An ant is places on a vertex of cube.

It randomly choses between the three edges
to walk down.

When it reaches a new vertex, it again
randomly choses between the three edges
to walk down.

What is the expectation value number of
edges that it walks before reaching the opposite
edge of the cube from its starting point?

This is easily answered using a Toy MC.
The analytical answer is 10 edges.
"""


import numpy as np
import matplotlib.pyplot as plt


def walk_edges(probability_matrix, end_vertex=1, start_vertex=1):
    """
    Walk around the edges of a cube.
    Uses a probability matrix to determine which
    next vertex to walk towards.

    Parameters
    ----------
    probability_matrix : array-like
        Transition matrix at each vertex.
    start_vertex : int
        Vertex number of first vertex.
    end_vertex : int
        Vertex number of last vertex.

    Returns
    -------
    out : int
        Number of edges traversed between the
        start and end vertices.
    """

    cur_vertex = start_vertex
    n_steps = 0
    while True:

        cur_vector = np.zeros(probability_matrix.shape[0])
        cur_vector[cur_vertex-1] = 1

        transition = probability_matrix.dot(cur_vector)
        cur_vertex = np.random.choice(np.arange(1, probability_matrix.shape[0]+1),
                                      p=transition)
        n_steps += 1

        if(cur_vertex == end_vertex):
            return n_steps


if __name__ == "__main__":

    probability_matrix = np.array([[0, 1, 0, 1, 0, 1, 0, 0],
                                   [1, 0, 1, 0, 0, 0, 1, 0],
                                   [0, 1, 0, 1, 0, 0, 0, 1],
                                   [1, 0, 1, 0, 1, 0, 0, 0],
                                   [0, 0, 0, 1, 0, 1, 0, 1],
                                   [1, 0, 0, 0, 1, 0, 1, 0],
                                   [0, 1, 0, 0, 0, 1, 0, 1],
                                   [0, 0, 1, 0, 1, 0, 1, 0]],
                                  dtype='float')
    probability_matrix *= (1/3)

    # Number of Toy MC iterations.
    n_throws = 100000

    start_vertex = 1
    end_vertex = 8

    vfunc_walk_edges = np.vectorize(walk_edges,
                                    excluded=['probability_matrix'])

    results = vfunc_walk_edges(probability_matrix=probability_matrix,
                               end_vertex=end_vertex * np.ones(n_throws, dtype='int'),
                               start_vertex=start_vertex * np.ones(n_throws, dtype='int'))

    num_exp_value = np.mean(results)
    ana_exp_value = 10.0

    plt.hist(results,
             range=(3, 101),
             bins=49,
             density=True,
             log=True)
    plt.axvline(num_exp_value,
                label="Numerical Expectation Value: %.2f" % num_exp_value,
                color='black')
    plt.axvline(ana_exp_value,
                label="Analytical Expectation Value: %.2f" % ana_exp_value,
                color='red',
                alpha=0.5)
    plt.xlabel("Number of steps until opposite vertex")
    plt.ylabel("Probability Density Function")
    plt.grid()
    plt.legend()

    plt.savefig("./plots/ants_on_cube.png", dpi=300)

    plt.show()
