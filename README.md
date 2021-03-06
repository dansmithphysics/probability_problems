# Numerical Solutions to Problems in Probability

Presented here are numerical solutions to common probability problems.

Please direct all code-related questions to [danielsmith@uchicago.edu](mailto:danielsmith@uchicago.edu).

Problems include:

## tank_problem.py, German Tank Problem

During WW2, Germany was producing tanks with a serial number. The first tank had a serial number of 0, the second of 1, and so on. The allies forces were capturing tanks, with uniform likely of capturing any given tank. Given the serial number of captured tanks, what is the expected number of total tanks produced?

To answer this question, I compute the probability mass function of the total number of produced tanks, given the serial numbers of captured tanks.

## ants_on_cube.py

An ant is places on a vertex of cube. It randomly choses between the three edges to walk down. When it reaches a new vertex, it again randomly choses between the three edges to walk down. What is the expectation value number of edges that it walks before reaching the opposite edge of the cube from its starting point? This is easily answered using a Toy MC and the analytical answer is 10 edges.

## austen_markov_chain.py

Using a Markov Chain to produce Jane Austen-like text.

## airplane_loading_problem.py

Passengers are lined up to board an airplane. Everyone has pre-determined seat on their ticket. The first passenger gets to the gate and realizes that they lost their ticket. They are instructed to sit in a random seat on the plane. The remaining passengers are instructed to sit in their designated spots if possible. If not possible, they are instructed to sit in a random available seat.

What is the probability that the final passenger sits in their predetermined seat?

The answer is 50% of the time, proven using a Toy MC.

## optiver_prb1.py, optiver_prb2.py, and optiver_prb3.py

The company Optiver presents three puzzles to solve along with their application to be a quantitative researcher with them.

An ant starts at the origin. It can take a random step in any of the cardinal directions every second. It moves 10 cm / s and is looking for food.

### Prob. 1

If the ant starts in the middle of a box that is 40 cm in side length, how long does it take to get to the food on average?

Using a Toy MC to solve this Markov chain problem, the answer is 4.5 seconds.

### Prob. 2

Food is located along a diagonal line passing through (10cm, 0cm) and (0cm, 10cm) points. How long does it take to get to the food on average?

The mean time is infinite. Increasing the `max_step` in the function `ant_walk` returns longer and longer mean time. I am tempted to say that it converges since diffusion should go as 1/r^2. However, numerical solutions suggest the mean does not converge.

### Prob. 3

Food is located outside the barrier:

((x ??? 2.5cm) / 30cm)^2 + ((y ??? 2.5cm) / 40cm)^2 < 1
How long does it take to get to the food on average?

Using a Toy MC to solve this Markov chain problem, the answer is 14 seconds.

## dots_on_edges.py

Given $n_{dots}$ placed randomly on the $n_{edges}$ of a shape, what is the probability that all $n_{dots}$ are on the same edge?

The analytical result is straight forward:
$$
P = \left(\frac{1.0}{n_{edges}}\right)^(n_{dots} - 1)
$$

I compare this result with a probability calculated from a Toy MC.

## coin_flip_game.py

Players take turns flipping a coin. Whoever gets heads first wins. The 1st player always plays first. The 2nd always plays 2nd, and so on. What is the probability that a given player wins?

I answer this question using a Toy MC, by playing many iterations of the game via the function `game`. I also double check against an infinite series that gives the analytical result. The analytical probability of the ith player winning is,

$$
P = \Sum_{k=0}^{infty} (1/2)^{n*k + ith_player},
$$

where $n$ = number of players in the game.

## tosses_until_three_heads.py

What is the expectation number of tosses until a fair coin achieves three heads in a row? Easily done via a Toy MC that simulates the tosses of the coins. From the resulting distribution of tosses, the mean is the numerically calculated expectation value of tosses until three heads.