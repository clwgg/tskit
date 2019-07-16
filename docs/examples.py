"""
Examples for the tutorial.
"""
import os
import sys
sys.path.insert(0, os.path.abspath('../python'))

import msprime
import tskit

def moving_along_tree_sequence():
    ts = msprime.simulate(5, recombination_rate=1, random_seed=42)

    print("Tree sequence has {} trees".format(ts.num_trees))
    print()
    for tree in ts.trees():
        print("Tree {} covers [{:.2f}, {:.2f}); TMRCA = {:.4f}".format(
            tree.index, *tree.interval, tree.time(tree.root)))

    print()
    for tree in reversed(ts.trees()):
        print("Tree {} covers [{:.2f}, {:.2f}); TMRCA = {:.4f}".format(

            tree.index, *tree.interval, tree.time(tree.root)))

    print()
    for tree in list(ts.trees()):
        print("Tree {} covers [{:.2f}, {:.2f}): id={:x}".format(
            tree.index, *tree.interval, id(tree)))

    print()
    for tree in ts.aslist():
        print("Tree {} covers [{:.2f}, {:.2f}): id={:x}".format(
            tree.index, *tree.interval, id(tree)))

    print()
    tree = ts.at(0.5)
    print("Tree {} covers [{:.2f}, {:.2f}): id={:x}".format(
        tree.index, *tree.interval, id(tree)))
    tree = ts.at_index(0)
    print("Tree {} covers [{:.2f}, {:.2f}): id={:x}".format(
        tree.index, *tree.interval, id(tree)))
    tree = ts.at_index(-1)
    print("Tree {} covers [{:.2f}, {:.2f}): id={:x}".format(
        tree.index, *tree.interval, id(tree)))

    print()
    tree = tskit.Tree(ts)
    tree.seek_index(ts.num_trees // 2)
    print("Tree {} covers [{:.2f}, {:.2f})".format(tree.index, *tree.interval))
    tree.seek(0.95)
    print("Tree {} covers [{:.2f}, {:.2f})".format(tree.index, *tree.interval))

    print()
    tree.prev()
    print("Tree {} covers [{:.2f}, {:.2f})".format(tree.index, *tree.interval))
    tree.next()
    print("Tree {} covers [{:.2f}, {:.2f})".format(tree.index, *tree.interval))

    print()
    tree = tskit.Tree(ts)
    print("Tree {}: parent_dict = {}".format(tree.index, tree.parent_dict))
    tree.first()
    print("Tree {}: parent_dict = {}".format(tree.index, tree.parent_dict))
    tree.prev()
    print("Tree {}: parent_dict = {}".format(tree.index, tree.parent_dict))

    tree = tskit.Tree(ts)
    while tree.next():
        print("Tree {} covers [{:.2f}, {:.2f})".format(tree.index, *tree.interval))
    print("After loop: tree index =", tree.index)
    while tree.prev():
        print("Tree {} covers [{:.2f}, {:.2f})".format(tree.index, *tree.interval))


def parsimony():

    tree = msprime.simulate(6, random_seed=42).first()
    alleles = ["red", "blue", "green"]
    genotypes = [0, 0, 0, 0, 1, 2]
    node_colours = {j: alleles[g] for j, g in enumerate(genotypes)}
    ancestral_state, mutations = tree.map_mutations(genotypes, alleles)
    print("Ancestral state = ", ancestral_state)
    for mut in mutations:
        print(f"Mutation: node = {mut.node} derived_state = {mut.derived_state}")
    tree.draw("_static/parsimony1.svg", node_colours=node_colours)


    ts = msprime.simulate(6, random_seed=23)
    ts = msprime.mutate(
        ts, rate=3, model=msprime.InfiniteSites(msprime.NUCLEOTIDES), random_seed=2)

    tree = ts.first()
    tables = ts.dump_tables()
    # Reinfer the sites and mutations from the variants.
    tables.sites.clear()
    tables.mutations.clear()
    for var in ts.variants():
        ancestral_state, mutations = tree.map_mutations(var.genotypes, var.alleles)
        tables.sites.add_row(var.site.position, ancestral_state=ancestral_state)
        parent_offset = len(tables.mutations)
        for mutation in mutations:
            parent = mutation.parent
            if parent != tskit.NULL:
                parent += parent_offset
            tables.mutations.add_row(
                var.index, node=mutation.node, parent=parent,
                derived_state=mutation.derived_state)

    assert tables.sites == ts.tables.sites
    assert tables.mutations == ts.tables.mutations
    print(tables.sites)
    print(tables.mutations)

    tree = msprime.simulate(6, random_seed=42).first()
    alleles = ["red", "blue", "green", "white"]
    genotypes = [-1, 0, 0, 0, 1, 2]
    node_colours = {j: alleles[g] for j, g in enumerate(genotypes)}
    ancestral_state, mutations = tree.map_mutations(genotypes, alleles)
    print("Ancestral state = ", ancestral_state)
    for mut in mutations:
        print(f"Mutation: node = {mut.node} derived_state = {mut.derived_state}")
    tree.draw("_static/parsimony2.svg", node_colours=node_colours)

    tree = msprime.simulate(6, random_seed=42).first()
    alleles = ["red", "blue", "white"]
    genotypes = [1, -1, 0, 0, 0, 0]
    node_colours = {j: alleles[g] for j, g in enumerate(genotypes)}
    ancestral_state, mutations = tree.map_mutations(genotypes, alleles)
    print("Ancestral state = ", ancestral_state)
    for mut in mutations:
        print(f"Mutation: node = {mut.node} derived_state = {mut.derived_state}")
    tree.draw("_static/parsimony3.svg", node_colours=node_colours)


# moving_along_tree_sequence()
parsimony()
