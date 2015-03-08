# -------------------------------------------------------------------------------
# Name:        shingling minhashing
# 
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------
# !/usr/bin/env python

from __future__ import division
from math import *

# example of stop words
STOP_WORDS = set(('i', 'you', 'they', 'the', 'no', 'none', 'all', 'a', 'for', 'not', 'nor'))
# example of hash function
HASH_FCT_EX = lambda val: (2 * val + 4) % 5


def k_shingles(string, k=2, use_stop_words=False, verbose=False):
    """
    Return the set of k-shingles of the current text
    """
    shingles = []
    string_len = len(string)
    for i in range(0, string_len - k + 1):
        txt = [string[i:i + k]]
        shingles += txt
    k_sh = set(sorted(shingles))
    if use_stop_words:
        k_sh = k_sh - STOP_WORDS
    if verbose:
        print "All possible shingles 27^%s = %s" % (k, 27 ** k)
        print "%s-shingles for %s : %s" % (k, string, k_sh)
    return k_sh


def charateristic_matrix(list_sets, verbose=False):
    """
        Retutrn the characterisc matrix for the current list of sets
    """
    nbr_columns = len(list_sets)
    # constructiong the elements based on the union of sets
    elements = set()
    for i in list_sets:
        elements = elements | i
    elements = sorted(list(elements))
    nbr_rows = len(elements)
    char_matrix = []
    #initialising the characteristic matrix
    for i in range(0, nbr_rows):
        char_matrix.append([0] * nbr_columns)
    #constructiong the charastristic matrix
    for e in range(0, nbr_rows):
        for s in range(0, nbr_columns):
            char_matrix[e][s] = 1 if elements[e] in list_sets[s] else 0

    if verbose: print char_matrix
    return char_matrix


def signature_vector(characteristic_matrix, hash_fct, verbose=False):
    """
        Computing Minhash Signatures fot the current characteristic matrix, with hash_fct hash function
    """
    nbr_columns = len(characteristic_matrix[0])
    nbr_rows = len(characteristic_matrix)
    signature = [-1] * nbr_columns
    for r in range(0, nbr_rows):
        hash_value = hash_fct(r)
        for c in range(0, nbr_columns):
            if characteristic_matrix[r][c] == 1:
                # the row r has 1 in the column c, so it is potentially object to change
                if signature[c] > hash_value or signature[c] < 0:
                    signature[c] = hash_value
    if verbose: print signature
    return signature


def and_or_construction(p, r, b, and_first=True):
    """
        function of r and b, the point of maximum slope and the value of that slope, for families of functions
        defined from the minhash functions.
        if and_first = True : An r-way AND construction followed by a b-way OR construction.
        else : A b-way OR construction followed by an r-way AND construction.
    """
    return 1 - (1 - p ** r) ** b if and_first else (1 - (1 - p) ** b) ** r


def and_or_s_curve(r, b, and_first=True):
    """
        For an r and b given : it generates the s-curve
    """
    p = 0.1
    for i in range(0, 9):
        p += 0.1
        print and_or_construction(p, r, b, and_first)


def bloom_filter(n, m, k):
    """
        A Bloom filter consists of:
        1. An array of n bits, initially all 0?s.
        2. A collection of hash functions h1, h2, . . . , hk. Each hash function maps
        ?key? values to n buckets, corresponding to the n bits of the bit-array.
        3. A set S of m key values.
        The purpose of the Bloom filter is to allow through all stream elements whose
        keys are in S, while rejecting most of the stream elements whose keys are not
        in S.
        To initialize the bit array, begin with all bits 0. Take each key value in S
        and hash it using each of the k hash functions. Set to 1 each bit that is hi(K)
        for some hash function hi and some key value K in S.
        To test a key K that arrives in the stream, check that all of
        h1(K), h2(K), . . . , hk(K)
        are 1?s in the bit-array. If all are 1?s, then let the stream element through. If
        one or more of these bits are 0, then K could not be in S, so reject the stream
        element.
    """
    # probability that a bit remains 0
    a = long(k * m)
    b = float(a) / float(n)
    prob_bit_0 = exp(- b)
    #the probability of a false positive is the probability of a 1 bit
    prob_false_positive = (1 - prob_bit_0) ** k
    print prob_false_positive
