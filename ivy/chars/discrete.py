"""
Functions for fitting mk model to a tree
"""
import ivy
import numpy as np
import math
from ivy.chars.expokit import cyexpokit
import scipy
from scipy import special
from scipy.optimize import minimize
from scipy.special import binom
import random


def nodeLikelihood(node):
    """
    Take node "node" and calculate its likelihood given its children's likelihoods,
    branch lengths, and p-matrix.
    Args:
        node (Node): A node to calculate the likelihood for
    Returns:
        float: The likelihood of the node given the data
    """
    likelihoodNode = {}
    for state in range(node.children[0].pmat.shape[0]): # Calculate the likelihood of the node being any one of these states
        likelihoodStateN = [] # Likelihood of node being at state N
        for ch in node.children:
            likelihoodStateN.append(ch.pmat[state, ch.charstate])
        likelihoodNode[state] = np.product(likelihoodStateN)

    return sum(likelihoodNode.values())

def tip_age_rank_sum(tree, chars):
    """
    Calculate tip age rank sums of two traits
    and return test statistic and p-value

    See: Bromham et al. 2016
    """
    tip_ages = [(n.length, chars[i]) for i,n in enumerate(tree.leaves())]
    tip_ages.sort(key = lambda x: x[0])
    lens0 = [ i[0] for i in tip_ages if i[1]==0]
    lens1 = [ i[0] for i in tip_ages if i[1]==1]

    stat, pval = scipy.stats.ranksums(lens1, lens0)

    return stat, pval

def NoTO(tree, chars):
    """
    Number of Tips Per Origin

    See: Bromham et al. 2016
    """
    parsimonyStates = ivy.chars.anc_recon.parsimony_recon(tree, chars)
    rootState = int(parsimonyStates[tree][0])

    origins = []
    for node in tree.descendants():
        if not node.isleaf:
            if int(parsimonyStates[node][0]) != rootState and parsimonyStates[node.parent][0] == rootState:
                origins.append(node)
    return len([i for i in chars if not i==rootState])/len(origins)


def monotypic_clade_size(tree, chars):
    """
    Count diversity contained within subclades having the same character
    state.
    """
    if len(set(chars)) == 1:
        return [len(chars)]
    chardict = {t:chars[i] for i,t in enumerate(tree.leaves())}
    subclades = [n for n in tree.postiter() if not n.isleaf]
    monotypic_clades = [None]*len(subclades)
    for i,sc in enumerate(subclades):
        largest_monotypic = None
        cur = sc
        while 1:
            if is_monotypic(cur, chardict):
                largest_monotypic = cur
                cur = cur.parent
            else:
                break
        monotypic_clades[i] = largest_monotypic
    monotypic_clade_set = set([i for i in monotypic_clades if i is not None])
    monotypic_clade_descendants = [ n.leaves() for n in list(monotypic_clade_set)]
    monotypic_clade_sizes = [len(i) for i in monotypic_clade_descendants]
    monotypic_clade_descendants_flat = [i for s in monotypic_clade_descendants for i in s]

    singletons = [l for l in tree.leaves() if not l in monotypic_clade_descendants_flat ]

    return sorted(monotypic_clade_sizes+[1 for _ in singletons])


def is_monotypic(node, chardict):
    return len(set([chardict[i] for i in node.leaves()])) == 1
