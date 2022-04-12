#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markov Chain writes Jane Austen

Using the NLTK library, I load Jane Austen's Emma
and create a transition matrix to generate
Jane Austen-like writing.

The transition matrix gives the probability that
a word follows a given word.

To generate sentences, I use the transition matrix,
a random number generator, and a starter word to
generate text that is similar to the 'training' set.
"""


import numpy as np
from nltk.corpus import gutenberg


def create_prob_matrix(text):
    """
    Calculate the transition matrix given text.
    Not optimized, but good enough for this data set.

    Parameters
    ----------
    text : array
        Array where each entry is a word from a text

    Returns
    -------
    prob_matrix : array
        The transition matrix
    """

    unique_words = np.unique(text)

    index_map = np.zeros(len(text), dtype='int')
    for i_unique_word, unique_word in enumerate(unique_words):
        index_map[text == unique_word] = i_unique_word

    prob_matrix = np.zeros((len(unique_words), len(unique_words)))
    for i_word in range(len(text)-1):
        prob_matrix[index_map[i_word], index_map[i_word+1]] += 1

    for i_unique_word, unique_word in enumerate(unique_words):
        sum_ = np.sum(prob_matrix[i_unique_word])
        if(sum_ != 0):
            prob_matrix[i_unique_word] /= sum_

    return prob_matrix


def generate_sentence_map(prob_matrix, start_pt=0, n_words=100):
    """
    Given a transition matrix, generate a series of
    indices that match with words in the matrix.

    Parameters
    ----------
    prob_matrix : array
        The transition matrix
    start_pt : int
        The index of the first word.
    n_words : int
        The number of words to generate.

    Returns
    -------
    out : array
        An array of indices that can be converted
        to words. The indices represent the likely
        sequence of words as derived from prob_matrix.
    """

    cur_word = start_pt
    return_map = np.zeros(n_words, dtype=int)
    for i in range(n_words):
        return_map[i] = cur_word
        next_word = np.random.choice(np.arange(prob_matrix.shape[0]),
                                     p=prob_matrix[cur_word])
        cur_word = next_word
    return return_map


def print_sentence_map(text, sentence_map):
    """
    Translate indices to words and prints it.

    Parameters
    ----------
    text : array
        Array where each entry is a word from a text
    sentence_map : array
        Array of indices generated from the transition
        matrix that needs to be converted.
    """

    unique_words = np.unique(text)
    punct = np.array([".", ",", ")", "(", "?", "!", ":", "'", ";"])

    for sentence_map_ in sentence_map:
        cur_word = unique_words[sentence_map_]
        start = " "
        if np.any(punct == cur_word):
            start = ""
        print(start + cur_word, end="")
    print("")


if __name__ == "__main__":

    # Load the text from Jane Austen's Emma.
    text = gutenberg.words('austen-emma.txt')
    text = np.array([word.lower() for word in text])
    text = np.array([word.replace("_", "") for word in text])
    text = np.array([word.replace("-", "") for word in text])

    # Calculate the transition matrix.
    prob_matrix = create_prob_matrix(text)

    # Generate a sentence.
    sentence_map = generate_sentence_map(prob_matrix)

    # Print the sentence.
    print_sentence_map(text, sentence_map)
