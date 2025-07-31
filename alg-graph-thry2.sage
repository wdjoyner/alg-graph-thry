r"""
Functions to deal with oriented graphs and harmonic morphisms,
as in Norman Biggs's and Matt Baker's works. 

A list of functions is given below.

Modified 2019: (a) Added morphism check in is_harmonic_graph_morphism
               (b) Fixed syntax to use in python3

Modified 2020-03-06 (converted strings to raw strings, 
                          added example, added a definition to docstring)

modified 2020-09-01:  fixed vertical_mult_of_harmonic_map

modified 2020-10-31: added edge_set_is_a_walk, 
                                image_of_walk_under_graph_morphism, 
                                plot_walk_in_graph(Gamma, W),
                                number_of_edges_set_in_a_walk,
                                edges_in_cycle_basis

modified 2020-11-23: changed zeta_function_graph -> zeta_polynomial_graph
                          and revised (corrected?) the quadratic term

modified 2020-12-11: added oriented_edge_matrix (Terras' (0,1)-edge matrix
                                for Bass' defn of the Ihara zeta fcn)
                     added: if the edges are labeled then it will
                            sort the edges according to the labels.

modified 2021-02-03: fixed bugs introduced when default behaviour of some
                     SageMath methods changed slightly.

modified 2021-05-21: added weighted_incidence_matrix, weight_at_edge, 
                           weighted_degree

modified 2021-05-31: added weighted_horizontal_multiplicity_of_harmonic_map,
                     weighted_local_horizontal_multiplicity_of_harmonic_map,
                     is_weighted_harmonic_graph_morphism,
                     and made lots of changes to fix ordering of 
                     orientation and weight list

modified 2021-06-05: added weighted_vertical_multiplicity_of_harmonic_map

modified 2021-08-26: added codifferential_basis (related to cycle_space)

modified 2021-08-28: added codifferential_matrix, List of Functions,
                     pushforward_matrix_vertex_functions,
                     pushforward_matrix_edge_functions,
                     pullback_matrix_vertex_functions,
                     fixed bug in incidence_value (edges must be a list)
                     
modified 2021-09-13: added proj_blowup, blowup_balance_graph

modified 2021-09-16: added graph_convert_to_standard

modified 2021-09-19: added local_horizontal_multiplicity_of_harmonic_map

modified 2021-09-22: "bug fix" to is_harmonic_graph_morphism (fixed, but bug unknown),
                     added find_cover_graph

modified 2021-10-01: added find_random_incidence_matrix

modified 2021-11-01: added flower_graph

modified 2021-11-10: added vertex_matrix_map_to_CL

modified 2021-11-13: added vertical_edges_list, adjacency_matrix_decomposition,
                     harmonic_edge_irreducible_subgraph, is_harmonic_edge_irreducible,
                     coalescence_vertex, coalescence_edge

modified 2021-11-20: added barycentric_subdivision_graph, harmonic_edge_irreducible_subgraph,
                     one_vertex_corona, corona

modified 2021-12-10: added CL_of_product_of_morphisms

modified 2021-12-15: added matrix_of_graph_of_product_of_morphisms_vertices, 
                     is_cartesian_product_of_graph_morphisms_harmonic, 
                     is_cartesian_product_of_graph_morphisms_a_morphism,
                     modified is_graph_morphism

modified 2021-12-18: added is_tensor_product_of_graph_morphisms_harmonic,
                     is_tensor_product_of_graph_morphisms_a_morphism

modified 2021-12-20: added is_strong_product_of_graph_morphisms_harmonic

modified 2022-01-07: added  CL_product_projection1_harmonic,  CL_product_projection2_harmonic,
                     is_cartesian_product_projection1_harmonic, is_tensor_product_projection1_harmonic,  
                     is_strong_product_projection1_harmonic, is_lexicographic_product_projection1_harmonic,  
                     is_strong_product_of_graph_morphisms_a_morphism,
                     is_lexicographic_product_of_graph_morphisms_harmonic,
                     is_lexicographic_product_projection1_harmonic, is_lexicographic_product_projection2_harmonic,
                     is_disjunctive_product_of_graph_morphisms_a_morphism,
                     is_disjunctive_product_projection1_harmonic, is_disjunctive_product_projection2_harmonic

modified 2022-01-11: Fixed bug in is_graph_morphism where vertex 0 was confused
                     (in Python) with False

modified 2022-01-16: added morphism_of_line_graphs

modified 2022-01-23: fixed typo in docstring of morphism_of_line_graphs

modified 2022-02-04: Fixed another bug in is_graph_morphism (which propogated to 
                     is_harmonic_graph_morphism)

modified 2022-02-12: added LC_multipartite_graph, alias
                     horizontal_multiplicity_of_harmonic_map = horizonal_multiplicity_of_harmonic_map

modified 2022-02-21: added blowup_graph, which generalizes both LC_multipartite_graph and
                     blowup_balanced_graph

modified 2022-03-08: added degree_of_harmonic_morphism

modified 2022-03-30: added blowdown_morphism

modified 2022-05-15: Fixed yet another bug in is_graph_morphism (which propogated to 
                     is_harmonic_graph_morphism)

modified 2022-05-17: Renamed subdivision_graph -> barycentric_subdivision_graph and
                     added new subdivision_graph

modified 2022-05-19: added lower_upper_bound_sgon, subdivision_graph_morphism

modified 2022-05-22: added is_smooth_vertex, smooth_graph, compactify_list, smooth_graph_morphism

modified 2022-05-25: added delete_vertex_graph_morphism

modified 2022_06-06: added utility table_of_local_horizontal_multiplicities

modified 2022-06-09: added CL_of_join_of_morphisms

modified 2022-07-11: added is_harmonic_graphWB_morphism, for graphs with boundaries

modified 2022-07-14: added partial_join_graph, leaf_addition_graph_morphism
modified 2022-07-21: significantly modified leaf_addition_graph_morphism

modified 2022-08-05: added sub_graph4edge (generalizing subdivision_graph)

modified 2022-08-08: edited code and docstring of quotient_graph, added quotient_graph_morphism,
                     has_harmonic_quotient

modified 2022-08-14: added double_point_construction

modified 2022-09-07: added graph_id_graph6

modified 2022-10-07: added effective_resistance_matrix

modified 2022-12-05: replaced Gamma.edges(labels=None) by
                      Gamma.edges(labels=None,sort=True),
		      since sort behaviour changed in the
		      underlying SageMath code for the
		      vertices and edges methods.

modified 2023-02-20: rewrote matrix_of_graph_morphism_edges(Gamma1, Gamma2, f, iota2, iota1),
                     therefore also graph_morphism_edge_matrix, and
                     rewrote index_of_graph_morphism_edges(Gamma1, Gamma2, f, e0, s0, iota2, iota1)

modified 2023-02-21: added vertical_multiplicity_of_graph_morphism (same as
                     vertical_multiplicity_of_harmonic_map), is_graph_homomorphism

modified 2023-03-17: added orthogonal_eigenbasis_sorted (a utility function)

modified 2023-03-21: added find_matrix_permutation (another utility) and fixed orthogonal_eigenbasiis_sorted

modified 2023-04-01: modified orthogonal_eigenbasis_sorted 

modified 2023-05-18: added intersection_number_of_vertex_subset, is_equitable_partition

modified 2023-10-09: Fixed another bug in is_graph_morphism (which propogated to 
                     is_harmonic_graph_morphism)

modified 2023-11-02: Fixed a bug in is_equitable_partition, 
                     added associated_partition_to_morphism, is_associated_partition_equitable

modified 2024-01-22: Edited comments in graph_convert_to_standard code.

modified 2024-03-01: Added partition_cell_edges, weights_of_vertex_to_cell, is_weighted_equitable_partition

modified 2024-03-15: Minor edits to (buggy?) weighted code.

modified 2024-04-14: Added weighted_cayley_graph

modified 2024-04-20: Minor additions to weighted_cayley_graph

modified 2024-06-03 and 2024-06-06 and 2024-06-07: Bug fixes, minor additions, and doc string edits.

modified 2024-06-28: Added convolve_function_with_filter

modified 2024-07-29 to 2025-07-31: Expanded on an example in numerous docstrings, eg, for convolve_function_with_filter

List of Functions (in order of occurrence):

 * compactify_list(L)
 * graph_convert_to_standard(Gamma)
 * find_matrix_permutation(L1, L2)
 * orthogonal_eigenbasis_sorted(M)

The above are more general utility functions.

 * plot_walk_in_graph(Gamma, W)
 * edges_in_cycle_basis(Gamma)
 * tree_component_plus(Gamma, e, T, eo)
 * tree_component_minus(Gamma, e, T, eo)
 * is_incident_to(Gamma, e, v)
 * incidence_value(Gamma, v, e, eo)
 * incidence_matrix(Gamma, eo)
 * weight_at_edge(Gamma, w0, e)
 * weight_degree(Gamma, w0, v):
 * weighted_degree_matrix(Gamma, w0)
 * weighted_incidence_matrix(Gamma, eo, w0)
 * oriented_edge_matrix(Gamma, eo)
 * cycle_space(Gamma, eo, F = QQ)
 * cocycle_space(Gamma, eo)
 * cut_space(Gamma, eo)
 * cuts_list(Gamma, verbose = False)
 * flipit(t)
 * cut_matrix(Gamma)
 * cut_oriented_matrix(Gamma) ## indep of eo
 * cut_matrix_oriented(Gamma) ## same as above
 * incidence_matrix_tree_inverse_value(Gamma, eo, x, T, e, v)
 * incidence_tree_matrix(Gamma, eo, x, T)
 * incidence_matrix_tree(Gamma, eo, x, T) ## same as above
 * fund_vertex_cut_char_fcn(Gamma, v, e, eo)
 * fund_cut_char_fcn(Gamma, v, e, eo)
 * fund_cycle_char_fcn(Gamma, q, e, eo)
 * fund_cycle(Gamma, T, e, eo)
 * laplacian_reduced_matrix(Gamma, eo, s)
 * laplacian_reduced(Gamma, eo, s) ## same as above
 * laplacian_reduced_punctured_matrix(Gamma, eo, s, p, q)
 * laplacian_reduced_punctured(Gamma, eo, s, p, q) ## same as above
 * potential_induced(Gamma, e0, j, s, p, q)
 * number_of_2_trees(Gamma, e0, v, w)
 * critical_group(Gamma)
 * laplacian_vertex_matrix(Gamma, eo)
 * laplacian_vertex(Gamma, eo) ## same as above
 * laplacian_edge_matrix(Gamma, eo)
 * laplacian_edge(Gamma, eo)  ## same as above
 * quotient_adjacent(orbits, VG, EG, i, j)
 * quotient_graph(Gamma, G, verbose = False)
 * quotient_graph_morphism(Gamma, G)
 * zeta_polynomial_graph(Gamma)
 * star_subgraph(Gamma, v)
 * is_graph_morphism(Gamma1, Gamma2, f)
 * edge_image_list(Gamma1, Gamma2, f)
 * number_of_edges_set_in_a_walk(Gamma, W, verbose = False)
 * edge_set_is_a_walk(Gamma, W, verbose = False)
 * image_of_walk_under_graph_morphism(Gamma1, Gamma2, f, W)
 * index_of_graph_morphism_edges(Gamma1, Gamma2, f, e2, e1, e0)
   -> index_of_graph_morphism_edges(Gamma1, Gamma2, f, e0, s0, iota2, iota1)
 * index_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f, e2, e1)
 * index_of_graph_morphism_vertices(Gamma1, Gamma2, f, v2, v1)
 * graph_morphism_vertices_matrix(Gamma1, Gamma2, f)
 * matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)  ## same as above
 * graph_morphism_edge_matrix(Gamma1, Gamma2, f, e0)
   -> graph_morphism_edge_matrix(Gamma1, Gamma2, f, iota2, iota1)
 * matrix_of_graph_morphism_edges(Gamma1, Gamma2, f, e0) ## same as above
   -> matrix_of_graph_morphism_edges(Gamma1, Gamma2, f, iota2, iota1)
 * matrix_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f)
 * matrix_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f) ## same as above
 * preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v)
 * preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)
 * preimage_of_edges_under_graph_morphism(Gamma1, Gamma2, f, S)
 * graph_preimage_of_edges_under_graph_morphism(Gamma1, Gamma2, f, S)
 * image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)
 * image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v)
 * local_horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2, e)
 * weighted_local_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2, e)
 * weighted_vertical_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2)
 * weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2)
 * is_weighted_harmonic_graph_morphism(woGamma1, woGamma2, f, verbose = False)
 * is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose = False):
 * find_all_harmonic_graph_morphism(Gamma1, Gamma2, out_filename = "")
 * vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2)
 * horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2)
 * horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2)
 * genus(Gamma)
 * perm_number_action(G, g0)
 * lifted_vertex_to_cover(G, Gamma, v, g0)        ##  ???
 * lifted_vertices_to_cover(G, Gamma, v, g0 = 1)  ##  ???
 * lifted_edges_to_cover(G, Gamma, e)
 * lifted_graph_to_cover(G, Gamma)  
 * cayley_expander_graph_from_gen_mat(G)
 * cayley_expander_graph_from_code(C)   
 * edge_expansion(Gamma):
 * laplacian_pseudoinverse(Gamma)
 * hamiltonian_paths0(Gamma)
 * hamiltonian_paths(Gamma, signed_adjacency_matrix = [])
 * random_walk(Gamma, m)
 * random_trek(Gamma, m)
 * codifferential_basis(v, e, Gamma)
 * codifferential_matrix(Gamma)
 * pushforward_matrix_vertex_functions(Gamma1, Gamma2, f)
 * pushforward_matrix_edge_functions(Gamma1, Gamma2, f)
 * pullback_matrix_vertex_functions(Gamma1, Gamma2, f)
 * proj_blowup(x, Gamma, r)
 * blowup_balance_graph(Gamma, r)
 * blowup_weighted_graph(wGamma, r)
 * find_cover_graph(Gamma, r, verbose=False)
 * find_random_incidence_matrix(m,n)
 * flower_graph(N)
 * vertex_matrix_map_to_CL(Gamma1, Gamma2, Phi, verbose = False)
 * vertical_edges_list(Gamma1, Gamma2, f)
 * adjacency_matrix_decomposition(Gamma1, Gamma2, f)
 * harmonic_edge_irreducible_subgraph(Gamma1, Gamma2, f)
 * is_harmonic_edge_irreducible(Gamma1, Gamma2, f)
 * coalescence_vertex(Gamma1, Gamma2)
 * coalescence_edge(Gamma1, Gamma2)
 * barycentric_subdivision_graph(Gamma)
 * harmonic_edge_irreducible_subgraph(Gamma1, Gamma2, f)
 * one_vertex_corona(Gamma)
 * corona(Gamma1, Gamma2)
 * CL_of_join_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
 * CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
 * matrix_of_graph_of_product_of_morphisms_vertices(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
 * is_cartesian_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)
 * is_cartesian_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)
 * is_tensor_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)
 * is_tensor_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)
 * is_strong_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)
 * CL_product_projection1_harmonic(Gamma1, Gamma2)
 * CL_product_projection2_harmonic(Gamma1, Gamma2)
 * is_cartesian_product_projection1_harmonic(Gamma1, Gamma2, verbose=False)
 * is_tensor_product_projection1_harmonic(Gamma1, Gamma2, verbose=False)
 * is_strong_product_projection1_harmonic(Gamma1, Gamma2, verbose=False)
 * is_strong_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose = False)
 * is_lexicographic_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)
 * is_lexicographic_product_projection1_harmonic(Gamma1, Gamma2, verbose=False)
 * is_lexicographic_product_projection2_harmonic(Gamma1, Gamma2, verbose=False)
 * is_disjunctive_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose = False)
 * is_disjunctive_product_projection1_harmonic(Gamma1, Gamma2, verbose=False)
 * is_disjunctive_product_projection2_harmonic(Gamma1, Gamma2, verbose=False)
 * morphism_of_line_graphs(Gamma1, Gamma2, f, verbose=False)
 * LC_multipartite_graph(L, cyclic=False)
 * blowup_graph(Gamma, L)
 * blowdown_morphism(Gamma, L)
 * degree_of_harmonic_morphism(Gamma1, Gamma2, f)
 * subdivision_graph(Gamma, e)
 * lower_upper_bound_sgon(Gamma)
 * subdivision_graph_morphism(Gamma1, Gamma2, f, s)
 * is_smooth_vertex(Gamma, v0)
 * smooth_graph(Gamma, v0)
 * smooth_graph_morphism(Gamma1, Gamma2, f, x0)
 * delete_vertex_graph_morphism(Gamma1, Gamma2, f, x0)
 * table_of_local_horizontal_multiplicities(Gamma1, Gamma2, f)
 * is_harmonic_graphWB_morphism(Gamma1, Gamma2, f, B1, B2, verbose = False)
 * partial_join_graph(Gamma, S)
 * leaf_addition_graph_morphism(Gamma1, Gamma2, f, x0)
 * sub_graph4edge(Gamma1, e0, Gamma, a, b)
 * has_harmonic_quotient(Gamma, verbose=False)
 * double_point_construction(Gamma)
 * graph_id_graph6(Gamma, verbose=False)
 * effective_resistance_matrix(Gamma)
 * vertical_multiplicity_of_graph_morphism(Gamma1, Gamma2, f, v2)
 * is_graph_homomorphism(Gamma1, Gamma2, f, verbose=False)
 * intersection_number_of_vertex_subset(Gamma, C, v)
 * associated_partition_to_morphism(Gamma1, Gamma2, f)     
 * is_equitable_partition(Gamma, P, verbose=False)
 * is_associated_partition_equitable(Gamma1, Gamma2, f, verbose=False)
 * partition_cell_edges(Gamma, C1, C2)
 * weights_of_vertex_to_cell(woGamma, C, v)
 * is_weighted_equitable_partition(woGamma, P, verbose=False)
 * weighted_cayley_graph(gp, symm_gp_gens)
 * convolve_function_with_filter(g, h, S)

Copyright 2014-2025 - David Joyner wdjoyner@gmail.com

Licensed modified BSD

Cleanup and edits of docstrings summer 2025 by wdj.
"""

def compactify_list(L):
    """
    L is a length n list of integers, possibly with repitition, 
    taken from an ordered set S of distinct integers of length k<=n.
    This function returns a corresponding list (also of length n)
    of integers taken from the range {0, 1, ..., k-1}, obtained by
    0-based reindexing.

    EXAMPLES:
        sage: compactify_list([10, 30, 10, 20])  # Mapping: 10 -> 0, 20 -> 1, 30 -> 2
         [0, 2, 0, 1]
        sage: compactify_list( [5, 7, 5, 9] ) 
         [0, 1, 0, 2]
    """
    S = list(Set(L))
    k = len(S)
    S0 = srange(k)
    L0 = []
    n = len(L)
    for i in range(n):
        j = S.index(L[i])
        L0.append(S0[j])
    return L0
    
def graph_convert_to_standard(Gamma):
    """
    This utility function simply converts the (unlabeled,
    ie, no edge weights) graph Gamma = (V, E), assumed 
    to be in some other indexing (eg, as a grid graph or cube graph) 
    into the standard numerical ordering (so the vertices are 
    [0, ..., n-1], for example.

    The ordering is preserved (I hope).

    EXAMPLES:
        sage: Gamma = graphs.CubeGraph(3)    
        sage: Gamma.vertices(sort=True)
         ['000', '001', '010', '011', '100', '101', '110', '111']
        sage: Gamma.edges(labels=None,sort=True)
         [('000', '001'), ('000', '010'), ('000', '100'), ('001', '011'),
          ('001', '101'), ('010', '011'), ('010', '110'), ('011', '111'),
          ('100', '101'), ('100', '110'), ('101', '111'), ('110', '111')]
        sage: Gamma0 = graph_convert_to_standard(Gamma)
        sage: Gamma0.vertices(sort=True)
         [0, 1, 2, 3, 4, 5, 6, 7]
        sage: Gamma0.edges(labels=None,sort=True)
         [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6),
          (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
        sage: Gamma.is_isomorphic(Gamma0)
         True

    """
    V = Gamma.vertices(sort=True)
    n = len(V)
    E = Gamma.edges(labels=None,sort=True)
    m = len(E)
    V0 = list(range(n))
    #V0.sort()
    #print(V, "\n", V0)
    E0 = [(V.index(e[0]), V.index(e[1])) for e in E]
    #print(len(E), len(E0))
    Gamma0 = Graph([V0, E0])
    return Gamma0

def find_matrix_permutation(L1, L2):
    """
    INPUT: Two lists (possibly with repeated elements) of length n, L1, L2
    OUTPUT: A permutation matrix sending L1 to L2

    EXAMPLE:
        sage: find_matrix_permutation([2,4,4,0,0], [0,0,2,4,4])
        [0 0 0 1 0]
        [0 0 0 0 1]
        [1 0 0 0 0]
        [0 1 0 0 0]
        [0 0 1 0 0]

    REFERENCE:
     Uses material from
        https://ask.sagemath.org/question/60779/how-to-find-a-permutation-which-sends-a-given-list-to-another-given-list-in-sagemath/
     """
    oneline = []
    for n in L1:
        # Look for n in L2.
        # Sage's one-line permutation format expects indices to start at 1, not 0,
        # so add 1 to all indices here.
        j = L2.index(n) + 1
        # If we've already found this instance, look in the rest of the list for another one.
        while j in oneline:
            j += L2[j:].index(n) + 1
        oneline.append(j)
    return matrix(Permutation(oneline))

def orthogonal_eigenbasis_sorted(M, F=QQ):
    """
    Input:
      M -- a nxn symmetric real matrix (with real eigenvalues)
    Outputs:
      D -- a matrix with eigenvalues D_i sorted in monotonically
           increasing order
      P -- a matrix whose n columns P_i are orthogonal (noto.n.) eigenvectors of M s.t.
	   M*P_i = D_i*P_i
      N -- a diagonal matrix of norms of the P_i, so
           that P*N^(-1) is orthonormal.

    This works because the diagonalization method uses a matrix of eigenvectors for the transformation matrix.
    
    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)
        sage: Q1 = Gamma1.laplacian_matrix(); Q1
        [ 1 -1  0]
        [-1  2 -1]
        [ 0 -1  1]
        sage:  orthogonal_eigenbasis_sorted(Q1)
        (
        [0 0 0]  [ 1  1  1]  [sqrt(3)       0       0]
        [0 1 0]  [ 1  0 -2]  [      0 sqrt(2)       0]
        [0 0 3], [ 1 -1  1], [      0       0 sqrt(6)]
        )
        sage: D,P,N = orthogonal_eigenbasis_sorted(Q1)
        sage: i=0; Q1*P.columns()[i] == D.diagonal()[i]*P.columns()[i]
        True
        sage: i=1; Q1*P.columns()[i] == D.diagonal()[i]*P.columns()[i]
        True
        sage: i=2; Q1*P.columns()[i] == D.diagonal()[i]*P.columns()[i]
        True
        sage: U = P*N^(-1)
        sage: U.transpose()*U
        [1 0 0]
        [0 1 0]
        [0 0 1]

    """
    Da,Pa = M.diagonalization(base_field=F)
    Db = diagonal_matrix(sorted(Da.diagonal()))
    L1 = Da.diagonal()
    L2 = sorted(Da.diagonal())
    Perm = find_matrix_permutation(L1, L2)
    Pags = Pa.transpose().gram_schmidt()[0].transpose() 
    Pb = Pags*Perm^(-1)
    N = diagonal_matrix([v.norm() for v in Pb.columns()])
    return Db, Pb, N
    
def plot_walk_in_graph(Gamma, W):
    """
    This function plots a walk W in a graph Gamma, returned as a graphics
    object (append ".show()" to view). The graph is plotted as usual 
    and the edges of the walk (more precisely the edges of the path 
    determined by it) are plotted in thick red.
    Returns False if W is not a walk in Gamma.

    EXAMPLES:
        sage: Gamma = graphs.ButterflyGraph()
        sage: W = [(0,4),(4,1)]
        sage: P = plot_walk_in_graph(Gamma, W)

    Type P.show() to view.
    """
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(labels=None,sort=True)
    #print(V, E, edge_set_is_a_walk(Gamma, W))
    if edge_set_is_a_walk(Gamma, W):
        options1 = {"layout":"circular","axes":False}
        P1 = GraphPlot(Gamma,options=options1).plot()
        Gamma2 = Gamma.subgraph(vertices = V, edges = W)
        options2 = {"layout":"circular", "edge_thickness":2, "edge_color":"red","axes":False}
        P2 = GraphPlot(Gamma2,options=options2).plot()
        return P1+P2
    return False

def edges_in_cycle_basis(Gamma):
    """
    Computes L = Gamma.cycle_basis(), each element of which is a 
    list of vertices of a "basis" cycle in Gamma, then for each r in L,
    returns the list of edges determined by r.

    EXAMPLES:
        sage: V2 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        sage: E2 = [(0,1),(0,2),(0,7),(0,8),(1,2),(1,3),(1,7),(2,3),(2,8),
        ....: (3, 4), (3, 5), (4, 5), (4, 6), (4, 8), (5, 6), (5, 7), (6, 7), (6, 8)]
        sage: Gamma2 = Graph([V2,E2])
        sage: Gamma2.cycle_basis()
        [[2, 8, 0],
         [4, 6, 8],
         [7, 6, 8, 0],
         [4, 5, 6],
         [7, 5, 6],
         [1, 3, 5, 6, 8, 0],
         [2, 3, 5, 6, 8],
         [4, 3, 5],
         [1, 7, 0],
         [1, 2, 0]]
        sage: edges_in_cycle_basis(Gamma2)
        [[(2, 8), (8, 0), (0, 2)],
         [(4, 6), (6, 8), (8, 4)],
         [(7, 6), (6, 8), (8, 0), (0, 7)],
         [(4, 5), (5, 6), (6, 4)],
         [(7, 5), (5, 6), (6, 7)],
         [(1, 3), (3, 5), (5, 6), (6, 8), (8, 0), (0, 1)],
         [(2, 3), (3, 5), (5, 6), (6, 8), (8, 2)],
         [(4, 3), (3, 5), (5, 4)],
         [(1, 7), (7, 0), (0, 1)],
         [(1, 2), (2, 0), (0, 1)]]

    """
    L = Gamma.cycle_basis()
    edges = []
    for r in L:
        m = len(r)
        r_edges = []
        for i in range(m-1):
            r_edges.append((r[i],r[i+1]))
        r_edges.append((r[m-1],r[0]))
        edges.append(r_edges)
    return edges
    
def tree_component_plus(Gamma, e, T, eo):
    r"""
    This computes the positive component T_e^+ of a 
    spanning tree T in a graph Gamma, with e in T.

    INPUT:
        Gamma - graph
        e  - edge of Gamma
        T  - spanning tree of Gamma  
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: T = Gamma.min_spanning_tree()
        sage: E = Gamma.edges(sort=True)
        sage: e = E[5]
        sage: e in T
        True
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: tree_component_plus(Gamma, e, T, eo)
        Subgraph of (): Graph on 1 vertex
        sage: tree_component_plus(Gamma, e, T, eo).vertices(sort=True)
        [a + 2]
        sage: tree_component_minus(Gamma, e, T, eo)
        Subgraph of (): Graph on 8 vertices

    """
    E = Gamma.edges(sort=True)
    GammaT = Graph(T)
    if not(e in T):
        return T
    k = E.index(e)
    GammaT.delete_edge(E[k])
    GammaTcc = GammaT.connected_components_subgraphs()
    GammaT1 =  GammaTcc[0]
    GammaT2 =  GammaTcc[1]
    V1 = GammaT1.vertices(sort=True)
    V2 = GammaT2.vertices(sort=True)
    if eo[k] == 1:
        v = e[0]
    else:
        v = e[1]
    if v in V1:
        return GammaT1
    else:
        return GammaT2

def tree_component_minus(Gamma, e, T, eo):
    r"""
    This computes the negative component T_e^- of a 
    spanning tree T in a graph Gamma, with e in T.

    INPUT:
        Gamma - graph
        e  - edge of Gamma
        T  - spanning tree of Gamma  
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: T = Gamma.min_spanning_tree()
        sage: E = Gamma.edges(sort=True)
        sage: e = E[5]
        sage: e in T
        True
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: tree_component_plus(Gamma, e, T, eo)
        Subgraph of (): Graph on 1 vertex
        sage: tree_component_plus(Gamma, e, T, eo).vertices(sort=True)
        [a + 2]
        sage: tree_component_minus(Gamma, e, T, eo).vertices(sort=True)
        [0, 1, 2, a, a + 1, 2*a, 2*a + 1, 2*a + 2]

    """
    E = Gamma.edges(sort=True)
    GammaT = Graph(T)
    if not(e in T):
        return T
    k = E.index(e)
    GammaT.delete_edge(E[k])
    GammaTcc = GammaT.connected_components_subgraphs()
    GammaT1 =  GammaTcc[0]
    GammaT2 =  GammaTcc[1]
    V1 = GammaT1.vertices(sort=True)
    V2 = GammaT2.vertices(sort=True)
    if eo[k] == -1:
        v = e[0]
    else:
        v = e[1]
    if v in V1:
        return GammaT1
    else:
        return GammaT2

def is_incident_to(Gamma, e, v):
    r"""
    Returns True if 
       (a) v is a vertex of a graph Gamma, and
       (b) e is an edge of the graph Gamma,
       (c) e is incident to v
    Returns False otherwise.

    EXAMPLES:
         sage: V1 = [0,1,2,3]
         sage: E1 = [(0, 1), (1, 2), (1, 3)]
         sage: Gamma1 = Graph([V1,E1])
         sage: is_incident_to(Gamma1, E1[0], V1[2])
         False
         sage: is_incident_to(Gamma1, E1[0], V1[1])
         True

    """
    E = Gamma.edges(labels=None, sort=True)
    V = Gamma.vertices(sort=True)
    if (v in V) and (e in E) and ((v == e[0]) or (v == e[1])):
        return True
    else:
        return False
	
def incidence_value(Gamma, v, e, eo):
    r"""
    This computes the incidence value of a vertex and edge of 
    a graph Gamma with edge-orientation vector eo. 

    INPUT:
        Gamma - graph
        v  - vertex of Gamma
        e  - edge of Gamma  
        eo - a pair [E, e0] where e0 is a vector of 1's and -1's of 
             length |E|
 
    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = list(Gamma.edges(labels=None,sort=True))
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [E, [1]*len(E)]
        sage: incidence_value(Gamma, V[2], E[3], eo)
        0
        sage: incidence_value(Gamma, V[8], E[3], eo)
        -1

    """
    E = list(eo[0])
    e0 = eo[1]
    if not(e in E):
       print("%s must be an edge"%str(e))
       return 0
    if v in e:
        if v == e[0]:
            k = E.index(e)
            return e0[k]
        elif v == e[1]:
            k = E.index(e)
            return -e0[k]
        else:
            return 0
    return 0

def incidence_matrix(Gamma, eo):
    r"""
    This computes the incidence matrix (whose rows are indexed by edges
    and whose columns are indexed by vertices) of a graph Gamma with 
    edge-orientation vector eo. The ordering of the edges and of the vertices is the same 
    as Sage's vertices and edges methods.

    INPUT:
        Gamma - graph
        eo - a pair [E, e0] where e0 is a vector of 1's and -1's whose 
             length is |E|     (ie, the size of Gamma, M)

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = list(Gamma.edges(labels=None,sort=True))
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [E, [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]]
        sage: incidence_matrix(Gamma, eo)
        [ 1 -1  1  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
        [-1  0  0  0 -1 -1  1  0  0  0  0  0  0  0  0  0  0  0]
        [ 0  1  0  0  1  0  0 -1  1  0  0  0  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  0  1  0  1 -1 -1  0  0  0  0  0  0]
        [ 0  0 -1  0  0  0  0  0  0 -1  0  0  1 -1  0  0  0  0]
        [ 0  0  0  0  0  1  0  0  0  0  1  0 -1  0  1  0  0  0]
        [ 0  0  0  0  0  0 -1  0  0  0  0  0  0  0 -1  1 -1  0]
        [ 0  0  0  0  0  0  0  0 -1  0  0  1  0  0  0 -1  0 -1]
        [ 0  0  0 -1  0  0  0  0  0  0  0  0  0  1  0  0  1  1]

        sage: IM = incidence_matrix(Gamma, eo)
        sage: IM1 = IM.delete_rows([0])
        sage: Proj1 = IM1.transpose()*(IM1*IM1.transpose())^(-1)*IM1
        sage: Proj1.image() # row space
        Vector space of degree 18 and dimension 8 over Rational Field
        Basis matrix:
        [ 1  0  0  0  1  0  0  0  0  0 -1  0  1  0  0 -1  1  0]
        [ 0  1  0  0  1  0  0  0  0  1 -1  0  0  0  0 -1  0 -1]
        [ 0  0  1  0  0  0  0  0  0  1  0  0 -1  1  0  0  0  0]
        [ 0  0  0  1  0  0  0  0  0  0  0  0  0 -1  0  0 -1 -1]
        [ 0  0  0  0  0  1  0  0  0  0  1  0 -1  0  1  0  0  0]
        [ 0  0  0  0  0  0  1  0  0  0  0  0  0  0  1 -1  1  0]
        [ 0  0  0  0  0  0  0  1  0  1 -1 -1  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  0  0  1  0  0 -1  0  0  0  1  0  1]
        sage: cut_space(Gamma, eo)
        Vector space of degree 18 and dimension 8 over Rational Field
        Basis matrix:
        [ 1  0  0  0  1  0  0  0  0  0 -1  0  1  0  0 -1  1  0]
        [ 0  1  0  0  1  0  0  0  0  1 -1  0  0  0  0 -1  0 -1]
        [ 0  0  1  0  0  0  0  0  0  1  0  0 -1  1  0  0  0  0]
        [ 0  0  0  1  0  0  0  0  0  0  0  0  0 -1  0  0 -1 -1]
        [ 0  0  0  0  0  1  0  0  0  0  1  0 -1  0  1  0  0  0]
        [ 0  0  0  0  0  0  1  0  0  0  0  0  0  0  1 -1  1  0]
        [ 0  0  0  0  0  0  0  1  0  1 -1 -1  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  0  0  1  0  0 -1  0  0  0  1  0  1]
        sage: B = incidence_matrix(Gamma, eo) 
        sage: B*B.transpose() == Gamma.laplacian_matrix()
        True

        sage: V = range(10)
        sage: E = [(0,1),(0,2),(0,5),(1,2),(1,3),(1,5),(2,4),(2,5),(3,4),(3,5),(3,6),\
        ....: (4,5),(4,7),(5,6),(5,7),(5,8),(6,7),(6,8),(7,8),(8,9)]
        sage: Gamma = Graph([V,E]) # Seifrot graph of Kaballah mysticism
        sage: eo = [E,20*[1]]
        sage: incidence_matrix(Gamma, eo)
        [ 1  1  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
        [-1  0  0  1  1  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
        [ 0 -1  0 -1  0  0  1  1  0  0  0  0  0  0  0  0  0  0  0  0]
        [ 0  0  0  0 -1  0  0  0  1  1  1  0  0  0  0  0  0  0  0  0]
        [ 0  0  0  0  0  0 -1  0 -1  0  0  1  1  0  0  0  0  0  0  0]
        [ 0  0 -1  0  0 -1  0 -1  0 -1  0 -1  0  1  1  1  0  0  0  0]
        [ 0  0  0  0  0  0  0  0  0  0 -1  0  0 -1  0  0  1  1  0  0]
        [ 0  0  0  0  0  0  0  0  0  0  0  0 -1  0 -1  0 -1  0  1  0]
        [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1  0 -1 -1  1]
        [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1]

    """
    E = eo[0]
    e0 = eo[1]
    V = Gamma.vertices(sort=True)
    IG = [[incidence_value(Gamma, v, e, eo) for v in V] for e in E]
    return matrix(QQ, IG).transpose()


def weight_at_edge(Gamma, w0, e):
    """
    returns the edge weight of e on an edge-weighted graph Gamma
    (the value is independent of edge orientation)
    returns -1 if w0 is not a legal set of edge-weights

    eo - a pair [E, e0] where e0 is a vector of 1's and -1's of length |E|
    w0 - a pair [E, wt0] where wt0 is a vector of length |E| whose entries are > 0

    EXAMPLES:
        sage: V = [0,1,2,3]
        sage: E = [(0, 1), (0, 2), (0, 3), (1, 2)]
        sage: Gamma = Graph([V, E])
        sage: w0 = [E, [1/2, 3/5, 4/3, 2/3]]
        sage: weight_at_edge(Gamma, w0, (2, 1))
         2/3
        sage: weight_at_edge(Gamma, w0, (0, 3))
         4/3
        sage: Ew = [(0, 1, 1/2), (0, 2, 3/5), (0, 3, 4/3), (1, 2, 2/3)]
        sage: Gamma_w = Graph([V,Ew], weighted = True)
        sage: Gamma_w.weighted_adjacency_matrix()
         [  0 1/2 3/5 4/3]
         [1/2   0 2/3   0]
         [3/5 2/3   0   0]
         [4/3   0   0   0]

    """
    E = list(Gamma.edges(sort=True, labels=None))
    wt0 = w0[1]
    x = e[0]
    y = e[1]
    #if not((x,y) in E or (y,x) in E):
    #    return 0
    if (x,y) in E:
        i0 = E.index((x,y))
        return wt0[i0]
    if (y,x) in E:
        i0 = E.index((y,x))
        return wt0[i0]
    return "the edge e is not an edge"
    
def weighted_degree(Gamma, w0, v):
    """
    returns the weighted degree of v on an edge-weighted graph Gamma
    (the value is independent of edge orientation)

    w0 - a pair [E, wt0] where wt0 is a vector of length |E| whose entries are > 0
    v - a vertex of Gamma
 
    EXAMPLES:
        sage: V = [0,1,2,3]
        sage: E = [(0, 1), (0, 2), (0, 3), (1, 2)]
        sage: Gamma = Graph([V, E])
        sage: w0 = [E, [1/2, 3/5, 4/3, 2/3]]
        sage: weighted_degree(Gamma, w0, 0)
         73/30

    """
    Nbrs = Gamma.neighbors(v)
    degs = [weight_at_edge(Gamma, w0, (v,w)) for w in Nbrs]
    return sum(degs)


def weighted_degree_matrix(Gamma, w0):
    """
    Returns the diagonal weighted degree matrix of Gamma.
    (the value is independent of edge orientation)

    eo - a pair [E, e0] where e0 is a vector of 1's and -1's of length |E|
    w0 - a pair [E, wt0] where wt0 is a vector of length |E| whose entries are > 0

    EXAMPLES:
        sage: V = [0,1,2,3]
        sage: E = [(0, 1), (0, 2), (0, 3), (1, 2)]
        sage: Gamma = Graph([V, E])
        sage: w0 = [E, [1/2, 3/5, 4/3, 2/3]]
        sage: weighted_degree_matrix(Gamma, w0)
         [73/30     0     0     0]
         [    0   7/6     0     0]
         [    0     0 19/15     0]
         [    0     0     0   4/3]

    """
    V = Gamma.vertices(sort=True)
    n = len(V)
    nbrs = [(v, Gamma.neighbors(v)) for v in V]

    def d_entry(i,j):
        if i != j:
            return 0
        if i == j:
            v = i
            Nbrs = nbrs[i][1]
            wdegs = [weight_at_edge(Gamma, w0, (v,w)) for w in Nbrs]
            return sum(wdegs)

    return Matrix(n, n, d_entry)
    
def weighted_incidence_matrix(Gamma, eo, w0):
    r"""
    This computes the incidence matrix (whose rows are indexed by edges
    and whose columns are indexed by vertices) of an edge-weighted
    graph Gamma with 
    eo - a pair [E1,e0], where e0 an edge-orientation vector of length |E1|
               with entries in {-1, 1}
    w0 - a pair [E1,wt0], where wt0 an edge-weight vector of length |E1|
               with entries > 0. 
    (These are represented as pairs to ensure the ordering of the edges is the same 
    as that of the orientation list and weight list.)

    INPUT:
        Gamma - graph

    EXAMPLES:
        sage: V = [0,1,2,3]
        sage: E = [(0, 1), (0, 2), (0, 3), (1, 2)]
        sage: Gamma = Graph([V, E])
        sage: eo = [E,[1, 1, 1, 1]]
        sage: w0 = [E, [1/2, 3/5, 4/3, 2/3]]
        sage: B_w = weighted_incidence_matrix(Gamma, eo, w0); B_w
         [   sqrt(1/2)    sqrt(3/5)  2*sqrt(1/3)            0]
         [  -sqrt(1/2)            0            0    sqrt(2/3)]
         [           0   -sqrt(3/5)            0   -sqrt(2/3)]
         [           0            0 -2*sqrt(1/3)            0]
        sage: B_w*B_w.transpose()
         [73/30  -1/2  -3/5  -4/3]
         [ -1/2   7/6  -2/3     0]
         [ -3/5  -2/3 19/15     0]
         [ -4/3     0     0   4/3]
        sage: Ew = [(0, 1, 1/2), (0, 2, 3/5), (0, 3, 4/3), (1, 2, 2/3)]
        sage: Gamma_w = Graph([V,Ew], weighted = True)
        sage: Gamma_w.laplacian_matrix()
         [73/30  -1/2  -3/5  -4/3]
         [ -1/2   7/6  -2/3     0]
         [ -3/5  -2/3 19/15     0]
         [ -4/3     0     0   4/3]
        sage: weighted_degree_matrix(Gamma, e0, w0)
         [73/30     0     0     0]
         [    0   7/6     0     0]
         [    0     0 19/15     0]
         [    0     0     0   4/3]

    """
    E = w0[0]
    wt0 = w0[1]
    V = Gamma.vertices(sort=True)
    IG = [[sqrt(weight_at_edge(Gamma, w0, e))*incidence_value(Gamma, v, e, eo) for v in V] for e in E]
    return matrix(SR, IG).transpose()


def oriented_edge_matrix(Gamma, eo):
    r"""
    Returns the 2mx2m (0,1)-edge matrix as defined by Terras (who denotes it by 
    W or W_1), where m is the number of edges of Gamma. Satisfies 
    det(I_2m-x*W) = (Ihara zeta polynomial of Gamma).
    eo - a pair [E1,e0], where e0 an edge-orientation vector of length |E1|
               with entries in {-1, 1}
    

    EXAMPLES:
        sage: Gamma = graphs.CycleGraph(4)
        sage: E = list(Gamma.edges(labels=None,sort=True))
        sage: eo = [E, len(E)*[1]]
        sage: I2m = diagonal_matrix(2*m*[1])
        sage: W = oriented_edge_matrix(Gamma, eo); W
        [0 0 1 0 0 0 0 0]
        [0 0 0 0 0 0 0 1]
        [0 0 0 1 0 0 0 0]
        [0 0 0 0 0 1 0 0]
        [0 1 0 0 0 0 0 0]
        [1 0 0 0 0 0 0 0]
        [0 0 0 0 1 0 0 0]
        [0 0 0 0 0 0 1 0]
        sage: det(I2m-x*W)
        x^8 - 2*x^4 + 1
        sage: expand(zeta_polynomial_graph(Gamma))
        x^8 - 2*x^4 + 1

    """
    E = Gamma.edges(sort=True, key=lambda x: ZZ(x[2]))
    m = len(E)
    e0 = eo[1]
    entry = [[0 for i in range(2*m)] for j in range(2*m)]
    for i in range(2*m):
        for j in range(2*m):
            if i<m and j<m:
                if e0[i]==1 and e0[j]==1:
                    if E[i][1]==E[j][0]:
                        entry[i][j] = 1
                        #print(i,j,"eo[i]==1 and eo[j]==1")
            if i<m and j<m:
                if e0[i]==1 and e0[j]==-1:
                    if E[i][1]==E[j][1]:
                        entry[i][j] = 1			
            if i<m and j<m:
                if e0[i]==-1 and e0[j]==1:
                    if E[i][0]==E[j][0]:
                        entry[i][j] = 1
                        #print(i,j,"eo[i]==-1 and eo[j]==1")
            if i<m and j<m:
                if e0[i]==-1 and e0[j]==-1:
                    if E[i][0]==E[j][1]:
                        entry[i][j] = 1
            ## i>=m and j<m:
            if i>=m and j<m:
                if e0[i-m]==-1 and e0[j]==1:
                    if E[i-m][1]==E[j][0] and (E[i-m][0]!=E[j][1]):
                        entry[i][j] = 1
            if i>=m and j<m:
                if e0[i-m]==-1 and e0[j]==-1:
                    if E[i-m][1]==E[j][1] and (E[i-m][0]!=E[j][0]):
                        entry[i][j] = 1			
            if i>=m and j<m:
                if e0[i-m]==1 and e0[j]==1:
                    if E[i-m][0]==E[j][0] and (E[i-m][1]!=E[j][1]):
                        entry[i][j] = 1
                        #print(i,j,"eo[i-m]==1 and eo[j]==1")
            if i>=m and j<m:
                if e0[i-m]==1 and e0[j]==-1:
                    if E[i-m][0]==E[j][1] and (E[i-m][1]!=E[j][0]):
                        entry[i][j] = 1
            ## i<m and j>=m
            if i<m and j>=m:
                if e0[i]==1 and e0[j-m]==-1:
                    if E[i][1]==E[j-m][0] and (E[i][0]!=E[j-m][1]):
                        entry[i][j] = 1
            if i<m and j>=m:
                if e0[i]==1 and e0[j-m]==1:
                    if E[i][1]==E[j-m][1] and (E[i][0]!=E[j-m][0]):
                        entry[i][j] = 1
                        #print(i,j,"eo[i]==1 and eo[j-m]==1")
            if i<m and j>=m:
                if e0[i]==-1 and e0[j-m]==-1:
                    if E[i][0]==E[j-m][0] and (E[i][1]!=E[j-m][1]):
                        entry[i][j] = 1
            if i<m and j>=m:
                if e0[i]==-1 and e0[j-m]==1:
                    if E[i][0]==E[j-m][1] and (E[i][1]!=E[j-m][0]):
                        entry[i][j] = 1
            ## i>=m and j>=m:
            if i>=m and j>=m:
                if e0[i-m]==-1 and e0[j-m]==-1:
                    if E[i-m][1]==E[j-m][0]:
                        entry[i][j] = 1
                        #print(i,j,"eo[i-m]==-1 and eo[j-m]==-1")
            if i>=m and j>=m:
                if e0[i-m]==-1 and e0[j-m]==1:
                    if E[i-m][1]==E[j-m][1]:
                        entry[i][j] = 1
                        #print(i,j,"eo[i-m]==-1 and eo[j-m]==1")
            if i>=m and j>=m:
                if e0[i-m]==1 and e0[j-m]==-1:
                    if E[i-m][0]==E[j-m][0]:
                        entry[i][j] = 1
            if i>=m and j>=m:
                if e0[i-m]==1 and e0[j-m]==1:
                    if E[i-m][0]==E[j-m][1]:
                        entry[i][j] = 1
                        #print(i,j,"eo[i-m]==1 and eo[j-m]==1")
    #print(entry)
    return  matrix(QQ, entry)

def cycle_space(Gamma, eo, F = QQ):
    r"""
    This computes the cycle space Z of Gamma.

    INPUT:
        Gamma - graph
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = Gamma.edges(sort=True)
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: cycle_space(Gamma, eo)
        Vector space of degree 18 and dimension 10 over Rational Field
        Basis matrix:
        [ 1  0  0 -1  0  0  1  0  0  0  0  0  0  0  0  0 -1  0]
        [ 0  1  0  1  0  0  0  0 -1  0  0  0  0  0  0  0  0  1]
        [ 0  0  1 -1  0  0  0  0  0  0  0  0  0 -1  0  0  0  0]
        [ 0  0  0  0  1  0  1  0 -1  0  0  0  0  0  0  0 -1  1]
        [ 0  0  0  0  0  1  1  0  0  0  0  0  0  0 -1  0  0  0]
        [ 0  0  0  0  0  0  0  1  1  0  0  1  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  0  0  0  1  0  1  0 -1  0  0  0  1]
        [ 0  0  0  0  0  0  0  0  0  0  1 -1  0  0 -1  0  1 -1]
        [ 0  0  0  0  0  0  0  0  0  0  0  0  1  1  1  0 -1  0]
        [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  1 -1]
    """
    m = len(Gamma.edges(sort=True))
    n = len(Gamma.vertices(sort=True))
    MS = MatrixSpace(F, m, n)
    IG = MS(incidence_matrix(Gamma, eo).transpose())
    return IG.kernel()

def cocycle_space(Gamma, eo):
    r"""
    This computes the cocycle=cut space B of Gamma.
    eo - a pair [E1,e0], where e0 an edge-orientation vector of length |E1|
               with entries in {-1, 1}

    """
    return cut_space(Gamma, eo)

def cut_space(Gamma, eo):
    r"""
    This computes the cut space B of Gamma.

    INPUT:
        Gamma - graph
    eo - a pair [E ,e0], where e0 an edge-orientation vector of length |E|
               with entries in {-1, 1}

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = list(Gamma.edges(labels=None,sort=True))
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [E, [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]]
        sage: cut_space(Gamma, eo)
        Vector space of degree 18 and dimension 8 over Rational Field
        Basis matrix:
        [ 1  0  0  0  1  0  0  0  0  0 -1  0  1  0  0 -1  1  0]
        [ 0  1  0  0  1  0  0  0  0  1 -1  0  0  0  0 -1  0 -1]
        [ 0  0  1  0  0  0  0  0  0  1  0  0 -1  1  0  0  0  0]
        [ 0  0  0  1  0  0  0  0  0  0  0  0  0 -1  0  0 -1 -1]
        [ 0  0  0  0  0  1  0  0  0  0  1  0 -1  0  1  0  0  0]
        [ 0  0  0  0  0  0  1  0  0  0  0  0  0  0  1 -1  1  0]
        [ 0  0  0  0  0  0  0  1  0  1 -1 -1  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  0  0  1  0  0 -1  0  0  0  1  0  1]
        sage: v = cut_space(Gamma, eo).random_element()
        sage: w = cycle_space(Gamma, eo).random_element()
        sage: v.inner_product(w)
        0
    """
    Z = cycle_space(Gamma, eo)
    return Z.complement()

def cuts_list(Gamma, verbose=False):
    r"""
    Returns list of all cuts of Gamma

    EXAMPLES:
        sage: Gamma =  graphs.DiamondGraph()
        sage: cuts_list(Gamma)

        [[(0, 1), (0, 2)],
         [(1, 0), (1, 2), (1, 3)],
         [(0, 2), (1, 2), (1, 3)],
         [(2, 0), (2, 1), (2, 3)],
         [(0, 1), (2, 1), (2, 3)],
         [(1, 0), (1, 3), (2, 0), (2, 3)],
         [(1, 3), (2, 3)]]
        sage: Gamma = graphs.CompleteGraph(4)
        sage: cuts_list(Gamma)

        [[(0, 1), (0, 2), (0, 3)],
         [(1, 0), (1, 2), (1, 3)],
         [(0, 2), (0, 3), (1, 2), (1, 3)],
         [(2, 0), (2, 1), (2, 3)],
         [(0, 1), (0, 3), (2, 1), (2, 3)],
         [(1, 0), (1, 3), (2, 0), (2, 3)],
         [(0, 3), (1, 3), (2, 3)]]
        sage: Gamma = graphs.HouseGraph()
        sage: cuts_list(Gamma, verbose=True)

        [[[[], [0, 1, 2, 3, 4]]],
         [[[0], [1, 2, 3, 4]], (0, 1), (0, 2)],
         [[[1], [0, 2, 3, 4]], (1, 0), (1, 3)],
         [[[0, 1], [2, 3, 4]], (0, 2), (1, 3)],
         [[[2], [0, 1, 3, 4]], (2, 0), (2, 3), (2, 4)],
         [[[0, 2], [1, 3, 4]], (0, 1), (2, 3), (2, 4)],
         [[[1, 2], [0, 3, 4]], (1, 0), (1, 3), (2, 0), (2, 3), (2, 4)],
         [[[0, 1, 2], [3, 4]], (1, 3), (2, 3), (2, 4)],
         [[[3], [0, 1, 2, 4]], (3, 1), (3, 2), (3, 4)],
         [[[0, 3], [1, 2, 4]], (0, 1), (0, 2), (3, 1), (3, 2), (3, 4)],
         [[[1, 3], [0, 2, 4]], (1, 0), (3, 2), (3, 4)],
         [[[0, 1, 3], [2, 4]], (0, 2), (3, 2), (3, 4)],
         [[[2, 3], [0, 1, 4]], (2, 0), (2, 4), (3, 1), (3, 4)],
         [[[0, 2, 3], [1, 4]], (0, 1), (2, 4), (3, 1), (3, 4)],
         [[[1, 2, 3], [0, 4]], (1, 0), (2, 0), (2, 4), (3, 4)],
         [[[0, 1, 2, 3], [4]], (2, 4), (3, 4)]]

    """
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(labels=None,sort=True)
    n = len(V)
    Qn = GF(2)^n
    M = []
    for x in Qn:
        if Qn([1]*n)+x in M:
            break
        else:
            M=M+[x]
    cuts = []
    for x in M:
        A = [V[i] for i in range(n) if x[i]==1]
        B = [V[i] for i in range(n) if x[i]==0]
        cuts = cuts+[[A,B]]
    ##print cuts # partitions but not complements
    L = []
    for y in cuts:
        if verbose==True:
            coc = [y]
        else:
            coc = []
        A = y[0]
        B = y[1]
        for v in A:
            for w in B:
                if (v,w) in E or (w,v) in E:
                    coc = coc+[(v,w)]
        if coc != []:
            L = L+[coc]
    return L

def flipit(t):
    r"""
    t is a 2-tuple
    returns reverse tuple

    """
    return tuple([t[1],t[0]])
    
def cut_matrix(Gamma):
    r"""
    Returns cut matrix of Gamma

    EXAMPLES:
        sage: Gamma =  graphs.DiamondGraph()
        sage: cut_matrix(Gamma)

        [1 1 0 0 0]
        [1 0 1 1 0]
        [0 1 1 1 0]
        [0 1 1 0 1]
        [1 0 1 0 1]
        [1 1 0 1 1]
        [0 0 0 1 1]

    """
    E = Gamma.edges(labels=None,sort=True)
    C = cuts_list(Gamma)
    L = []
    for c in C:
        L = L+[[int(e in c or flipit(e) in c) for e in E]]
    CM = matrix(L)
    return CM

def cut_oriented_matrix(Gamma, e0):
    return cut_matrix_oriented(Gamma, e0)

def cut_matrix_oriented(Gamma):
    r"""
    Returns oriented cut matrix of Gamma
    (does not depand on orientation vector)

    EXAMPLES:
        sage: Gamma = graphs.CompleteGraph(4)
        sage: cut_matrix_oriented(Gamma)

        [ 1  1  1  0  0  0]
        [-1  0  0  1  1  0]
        [ 0  1  1  1  1  0]
        [ 0 -1  0 -1  0  1]
        [ 1  0  1 -1  0  1]
        [-1 -1  0  0  1  1]
        [ 0  0  1  0  1  1]

    """
    E = Gamma.edges(labels=None,sort=True)
    C = cuts_list(Gamma)
    L = []

    def shore(c,e):
        if e in c:
            return 1
        if flipit(e) in c:
            return -1
        return 0

    for c in C:
        L = L+[[shore(c,e) for e in E]]
    CM = matrix(L)
    return CM

def incidence_matrix_tree_inverse_value(Gamma, eo, x, T, e, v):
    r"""
    This computes the matrix entries of the inverse of the truncated 
    incidence matrix, D(x,T)^(-1), with edge-orientation vector eo, 
    associated to a vertex x in a spanning tree T.

    INPUT:
        Gamma - graph
        x,v  - distinct vertices of Gamma
        T  - spanning tree of Gamma  
        e  - an edge of Gamma in T
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = Gamma.edges(sort=True)
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: T = Gamma.min_spanning_tree()
        sage: x = V[2]
        sage: [incidence_matrix_tree_inverse_value(Gamma, eo, x, T, e, v) for v in V if v != x]
        [0, 0, 0, 0, 1, 0, 0, 0]
        sage: e = E[0]
        sage: e in T
        True
        sage: [incidence_matrix_tree_inverse_value(Gamma, eo, x, T, e, v) for v in V if v != x]
        [0, -1, 0, 0, -1, -1, 0, 0]

    This is consistent with the inverse matrix example for incidence_matrix_tree(Gamma, eo, x, T).

    """
    VT_e_plus = tree_component_plus(Gamma, e, T, eo).vertices(sort=True)
    VT_e_minus = tree_component_minus(Gamma, e, T, eo).vertices(sort=True)
    if v in VT_e_plus and x in VT_e_minus:
        return 1
    if x in VT_e_plus and v in VT_e_minus:
        return -1
    return 0

def incidence_tree_matrix(Gamma, eo, x, T):
    return incidence_matrix_tree(Gamma, eo, x, T)

def incidence_matrix_tree(Gamma, eo, x, T):
    r"""
    This computes the truncated incidence matrix D(x,T) with 
    edge-orientation vector eo, associated to a vertex x
    in a spanning tree T.

    INPUT:
        Gamma - graph
        x  - vertex of Gamma
        T  - spanning tree of Gamma  
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = Gamma.edges(sort=True)
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: T = Gamma.min_spanning_tree()
        sage: v = V[2]
        sage: incidence_matrix_tree(Gamma, eo, v, T)
        [ 1 -1  0  0  0  0  0  0]
        [-1  0  0  0  0  0  0  0]
        [ 1  0  0 -1  0  0  0  0]
        [ 1  0  0  0  0  0  0 -1]
        [ 0 -1  0  0  1  0  0  0]
        [ 0  1  0  0  0 -1  0  0]
        [ 0  0  1  0  0  0  0  0]
        [ 0  0  0  0  0  0 -1  0]
        sage: DvT^(-1)
        [ 0 -1  0  0  0  0  0  0]
        [-1 -1  0  0  0  0  0  0]
        [ 0  0  0  0  0  0  1  0]
        [ 0 -1 -1  0  0  0  0  0]
        [-1 -1  0  0  1  0  0  0]
        [-1 -1  0  0  0 -1  0  0]
        [ 0  0  0  0  0  0  0 -1]
        [ 0 -1  0 -1  0  0  0  0]

    """
    L = []
    E = Gamma.edges(sort=True)
    V = Gamma.vertices(sort=True)
    IM = incidence_matrix(Gamma, eo).transpose()
    i = V.index(x)
    DvT = IM.delete_columns([i])
    EnotT = [e for e in E if not(e in T)]
    for e in EnotT:
        L.append(E.index(e))
    DvT = DvT.delete_rows(L)
    return DvT

def fund_vertex_cut_char_fcn(Gamma, v, e, eo):
    r"""
    This computes the characteristic function of the fundamental 
    cut defined by a vertex v, evaluated at an edge e of a graph Gamma with 
    edge-orientation vector eo. 

    INPUT:
        Gamma - graph
        v  - vertex of Gamma
        e  - edge of Gamma  
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        1, if v is the head of e (defined by eo)
        -1, if v is the tail of e (defined by eo)
        0, otherwise.

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = Gamma.edges(sort=True)
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: v = V[2]
        sage: e = E[1]
        sage: fund_vertex_cut_char_fcn(Gamma, v, e, eo)
        1
        sage: [fund_vertex_cut_char_fcn(Gamma, V[2], e, eo) for e in E]
        [0, 1, 0, 0, 1, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 3rd column of incidence_matrix(Gamma, eo)
        sage: [fund_vertex_cut_char_fcn(Gamma, v, E[1], eo) for v in V]
        [-1, 0, 1, 0, 0, 0, 0, 0, 0]
        # 2nd row of incidence_matrix(Gamma, eo)

    """
    E = Gamma.edges(sort=True)
    V = Gamma.vertices(sort=True)
    k = E.index(e)
    IG = incidence_matrix(Gamma, eo).transpose()
    char_fcn = IG.rows()[k]
    j = V.index(v)
    return char_fcn[j]

def fund_cut_char_fcn(Gamma, v, e, eo):
    r"""
    This computes the characteristic function of the fundamental 
    cut defined by a subset U of vertices, evaluated at an edge e of a graph Gamma with 
    edge-orientation vector eo. The cut defined by U is the set of edges having exactly 
    one vertex in U.

    INPUT:
        Gamma - graph
        U  - a list of vertices of Gamma
        e  - edge of Gamma  
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        1, if v is the head of e (defined by eo)
        -1, if v is the tail of e (defined by eo)
        0, otherwise.

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: E = Gamma.edges(sort=True)
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: U = [V[2],V[4]]
        sage: e = E[1]
        sage: fund_cut_char_fcn(Gamma, U, e, eo)
        1
        sage: [fund_cut_char_fcn(Gamma, U, e, eo) for e in E]
        [0, 1, -1, 0, 1, 0, 0, -1, 1, -1, 0, 0, 1, -1, 0, 0, 0, 0]

    """
    L = [fund_vertex_cut_char_fcn(Gamma, v, e, eo) for v in U]
    return sum(L)

def fund_cycle_char_fcn(Gamma, q, e, eo):
    r"""
    This computes the characteristic function of the fundamental 
    cycle q, evaluated at an edge e of a graph Gamma with 
    edge-orientation vector eo. 

    INPUT:
        Gamma - graph
        q  - fundamental cycle of Gamma
        e  - edge of Gamma  
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        1, if v is the head of e (defined by eo)
        -1, if v is the tail of e (defined by eo)
        0, otherwise.

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: Q = Gamma.cycle_basis()
        sage: V = Gamma.vertices(sort=True)
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: e = E[1]
        sage: [fund_cycle_char_fcn(Gamma, q, e, eo) for q in Q]
        [0, 0, 0, 0, 0, 0, -1, 0, -1, -1]

    """
    Q = Gamma.cycle_basis()
    Qset = [Set(qq) for qq in Q]
    if Set(q) in Qset:
        E = Gamma.edges(sort=True)
        V = Gamma.vertices(sort=True)
        sgn = eo[E.index(e)]
        if e[0] in q and e[1] in q:
            i = q.index(e[0])
            j = q.index(e[1])
            lq = len(q)
            if i-j==1*sgn or i-j==(lq-1)*sgn:
                return 1
            if i-j==(-1)*sgn or i-j==-(lq-1)*sgn:
                return -1 
    return 0

def fund_cycle(Gamma, T, e, eo):
    r"""
    This computes the fundamental cycle C(T,F) associated to a tree T
    and an edge e of a graph Gamma, not in T, with edge-orientation  
    vector eo. 

    INPUT:
        Gamma - graph
        T  - a tree of Gamma
        e  - edge of Gamma not in T
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        C(T,f)

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: Q = Gamma.cycle_basis()
        sage: V = Gamma.vertices(sort=True)
        sage: E = Gamma.edges(sort=True)
        sage: eo = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
        sage: e = E[9]
        sage: T = Gamma.min_spanning_tree()
        sage: e in T
        False
        sage: fund_cycle(Gamma, T, e, eo)
        [(a, 2, None), (2, 0, None), (0, a + 1, None), (a + 1, a, None)]

    """
    V = Gamma.vertices(sort=True)
    i = V.index(e[0])
    j = V.index(e[1])
    P1 = Graph(T).shortest_path(V[i],V[j])
    N = len(L)
    P2 = [(L[i],L[i+1],None) for i in range(N-1)]+[(L[N-1],L[0],None)]
    return P2

def laplacian_reduced_matrix(Gamma, eo, s):
    return laplacian_reduced(Gamma, eo, s)

def laplacian_reduced(Gamma, eo, s):
    r"""
    This computes the reduced (vertex) Laplacian of a graph Gamma with 
    edge-orientation vector eo, where the row column associated to s has been removed.

    INPUT:
        Gamma - graph having N vertices
        s - a (source) vertex of Gamma
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        (N-1)x(N-1) matrix of integers which agrees with the usual adjacency 
        matrix Laplacian except for the entries associated to the vertex s.

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: eo = [1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1]
        sage: s = V[2]
        sage: LR = laplacian_reduced(Gamma, eo, s)
        sage: LR
        [ 4 -1  0 -1  0  0  0 -1]
        [-1  4  0  0 -1 -1  0  0]
        [ 0  0  4 -1 -1  0 -1  0]
        [-1  0 -1  4 -1  0  0 -1]
        [ 0 -1 -1 -1  4 -1  0  0]
        [ 0 -1  0  0 -1  4 -1 -1]
        [ 0  0 -1  0  0 -1  4 -1]
        [-1  0  0 -1  0 -1 -1  4]
        sage: LR.dimensions()
        (8, 8)
        sage: A = ZZ^8/LR.image()
        sage: A.cardinality()
        11664
        sage: Gamma.spanning_trees_count()
        11664
        sage: det(LR)
        11664
        sage: factor(11664)
        2^4 * 3^6

    """
    L = Gamma.laplacian_matrix()
    V = Gamma.vertices(sort=True)
    i = V.index(s)
    L1 = L.delete_rows([i])
    L2 = L1.delete_columns([i])
    return matrix(ZZ, L2)

def laplacian_reduced_punctured_matrix(Gamma, eo, s, p, q):
    return laplacian_reduced_punctured(Gamma, eo, s, p, q)

def laplacian_reduced_punctured(Gamma, eo, s, p, q):
    r"""
    This computes the reduced, punctured (vertex) Laplacian of a graph Gamma with 
    edge-orientation vector eo, where row for p, s are removed and columns for q,s
    are removed. It's determinant is equal to (pq||s), in Biggs notation [B], section 13-14.


    INPUT:
        Gamma - graph having N vertices
        s - a (source) vertex of Gamma
        p.q - two vertices, each distinct from s
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        (N-2)x(N-2) matrix of integers which agrees with the usual
        adjacency matrix Laplacian except for the entries associated to the
        vertex s.

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: eo = [1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1]
        sage: V = Gamma.vertices(sort=True)
        sage: s = V[2]; p = V[4]; q = V[6]
        sage: LRP = laplacian_reduced_punctured(Gamma, eo, s, p, q)
        sage: LRP
        [ 4 -1  0 -1  0  0 -1]
        [-1  4  0  0 -1 -1  0]
        [ 0  0  4 -1 -1  0  0]
        [-1  0 -1  4 -1  0 -1]
        [ 0 -1  0  0 -1  4 -1]
        [ 0  0 -1  0  0 -1 -1]
        [-1  0  0 -1  0 -1  4]
        sage: LRP.dimensions()
        (7, 7)
        sage: det(LRP)
        2592

    REFERENCES:
        Biggs, Norman, "Algebraic potential theory on graphs", BLMS, 1997.

    """
    LR = laplacian_reduced(Gamma, eo, s)
    V = Gamma.vertices(sort=True)
    i = V.index(p)
    j = V.index(q)
    L1 = LR.delete_rows([i])
    L2 = L1.delete_columns([j])
    return matrix(ZZ, L2)
    
def potential_induced(Gamma, e0, j, s, p, q):
    r"""
    Returns the potential function phi:V -> QQ which is induced by a source
    s having magnitude j, with input p and output q and satisfies phi(q)=0.
    Such a phi satisfies the "differential equation" 
                            D^t*phi = Pc,
    where 
      * D is the incidence matrix, and
      * P is the orthogonal projection from the space, C^1(Gamma, RR), 
        of functions on E (the edges of Gamma) to the cut space B.
    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: e0 = [1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1]
        sage: V = Gamma.vertices(sort=True)
        sage: s = V[2]; p = V[4]; q = V[6]
        sage: j = 5
        sage: potential_induced(Gamma, e0, j, s, p, q)
        2/45

    """
    LR = laplacian_reduced(Gamma, eo, s)
    LRP = laplacian_reduced_punctured(Gamma, eo, s, p, q)
    return det(LRP)/(det(LR)*j)

def number_of_2_trees(Gamma, e0, v, w):
    r"""
    Returns the number of 2-trees for which one component contains
    v and the other contains w, (v||w).

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: eo = [1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1]
        sage: V = Gamma.vertices(sort=True)
        sage: v = V[4]; w = V[6]
        sage: number_of_2_trees(Gamma, e0, v, w)
        6480

    """
    LRP = laplacian_reduced_punctured(Gamma, eo, w, v, v)
    return det(LRP)

def critical_group(Gamma):
    r"""
    Returns the co-kernel of a reduced Laplacian
    of the graph Gamma.

    EXAMPLES:
        sage: WG6 = graphs.WheelGraph(6)
        sage: critical_group(WG6)
        Finitely generated module V/W over Integer Ring with invariants (11, 11)
        sage: G = graphs.PaleyGraph(9); G
        Paley graph with parameter 9: Graph on 9 vertices
        sage: critical_group(G)
        Finitely generated module V/W over Integer Ring with invariants (6, 6, 18, 18)
        sage: 18*18*6*6
        11664
        sage: G = graphs.CompleteGraph(4); G
        Complete graph: Graph on 4 vertices
        sage: critical_group(G)
        Finitely generated module V/W over Integer Ring with invariants (4, 4)
        sage: WG4 = graphs.WheelGraph(4)
        sage: WG4.delete_edge((2,3))
        sage: WG4.add_vertex(5)
        sage: WG4.add_edges([(2,5),(3,5)])
        sage: critical_group(WG4)
        Finitely generated module V/W over Integer Ring with invariants (24)
        sage: WG4 = graphs.WheelGraph(4)
        sage: critical_group(WG4)
        Finitely generated module V/W over Integer Ring with invariants (4, 4)

        sage: G = DihedralGroup(4)
        sage: G.gens()
        [(1,2,3,4), (1,4)(2,3)]
        sage: S = G.gens()+[G.gens()[0]^(-1)]; S
        [(1,2,3,4), (1,4)(2,3), (1,4,3,2)]
        sage: A = G.cayley_graph(generators=S,simple=True).adjacency_matrix()
        sage: Gamma = Graph(A)
        sage: critical_group(Gamma)
        Finitely generated module V/W over Integer Ring with invariants (2, 8, 24)

    """
    L = Gamma.laplacian_matrix()
    L1 = L.delete_rows([0])
    L2 = L1.delete_columns([0])
    n = L2.dimensions()[0]
    return ZZ^n/L2.image()

def laplacian_vertex_matrix(Gamma, eo):
    return laplacian_vertex(Gamma, eo)

def laplacian_vertex(Gamma, eo):
    r"""
    This computes the vertex Laplacian of a graph Gamma with 
    edge-orientation vector eo. 

    INPUT:
        Gamma - graph having N vertices
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        NxN matrix of 1, -1, 0's (except on the diagonal) which agrees 
        with the usual adjacency matrix Laplacian 

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: eo = [1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1]
        sage: laplacian_vertex(Gamma, eo)
        [ 4 -1 -1  0 -1  0  0  0 -1]
        [-1  4 -1  0  0 -1 -1  0  0]
        [-1 -1  4 -1  0  0  0 -1  0]
        [ 0  0 -1  4 -1 -1  0 -1  0]
        [-1  0  0 -1  4 -1  0  0 -1]
        [ 0 -1  0 -1 -1  4 -1  0  0]
        [ 0 -1  0  0  0 -1  4 -1 -1]
        [ 0  0 -1 -1  0  0 -1  4 -1]
        [-1  0  0  0 -1  0 -1 -1  4]
        sage: Gamma.laplacian_matrix()
        [ 4 -1 -1  0 -1  0  0  0 -1]
        [-1  4 -1  0  0 -1 -1  0  0]
        [-1 -1  4 -1  0  0  0 -1  0]
        [ 0  0 -1  4 -1 -1  0 -1  0]
        [-1  0  0 -1  4 -1  0  0 -1]
        [ 0 -1  0 -1 -1  4 -1  0  0]
        [ 0 -1  0  0  0 -1  4 -1 -1]
        [ 0  0 -1 -1  0  0 -1  4 -1]
        [-1  0  0  0 -1  0 -1 -1  4]
        sage: laplacian_vertex(Gamma, eo).kernel()
        Vector space of degree 9 and dimension 1 over Rational Field
        Basis matrix:
        [1 1 1 1 1 1 1 1 1]


    """
    D = incidence_matrix(Gamma, eo)
    return D.transpose()*D

def laplacian_edge_matrix(Gamma, eo):
    return laplacian_edge(Gamma, eo)

def laplacian_edge(Gamma, eo):
    r"""
    This computes the edge Laplacian of a graph Gamma with 
    edge-orientation vector eo. 

    INPUT:
        Gamma - graph having N vertices
        eo - a vector of 1's and -1's whose length is the number of edges in Gamma
             (ie, the size of Gamma, M)

    OUTPUT:
        MxM matrix of 1, -1, 0's which agrees with the edge
        adjacency matrix Laplacian 

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(9)
        sage: eo = [1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1]
        sage: laplacian_edge(Gamma, eo)
        [ 2  1 -1  1 -1  1  1  0  0  0  0  0  0  0  0  0  0  0]
        [ 1  2 -1  1  1  0  0  1 -1  0  0  0  0  0  0  0  0  0]
        [-1 -1  2 -1  0  0  0  0  0 -1  0  0  1 -1  0  0  0  0]
        [ 1  1 -1  2  0  0  0  0  0  0  0  0  0 -1  0  0  1 -1]
        [-1  1  0  0  2 -1 -1  1 -1  0  0  0  0  0  0  0  0  0]
        [ 1  0  0  0 -1  2  1  0  0  0  1  0 -1  0 -1  0  0  0]
        [ 1  0  0  0 -1  1  2  0  0  0  0  0  0  0  1 -1  1  0]
        [ 0  1  0  0  1  0  0  2 -1  1 -1 -1  0  0  0  0  0  0]
        [ 0 -1  0  0 -1  0  0 -1  2  0  0 -1  0  0  0 -1  0  1]
        [ 0  0 -1  0  0  0  0  1  0  2 -1 -1 -1  1  0  0  0  0]
        [ 0  0  0  0  0  1  0 -1  0 -1  2  1 -1  0 -1  0  0  0]
        [ 0  0  0  0  0  0  0 -1 -1 -1  1  2  0  0  0  1  0 -1]
        [ 0  0  1  0  0 -1  0  0  0 -1 -1  0  2 -1  1  0  0  0]
        [ 0  0 -1 -1  0  0  0  0  0  1  0  0 -1  2  0  0 -1  1]
        [ 0  0  0  0  0 -1  1  0  0  0 -1  0  1  0  2 -1  1  0]
        [ 0  0  0  0  0  0 -1  0 -1  0  0  1  0  0 -1  2 -1 -1]
        [ 0  0  0  1  0  0  1  0  0  0  0  0  0 -1  1 -1  2 -1]
        [ 0  0  0 -1  0  0  0  0  1  0  0 -1  0  1  0 -1 -1  2]

    """
    D = incidence_matrix(Gamma, eo)
    return D*D.transpose()
    
def quotient_adjacent(orbits, VG, EG, i, j):
    if (orbits[i],orbits[j]) in EG or (orbits[j],orbits[i]) in EG:
        return 1
    else:
        return 0


def quotient_graph(Gamma, G, verbose=False, morphism=False):
    r"""
    This function returns the graph quotient, and in verbose mode
    information on the vertex correspondence of the quotient map.
    If morphism=True then it returns the associated quotient
    morphism in CL notation.

    If Gamma = (V, E) is a graph and G a subgroup of its 
    automorphism group acting faithfully on Gamma, we define 
    the quotient graph Gamma/G as follows:
    (1) The vertices of Gamma/G are the G-orbits in V. 
    (2) Distinct vertices v1, v2 of Gamma/G are connected by an 
        edge of Gamma/G if and only if there is 
          a vertex v1' in V belonging to the orbit 
             of v1, and 
          a vertex v2' in V belonging to the orbit 
             of v2 (note v1', v2' belong to different $G$-orbits,
             by hypothesis), 
         for which (v1', v2') belongs to E.
    Note: Gamma/G is simple.
    
    Input: Gamma - a graph in standard form,
           G     - a subgroup of its automorphism group
                   that acts faithfully on Gamma.
                   (for each non-trivial g in G, there is a v in V such that g(v)\not= v)
    Output: The quotient graph.

    EXAMPLES:
        sage: Gamma = graphs.PaleyGraph(13)
        sage: G = Gamma.automorphism_group(); G
        Permutation Group with generators [(1,9,3)(2,5,6)(4,10,12)(7,11,8), (1,10,9,12,3,4)(2,7,5,11,6,8), (0,1,2,3,4,5,6,7,8,9,10,11,12)]
        sage: quotient_graph(Gamma, G)
        Graph on 1 vertex
        sage: G2 = G.sylow_subgroup(2)
        sage: G2.order()
        2
        sage: quotient_graph(Gamma, G2)
        Graph on 7 vertices
        sage: G3 = G.sylow_subgroup(3)
        sage: G3.order()
        3
        sage: quotient_graph(Gamma, G3)
        Graph on 5 vertices
        sage: quotient_graph(Gamma, G3, verbose=True)
        (Graph on 5 vertices,
         [0, 1, 2, 3, 4],
         [({8, 11, 7}, {2, 5, 6}),
          ({8, 11, 7}, {1, 3, 9}),
          ({2, 5, 6}, {1, 3, 9}),
          ({0}, {1, 3, 9}),
          ({4, 10, 12}, {8, 11, 7}),
          ({4, 10, 12}, {1, 3, 9}),
          ({4, 10, 12}, {2, 5, 6}),
          ({4, 10, 12}, {0})],
         [{4, 10, 12}, {8, 11, 7}, {2, 5, 6}, {0}, {1, 3, 9}])

    """
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(labels=None,sort=True)
    orbits = list(Set([Set([g(v) for g in G]) for v in V]))
    #print(orbits)
    for g in G:
        if g.order()!=1:
            #print(g, [g(v)==v for v in V])
            if not(False in [g(v)==v for v in V]):
               print("Group", G, " is not faithful on Gamma.")
               return Gamma
    if len(orbits) == 1:
        return Graph(matrix([[0]]))
    n = len(orbits)
    VG = range(n)
    EG = []
    for v in orbits:
        for w in orbits:
            if v != w:
                for x in v:
                    for y in w:
                        if (x,y) in E or (y,x) in E:
                            if not((w,v) in EG):
                                EG = EG+[(v,w)]
                                break
    EG = list(Set(EG))
    orbs = [list(x) for x in orbits]
    #print(orbs)
    if morphism:
        orbit_number = []
        for v in V:
            for O in orbs:
                if v in O:
                    orbit_number = orbit_number + [(v, orbs.index(O))]
        f0 = [x[1] for x in orbit_number]
    #print(orbit_number)
    A = [[quotient_adjacent(orbits, VG, EG, i, j) for i in VG] for j in VG]
    if verbose==True and morphism==False:
        return Graph(matrix(A), format = "adjacency_matrix"), VG, EG, orbs
    elif verbose==True and morphism==True:
        return Graph(matrix(A), format = "adjacency_matrix"), VG, EG, orbs, f0
    elif verbose==False and morphism==True:
        return Graph(matrix(A), format = "adjacency_matrix"), f0	
    else:
        return Graph(matrix(A), format = "adjacency_matrix")

def quotient_graph_morphism(Gamma, G):
    r"""
    This function returns the graph quotient morphism, 
                   f: Gamma -> Gamma/G,
    in CL format.

    If Gamma = (V, E) is a graph and G a subgroup of its 
    automorphism group acting faithfully on Gamma, we define 
    the quotient graph Gamma/G as follows:
    (1) The vertices of Gamma/G are the G-orbits in V. 
    (2) Distinct vertices v1, v2 of Gamma/G are connected by an 
        edge of Gamma/G if and only if there is 
          a vertex v1' in V belonging to the orbit 
             of v1, and 
          a vertex v2' in V belonging to the orbit 
             of v2 (note v1', v2' belong to different $G$-orbits,
             by hypothesis), 
         for which (v1', v2') belongs to E.
    Note: Gamma/G is simple.
    
    Input: Gamma - a graph in standard form,
           G     - a subgroup of its automorphism group
                   that acts faithfully on Gamma.
                   (for each non-trivial g in G, there is a v in V such that g(v)\not= v)
    Output: The quotient graph morphism.

    EXAMPLES:
        sage: Gamma2 = graphs.HouseGraph()  
        sage: G2 = Gamma2.automorphism_group(); G2; G2.cardinality() 
         Permutation Group with generators [(0,1)(2,3)]
         2
        sage: Gamma1 = quotient_graph(Gamma2, G2)  ## P3  
        sage: f21_0 = quotient_graph_morphism(Gamma2, G2); f21_0
         [0, 0, 1, 1, 2]                                                        
        sage: V2 = Gamma2.vertices(sort=True)  
        sage: f21 = [V2, f21_0] 
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f21, verbose=False) 
         True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f21, v) for v in V2] 
         [1, 1, 1, 1, 2]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f21, v) for v in V2]
         [1, 1, 1, 1, 0]
        sage: Gamma2 = graphs.ButterflyGraph()  
        sage: G2 = Gamma2.automorphism_group(); G2; G2.cardinality() 
         Permutation Group with generators [(1,2), (0,1)(2,3)]
         8
        sage: Gamma1 = quotient_graph(Gamma2, G2)     ## P3       
        sage: V2 = Gamma2.vertices(sort=True)   
        sage: f21_0 = quotient_graph_morphism(Gamma2, G2); f21_0   
         [0, 0, 0, 0, 1]
        sage: f21 = [V2, f21_0] 
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f21, verbose=False)
         True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f21, v) for v in V2] 
         [1, 1, 1, 1, 4]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f21, v) for v in V2] 
         [1, 1, 1, 1, 0]

    """
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(labels=None,sort=True)
    orbits = list(Set([Set([g(v) for g in G]) for v in V]))
    for g in G:
        if g.order()!=1:
            #print(g, [g(v)==v for v in V])
            if not(False in [g(v)==v for v in V]):
               print("Group", G, " is not faithful on Gamma.")
               return Gamma
    if len(orbits) == 1:
        return Graph(matrix([[0]]))
    n = len(orbits)
    orbs = [list(x) for x in orbits]
    orbit_number = []
    for v in V:
        for O in orbs:
            if v in O:
                orbit_number = orbit_number + [(v, orbs.index(O))]
    f0 = [x[1] for x in orbit_number]
    return f0

def zeta_polynomial_graph(Gamma):
    r"""
    Returns the zeta polynomial of the graph Gamma. The reciprocal is the
    Bass-Sunada-Ihara zeta function of Gamma. 


    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(5)
        sage: zeta_polynomial_graph(Gamma1)
        (x^4 + x^3 + x^2 + x + 1)^2*(x - 1)^2
        sage: Gamma = graphs.DorogovtsevGoltsevMendesGraph(2)
        sage: zeta_polynomial_graph(Gamma)
        -(3*x^4 + x^3 + 3*x^2 + x + 1)^2*(3*x^3 + x^2 + x - 1)*(x^2 - 1)^3*(x - 1)

    """
    x = var("x")
    A = Gamma.adjacency_matrix()
    r = len(Gamma.edges(sort=True)) - len(Gamma.vertices(sort=True))
    n = len(Gamma.vertices(sort=True))
    In = identity_matrix(n)
    Q = diagonal_matrix(Gamma.degree_sequence())-In
    return (1-x^2)^r*(In - A*x + Q*x^2).determinant().factor()

def star_subgraph(Gamma, v):
    r"""
    Returns the star subgraph of Gamma based at the vertex v.

    EXAMPLES:
        sage: Gamma = graphs.WheelGraph(4)
        sage: Gamma1 = star_subgraph(Gamma, 0)
        sage: Gamma1.vertices(sort=True)
        [0, 1, 2, 3]
        sage: Gamma1.edges(sort=True)
        [(0, 1, None), (0, 2, None), (0, 3, None)]

    """
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(sort=True)
    Vv = Gamma.neighbors(v)
    Ev = [e for e in E if v in e]
    #Ev = [(e[0],e[1]) for e in Ev]
    return Gamma.subgraph(edges = Ev)

def is_graph_homomorphism(Gamma1, Gamma2, f, verbose=False):
    r"""
    Returns True if f defines a graph-theoretic homomorphism
    from Gamma2 to Gamma 1(ie, vertices to vertices, 
    edges to edges), and False otherwise. 

    Gamma1, Gamma2 must be in standard form.

    Suppose Gamma2 has n vertices and m edges. A morphism 
    f: Gamma2 -> Gamma1
    can represented by 2 pairs of lists [VL2, VL1] and [EL2, EL1],
    where VL2 is the list of all n vertices of Gamma2,
    VL1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f, EL2 is the list of all m edges of Gamma2,
    EL1 is the list of length m of the edges
    in Gamma1 that form the corresponding image under
    the map f (including None). However, the pair [EL2, EL1]
    can be deduced from the pair [VL2, VL1], so we 
    drop [EL2, EL1].

    EXAMPLES:
        sage: Gamma2 = graphs.WheelGraph(5)
        sage: Gamma1 = graphs.WheelGraph(2)
        sage: f = [[0,1,2,3,4],[0,1,1,1,1]]
	sage: L = [vertical_multiplicity_of_graph_morphism(Gamma1, Gamma2, f, v2) for v2 in V2]; L
        [0, 2, 2]
        sage: is_graph_homomorphism(Gamma1, Gamma2, f)
        False
        sage: Gamma1 = graphs.CycleGraph(4)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f0 = [0,1,2,1]  
        sage: f = [V2, f0]
	sage: L = [vertical_multiplicity_of_graph_morphism(Gamma1, Gamma2, f, v2) for v2 in V2]; L
        [0, 0, 0]
        sage: is_graph_homomorphism(Gamma1, Gamma2, f) 
        True

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    ans = is_graph_morphism(Gamma1, Gamma2, f, verbose=False)
    if not(ans):
        print(" not a morphism \n")
        return ans
    L = [vertical_multiplicity_of_graph_morphism(Gamma1, Gamma2, f, v2) for v2 in V2]
    n2 = len(V2)
    if L==n2*[0]:
        return True
    else:
        return False
  

def is_graph_morphism(Gamma1, Gamma2, f, verbose=False):
    r"""
    Returns True if f defines a graph-theoretic mapping
    from Gamma2 to Gamma 1 (ie, vertices to vertices, 
    edges to edges or vertices), and False otherwise. 

    Gamma1, Gamma2 must be in standard form.

    Suppose Gamma2 has n vertices and m edges. A morphism 
    f: Gamma2 -> Gamma1
    can represented by 2 pairs of lists [VL2, VL1] and [EL2, EL1],
    where VL2 is the list of all n vertices of Gamma2,
    VL1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f, EL2 is the list of all m edges of Gamma2,
    EL1 is the list of length m of the edges
    in Gamma1 that form the corresponding image under
    the map f (including None). However, the pair [EL2, EL1]
    can be deduced from the pair [VL2, VL1], so we 
    drop [EL2, EL1].

    BUG: Changed (ans in ZZ) to (type(ans) is bool).
    
    EXAMPLES:
        sage: Gamma2 = graphs.WheelGraph(5)
        sage: Gamma1 = graphs.WheelGraph(2)
        sage: f = [[0,1,2,3,4],[0,1,1,1,1]]
        sage: is_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: Gamma1 = graphs.WheelGraph(5)
        sage: Gamma2 = graphs.WheelGraph(6)
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f0 = [0,1,2,3,4,4]  
        sage: f = [V2, f0]   
        sage: is_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: f0 = [0,1,4, 2,3,4] 
        sage: f = [V2, f0]   
        sage: is_graph_morphism(Gamma1, Gamma2, f, verbose=True) 
        Gamma1 = (V1, E1) =  [0, 1, 2, 3, 4]
          [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)]
        Gamma2 = (V2, E2) =  [0, 1, 2, 3, 4, 5]
          [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 5),
           (2, 3), (3, 4), (4, 5)]
        f = [V2, f0], where f0 =  [0, 1, 4, 2, 3, 4]
        The edge e =  (2, 3)  has no image in Gamma1 under f.
        False

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    E1 = list(Gamma1.edges(labels=None,sort=True))
    #EE1 = [(x[0],x[1]) for x in E1]
    E2 = list(Gamma2.edges(labels=None,sort=True))
    domainfV = f[0]
    imagefV = f[1]
    if verbose:
        print("Gamma1 = (V1, E1) = ", V1, E1)
        print("Gamma2 = (V2, E2) = ", V2, E2)
        print("f = [V2, f0], where f0 = ", f[1])
        for e in E2:
            ans = image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)
            #print(e, ans)	    
            if ans in ZZ:
                print("The edge e = ", e, " is vertical under f.")
                #return True
            elif ans == False:
                print("The edge e = ", e, " has no image in Gamma1 under f.")
                return False
    else:
        for e in E2:
            ans = image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)
            #print(e, ans)	    
            #if ans in ZZ:
            #    return ans
            if (type(ans) is bool) and ans == False:
                return False
    for i in domainfV:
        if not(i in V2):
            print( "Not a function on all of Gamma2")
            return False
    for i in imagefV:
        if not(i in V1):
            print( "Not a function whose image is in Gamma1")
            return False
    for e in E2:
        s = image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)
        if s in V1:
            return True
        if s == False:
            if verbose:
                print("The Gamma2 edge", e, " does not map to Gamma1 edge set ", E1, " or vertex set ", V1)
                print( "Error: Does not send edges to {edges} union {vertices}")
            return False
        x0 = s[0]
        x1 = s[1]
        if x0 != x1 and not((x0,x1) in E1) and not((x1,x0) in E1):
            if verbose:
                print("The Gamma2 edge", e, " does not map to Gamma1 edge set ", E1, " or vertex set ", V1)
                print( "Error: Does not send edges to {edges} union {vertices}")
            return False
    return True

def edge_image_list(Gamma1, Gamma2, f):
    r"""
    Returns a list of the images of the edges under 
    the graph morphism f:Gamma2->Gamma1 in color list notation.

    EXAMPLES:
        sage: Gamma2 = graphs.WheelGraph(5)
        sage: Gamma1 = graphs.WheelGraph(2)
        sage: f = [[0,1,2,3,4],[0,1,1,1,1]]
        sage: is_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: edge_image_list(Gamma1, Gamma2, f)
        [[(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)],
         [(0, 1), (0, 1), (0, 1), (0, 1), 'None', 'None', 'None', 'None']]

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    E1 = Gamma1.edges(sort=True)
    EE1 = [(x[0],x[1]) for x in E1]
    E2 = Gamma2.edges(sort=True)
    EE2 = [(x[0],x[1]) for x in E2]
    domainfV = f[0]
    imagefV = f[1]
    imageE2 = []
    for e in E2:
        x2 = e[0]
        y2 = e[1]
        i2 = V2.index(x2)
        j2 = V2.index(y2)
        i1 = imagefV[i2]
        j1 = imagefV[j2]
        if (i1,j1) in EE1 or (j1,i1) in EE1:
            imageE2.append((i1,j1))
        else:
            imageE2.append("None")
    return [EE2, imageE2]

def number_of_edges_set_in_a_walk(Gamma, W, verbose= False):
    r"""
    Gamma = (V,E) is a graph
    W is represented as a sequence of incident unlabeled, 
    "directed" edges in E
    returns the cardinality of the set of edges in a walk W,
    and False if W is not a walk in Gamma
    
    EXAMPLES:
        sage: V = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        sage: E = [(0,1),(0,2),(0,7),(0,8),(1,2),(1,3),(1,7),(2,3),(2,8), (3, 4), (3, 5), (4, 5), (4, 6), (4, 8), (5, 6), (5, 7), (6, 7), (6, 8)]
        sage: Gamma = Graph([V,E])
        sage: W = [(0,1), (1,7), (7,5), (5,7)]
        sage: number_of_edges_set_in_a_walk(Gamma, W)
        3
    """
    E = Gamma.edges(labels=None,sort=True)
    E_W = []
    if edge_set_is_a_walk(Gamma, W, verbose= False):
        for w in W:
            w1 = (w[1],w[0])
            if (w in W) or (w1 in W):
                wlist = list(w)
                wlist.sort()
                if not(wlist in E_W):
                    E_W.append(wlist)		
        return len(list(Set(E_W)))
    return False
    
def edge_set_is_a_walk(Gamma, W, verbose = False):
    r"""
    Gamma = (V,E) is a graph
    W is represented as a sequence of incident unlabeled, 
    "directed" edges in E
    returns True if W is a walk in Gamma and False otherwise
    
    EXAMPLES:
        sage: V2 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        sage: E2 = [(0,1),(0,2),(0,7),(0,8),(1,2),(1,3),(1,7),(2,3),(2,8), (3, 4), (3, 5), (4, 5), (4, 6), (4, 8), (5, 6), (5, 7), (6, 7), (6, 8)]
        sage: Gamma2 = Graph([V2,E2])
        sage: W = [(0,1), (1,7), (7,5), (5,0)] ## not a walk in Gamma2
        sage: edge_set_is_a_walk(Gamma2, W, verbose= True)
        Edge (5, 0) is not in the graph
        False
        sage: W = [(0,1), (1,7), (7,5)]
        sage: edge_set_is_a_walk(Gamma2, W, verbose= True)
        True
        sage: edge_set_is_a_walk(Gamma2, W, verbose= False)
        True
    """
    E = Gamma.edges(labels=None,sort=True)
    for w in W:
        w1 = (w[1],w[0])
        if not(w in E) and not(w1 in E):
            if verbose == True:
                print("Edge %s is not in the graph"%str(w))
            return False
    m = len(W)
    for i in range(m-1):
        x1 = W[i][0]
        y1 = W[i][1]
        x2 = W[i+1][0]
        y2 = W[i+1][1]
        if y1 != x2:
            if verbose == True:
                print("Edges %s[0] and %s[1] are not incident"%(str(W[i]).str(W[i+1])))
            return False
    return True

def image_of_walk_under_graph_morphism(Gamma1, Gamma2, f, W):
    """
    Gamma1, Gamma2 are graphs
    W is represented as a sequence of incident "directed" edges in E2
    f : Gamma2 -> Gamma1 is represented f = [V2,f(V2)]
    This function returns the walk in Gamma1 represented
    as a list of incident edges in E1 given by f(W).
    
    Returns False if W is not a walk.
    
    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(3)
        sage: V2 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        sage: E2 = [(0,1),(0,2),(0,7),(0,8),(1,2),(1,3),(1,7),(2,3),(2,8), (3, 4), (3, 5), (4, 5), (4, 6), (4, 8), (5, 6), (5, 7), (6, 7), (6, 8)]
        sage: Gamma2 = Graph([V2,E2])
        sage: f = [V2, [2, 1, 0, 2, 0, 1, 2, 0, 1]]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in Gamma2.vertices(sort=True)]
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in Gamma2.vertices(sort=True)]
        [2, 2, 2, 2, 2, 2, 2, 2, 2]
        sage: W = [(0,1), (1,7), (7,5)]
        sage: image_of_walk_under_graph_morphism(Gamma1, Gamma2, f, W)
        [(2, 1), (1, 0), (0, 1)]
        sage: W = [(0,1), (1,7), (7,5), (5,6), (6,8), (8,0)]
        sage: image_of_walk_under_graph_morphism(Gamma1, Gamma2, f, W)
        [(2, 1), (1, 0), (0, 1), (1, 2), (2, 1), (1, 2)]
        sage: W = [(0,1), (1,7), (7,5), (5,0)] ## not a walk in Gamma2
        sage: image_of_walk_under_graph_morphism(Gamma1, Gamma2, f, W)
        False
    
    """
    if not(edge_set_is_a_walk(Gamma2, W, verbose= False)):
        return False
    L = []
    for e in W:
        x = e[0]
        y = e[1]
        L.append(image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e))
    return L

def index_of_graph_morphism_edges(Gamma1, Gamma2, f, e0, s0, iota2, iota1):
    r"""
    These are the entries of the signed edge matrix, matrix_of_graph_morphism_edges,
    attached to the harmonic map f : Gamma2 -> Gamma1.

    Here s0 is an edge in Gamma1 (assumes s0[0]<s0[1]),
         e0 is an edge in Gamma2 (assumes e0[0]<e0[1]),
         iota1 is an orientation on Gamma1,
         iota2 is an orientation on Gamma2. 
    Recall an orientation iota on the edges E of Gamma is with
    respect to the standard orientation (all edges are represented
    e=(x,y) with x<y, in which case we have iota(e)=+1). An
    orientation is represented by a list of 1, -1's of length |E|).
    If an edge e=(x,y) has iota(e)=-1 then x>y (which can be
    represented as (y,x), if desired).
    If f does not send e0 to s0 then the index is 0.
    If f sends e0 to s0 and sends the head of e0 (wrt iota2)
    to the head of s0 (wrt iota1) then the index is +1.
    If f sends e0 to s0 and sends head to tail then the index is +1.

    For examples, see matrix_of_graph_morphism_edges.
    
    """
    E1 = list(Gamma1.edges(sort=True,labels=None))
    E2 = list(Gamma2.edges(sort=True,labels=None))
    u0 = e0[0]
    v0 = e0[1]
    x0 = s0[0]
    y0 = s0[1]
    x00 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, u0)
    y00 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v0)
    Ef = edge_image_list(Gamma1, Gamma2, f)
    if x00==x0 and y00==y0:
        j_e0 = E2.index(e0)
        j_s0 = E1.index(s0)
        #print("1", e0, j_e0, (x00, y00), s0, j_s0)
        iota_e0 = iota2[j_e0]
        iota_s0 = iota1[j_s0]
        return sign(iota_e0*iota_s0)
    if x00==y0 and y00==x0:
        j_e0 = E2.index(e0)
        j_s0 = E1.index(s0)
        #print("2", e0, j_e0, (x00, y00), s0, j_s0)
        iota_e0 = iota2[j_e0]
        iota_s0 = iota1[j_s0]
        return -sign(iota_e0*iota_s0)
    return 0

       
def index_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f, e2, e1):
    r"""
    These are the entries of the signed edge matrix attached to the 
    harmonic map f : Gamma2 -> Gamma1.

    Here e1 is an edge in Gamma1 and e2 is an edge in Gamma2.

    This function helps answer a very specific question:

           “Does this edge e2 in the big graph Gamma2 get mapped to this 
            edge e1 in the smaller graph Gamma1 under the function f?”

    It returns:
      --  1 if yes (it matches — in either direction),
      --  0 if no,
    and raises an error if e2 isn't an edge in the domain of the morphism.

    Called the unsigned edge incidence — it doesn't care about direction, just whether the edge gets mapped or not.

    """
    Ef = edge_image_list(Gamma1, Gamma2, f)
    V1 = Gamma1.vertices(sort=True)
    E1 = Gamma1.edges(sort=True)
    EE1 = [(x[0],x[1]) for x in E1]
    i_e1 = V1.index(e1[0])
    j_e1 = EE1.index(e1)
    if e2 in Ef[0]:
        i = Ef[0].index(e2)
    else:
        i = Ef[0].index((e2[1],e2[0]))
    if not(e2 in Ef[0]):
        raise ValueError("argument is not an edge of the graph")
    if (e1[0],e1[1]) == Ef[1][i]:
        return 1
    elif (e1[1],e1[0]) == Ef[1][i]:
        return 1
    else:
        return 0

def index_of_graph_morphism_vertices(Gamma1, Gamma2, f, v2, v1):
    i =f[0].index(v2)
    if v1 == f[1][i]:
        return 1
    else:
        return 0

def graph_morphism_vertices_matrix(Gamma1, Gamma2, f):
    return matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)

def matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f, verbose = False):
    r"""
    Returns an n2 x n1 (0,1)-matrix representing Phi_V 
    if f defines a graph-theoretic morphism
    from Gamma2 to Gamma 1 (ie, vertices to vertices, 
    edges to edges), and False otherwise. 

    Suppose Gamma2 has n vertices and m edges. A morphism 
    f: Gamma2 -> Gamma1
    can represented by 2 pairs of lists [VL2, VL1] and [EL2, EL1],
    where VL2 is the list of all n vertices of Gamma2,
    VL1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f, EL2 is the list of all m edges of Gamma2,
    EL1 is the list of length m of the edges
    in Gamma1 that form the corresponding image under
    the map f (including None). However, the pair [EL2, EL1]
    can be deduced from the pair [VL2, VL1].

    EXAMPLES:
        sage: Gamma2 = graphs.CubeGraph(2)
        sage: Gamma1 = Gamma2.subgraph(vertices = ['00', '01'], edges = [('00', '01')])
        sage: f = [['00', '01', '10', '11'], ['00', '01', '00', '01']]
        sage: is_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f); Phi
        [1 0 1 0]
        [0 1 0 1]
        sage: Phi.transpose()*Phi
        [1 0 1 0]
        [0 1 0 1]
        [1 0 1 0]
        [0 1 0 1]
        sage: Phi*Phi.transpose()
        [2 0]
        [0 2]
        sage: Gamma2 = graphs.CubeGraph(3)
        sage: Gamma1 = graphs.TetrahedralGraph()
        sage: f = [['000', '001', '010', '011', '100', '101', '110', '111'], [0, 1, 2, 3, 3, 2, 1, 0]]
        sage: Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f); Phi
        [1 0 0 0 0 0 0 1]
        [0 1 0 0 0 0 1 0]
        [0 0 1 0 0 1 0 0]
        [0 0 0 1 1 0 0 0]
        sage: D = vector([-1,0,1,2,2,1,0,-1])
        sage: Phi*D
        (-2, 0, 2, 4)
        sage: Phi*Phi.transpose()
        [2 0 0 0]
        [0 2 0 0]
        [0 0 2 0]
        [0 0 0 2]
        sage: Phi.transpose()*Phi
        [1 0 0 0 0 0 0 1]
        [0 1 0 0 0 0 1 0]
        [0 0 1 0 0 1 0 0]
        [0 0 0 1 1 0 0 0]
        [0 0 0 1 1 0 0 0]
        [0 0 1 0 0 1 0 0]
        [0 1 0 0 0 0 1 0]
        [1 0 0 0 0 0 0 1]
        sage: Gamma2 = graphs.WheelGraph(5)
        sage: Gamma1 = graphs.WheelGraph(2)
        sage: f = [[0,1,2,3,4],[0,1,1,1,1]]
        sage: Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f); Phi
        [1 0 0 0 0]
        [0 1 1 1 1]
        sage: Phi.transpose()*Phi
        [1 0 0 0 0]
        [0 1 1 1 1]
        [0 1 1 1 1]
        [0 1 1 1 1]
        [0 1 1 1 1]
        sage: Phi*Phi.transpose()
        [1 0]
        [0 4]
        sage: Q1 = Gamma1.laplacian_matrix()
        sage: Q2 = Gamma2.laplacian_matrix()
        sage: Q1*Phi
        [ 1 -1 -1 -1 -1]
        [-1  1  1  1  1]
        sage: Phi*Q2
        [ 4 -1 -1 -1 -1]
        [-4  1  1  1  1]
        sage: Gamma3 = graphs.CycleGraph(4)
        sage: Gamma3.add_edge([0,2])
        sage: f2 = [[0,1,2,3,4],[0,2,1,2,3]]
        sage: Phi2 = matrix_of_graph_morphism_vertices(Gamma3, Gamma2, f2); Phi2
        [1 0 0 0 0]
        [0 0 1 0 0]
        [0 1 0 1 0]
        [0 0 0 0 1]
        sage: Phi2.transpose()*Phi2
        [1 0 0 0 0]
        [0 1 0 1 0]
        [0 0 1 0 0]
        [0 1 0 1 0]
        [0 0 0 0 1]
        sage: Phi2*Phi2.transpose()
        [1 0 0 0]
        [0 1 0 0]
        [0 0 2 0]
        [0 0 0 1]
        sage: v = Q3.right_eigenspaces()[0][1].basis()[0]; v
        (0, 1, 0, -1)
        sage: Q3*v ## Does Phi2 send eigenspaces to eigenspaces?
        (0, 2, 0, -2)
        sage: Phi2.transpose()*Phi2*Q2*Phi2.transpose()*v
        (0, 0, 3, 0, -3)
        sage: w = Q3.right_eigenspaces()[2][1].basis()[0]; w
        (1, 0, -1, 0)
        sage: Q3*w # A: No.
        (4, 0, -4, 0)
        sage: Phi2.transpose()*Phi2*Q2*Phi2.transpose()*w
        (6, -8, 1, -8, 1)

    """
    if verbose and not(is_graph_morphism(Gamma1, Gamma2, f)):
         print("The map given is not a graph morphism")
    if verbose and is_graph_morphism(Gamma1, Gamma2, f):
         print("The map given is a graph morphism")
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    MS = MatrixSpace(ZZ, n1, n2)
    L = [[index_of_graph_morphism_vertices(Gamma1, Gamma2, f, v2, v1) for v2 in V2] for v1 in V1]
    return MS(L).transpose()

def matrix_of_graph_morphism_edges(Gamma1, Gamma2, f, iota2, iota1):
    return graph_morphism_edges_matrix(Gamma1, Gamma2, f, iota2, iota1)
    
def graph_morphism_edges_matrix(Gamma1, Gamma2, f, iota2, iota1):
    r"""
    Returns an m2 x m1 (0,1, -1)-matrix representing Phi_E 
    if f defines a graph-theoretic mapping
    from Gamma2 to Gamma 1 (ie, vertices to vertices, 
    edges to edges), and False otherwise. 

    Here iota1 is an orientation on Gamma1,
         iota2 is an orientation on Gamma2. 

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)
        sage: Gamma2 = graphs.HouseGraph()
        sage: V2 = Gamma2.vertices()
        sage: f0 = [0, 0, 1, 1, 2]
        sage: f = [V2, f0]
        sage: Phi_E_signed = matrix_of_graph_morphism_edges(Gamma1, Gamma2, f, iota2=[1]*6, iota1=[1,-1]); Phi_E_signed
	[ 0  0]
	[ 1  0]
	[ 1  0]
	[ 0  0]
	[ 0 -1]
	[ 0 -1]
        sage: Gamma2 = graphs.CycleGraph(4)
        sage: Gamma1 = graphs.PathGraph(2)
        sage: V2 = Gamma2.vertices()
        sage: f0 = [0, 1, 1, 0]
        sage: f = [V2, f0]
        sage: PhiE = matrix_of_graph_morphism_edges(Gamma1, Gamma2, f, iota2=[1]*4, iota1=[1]); PhiE
        [1]
        [0]
        [0]
        [-1]
        sage: PhiE.transpose()*PhiE
        [2]

        sage: Gamma2 = graph_convert_to_standard(graphs.PaleyGraph(9))
        sage: Gamma1 = graphs.CycleGraph(3)
        sage: E1 = Gamma1.edges(labels=None)
        sage: E2 = Gamma2.edges(labels=None)
        sage: V2 = Gamma2.vertices(sort=True)
        sage: iota2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        sage: iota1 = [1,1,1]
        sage: B1 = incidence_matrix(Gamma1, [E1,iota1])
        sage: B2 = incidence_matrix(Gamma2, [E2,iota2])
        sage: f = [V2, [0,0,0,2,2,2,1,1,1]]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: PhiV = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)
        sage: PhiE = matrix_of_graph_morphism_edges(Gamma1, Gamma2, f, iota2, iota1)
        sage: PhiE*B1.transpose() == B2.transpose()*PhiV   
        True

    """
    if not(is_graph_morphism(Gamma1, Gamma2, f)):
         raise ValueError("the map given is not a graph morphism")
    E1 = Gamma1.edges(sort=True)
    E2 = Gamma2.edges(sort=True)
    EE1 = [(x[0],x[1]) for x in E1]
    EE2 = [(x[0],x[1]) for x in E2]
    m1 = len(E1)
    m2 = len(E2)
    MS = MatrixSpace(ZZ, m1, m2)
    L = [[index_of_graph_morphism_edges(Gamma1, Gamma2, f, e2, e1, iota2, iota1) for e2 in EE2] for e1 in EE1]
    return MS(L).transpose()

def matrix_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f):
    return graph_morphism_edges_matrix_unsigned(Gamma1, Gamma2, f)
    
def graph_morphism_edges_matrix_unsigned(Gamma1, Gamma2, f):
    r"""
    Returns an m2 x m1 (0,1)-matrix representing Phi_E 
    if f defines a graph-theoretic mapping
    from Gamma2 to Gamma 1 (ie, vertices to vertices, 
    edges to edges), and False otherwise. 

    Here e0 is an orientation on Gamma1. 

    EXAMPLES:
        sage: Gamma3 = graphs.CycleGraph(4)
        sage: Gamma2 = graphs.WheelGraph(5)
        sage: Gamma3.add_edge([0,2])
        sage: f2 = [[0,1,2,3,4],[0,2,1,2,3]]
        sage: PhiE2 = matrix_of_graph_morphism_edges_unsigned(Gamma3, Gamma2, f2); PhiE2.transpose()
        [ 0  1  0  0  0  0  0  0]
        [ 1  0  1  0  0  0  0  0]
        [ 0  0  0  1  0  0  0  0]
        [ 0  0  0  0  1  0  1  0]
        [ 0  0  0  0  0  1  0  1]

    """
    if not(is_graph_morphism(Gamma1, Gamma2, f)):
         raise ValueError("the map given is not a graph morphism")
    E1 = Gamma1.edges(sort=True)
    E2 = Gamma2.edges(sort=True)
    EE1 = [(x[0],x[1]) for x in E1]
    EE2 = [(x[0],x[1]) for x in E2]
    m1 = len(E1)
    m2 = len(E2)
    MS = MatrixSpace(ZZ, m1, m2)
    L = [[index_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f, e2, e1) for e2 in EE2] for e1 in EE1]
    return MS(L).transpose()


def preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v):
    r"""
    Returns the (vertex) preimage(s) of v under f:Gamma2 -> Gamma 1,
    where v is an vertex in Gamma1.

    A morphism  f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    EXAMPLES:
        sage: Gamma2 = graphs.CubeGraph(2)
        sage: Gamma1 = Gamma2.subgraph(vertices = ['00', '01'], edges = [('00', '01')])
        sage: f = [['00', '01', '10', '11'], ['00', '01', '00', '01']]
        sage: Gamma1.vertices(sort=True)
        [('00', '01', None)]
        sage: v = Gamma1.vertices(sort=True)[0]
        sage: preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v)
        ['00', '10']

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    domainf = f[0]
    imagef = f[1]
    indices = [i for i in range(len(V2)) if imagef[i]==v]
    return [V2[i] for i in indices]

def preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e, labels=None):
    r"""
    Returns the preimage(s) of e under f:Gamma2 -> Gamma1,
    where e is an edge in Gamma1. It is returned as a list,
    with the default being that the edges are unlabled.

    A morphism  f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    EXAMPLES:
        sage: Gamma2 = graphs.CubeGraph(2)
        sage: Gamma1 = Gamma2.subgraph(vertices = ['00', '01'], edges = [('00', '01')])
        sage: f = [['00', '01', '10', '11'], ['00', '01', '00', '01']]
        sage: Gamma2 = graphs.CubeGraph(2)
        sage: Gamma1.edges(sort=True)
        [('00', '01', None)]
        sage: e = Gamma1.edges(sort=True)[0]
        sage: preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e, labels = True)
        [('00', '01', None), ('10', '11', None)]
        sage: Gamma2 = graphs.CubeGraph(3)
        sage: Gamma1 = graphs.TetrahedralGraph()
        sage: f = [['000', '001', '010', '011', '100', '101', '110', '111'], [0, 1, 2, 3, 3, 2, 1, 0]]
        sage: e = Gamma1.edges(sort=True)[1]; e
        (0, 2, None)
        sage: preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e, labels = True)
        [('000', '010', None), ('101', '111', None)]
        sage: preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)   
         [('000', '010'), ('101', '111')]
        sage: preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e, labels = None) 
         [('000', '010'), ('101', '111')]
        sage: Gamma3 = graphs.PathGraph(2)             
        sage: Gamma4 = graphs.CycleGraph(4)             
        sage: V4 = Gamma4.vertices(sort=True)                   
        sage: g0 = [0,1,1,0]                            
        sage: g = [V4, g0]                             
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g) 
        True
        sage: image_of_edge_under_graph_morphism(Gamma3, Gamma4, g, (0,3))
        0
        sage: image_of_edge_under_graph_morphism(Gamma3, Gamma4, g, (0,1))
        (0, 1)

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    if labels == None:
        E1 = Gamma1.edges(labels = None, sort = True)
        E2 = Gamma2.edges(labels = None, sort = True)
    else:
        E1 = Gamma1.edges(sort=True)
        E2 = Gamma2.edges(sort=True)
    domainf = f[0]
    imagef = f[1]
    imagef_e = []
    vs = preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, e[0])
    ws = preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, e[1])
    edges = []
    for x in vs:
        for y in ws:
            for e in E2:
                if (x,y) == (e[0],e[1]) or (x,y) == (e[1],e[0]):
                    edges.append(e)
    return edges

def preimage_of_edges_under_graph_morphism(Gamma1, Gamma2, f, S):
    r"""
    Returns the preimage of S under f:Gamma2 -> Gamma 1,
    where S is a list of edges in Gamma1. It is returned as a list,
    without repetition.

    A morphism  f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    EXAMPLES:
        sage: Gamma2 = graphs.CubeGraph(3)
        sage: V2 = Gamma2.vertices(sort=True); V2  
        ['000', '001', '010', '011', '100', '101', '110', '111']
        sage: E2 = Gamma2.edges(labels=None,sort=True); E2 
        [('000', '001'), ('000', '010'), ('000', '100'), ('001', '011'),
         ('001', '101'), ('010', '011'), ('010', '110'), ('011', '111'),
         ('100', '101'), ('100', '110'), ('101', '111'), ('110', '111')]
        sage: Gamma1 = graphs.TetrahedralGraph() 
        sage: E1 = Gamma1.edges(labels=None,sort=True); E1       
        [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        sage: f  = [['000', '001', '010', '011', '100', '101', '110', '111'], [0, 1, 2, 3, 3, 2, 1, 0]] 
        sage: S = [(0, 2), (0, 3), (1, 2), (1, 3)]         
        sage: preimage_of_edges_under_graph_morphism(Gamma1, Gamma2, f, S) 
        [('100', '110'),
         ('000', '010'),
         ('001', '101'),
         ('011', '111'),
         ('101', '111'),
         ('010', '110'),
         ('001', '011'),
         ('000', '100')]
    """
    L = []
    for e in S:
        L = L+preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e, labels=None)
    return list(Set(L))


def graph_preimage_of_edges_under_graph_morphism(Gamma1, Gamma2, f, S):
    r"""
    Returns the preimage of S under f:Gamma2 -> Gamma 1,
    where S is a list of edges in Gamma1. 
    It is returned as a subgraph of Gamma2.

    EXAMPLES:
        sage: Gamma2 = graphs.CubeGraph(3)
        sage: V2 = Gamma2.vertices(sort=True); V2  
        ['000', '001', '010', '011', '100', '101', '110', '111']
        sage: E2 = Gamma2.edges(labels=None,sort=True); E2 
        [('000', '001'), ('000', '010'), ('000', '100'), ('001', '011'),
         ('001', '101'), ('010', '011'), ('010', '110'), ('011', '111'),
         ('100', '101'), ('100', '110'), ('101', '111'), ('110', '111')]
        sage: Gamma1 = graphs.TetrahedralGraph() 
        sage: E1 = Gamma1.edges(labels=None,sort=True); E1       
        [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        sage: f  = [['000', '001', '010', '011', '100', '101', '110', '111'], [0, 1, 2, 3, 3, 2, 1, 0]] 
        sage: S = [(0, 2), (0, 3), (1, 2), (1, 3)]       
        sage: graph_preimage_of_edges_under_graph_morphism(Gamma1, Gamma2, f, S) 
         Subgraph of (3-Cube): Graph on 8 vertices

    """
    E2_S = preimage_of_edges_under_graph_morphism(Gamma1, Gamma2, f, S)
    return Gamma2.subgraph(edges = E2_S)


def image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e, verbose=False):
    r"""
    Returns the image of e under f:Gamma2 -> Gamma 1,
    where e is an edge in Gamma2.

    A morphism  f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    EXAMPLES:
        sage: Gamma2 = graphs.CubeGraph(2)
        sage: Gamma1 = Gamma2.subgraph(vertices = ['00', '01'], edges = [('00', '01')])
        sage: f = [['00', '01', '10', '11'], ['00', '01', '00', '01']]
        sage: Gamma2 = graphs.CubeGraph(2)
        sage: Gamma1.edges(sort=True)
        [('00', '01', None)]
        sage: e = Gamma1.edges(sort=True)[0]; e
        ('00', '01', None)
        sage: image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)
        ('00', '01', None)
        sage: e = Gamma2.edges(sort=True)[1]; e
        ('00', '10', None)
        sage: image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e)
        ('00', '00')

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    E1 = Gamma1.edges(labels=None,sort=True)
    E2 = Gamma2.edges(labels=None,sort=True)
    v0 = e[0]
    v1 = e[1]
    x0 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v0)
    x1 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v1)
    #print(x0,x1,V1[x0],V1[x1],E1)
    if x0==x1:
        return x0
    if (V1[x0],V1[x1]) in E1:
        return (V1[x0],V1[x1])
    elif (V1[x1],V1[x0]) in E1:
        return (V1[x1],V1[x0])
    else:
        if verbose:
            print("This edge e = ", e, " has no image in Gamma1 under f.")
            return False   
        else:
            return False
	    
def image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v):
    r"""
    Returns the image of v under f:Gamma2 -> Gamma 1,
    where v is an vertex in Gamma2.

    A morphism  f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    EXAMPLES:
        sage: Gamma2 = graphs.CubeGraph(2)
        sage: Gamma1 = Gamma2.subgraph(vertices = ['00', '01'], edges = [('00', '01')])
        sage: f = [['00', '01', '10', '11'], ['00', '01', '00', '01']]
        sage: v = Gamma2.vertices(sort=True)[0]
        sage: image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v)
        '00'

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    domainf = f[0]
    imagef = f[1]
    i = V2.index(v)
    j = imagef[i]
    return j

def local_horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2, e):
    r"""
    Returns mu_{phi}(v2, e)
     = \mu_{\phi}(v,e) = \sum_{u\in N_{\Gamma_2}(v), \phi(u)=y} 1,
    if e=(\phi(u), \phi(v)) 

    Gamma1 is a graph in standard form and so is Gamma2.

    f : defines a graph-theoretic mapping
     from Gamma2 to Gamma1 represented by a pair of lists [L1, L2],
     where L1 is the list of all n2 vertices of Gamma2,
     and L2 is the list of length n2 of the vertices in Gamma1: L2 forms 
     the corresponding image of L1 under the map f)
    v2 : a vertex of Gamma2
    e : an edge of Gamma1 incident to phi(v2)

    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (0, 2), (0, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: V1 = [0,1,2]
        sage: E1 = [(0, 1), (1, 2), (0, 2)]
        sage: Gamma1 = Graph([V1, E1])
        sage: f = [[0,1,2,3], [0, 1, 2, 0]]
        sage: e = (1, 2)
        sage: [local_horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v, e) for v in V2]
         [0, 1, 1, 0]

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    Nbh2 = Gamma2.neighbors(v2)
    total = 0
    for u in Nbh2:
        x = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, u)
        y = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v2)
        if e==(x,y) or e==(y,x):
            total = total + 1
    return total

def weighted_local_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2, e):
    r"""
    Returns mu_{wt1, wt2, phi}(v2, e)
     = \mu_{w,\phi}(v,e) = \sum_{u\in N_{\Gamma_2}(v), \phi(u)=y} w_2(u,v),
    if e=(\phi(u), \phi(v)), divided by the wt1(e) (wt1 the edge weights of woGamma1).

    For the sum, first fix a vertex v2 on Gamma2 and an edge s of Gamma1. If
    s is not incident to phi(v) then discard it and pick a new one that is.
    Now let Nb_{v2, s} denote the set of neighbors u of v2 in Gamma2 such that
    (1) phi(v2) != phi(u), 
    (2) s = (phi(u), phi(v2)).
    The sum in  mu_{wt1, wt2, phi}(v2, e) runs over all such neighbors u. It may seem
    that (u,v2) runs over the preimages of e, but really (u,v2) only runs over those
    preimages that are incident to v2 (which has been fixed once and for all).

    woGamma1 is a triple: [Gamma1 = (V1, E1), epsilon1, wt1], where 
     epsilon1 is a pair [E1,e1], where e1 is a list of length |E1| of edge orientations,
     wt1 is a pair [E1,w1], where w1 is a list of length |E1| of edge weights > 0.
    woGamma2 is similar.
    f : defines a graph-theoretic mapping
     from Gamma2 to Gamma1 represented by a pair of lists [L1, L2],
     where L1 is the list of all n2 vertices of Gamma2,
     and L2 is the list of length n2 of the vertices in Gamma1: L2 forms 
     the corresponding image of L1 under the map f)
    v2 : a vertex of Gamma2
    e : an edge of Gamma1 incident to phi(v2)

    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (0, 2), (0, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: eps2 = [1,1,1,1]
        sage: wt2 = [E2, [1/2, 2/3, 3/5, 4/3]]
        sage: woGamma2 = [Gamma2, eps2, wt2]
        sage: V1 = [0,1,2]
        sage: E1 = [(0, 1), (1, 2), (0, 2)]
        sage: Gamma1 = Graph([V1, E1])
        sage: eps1 = [1,1,1]
        sage: wt1 = [E1, [1/2, 2/3, 3/5]]
        sage: woGamma1 = [Gamma1, eps1, wt1]
        sage: f = [[0,1,2,3], [0, 1, 2, 0]]
        sage: e = (1, 2)
        sage: [weighted_local_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v, e) for v in V2]
         [0, 1, 1, 0]

    """
    Gamma1 = woGamma1[0]
    eps1 = woGamma1[1]
    wt1 = woGamma1[2]
    Gamma2 = woGamma2[0]
    eps2 = woGamma2[1]
    wt2 = woGamma2[2]
    V1 = Gamma1.vertices(sort=True)
    E1 = Gamma1.edges(labels=None,sort=True)
    V2 = Gamma2.vertices(sort=True)
    Nbh2 = Gamma2.neighbors(v2)
    #print(f, w2, v2, Nbh2)
    wts = []
    for u in Nbh2:
        x = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, u)
        y = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v2)
        if (e in E1) and (e==(x,y) or e==(y,x)):
            wts.append(weight_at_edge(Gamma2, wt2, (u,v2))/weight_at_edge(Gamma1, wt1, e)) ################ doesn't seem to work at all !!!
        #print(u, x, y, weight_at_edge(Gamma2, wt2, (u,v2)), weight_at_edge(Gamma1, wt1, e), wts, (e in E1), e==(x,y) or e==(y,x))
    return sum(wts)

def weighted_vertical_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2):
    r"""
    returns the weighted vertical multiplicity of f at v2

    woGamma1 is a triple: [Gamma1 = (V1, E1), epsilon1, wt1], where 
     epsilon1 is a pair [E1,e1], where e1 is a list of length |E1| of edge orientations,
     wt1 is a pair [E1,w1], where w1 is a list of length |E1| of edge weights > 0.
    woGamma2 is similar.
    f : defines a graph-theoretic mapping
     from Gamma2 to Gamma1 represented by a pair of lists [L1, L2],
     where L1 is the list of all n2 vertices of Gamma2,
     and L2 is the list of length n2 of the vertices in Gamm
    v2 : a vertex of Gamma2.
    If f is not harmonic, this function works anyway.

    Returns nu_phi(v1)

    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (0, 2), (0, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: eps2 = [1,1,1,1]
        sage: wt2 = [E2, [1/2, 2/3, 3/5, 4/3]]
        sage: woGamma2 = [Gamma2, eps2, wt2]
        sage: V1 = [0,1,2]
        sage: E1 = [(0, 1), (1, 2), (0, 2)]
        sage: Gamma1 = Graph([V1, E1])
        sage: eps1 = [1,1,1]
        sage: wt1 = [E1, [1/2, 2/3, 3/5]]
        sage: woGamma1 = [Gamma1, eps1, wt1]
        sage: f = [[0,1,2,3], [0, 1, 2, 0]]
        sage: weighted_vertical_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 0)
         4/3

    """
    Gamma1 = woGamma1[0]
    Gamma2 = woGamma2[0]
    V2 = Gamma2.vertices(sort=True)
    Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)
    wt2 = woGamma2[2]
    #print(wt2)
    E2 = wt2[0]
    w2 = wt2[1]
    #print(w2)
    E2w = [(E2[i][0], E2[i][1],w2[i]) for i in range(len(E2))]
    Gamma2w = Graph([V2,E2w], weighted=True)
    A2w = Gamma2w.weighted_adjacency_matrix()
    #print(A2,"\n\n",Phi,"\n\n",A2*Phi)
    #print([[i,f[1][i]] for i in V2])
    nus = [(A2w*Phi)[i,f[1][i]] for i in V2]
    return nus[v2]

def weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2, verbose=False):
    """
    Returns the pair (True, mu_{wt2, phi}(v2)) if  mu_{wt2, phi}(v2, e)
    is independent of e incident to phi(v2), and the pair
    (False, [mu_{wt2, phi}(v2, e) for e incident to phi(v2)])
    otherwise.

    woGamma1 is a triple: [Gamma1 = (V1, E1), epsilon1, wt1], where 
     epsilon1 is a pair [E1,e1], where e1 is a list of length |E1| of edge orientations,
     wt1 is a pair [E1,w1], where w1 is a list of length |E1| of edge weights > 0.
    woGamma2 is similar.
    f : defines a graph-theoretic mapping
     from Gamma2 to Gamma1 represented by a pair of lists [L1, L2],
     where L1 is the list of all n2 vertices of Gamma2,
     and L2 is the list of length n2 of the vertices in Gamma1: L2 forms 
     the corresponding image of L1 under the map f)
    v2 : a vertex of Gamma2
    e : an edge of Gamma1 incident to phi(v2)

    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (0, 2), (0, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: eps2 = [1,1,1,1]
        sage: wt2 = [E2, [1/2, 2/3, 3/5, 4/3]]
        sage: woGamma2 = [Gamma2, eps2, wt2]
        sage: V1 = [0,1,2]
        sage: E1 = [(0, 1), (1, 2), (0, 2)]
        sage: Gamma1 = Graph([V1, E1])
        sage: eps1 = [1,1,1]
        sage: wt1 = [E1, [1/2, 2/3, 3/5]]
        sage: woGamma1 = [Gamma1, eps1, wt1]
        sage: f = [[0,1,2,3], [0, 1, 2, 0]]
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 0)
         (True, 1)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 1)
         (True, 1)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 2)
         (True, 1)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 3)
         (True, 0)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 0, verbose=True)
         The image of  0  under phi is  0 .   The (mu(phi, v, s), v, s), s incident to phi(v):   [(1, 0, (0, 1)), (1, 0, (0, 2))] .
         (True, 1)

    """
    Gamma1 = woGamma1[0]
    eps1 = woGamma1[1]
    wt1 = woGamma1[2]
    Gamma2 = woGamma2[0]
    eps2 = woGamma2[1]
    wt2 = woGamma2[2]
    E2 = wt2[0]
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    x = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v2)
    Nbh1 = Gamma1.neighbors(x)
    L = [weighted_local_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2, (x,y)) for y in Nbh1]
    if verbose:
        L_plus = [(weighted_local_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v2, (x,y)), v2, (x,y)) for y in Nbh1]
        print("The image of ",v2," under phi is ", x, ".   The (mu(phi, v, s), v, s), s incident to phi(v): ", L_plus,".")
    if len(list(Set(L)))==1:
        return (True, L[0])
    else:
        return (False, L)    

def is_weighted_harmonic_graph_morphism(woGamma1, woGamma2, f, verbose = False):
    """
    Returns true if f defines a weighted graph-theoretic mapping
    with a "constant" local horizontal multiplicity and False otherwise. 

    If verbose=True then more information will be printed out when the
    map f is not a harmonic morphism.

    woGamma1 is a triple: [Gamma1 = (V1, E1), epsilon1, wt1], where 
     epsilon1 is a pair [E1,e1], where e1 is a list of length |E1| of edge orientations,
     wt1 is a pair [E1,w1], where w1 is a list of length |E1| of edge weights >0.
    woGamma2 is similar.

    Recall, f is given as a map from an edge-weighted, oriented graph Gamma2 to 
    an edge-weighted, oriented graph Gamma1.
    Suppose Gamma2 has n vertices. A morphism 
              f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2=V2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    Slightly different output format than
      is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose = False)


    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (0, 2), (0, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: eps2 = [E2,[1,1,1,1]]
        sage: wt2 = [E2, [1/2, 2/3, 3/5, 4/3]]
        sage: woGamma2 = [Gamma2, eps2, wt2]
        sage: V1 = [0,1,2]
        sage: E1 = [(0, 1), (1, 2), (0, 2)]
        sage: Gamma1 = Graph([V1, E1])
        sage: eps1 = [E1, [1,1,1]]
        sage: wt1 = [E1, [1/2, 2/3, 3/5]]
        sage: woGamma1 = [Gamma1, eps1, wt1]
        sage: f = [[0,1,2,3], [0, 1, 2, 0]]       
        sage: is_weighted_harmonic_graph_morphism(woGamma1, woGamma2, f, verbose = False)
         False
        sage: is_weighted_harmonic_graph_morphism(woGamma1, woGamma2, f, verbose = True)
         morphism phi has a non-constant local horizontal mult at 1
         False

    
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: eps2 = [E2, [1,1,1,1,1]]
        sage: wt2 = [E2, [1/2, 2/3, 1/2, 1/3, 2/3]]       
        sage: woGamma2 = [Gamma2, eps2, wt2]
        sage: V1 = [0,1,2]
        sage: E1 = [(0, 1), (1, 2)]
        sage: Gamma1 = Graph([V1,E1])
        sage: eps1 = [E1, [1,1]]
        sage: wt1 = [E1, [1/2, 1/3]]     
        sage: woGamma1 = [Gamma1, eps1, wt1]
        sage: f = [[0,1,2,3], [1, 0, 1, 2]]       
        sage: is_weighted_harmonic_graph_morphism(woGamma1, woGamma2, f, verbose = True)
          morphism phi has a non-constant local horizontal mult at 0
          False
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 0)
         (False, [1, 3/2])
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 1)
         (True, 5/3)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 2)
         (False, [2/3, 2])
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 3)
         (True, 7/2)

        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: eps2 = [E2, [1,1,1,1,1]]
        sage: wt2 = [E2, [1/2, 2/3, 1/2, 1/3, 1/3]]  ## slightly different than above
        sage: woGamma2 = [Gamma2, eps2, wt2]
        sage: V1 = [0,1,2]
        sage: E1 = [(0, 1), (1, 2)]
        sage: Gamma1 = Graph([V1,E1])
        sage: eps1 = [E1, [1,1]]
        sage: wt1 = [E1, [1/3, 1/3]]     ## slightly different than above
        sage: woGamma1 = [Gamma1, eps1, wt1]
        sage: f = [[0,1,2,3], [1, 0, 1, 2]]       
        sage: is_weighted_harmonic_graph_morphism(woGamma1, woGamma2, f, verbose = False)
         True
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 0)   
         (True, 3/2)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 1)   
         (True, 5/2)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 2)    
         (True, 1)
        sage: weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, 3)  
         (True, 5/2)

    """
    Gamma1 = woGamma1[0]
    eps1 = woGamma1[1][1]
    wtt1 = woGamma1[2]
    wt1 = wtt1[1]
    E1 = wtt1[0]
    Gamma2 = woGamma2[0]
    eps2 = woGamma2[1][1]
    wtt2 = woGamma2[2]
    wt2 = wtt2[1]
    E2 = wtt2[0]    
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    V2 = Gamma2.vertices(sort=True)
    n2 = len(V2)
    m1 = len(E1)
    m2 = len(E2)
    whm = [weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v)[0] for v in V2]
    edges_in_common = []
    for e in E2:
        v1 = e[0]
        v2 = e[1]
        w1 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v1)
        w2 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v2)
        if w1 != w2 and not((w1,w2) in E1) and not((w2,w1) in E1):
           if verbose:
               print( "This function is not a graph morphism: (",v1,",",v2,") -> (",w1,",",w2,")")
           return False
    for v in V2:
        if not(weighted_horizontal_multiplicity_of_harmonic_map(woGamma1, woGamma2, f, v)[0]):
            if not(verbose):
                return False
            else:
                #print(" Input: woGamma1, woGamma2, f, v >>>> \n", woGamma1,"\n", woGamma2,"\n", f,"\n", v)
                print(" morphism phi has a non-constant local horizontal mult at %s"%v)
                return False
    if False in whm:
        return False
    else:
        return True

def is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose = False):
    r"""
    Returns True if f defines a graph-theoretic mapping
    from Gamma2 to Gamma1 that is harmonic, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    Suppose Gamma2 has n vertices. A morphism 
              f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    EXAMPLES:
        sage: Gamma2 = graphs.TetrahedralGraph()
        sage: Gamma1 = graphs.CycleGraph(3)
        sage: f = [[0,1,2,3],[0,1,2,0]]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        False
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose=True)
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [1, [2, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [2, [2, 1]]
        False
        sage: V1 = [0,1,2]
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0,1),(1,2),(2,0),(2,3)]
        sage: E1 = [(0,1),(1,2),(2,0)]
        sage: Gamma2 = Graph([V2,E2],format='vertices_and_edges')
        sage: Gamma1 = Graph([V1,E1],format='vertices_and_edges')
        sage: f = [V2, [0,1,2,2]]    # thi is a retract
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose=True)
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [0, 0]]
        True
        sage: Gamma1 = graphs.TetrahedralGraph() 
        sage: Gamma2 = graphs.CubeGraph(3)
        sage: is_harmonic_graph_morphism(Gamma1,Gamma2,f)
         'Error! -- Gamma2 must be in standard form.'

    """
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    if V1 != list(range(n1)):
        return "Error! -- Gamma1 must be in standard form."    
    V2 = Gamma2.vertices(sort=True)
    n2 = len(V2)
    if V2 != list(range(n2)):
        return "Error! -- Gamma2 must be in standard form."       
    E1 = Gamma1.edges(labels=None,sort=True)
    m1 = len(E1)
    E2 = Gamma2.edges(labels=None,sort=True)
    m2 = len(E2)
    edges_in_common = []
    if not(is_graph_morphism(Gamma1, Gamma2, f, verbose)):
        return False
    for v2 in V2:
        w = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v2)
        star1w = star_subgraph(Gamma1, w)
        E1w = star1w.edges(labels = None, sort = True)
        star2v2 = star_subgraph(Gamma2, v2)
        E2v2 = star2v2.edges(labels = None, sort = True)
        sizes = []
        #print(v2, w, E1w, E2v2)
        for e in E1w:
            sizes.append(local_horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2, e))
        edges_in_common.append([v2, sizes]) # these common values = horiz. mult.
    ans = True
    for x in edges_in_common:
        sizesx = x[1]
        S = Set(sizesx)
        if S.cardinality() != 1:
            ans = False
            if verbose:
                print( "This [<vertex>, <intersection sizes>]] fails the check:", x)
        if verbose and ans==True:
            print( "This [<vertex>, <intersection sizes>]] passes the check:", x)
    return ans
    
def find_all_harmonic_graph_morphism(Gamma1, Gamma2, out_filename = ""):
    r"""
    Runs over all possible f:V1 -> V2 and checks if
    is_harmonic_graph_morphism(Gamma1, Gamma2, f) is true.
    If so, writes f to filename (unless out_filename = "", in
    which case it prints it), 

    EXAMPLES:

    """
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    V2 = Gamma2.vertices(sort=True)
    n2 = len(V2)
    f_vals = IntegerModRing(len(V2))^len(V1)
    if out_filename  !=  "":
        r = open(out_filename,"a")
    for f in f_vals:
        if out_filename == "":
            print( is_harmonic_graph_morphism(Gamma2, Gamma1, [V2,f]), f)
        else:
            r.write("is harmonic:  %s \n "%str(is_harmonic_graph_morphism(Gamma2, Gamma1, [V2,f])))
            r.write("f = %s \n "%str(f))
            r.write("Gamma1 = %s \n "%str(Gamma1))
            r.write("Gamma2 = %s \n\n "%str(Gamma2))            
        #if is_harmonic_graph_morphism(Gamma2, Gamma1, [V2,f]):
        #   print( "Gamma2 =", Gamma2, "Gamma1 = ", Gamma1, "f = ", f)
    r.close()
    return "finished writing file of even functions: %s"%out_filename


def vertical_multiplicity_of_graph_morphism(Gamma1, Gamma2, f, v2):
    r"""
    Gamma1 : a graph, 
    Gamma2 : a graph, 
    f : defines a graph morphism
     from Gamma2 to Gamma1 
     (represented by a pair of lists [L1, L2],
     where L1 is the list of all n2 vertices of Gamma2,
     and L2 is the list of length n2 of the vertices
     in Gamma1: L2 forms the corresponding image of L1 under the map f)
    v2 : a vertex of Gamma2.

    Returns nu_phi(v2) - the number of edges of Gamma2 incident to v2 that
    have the same (vertex) image as v2 under f.

    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (1, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: Gamma1 = graphs.PathGraph(3)
        sage: f = [[0,1,2,3],[2, 1, 1, 0]]
        sage: [vertical_multiplicity_of_graph_morphism(Gamma1, Gamma2, f, v) for v in V2]
        [0, 1, 1, 0]
        sage: Gamma2 = graphs.CycleGraph(6)
        sage: Gamma1 = graphs.PathGraph(3)
        sage: f = [[0,1,2,3,4,5],[2, 2, 1, 0, 0, 1]]
        sage: [vertical_multiplicity_of_graph_morphism(Gamma1, Gamma2, f, v) for v in Gamma2.vertices(sort=True)]
        [1, 1, 0, 1, 1, 0]

    """
    V2 = Gamma2.vertices(sort=True)
    Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)
    A2 = Gamma2.adjacency_matrix()
    #print(A2,"\n\n",Phi,"\n\n",A2*Phi)
    #print([[i,f[1][i]] for i in V2])
    nus = [(A2*Phi)[i,f[1][i]] for i in V2]
    return nus[v2]

def vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2):
    r"""
    Gamma1 : a graph, 
    Gamma2 : a graph, 
    f : defines a graph-theoretic mapping
     from Gamma2 to Gamma1 that (presumably) is harmonic
     (represented by a pair of lists [L1, L2],
     where L1 is the list of all n2 vertices of Gamma2,
     and L2 is the list of length n2 of the vertices
     in Gamma1: L2 forms the corresponding image of L1 under the map f)
    v2 : a vertex of Gamma2.
    If f is not harmonic, this function works anyway.

    Returns nu_phi(v1)

    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (1, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: Gamma1 = graphs.PathGraph(3)
        sage: f = [[0,1,2,3],[2, 1, 1, 0]]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V1]
        [0, 1, 1, 0]
        sage: Gamma2 = graphs.CycleGraph(6)
        sage: Gamma1 = graphs.PathGraph(3)
        sage: f = [[0,1,2,3,4,5],[2, 2, 1, 0, 0, 1]]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in Gamma2.vertices(sort=True)]
        [1, 1, 0, 1, 1, 0]

    """
    V2 = Gamma2.vertices(sort=True)
    Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)
    A2 = Gamma2.adjacency_matrix()
    #print(A2,"\n\n",Phi,"\n\n",A2*Phi)
    #print([[i,f[1][i]] for i in V2])
    nus = [(A2*Phi)[i,f[1][i]] for i in V2]
    return nus[v2]


def horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2):
    return horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2)


def horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v2):
    r"""
    Gamma1 : a graph, 
    Gamma2 : a graph, 
    f : defines a graph-theoretic mapping
     from Gamma2 to Gamma1 that is harmonic
     (represented by a pair of lists [L1, L2],
     where L1 is the list of all n2 vertices of Gamma2,
     and L2 is the list of length n2 of the vertices
     in Gamma1: L2 forms the corresponding image of L1 under the map f)
    v2 : a vertex of Gamma2

    Returns m_phi(v)

    EXAMPLES:
        sage: V2 = [0,1,2,3]
        sage: E2 = [(0, 1), (1, 2), (1, 3)]
        sage: Gamma2 = Graph([V2,E2])
        sage: Gamma1 = graphs.PathGraph(3)
        sage: f = [[0,1,2,3],[2, 1, 1, 0]]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [1, 1, 0, 1]
    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    mus = [int((Gamma2.degree(x) - vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, x))/Gamma1.degree(f[1][x])) for x in V2]
    return mus[v2]

def genus(Gamma):
    r"""
    Not the same as Gamma.genus()

    EXAMPLES:
        sage: Gamma2 = graphs.WheelGraph(5)
        sage: Gamma2.genus()
        0
        sage: genus(Gamma2)
        4

    """
    return len(Gamma.edges(sort=True)) - len(Gamma.vertices(sort=True)) + 1

def perm_number_action(G, g0):
    r"""
    Returns list of pairs, indexed by the number of elements of 
    the perm group G, where first number represents the group
    element and the second is where that group element is sent
    by right multiplication by g0.

    EXAMPLES:
        sage: attach("/home/david/sage+sagedays/alg-graph-thry2.sage")
        sage: G = SymmetricGroup(3)
        sage: g0 = G.random_element(); g0
        (1,2,3)
        sage: perm_number_action(G, g0)
        [(0, 2), (1, 0), (2, 1), (3, 5), (4, 3), (5, 4)]
   
    """
    Glist = G.list()
    #N = len(Glist)
    L = [(Glist.index(x),Glist.index(x*g0)) for x in G]
    return L

def lifted_vertex_to_cover(G, Gamma, v, g0):
    r"""
    In a (to be constructed) G-covering of Gamma, 
    call it Gamma' = (V', E'), this function 
    returns the vertex in V' that v lifts to associated to
    g0 under the inverse of the projection map 
    phi: Gamma' -> Gamma.

    INPUT:
        G - a non-trivial subgroup of a symmetric group,
        Gamma - a graph with vertices V and edges E
        v - a vertex in V
        g0 - a non-trivial element of G

    EXAMPLES:
        sage: Gamma = graphs.PathGraph(3)
        sage: V = Gamma.vertices(sort=True); V
         [0, 1, 2]
        sage: G = PermutationGroup([[(0,1)]])  # order 2 group: identity and (0 1)
        sage: G.list()
         [(), (0,1)]
        sage: g0 = G.list()[1]  # the nontrivial permutation (0 1)
        sage: lifted_vertex_to_cover(G, Gamma, 0, g0)
         1
        sage: lifted_vertex_to_cover(G, Gamma, 1, g0)
         0
        sage: lifted_vertex_to_cover(G, Gamma, 2, g0)
         2

    EXPLANATION:

        - The group G = {(), (0 1)} acts on the vertex set [0, 1, 2].
        - The cover has 2 × 3 = 6 vertices (one copy of [0,1,2] for each group element).
        - The lifted vertex (g0, v) is assigned an index in range(6) corresponding to 
          the action of g0 on v, computed via perm_number_action.

    """
    V1 = Gamma.vertices(sort=True)
    Glist = G.list()
    n = G.cardinality()
    V2 = range(n*len(V1))
    iv = V1.index(v)
    j = perm_number_action(G, g0)[iv][1]
    return iv+j


def lifted_vertices_to_cover(G, Gamma, v, g0 = 1):
    r"""
    Returns the fiber over a vertex v in the G-covering of Gamma.

    Suppose Gamma is a graph with vertex set V and G is a finite
    group acting on V (or on indices of V). The G-covering graph
    has vertex set V' = G × V. This function returns the list of
    vertices in V' that map down to v under the projection 
    phi: Gamma' → Gamma. These are the "lifted vertices" of v.

    If a group element g0 ≠ 1 is provided, the fiber is rotated
    by applying g0 to the index of v before lifting.

    INPUT:
        G   - a nontrivial subgroup of a symmetric group
        Gamma - a graph
        v   - a vertex in Gamma
        g0  - optional group element (defaults to identity)

    OUTPUT:
        A list of length |G| giving the indices of the lifted vertices
        in the flat vertex list of the cover graph.

    EXAMPLES:
        sage: Gamma = graphs.PathGraph(3)
        sage: V = Gamma.vertices(sort=True); V
        [0, 1, 2]
        sage: G = PermutationGroup([[(0,1)]])  # group of order 2
        sage: G.list()
        [(), (0,1)]
        sage: lifted_vertices_to_cover(G, Gamma, 0)
        [0, 3]
        sage: lifted_vertices_to_cover(G, Gamma, 1)
        [1, 4]
        sage: lifted_vertices_to_cover(G, Gamma, 2)
        [2, 5]
        sage: g0 = G.list()[1]  # (0 1)
        sage: lifted_vertices_to_cover(G, Gamma, 0, g0)
        [1, 4]

    The total cover has 2 × 3 = 6 vertices. Each call returns
    the indices of the 2 vertices in the fiber over v.

    """
    V1 = Gamma.vertices(sort=True)
    Glist = G.list()
    n = G.cardinality()
    n1 = len(V1)
    V2 = range(n*n1)
    iv = V1.index(v)
    if g0 != 1:
        iv = g0(iv)
    return [(iv+j*n1)%(n*n1) for j in range(n)]

def lifted_edges_to_cover(G, Gamma, e):
    r"""
    In a (to be constructed) G-covering of Gamma, 
    call it Gamma' = (V', E'), this function 
    returns the edges in E' that e lifts to associated to
    the inverse of the projection map 
    phi: Gamma' -> Gamma.

    INPUT:
        G - a non-trivial subgroup of a symmetric group,
        Gamma - a graph with vertices V and edges E
        e - a vertex in E

    EXAMPLES:

    """
    v, w = e
    V1 = Gamma.vertices(sort=True)
    n1 = len(V1)
    n = G.cardinality()
    E2 = []
    for g in G:
        Lv = lifted_vertices_to_cover(G, Gamma, v, g)
        Lw = lifted_vertices_to_cover(G, Gamma, w)
        for i in range(n):
            u = Lv[i]
            z = Lw[i]
            if u != z and not([u, z] in E2 or [z, u] in E2):
                E2.append([u, z])
    return E2


def lifted_graph_to_cover(G, Gamma):
    r"""
    Constructs a G-covering of Gamma.

    INPUT:
        G - a non-trivial subgroup of a symmetric group,
        Gamma - a graph with vertices V and edges E

    EXAMPLES:
        sage: Gamma = graphs.CycleGraph(3)
        sage: S3 = SymmetricGroup(3)
        sage: Gamma2 = lifted_graph_to_cover(S3, Gamma)
        sage: Gamma2.show()
        sage: Gamma2.automorphism_group().cardinality()
        768
        sage: quotient_graph(Gamma2, AG.sylow_subgroup(3))
        Graph on 6 vertices

    """
    V1 = Gamma.vertices(sort=True)
    n = G.cardinality()
    n1 = len(V1)
    Gamma2 = Graph(n*n1)
    E2 = []
    for e in Gamma.edges(sort=True):
        e = [e[0],e[1]]
        es = lifted_edges_to_cover(G, Gamma, e)
        E2 = E2+es
    Gamma2.add_edges(E2)
    return Gamma2



###################################################
####### Cayley graph for linear codes
###################################################

def cayley_expander_graph_from_gen_mat(G):
    r"""
    Start with a vector space C (the linear code associated to the matrix G)
    over GF(2) — this gives the vertices, V.

    Connect two vertices u and v if their difference (or sum, since it’s over GF(2))
    is a row of the generator matrix G - this gives the edges E.


    INPUT:
      G - a rank k kxn matrix over GF(2).

    Assumes k < n  

    OUTPUT:
      Cay(G) = (V, E)

    EXAMPLES:
        sage: C = codes.HammingCode(3, GF(2)); C
        Linear code of length 7, dimension 4 over Finite Field of size 2
        sage: G = C.generator_matrix()
        sage: cayley_expander_graph_from_gen_mat(G)
        Graph on 16 vertices

    """
    Gcols = G.columns()
    n = len(Gcols)
    k = len(G.rows()) # assumes G is full rank
    V = GF(2)**k
    f = lambda x: ZZ(x in Gcols)
    C = cartesian_product([range(2**k), range(2**k)])
    Vlist = V.list()                  
    E = [(x[0],x[1]) for x in C if f(Vlist[x[0]]+Vlist[x[1]])==1]
    E = Set([Set(s) for s in E])
    E = [tuple(s) for s in E] 
    Gamma = Graph(E)
    return Gamma

def cayley_expander_graph_from_code(C):
    r"""
    Builds a Cayley expander graph from a binary linear code C.

    Let G be the generator matrix returned by SageMath's 
    generator_matrix method for the LinearCode class C belongs to.

    The vertices V of the graph Cay(C) correspond to all vectors in C. 
    Two vertices u and v are connected if u + v is a row of G.

    INPUT:
        C -- a linear code over GF(2)

    OUTPUT:
        A undirected graph Gamma with 2^k vertices

    EXAMPLES:
       sage: C = codes.HammingCode(3, GF(2)); C
       Linear code of length 7, dimension 4 over Finite Field of size 2
       sage: Gamma = cayley_expander_graph_from_code(C)
       sage: Gamma.show(layout="circular")
       Launched png viewer for Graphics object consisting of 73 graphics primitives


    """
    G = C.generator_matrix()
    Gcols = G.columns()
    n = C.length()
    k = C.dimension()
    f = lambda x: ZZ(x in G.columns())
    V = GF(2)**k
    CP = cartesian_product([range(2**k), range(2**k)])
    Vlist = V.list()                  
    E = [(x[0],x[1]) for x in CP if f(Vlist[x[0]]+Vlist[x[1]])==1]
    E = Set([Set(s) for s in E])
    E = [tuple(s) for s in E] 
    Gamma = Graph(E)
    return Gamma

def edge_expansion_old(Gamma):
    r"""
    Returns the edge expansion of Gamma.
    The edge expansion (also isoperimetric number or Cheeger constant) 
    h(G) of a graph is defined in [0].

    REFERENCES:
        [0] https://en.wikipedia.org/wiki/Expander_graph#Edge_expansion

    EXAMPLE:

        sage: G = graphs.CycleGraph(6)
        sage: edge_expansion(G)
        1

    """
    V = Gamma.vertices(sort=True)
    SetV = Set(V) 
    return min([(QQ(len(Gamma.edge_boundary([V[i] for i in SV.list()])))/QQ(len(SV.list()))) for SV in SetV.subsets() if (len(SV.list()) != 0 and len(SV.list())<5)])

def edge_expansion(Gamma, max_subset_size=5):
    r"""
    Returns the edge expansion (Cheeger constant) h(G) of the graph Gamma.

    For a graph G = (V, E), the edge expansion is defined as:
        h(G) = min_{S ⊂ V, 0 < |S| < k} |∂S| / |S|

    where ∂S is the edge boundary of S — the set of edges with one endpoint in S 
    and one endpoint outside S.

    This function checks all subsets of vertices up to size max_subset_size 
    (default 5) and returns the minimum ratio.

    REFERENCES:
        [0] https://en.wikipedia.org/wiki/Expander_graph#Edge_expansion

    EXAMPLE:
        sage: G = graphs.CycleGraph(6)
        sage: edge_expansion(G)
        1

    """
    V = Gamma.vertices(sort=True)
    min_ratio = +Infinity
    for S in Subsets(V):
        if 0 < len(S) < max_subset_size:
            boundary_size = len(Gamma.edge_boundary(S))
            ratio = QQ(boundary_size) / QQ(len(S))
            min_ratio = min(min_ratio, ratio)
    return min_ratio


def laplacian_pseudoinverse(Gamma):
    r"""
    Returns Q^+

    EXAMPLES:
        sage: laplacian_pseudoinverse(graphs.CycleGraph(4))
         [ 5/16 -1/16 -3/16 -1/16]
         [-1/16  5/16 -1/16 -3/16]
         [-3/16 -1/16  5/16 -1/16]
         [-1/16 -3/16 -1/16  5/16]
        sage: Gamma = graphs.CycleGraph(5); Gamma
        Cycle graph: Graph on 5 vertices
        sage: laplacian_pseudoinverse(Gamma)
         [ 2/5    0 -1/5 -1/5    0]
         [   0  2/5    0 -1/5 -1/5]
         [-1/5    0  2/5    0 -1/5]
         [-1/5 -1/5    0  2/5    0]
         [   0 -1/5 -1/5    0  2/5]
      

    """
    Q = Gamma.laplacian_matrix()
    n = len(Q.rows())
    J = matrix(QQ, n, n, n^2*[1])
    Qplus = (Q+(1/n)*J)^(-1)-(1/n)*J
    return Qplus

def hamiltonian_paths0(Gamma):
    r"""
    Returns a list of hamiltonian paths (spanning trees of 
    max degree <=2).

    EXAMPLES:
        sage: Gamma = graphs.GridGraph([3,3])
        sage: HP = hamiltonian_paths(Gamma)
        sage: len(HP)
        20
    """
    ST = Gamma.spanning_trees()
    HP = []
    for X in ST:
        L = X.degree_sequence()
        #print L,ST.index(X), max(L)
        if max(L)<=2:
            HP.append(X)
    return HP
    
def hamiltonian_paths(Gamma, signed_adjacency_matrix = []):
    r"""
    Returns a list of hamiltonian paths (spanning trees of 
    max degree <=2).

    EXAMPLES:
        sage: Gamma = graphs.GridGraph([3,3])
        sage: HP = hamiltonian_paths(Gamma)
        sage: len(HP)
        20
        sage: A = matrix(QQ,[
        [0 , -1 , 1  , -1 , -1 , -1 ],
        [1,   0 ,  -1,  1,  1,   -1  ],
        [-1 , 1 ,  0 ,  1 , 1  , -1  ],
        [1 , -1 , -1,  0 ,  -1 , -1  ],
        [1 , - 1 , - 1 , 1 , 0 , - 1  ],
        [1 ,  1  ,  1  , 1  , 1  , 0 ]
        ])
        sage: Gamma = Graph(A, format='weighted_adjacency_matrix')
        sage: HP = hamiltonian_paths(Gamma, signed_adjacency_matrix = A)
        sage: L = [sum(x[2]) for x in HP]; max(L)
        5
        sage: L.index(5)
        21
        sage: HP[21]                                 
        [Graph on 6 vertices,
         [0, 5, 2, 1, 3, 4],
         [-1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1]]
        sage: L.count(5)
        1

    """
    ST = Gamma.spanning_trees()
    if signed_adjacency_matrix == []:
        HP = []
        for X in ST:
            L = X.degree_sequence()
            if max(L)<=2:
                HP.append(X)
        return HP
    if signed_adjacency_matrix != []:
        A = signed_adjacency_matrix
        HP = []
        for X in ST:
            L = X.degree_sequence()
            if max(L)<=2:
                #VX = X.vertices(sort=True)
                EX = X.edges(sort=True)
                if EX[0][1] != EX[-1][1]:
                    ranking = X.shortest_path(EX[0][0],EX[-1][1])
                else:
                   ranking = X.shortest_path(EX[0][0],EX[-1][0])
                signature = [A[ranking[i]][ranking[j]] for i in range(len(ranking)-1) for j in range(i+1,len(ranking))]
                # (use X.shortest_path(a,b) instead of path)
                HP.append([X,ranking,signature])
        return HP



def random_walk(Gamma, m):
    r"""
    Returns a random walk of length n in Gamma.

    EXAMPLES:
        sage: Gamma = graphs.HouseGraph()
        sage: random_walk(Gamma, 3)
        [1, 3, 2, 3]

    """
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(sort=True)
    n = len(V)
    v0 = V[int(random()*n)]
    W = [v0]
    for i in range(m):
        N0 = Gamma.neighbors(v0)
        v1 = N0[int(random()*len(N0))]
        W = W+[v1]
        v0 = v1
    return W
    

def random_trek(Gamma, m):
    r"""
    Returns a random trek of length n in Gamma.

    EXAMPLES:
        sage: Gamma = graphs.HouseGraph()
        sage: random_trek(Gamma, 10)
         [4, 2, 0, 1, 3, 2, 4, 3, 1, 0, 2]

    """
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(sort=True)
    n = len(V)
    v0 = V[int(random.random()*n)]
    W = [v0]
    for i in range(m):
        if len(W)>1:
            N0 = Gamma.neighbors(v0)
            N0.remove(W[-2])
            if len(N0)==0:
                v0 = V[int(random.random()*n)]
                W = W+[v0]
                break
        else:
            N0 = Gamma.neighbors(v0)
        #print( N0 )
        v1 = N0[int(random.random()*len(N0))]
        if v1 != W[len(W)-1]:
            W = W+[v1]
            v0 = v1
        else:
            i = i-1
        if Gamma.degree(v0)>1 and Gamma.degree(v1)==1:
            #print( W, N0 )
            v0 = V[int(random.random()*n)]
            i = i-1
            #break
    return W

def codifferential_basis(v, e, Gamma):
    """
    Returns the value of the codifferential
    delta:C^0(E) -> C^0(V)
    on the characteristic functions of E
    (so the argument "e" indicates the 
    function on E that is 1 at e and 0 elsewhere).

    EXAMPLES:
        sage: Gamma = graphs.DiamondGraph()  
        sage: V = Gamma.vertices(sort=True)   
        sage: E = list(Gamma.edges(labels=None,sort=True)); E
        [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
        sage: delta_matrix = matrix([[codifferential_basis(v, e, Gamma) for e in E] for v in V])        
        sage: delta_matrix  
        [ 1/2  1/2    0    0    0]
        [-1/3    0  1/3  1/3    0]
        [   0 -1/3 -1/3    0  1/3]
        [   0    0    0 -1/2 -1/2]
        sage: delta_matrix.right_kernel()
        Vector space of degree 5 and dimension 2 over Rational Field
        Basis matrix:
        [ 1 -1  0  1 -1]
        [ 0  0  1 -1  1]
        sage: cycle_space(Gamma, [E, [1,1,1,1,1]])
        Vector space of degree 5 and dimension 2 over Rational Field
        Basis matrix:
        [ 1 -1  0  1 -1]
        [ 0  0  1 -1  1]

    """
    if min(e) == v:
        return 1/Gamma.degree(v)
    elif max(e) == v:
        return -1/Gamma.degree(v)
    else:
        return 0

def codifferential_matrix(Gamma):
    """
    Returns the matrix of the codifferential
    delta:C^0(E) -> C^0(V)

    EXAMPLES:
        sage: Gamma = graphs.DiamondGraph() 
        sage: codifferential_matrix(Gamma) 
        [ 1/2  1/2    0    0    0]
        [-1/3    0  1/3  1/3    0]
        [   0 -1/3 -1/3    0  1/3]
        [   0    0    0 -1/2 -1/2]

    """
    V = Gamma.vertices(sort=True)   
    E = list(Gamma.edges(labels=None,sort=True))
    delta_matrix = matrix([[codifferential_basis(v, e, Gamma) for e in E] for v in V])        
    return delta_matrix

## pullback computations
## assume there is a graph morphism
## phi:Gamma2 -> Gamma1
## find matrix repn of phi_*:C^0(Gamma2) -> C^0(Gamma1)

def pushforward_matrix_vertex_functions(Gamma1, Gamma2, f):
    """
    If we assume there is a graph morphism
    phi:Gamma2 -> Gamma1, denoted f in the usual color list notation,
    find the matrix repn of phi_*:C^0(Gamma2) -> C^0(Gamma1)
    with respect to the standard characteristic function basis

    We want a |V1|x|V2| matrix P for which ei in RR^|V1| (0<=i<=|V1|)
    is the sum of ej in RR^|V2|, where phi(j)=i.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)
        sage: Gamma2 = graphs.DiamondGraph()
        sage: V2 = Gamma2.vertices(sort=True); V2
        [0, 1, 2, 3]
        sage: f = [V2, [0, 1, 1, 2]]
        sage: P = pushforward_matrix_vertex_functions(Gamma1, Gamma2, f); P
        [1 0 0 0]
        [0 1 1 0]
        [0 0 0 1]
        sage: P.rank() 
        3
        sage: matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)
        [1 0 0]
        [0 1 0]
        [0 1 0]
        [0 0 1]
        
    """
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    V2 = Gamma2.vertices(sort=True)
    n2 = len(V2)
    V = QQ^n1
    rowsP = [[0]*n1]*n2
    for i in range(n2):
        for j in range(n1):
            if j == image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, i):
               rowsP[i]=V(rowsP[i])+V.basis()[j]
    return matrix(rowsP).transpose()

def pushforward_matrix_edge_functions(Gamma1, Gamma2, f):
    """
    If we assume there is a graph morphism
    phi:Gamma2 -> Gamma1, denoted f in the usual color list notation,
    find the matrix repn of phi_*:C^1(Gamma2) -> C^1(Gamma1)
    with respect to the standard characteristic function basis

    We want a |E1|x|E2| matrix P for which ei in RR^|E1| (0<=i<=|E1|)
    is the sum of ej in RR^|E2|, where phi(E2[j])=E1[i].

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)
        sage: Gamma2 = graphs.DiamondGraph()
        sage: V2 = Gamma2.vertices(sort=True); V2
        [0, 1, 2, 3]
        sage: f = [V2, [0, 1, 1, 2]]
        sage: P = pushforward_matrix_edge_functions(Gamma1, Gamma2, f); P
        [1 1 0 0 0]
        [0 0 0 1 1]
        sage: matrix_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f)
        [1 0]
        [1 0]
        [0 0]
        [0 1]
        [0 1]

    """
    E1 = Gamma1.edges(labels=None,sort=True)
    m1 = len(E1)
    E2 = Gamma2.edges(labels=None,sort=True)
    m2 = len(E2)
    V = QQ^m1
    rowsP = [[0]*m1]*m2
    for i in range(m2):
        for j in range(m1):
            if E1[j] == image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, E2[i]):
               rowsP[i]=V(rowsP[i])+V.basis()[j]
    return matrix(rowsP).transpose()


def pullback_matrix_vertex_functions(Gamma1, Gamma2, f):
    """
    If we assume there is a graph morphism
    phi:Gamma2 -> Gamma1, denoted f in the usual color list notation,
    find the matrix repn of phi^*:C^0(Gamma1) -> C^0(Gamma2)
    with respect to the standard characteristic function basis.

    Thisis the transpose of pushforward_matrix_vertex_functions.

    We want a |V2|x|V1| matrix P for which ej in RR^|V1| (0<=j<=|V1|)
    is the ei in RR^|V2|, where phi(i)=j.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)
        sage: Gamma2 = graphs.DiamondGraph()
        sage: V2 = Gamma2.vertices(sort=True); V2
        [0, 1, 2, 3]
        sage: f = [V2, [0, 1, 1, 2]]
        sage: P = pullback_matrix_vertex_functions(Gamma1, Gamma2, f); P
        [1 0 0]
        [0 1 0]
        [0 1 0]
        [0 0 1]

    """
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    V2 = Gamma2.vertices(sort=True)
    n2 = len(V2)
    V = QQ^n1
    rowsP = [[0]*n1]*n2
    for i in range(n2):
        for j in range(n1):
            if j == image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, i):
               rowsP[i]=V.basis()[j]
    return matrix(rowsP)


def proj_blowup(x, Gamma, r):
    """
    This returns the projection map referenced in the function
    blowup_graph(Gamma, r).

    Assumes 0 <= x <= nr-1. If V = [x_0, ..., x_{n-1}]
    then this function sends 
      0, ..., r-1 to x_0 
      r, ..., 2r-1 to x_1, 
    and so on.

    EXAMPLES:
        sage: Gamma = graphs.DiamondGraph()
        sage: [proj_blowup(x, Gamma, 2) for x in range(8)]
         [0, 0, 1, 1, 2, 2, 3, 3]

    """
    V = Gamma.vertices(sort=True)
    n = len(V)
    Vr = range(n*r)
    i = int(x/r)
    return V[i]

def blowup_balanced_graph(Gamma, r):
    r"""
    Defn: The (balanced) $r$-blowup $\Gamma^{(r)}$ 
    of the graph $\Gamma$ is defined as follows: 
    *) For each vertex $x_i$ of of $\Gamma$, 
       the graph $\Gamma^{(r)}$ has $r$ vertices, 
       $ x_{i,1}, x_{i,2}, \dots , x_{i,r}$.
    *) There is an edge between vertices $x_{i,k}$ and $x_{j, \ell}$ 
       in $\Gamma^{(r)}$ if and only if there is an edge between 
       vertices $x_i$ and $x_j$ in $\Gamma$.

    Note: The projection map 
      $\phi : \Gamma^{(r)} \to \Gamma$ 
    given on vertices by 
      $\phi(x_{i,j}) = x_i$ 
    is a harmonic morphism (in fact, it's an r-multicover).

    This function returns the r-blowup of Gamma.

    EXAMPLES:
        sage: Gamma = graphs.DiamondGraph()  
        sage: Gamma.degree_sequence()        
         [3, 3, 2, 2]
        sage: Gammabu = blowup_balance_graph(Gamma, 2)
        sage: Gammabu.degree_sequence()      
         [6, 6, 6, 6, 4, 4, 4, 4]

        sage: Gamma = graphs.CycleGraph(4)   
        sage: Gammabu = blowup_balance_graph(Gamma, 2)
        sage: K44 = graphs.CompleteBipartiteGraph(4,4)
        sage: Gammabu.is_isomorphic(K44)      
         True

    """
    V = Gamma.vertices(sort=True)
    E = list(Gamma.edges(labels=None,sort=True))
    n = len(V)
    m = len(E)
    Vr = list(range(n*r))
    Er = []
    for x in Vr:
        for y in Vr:
            if (y>x and (proj_blowup(x, Gamma, r), proj_blowup(y, Gamma, r)) in E):
                Er = Er+[(x,y)]
    #print(Vr, "\n", Er)
    Gammar = Graph([Vr, Er])
    return Gammar


def blowup_weighted_graph(wGamma, r):
    r"""
    wGamma is a weighted graph given as a pair: 
    wGamma = [(V, E), wt], where wt is a pair [E,w], 
    where w is a list of length |E| of edge weights >0.

    Defn: The (weighted) $r$-blowup $\Gamma^{(r)}$ 
    of the graph $\Gamma$ is defined as follows: 
    *) For each vertex $x_i$ of of $\Gamma$, 
       the graph $\Gamma^{(r)}$ has $r$ vertices, 
       $ x_{i,1}, x_{i,2}, \dots , x_{i,r}$.
    *) There is an edge between vertices $x_{i,k}$ and $x_{j, \ell}$ 
       in $\Gamma^{(r)}$ if and only if there is an edge between 
       vertices $x_i$ and $x_j$ in $\Gamma$.
    *) Define $\pi^{(r)} : \Gamma^{(r)}\to \Gamma$ by
       $\pi^{(r)}(x_{i,j}) = x_i$. If the weights of 
       $\Gamma$ are defined by $w: E \to \rrr$ then 
       the weights of the $r$-blowup are defined by 
       $w^{(r)}: E^{(r)} \to \rrr$ where 
       $w^{(r)}(v_1,v_2) = w(\pi^{(r)}(v_1), \pi^{(r)}(v_2))$,
       if $(v_1, v_2)\in E$.

    Note: The projection map 
      $\phi : \Gamma^{(r)} \to \Gamma$ 
    given on vertices by 
      $\phi(x_{i,j}) = x_i$ 
    is a weighted harmonic morphism. 

    This function returns the weighted r-blowup of Gamma.

    EXAMPLES:
        sage: V = [0,1,2,3]
        sage: E = [(0, 1), (1, 2), (0, 2), (0, 3)]
        sage: Gamma = Graph([V, E])
        sage: wt = [E, [1, 2, 3, 4]] 
        sage: wGamma = [Gamma, wt]
        sage: blowup_weighted_graph(wGamma, 2)
        [Graph on 8 vertices,
         [[(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 2), (1, 3),
           (1, 4), (1, 5), (1, 6), (1, 7), (2, 4), (2, 5), (3, 4), (3, 5)],
          [1, 1, 3, 3, 4, 4, 1, 1, 3, 3, 4, 4, 2, 2, 2, 2]]] 

    """
    V = wGamma[0].vertices(sort=True)
    E = wGamma[1][0]
    n = len(V)
    m = len(E)
    wt = wGamma[1][1]
    Vr = list(range(n*r))
    Gamma = wGamma[0]
    Er = []
    for x in Vr:
        for y in Vr:
            if (y>x and (proj_blowup(x, Gamma, r), proj_blowup(y, Gamma, r)) in E):
                Er = Er+[(x,y)]
    wr = [wt[E.index((proj_blowup(e[0], Gamma, r), proj_blowup(e[1], Gamma, r)))] for e in Er]
    #print(wr, "\n", wt)
    Gammar = Graph([Vr, Er])
    return [Gammar, [Er, wr]]

def find_cover_graph(Gamma, r, verbose=False):
    """
    Returns a degree r covering graph pi: Gammar -> Gamma,
    found by random search over possible edge sets, and the 
    morphism f returned as an rn-tuple if entries from V,
    where V = [0, ..., n-1].

    Warning: Gammar can be disconnected.

    Assumes that Gamma is connected and in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(4)   
        sage: Gamma2, f0 = find_cover_graph(Gamma1, 3)  
        sage: Gamma2.is_connected()                   
         True
        sage: V2 = Gamma2.vertices(sort=True); V2               
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  
        sage: is_graph_morphism(Gamma1, Gamma2, f)   
         True
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
         False
        sage: Gamma2.degree_sequence() 
         [4, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    """
    V = Gamma.vertices(sort=True)
    n = len(V)
    E = Gamma.edges(labels=None,sort=True)
    Zn = IntegerModRing(n)
    Zr = IntegerModRing(r)
    Vr = list(range(r*n))
    # the ith fiber maps to vertex i under pi
    fibers = [[ i for i in Vr if i%n==j] for j in range(n)]
    f0 = [i%n for i in range(r*n)]
    Er = []
    for e in E: # construct a fiber over each edge e
        u = e[0]
        v = e[1]
        for x in fibers[u]:
             a = int(Zr.random_element())
             Er = Er+[(x, fibers[v][a])]
    Gammar = Graph([Vr, Er])
    if verbose:
        for x in V:
            print("fiber over %s is: "%x, fibers[x])
        return Gammar, f0
    else:
        return Gammar, f0

def find_random_incidence_matrix(m,n):
    """
    Returns either an mxn (0,1)-matrix M such that
    (a) each column has exactly two $1$'s, 
    (b) no row is all $0$s, 
    (c) no columns are repeated,
    or returns False if the random search did not find such a matrix.

    
    EXAMPLES:

    """
    MS = MatrixSpace(GF(2), m, n)
    MS_ZZ = MatrixSpace(ZZ, m, n)
    for i in range(100*n):
        M = MS.random_element()
        M = MS_ZZ(M)
        num_cols = len(list(Set(M.columns())))
        col_sums = [sum(c) for c in M.columns()]
        row_sums = [sum(r) for r in M.rows()]
        if (col_sums == [2]*n and num_cols == n and not(0 in row_sums)):
            return M
    return False

def flower_graph(N):
    """
    Returns the flower graph of cycle graphs 
    C_n1, C_n2, ..., C_nk, where k is the number
    of *petals* and where N = [n1,n2,...,nk] 
    is a list of integers ni>2. If k=1 then it returns
    the cycle graph C_n1.

    EXAMPLES:
        sage: N = [3,4,5,6]  
        sage: Gamma = flower_graph(N)  
        sage: Gamma.vertices(sort=True)     
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        sage: Gamma.edges(labels=None,sort=True)    
        [(0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (0, 9), (0, 10), (0, 14),
         (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (8, 9), (10, 11),
         (11, 12), (12, 13), (13, 14)]
        sage: Gamma.degree_sequence()    
        [8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    """
    k = len(N)
    V = list(range(sum(N)-k+1))
    Omits = [sum(N[:i])-i for i in range(1,k+1)]
    E = []
    for i in V:
        if not(i in Omits):
            E = E+[(i,i+1)]
    Adds = [(0, sum(N[:i])-i) for i in range(1,k)]
    Adds = Adds + [(0, sum(N[:i])-i+1) for i in range(1,k)]
    Adds = Adds+[(0,sum(N)-k)]
    E = E+Adds
    return Graph([V,E])

def vertex_matrix_map_to_CL(Gamma1, Gamma2, Phi, verbose = False):
    """
    Returns the color list associated to the n2xn1 matrix,
    if it is "legal". Otherwise, it returns an empty list.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(4)     
        sage: Gamma2 = graphs.CycleGraph(8)      
        sage: f0 = [0,1,2,3,0,1,2,3]    
        sage: V2 = Gamma2.vertices(sort=True)    
        sage: f = [V2, f0]         
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f); Phi 
        [1 0 0 0]
        [0 1 0 0]
        [0 0 1 0]
        [0 0 0 1]
        [1 0 0 0]
        [0 1 0 0]
        [0 0 1 0]
        [0 0 0 1]
        sage: vertex_matrix_map_to_CL(Gamma1, Gamma2, Phi, verbose = False)  
        [0, 1, 2, 3, 0, 1, 2, 3]
        sage: vertex_matrix_map_to_CL(Gamma1, Gamma2, Phi, verbose = True) 
        ([0, 1, 2, 3, 0, 1, 2, 3], True)

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    CL = []
    for r in Phi.rows():
        ii = r.nonzero_positions()
        if len(ii)>1:
            print(r, ii)
            if verbose == True:
                return [], False
            else:
                return []
        else:
            CL = CL+[ii[0]]
    if verbose == True:
        f = [V2, CL]
        return CL, is_harmonic_graph_morphism(Gamma1, Gamma2, f)
    else:
        return CL

def vertical_edges_list(Gamma1, Gamma2, f):
    """
    Returns the list of vertical edges, if any, of the graph
    morphism represented by the CL f.

    EXAMPLES:
        sage: Gamma2 = graphs.CycleGraph(4)    
        sage: Gamma1 = graphs.PathGraph(2)       
        sage: f0 = [0,0,1,1]          
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]    
        sage: PhiE = matrix_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f); PhiE 
        [0]
        [1]
        [1]
        [0]
        sage: vertical_edges_list(Gamma1, Gamma2, f) 
        [(0, 1), (2, 3)]
        sage: Gamma2 = graphs.FriendshipGraph(2)                                           
        sage: Gamma1 = graphs.PathGraph(3)                                                 
        sage: V2 = Gamma2.vertices(sort=True)                                                       
        sage: f0 = [0,0,2,2,1]                                                             
        sage: f = [V2, f0]                                                                 
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)                                
        True
        sage: PhiE = matrix_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f); PhiE      
        [0 0]
        [1 0]
        [1 0]
        [0 0]
        [0 1]
        [0 1]
        sage: vertical_edges_list(Gamma1, Gamma2, f)                                       
        [(0, 1), (2, 3)]

    """
    E2 = Gamma2.edges(labels=None,sort=True)
    PhiE = matrix_of_graph_morphism_edges_unsigned(Gamma1, Gamma2, f)
    PhiE_rows = PhiE.rows()
    V = PhiE_rows[0].parent()
    verts = []
    m2 = len(PhiE_rows)
    for i in range(m2):
        if PhiE_rows[i]==V(0):
            verts = verts+[E2[i]]
    return verts

def adjacency_matrix_decomposition(Gamma1, Gamma2, f):
    """
    Returns the decomposition A2 = A_h+A_v, where A_v
    is supported on the edge positions associated to
    vertical edges.

    EXAMPLES:
        sage: Gamma2 = graphs.FriendshipGraph(2)                                           
        sage: Gamma1 = graphs.PathGraph(3)                                                 
        sage: V2 = Gamma2.vertices(sort=True)                                                       
        sage: f0 = [0,0,2,2,1]                                                             
        sage: f = [V2, f0]                                                                 
        sage: vertical_edges_list(Gamma1, Gamma2, f)                                       
        [(0, 1), (2, 3)]
        sage: adjacency_matrix_decomposition(Gamma1, Gamma2, f)                            
        (
        [0 0 0 0 1]  [0 1 0 0 0]
        [0 0 0 0 1]  [1 0 0 0 0]
        [0 0 0 0 1]  [0 0 0 1 0]
        [0 0 0 0 1]  [0 0 1 0 0]
        [1 1 1 1 0], [0 0 0 0 0]
        )
        sage: A,B = adjacency_matrix_decomposition(Gamma1, Gamma2, f)                      
        sage: A2 = Gamma2.adjacency_matrix()
        sage: A2 == A+B                                                                    
        True

    """
    E_v = vertical_edges_list(Gamma1, Gamma2, f)
    V2 = Gamma2.vertices(sort=True)
    n2 = len(V2)
    A2 = Gamma2.adjacency_matrix()
    A_h = A2*0
    for e in E_v:
        u = e[0]
        v = e[1]
        A_h[u,v] = 1
        A_h[v,u] = 1
    A_v = A2-A_h
    return (A_v,A_h)

def harmonic_edge_irreducible_subgraph(Gamma1, Gamma2, f):
    """
    We say a harmonic morphism phi: Gamma2 -> Gamma1 is 
    *edge irreducible* if every vertical edge is a
    bridge. A harmonic morphism with no vertical edges is
    automatically edge irreducible.

    This function returns the smallest subgraph Gamma of Gamma2
    having the same vertices such that phi|Gamma is a harmonic 
    morphism with no vertical edges.

    EXAMPLES:
        sage: Gamma2 = graphs.FriendshipGraph(2)                                           
        sage: Gamma1 = graphs.PathGraph(3)                                                 
        sage: Gamma2.edges(labels=None,sort=True)                                                    
        [(0, 1), (0, 4), (1, 4), (2, 3), (2, 4), (3, 4)]
        sage: f0 = [0,0,2,2,1]                                                             
        sage: V2 = Gamma2.vertices(sort=True)                                                       
        sage: f = [V2, f0]  
        sage: harmonic_edge_irreducible_subgraph(Gamma1, Gamma2, f).edges(labels=None,sort=True)              
        [(0, 4), (1, 4), (2, 4), (3, 4)]

    """
    bridges = list(Gamma2.bridges())
    verts = vertical_edges_list(Gamma1, Gamma2, f)
    V2 = Gamma2.vertices(sort=True)
    E = []
    for e in Gamma2.edges(labels = None, sort = True):
        if not(e in verts) or ((e in verts) and (e in bridges)):
            E = E+[e]
    return Graph([V2, E])

def is_harmonic_edge_irreducible(Gamma1, Gamma2, f):
    """
    We say a harmonic morphism phi: Gamma2 -> Gamma1 is 
    *edge irreducible* if every vertical edge is a
    bridge. A harmonic morphism with no vertical edges is
    automatically edge irreducible.

    This function returns True if every vertical edge is a
    bridge. Otherwise, it returns False.

    EXAMPLES:
        sage: Gamma2 = graphs.FriendshipGraph(2)
        sage: Gamma1 = graphs.PathGraph(3)
        sage: f0 = [0,0,2,2,1] 
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]  
        sage: is_harmonic_edge_irreducible(Gamma1, Gamma2, f) 
        False

    """
    bridges = list(Gamma2.bridges())
    verts = vertical_edges_list(Gamma1, Gamma2, f)
    V2 = Gamma2.vertices(sort=True)
    E = []
    ans = is_harmonic_graph_morphism(Gamma1, Gamma2, f)
    if not(ans):
        return False
    for e in verts:
        if not(e in bridges):
            #print(e, not(e in bridges), verts, ans)
            return False
    return True

def coalescence_vertex(Gamma1, Gamma2):
    """
    Returns the graph obtained by identifying the vertex v=0
    in Gamma1 with the vertex v=0 in Gamma2, called the 
    vertex coalescence at 0.

    NOTE: This function assumes Gamma1 and Gamma2 are in 
    "standard form", that is V1 and V2 are integer ranges 
    of the form [0, 1, ..., n-1], for some n>0.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(3)                                                       
        sage: Gamma2 = graphs.CycleGraph(4)                                                       
        sage: Gamma = coalescence_vertex(Gamma2, Gamma1)                                       
        sage: Gamma.vertices(sort=True)                                                                    
        [0, 1, 2, 3, 4, 5]
        sage: Gamma.edges(labels=None,sort=True)                                                            
        [(0, 1), (0, 3), (0, 4), (0, 5), (1, 2), (2, 3), (4, 5)]

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    E1 = Gamma1.edges(labels=None,sort=True)
    E2 = Gamma2.edges(labels=None,sort=True)
    m1 = len(E1)
    m2 = len(E2)    
    if not(0 in V1):
        return False, "vertex 0 must belong to Gamma1"
    if not(0 in V2):
        return False, "vertex 0 must belong to Gamma2"
    V = list(range(n1+n2-1))
    E = E1
    for e in E2:
        if 0 in e:
            x = e[0]
            y = e[1]
            if 0 == x:
               E = E+[(0,y+n1-1)]
            elif 0 == y:
               E = E+[(x+n1-1,0)]
        if not(0 in e):
            x = e[0]
            y = e[1]
            E = E+[(x+n1-1,y+n1-1)]
    #print(V, E)
    return Graph([V,E])
    
def coalescence_edge(Gamma1, Gamma2):
    """
    Returns the graph obtained by identifying the edge e=(0,1)
    in Gamma1 with the edge e=(0,1) in Gamma2, called the 
    edge coalescence at e.

    NOTE: This function assumes Gamma1 and Gamma2 are in 
    "standard form", that is V1 and V2 are integer ranges 
    of the form [0, 1, ..., n-1], for some n>0. It also assume
    that both Gamma1 and Gamma2 contain the edge (0,1).

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(3)                                                       
        sage: Gamma2 = graphs.CycleGraph(4)                                                       
        sage: Gamma = coalescence_edge(Gamma2, Gamma1)                                       
        sage: Gamma.vertices(sort=True)
        [0, 1, 2, 3, 4]
        sage: Gamma.edges(labels=None,sort=True)                                                            
        [(0, 1), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3)]

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    E1 = Gamma1.edges(labels=None,sort=True)
    E2 = Gamma2.edges(labels=None,sort=True)
    m1 = len(E1)
    m2 = len(E2)    
    V = list(range(n1+n2-2))
    if not((0,1) in E1) and not((1,0) in E1):
        return False, "edge (0,1) must belong to Gamma1"
    if not((0,1) in E2):
        return False, "edge (0,1) must belong to Gamma2"
    E = E1
    for e in E2:
        if not((0,1) == e or (1,0) == e):
            x = e[0]
            y = e[1]
            if 0 == x:
               E = E+[(0,y+n1-2)]
            elif 0 == y:
               E = E+[(x+n1-2,0)]
            if 1 == x:
               E = E+[(1,y+n1-2)]
            elif 1 == y:
               E = E+[(x+n1-2,1)]
        if not(0 in e) and not(1 in e):
            E = E+[(x+n1-2,y+n1-2)]
    #print(V, E)
    return Graph([V,E])

def barycentric_subdivision_graph(Gamma):
    """
    Returns the subdivision graph of Gamma obtained by subdividing each edge, 
    but leaves Gamma itself unchanged. This always returns a bipartite graph.

    EXAMPLES:
        sage: Gamma = graphs.ButterflyGraph()            
        sage: subdivision_graph(Gamma).vertices(sort=True)              
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        sage: Gamma.vertices(sort=True) # to show Gamma is unchanged    
         [0, 1, 2, 3, 4]
        sage: Gamma = graphs.CycleGraph(3)
        sage: Gamma.is_bipartite()
         False
        sage: subdivision_graph(Gamma).is_bipartite()
         True

    """
    Gamma0 = Gamma.copy()
    E0 = Gamma0.edges(labels=None,sort=True)
    V0 = Gamma0.vertices(sort=True)
    Gamma0.subdivide_edges(E0, 1)
    E0 = Gamma0.edges(labels=None,sort=True)
    V0 = Gamma0.vertices(sort=True)
    #print(V0, E0)
    return Graph([V0,E0])

def which_edges_can_be_added(Gamma1, Gamma2,f):
    """
    Returns the list of edges that can be added to
    Gamma2 for which f is still harmonic when extended
    to the larger graph.

    EXAMPLES:
        sage: Gamma2 = graphs.CycleGraph(4)  
        sage: Gamma1 = graphs.PathGraph(3)   
        sage: f0 = [0, 1, 2, 1]    
        sage: V2 = Gamma2.vertices(sort=True)   
        sage: f = [V2, f0]          
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: which_edges_can_be_added(Gamma1, Gamma2,f) 
        [(1, 3)]
        sage:
        sage: Gamma2 = graphs.CycleGraph(6) 
        sage: Gamma1 = graphs.CycleGraph(3) 
        sage: f0 = [0, 1, 2, 0, 1, 2] 
        sage: V2 = Gamma2.vertices(sort=True)  
        sage: f = [V2, f0]          
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: which_edges_can_be_added(Gamma1, Gamma2, f) 
        [(0, 3), (1, 4), (2, 5)]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]  
        [0, 0, 0, 0, 0, 0]
        sage: E2 = Gamma2.edges(labels=None,sort=True) 
        sage: E3 = E2 + [(0, 3), (1, 4), (2, 5)] 
        sage: Gamma3 = Graph([V2, E3])     
        sage: is_harmonic_graph_morphism(Gamma1, Gamma3, f)  
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma3, f, v) for v in V2]
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma3, f, v) for v in V2] 
        [1, 1, 1, 1, 1, 1]
        sage: Gamma2 = graphs.StarGraph(4) # 5-vertex star graph
        sage: Gamma1 = graphs.PathGraph(3)                                              
        sage: f0 = [1, 0, 0, 2, 2]                                                      
        sage: V2 = Gamma2.vertices(sort=True)                                                    
        sage: f = [V2, f0]                                                              
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)                             
        True
        sage: which_edges_can_be_added(Gamma1, Gamma2, f) # adding these creates the butterfly graph      
        [(1, 2), (3, 4)]
        sage: f0 = [1, 0, 1, 1, 2]                                                      
        sage: f = [V2, f0]                                                              
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)                             
        True
        sage: which_edges_can_be_added(Gamma1, Gamma2, f)                               
        [(2, 3)]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [1, 1, 0, 0, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [2, 0, 1, 1, 0]
        sage: E2 = Gamma2.edges(labels=None,sort=True)  
        sage: E3 = E2 + [(2, 3)] 
        sage: Gamma3 = Graph([V2,E3]) # St4+edge
        sage: which_edges_can_be_added(Gamma1, Gamma3, f) 
        []
        sage: is_harmonic_graph_morphism(Gamma1, Gamma3, f)
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma3, f, v) for v in V2]
        [1, 1, 0, 0, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma3, f, v) for v in V2]
        [2, 0, 2, 2, 0]

    """
    if not(is_harmonic_graph_morphism(Gamma1, Gamma2, f)):
        print("f is not harmonic")
        return []
    V2 = Gamma2.vertices(sort=True)
    E2 = Gamma2.edges(labels=None,sort=True)
    add0 = []
    for v in V2:
        for w in V2:
            if (v != w) and not((v,w) in E2) and not((w,v) in E2):
                E3 = E2+[(v,w)]
                Gamma3 = Graph([V2,E3])
                if is_harmonic_graph_morphism(Gamma1, Gamma3, f):
                    if not((w,v) in add0):
                        add0 = add0+[(v,w)]
    return add0
  
def one_vertex_corona(Gamma):
    """
    Returns the graph obtained by adding a new vertex 0 to Gamma and 
    an edge from 0 to each vertex in Gamma.

    EXAMPLES:
        sage: Gamma = graphs.CycleGraph(4)    # cycle graph
        sage: E = Gamma.edges(labels=None,sort=True); E    
        [(0, 1), (0, 3), (1, 2), (2, 3)]
        sage: Gamma0 = one_vertex_corona(Gamma)   # wheel graph
        sage: E0 = Gamma0.edges(labels=None,sort=True); E0  
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)]

    """
    V = Gamma.vertices(sort=True)
    n = len(V)
    E = Gamma.edges(labels=None,sort=True)
    m = len(E)
    V0 = list(range(n+1))
    E0 = [(e[0]+1,e[1]+1) for e in E]
    for v in V:
        E0=E0+[(0,v+1)]
    return Graph([V0,E0])
  
def corona(Gamma1, Gamma2):
    """
    Returns the graph obtained by taking one copy of Gamma1 and n1 copies
    of Gamma2, and then joining the i-th vertex of Gamma1 to every vertex
    in the i-th copy of Gamma2.

    Assumes both Gamma1 and Gamma2 are in standard form.
  
    Here, the 0th copy (start counting at 0) of Gamma2 has vertices
    [n1, n1+1, ..., n1+n2-1], the 1st copy of Gamma2 has vertices
    [n1+n2, n1+n2+1, ..., n1+2*n2-1], ..., the jth copy of Gamma2 has 
    vertices [n1+j*n2, n1+j*n2+1, ..., n1+(j+1)*n2-1], ...
 
    NOTE: The corona graph construction was first introduced by
    Fruct and Harary. in "On the corona of two graphs," Aequationes
    Mathematicae (1970).

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)       
        sage: Gamma2 = graphs.CycleGraph(3)       
        sage: Gamma = corona(Gamma1, Gamma2)      
        sage: Gamma.vertices(sort=True)                    
        [0, 1, 2, 3, 4, 5, 6, 7]
        sage: Gamma.edges(labels=None,sort=True)           
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (1, 6), (1, 7), (2, 3), (2, 4),
         (3, 4), (5, 6), (5, 7), (6, 7)]

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    E1 = Gamma1.edges(labels=None,sort=True)
    E2 = Gamma2.edges(labels=None,sort=True)
    m1 = len(E1)
    m2 = len(E2)
    V = list(range(n1+n1*n2))
    #print(V)
    E = E1
    if n1==1:
        return one_vertex_corona(Gamma2)
    for i in range(n1):
        Ei = [(e[0]+n1+i*n2, e[1]+n1+i*n2) for e in E2]
        #print(i,Ei)
        Ei = Ei+[(i,v+n1+i*n2) for v in V2]
        #print("next",i,Ei)
        E = E+Ei
    return Graph([V,E])


def CL_of_join_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g):
    """
    All these graphs use the standard ordering, so Gamma_i has vertices
    0, 1, ...., n_i - 1, and
       f: Gamma2 -> Gamma1 and  g: Gamma4 -> Gamma3
    are morphisms in CL notation.

    The graph join of Gamma1 and Gamma2, denoted join(Gamma1, Gamma2),
    has vertex set V1 cup V2 (disjoint union), identified with
    {(0, v1) | v1 in V1} cup {(1,v2) | v2 in V2}, and edge set
    E1 cup E2 cup {(v1,v2) | v1 in V1, v2 in V2}, identified with
    {((0, v1), (0,v1')) | v1, v1' in V1} cup
     {((1, v2), (1,v2')) | v2, v2' in V2} cup
      {((0, v1), (1,v2)) | v1 in V1, v2 in V2}.
    This is then rewritten in lexicographic order.
    Except for the labeling, this is the same as 
       graph_convert_to_standard(Gamma1.join(Gamma2))

    Returns the CL associated to join(f,g) going from
          join(Gamma2, Gamma4) -> join(Gamma1, Gamma3).

    #### add gamma2=P4->Gamma1=P2 example as well.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)    
        sage: Gamma2 = graphs.PathGraph(4)     
        sage: f0 = [0,1,2,2]     
        sage: V2 = Gamma2.vertices(sort=True)  
        sage: f = [V2, f0]         
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)    
        True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [1, 1, 1, 0]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]  
        [0, 0, 1, 1]
        sage: Gamma3 = graphs.PathGraph(2)   
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: g0 = [0,1,1,0]   
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g = [V4, g0]   
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g)  
        True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]  
        [1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]  
        [1, 1, 1, 1]
        sage: CL_of_join_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)  
         [0, 1, 2, 2, 3, 4, 4, 3]
        sage: Gamma_2join4 = graph_convert_to_standard(Gamma2.join(Gamma4))    
        sage: Gamma_1join3 = graph_convert_to_standard(Gamma1.join(Gamma3))   
        sage: V_2join4 = Gamma_2join4.vertices(sort=True)    
        sage: f_join_g_0 = CL_of_join_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g) 
        sage: f_join_g = [V_2join4, f_join_g_0]    
        sage: is_harmonic_graph_morphism(Gamma_1join3, Gamma_2join4, f_join_g, verbose=True)   
        Gamma1 = (V1, E1) =  [0, 1, 2, 3, 4] [(0, 1), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        Gamma2 = (V2, E2) =  [0, 1, 2, 3, 4, 5, 6, 7] [(0, 1), (0, 4), (0, 5), (0, 6), (0, 7), (1, 2), (1, 4), (1, 5), 
                                                       (1, 6), (1, 7), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 4), 
                                                       (3, 5), (3, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7)]
        f = [V2, f0], where f0 =  [0, 1, 2, 2, 3, 4, 4, 3]
        The edge e =  (2, 3)  is vertical under f.
        The edge e =  (4, 7)  is vertical under f.
        The edge e =  (5, 6)  is vertical under f.
        This [<vertex>, <intersection sizes>]] fails the check: [0, [1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [1, [1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [2, [1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [3, [0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [4, [1, 1, 2, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [5, [1, 1, 2, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [6, [1, 1, 2, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [7, [1, 1, 2, 1]]
        False
        sage: [vertical_multiplicity_of_harmonic_map(Gamma_1join3, Gamma_2join4, f_join_g, v) for v in V_2join4]   
        [0, 0, 1, 1, 1, 1, 1, 1]
        sage: table_of_local_horizontal_multiplicities(Gamma_1join3, Gamma_2join4, f_join_g)                                                       
        [[(0, (0, 1), 1), (0, (0, 3), 2), (0, (0, 4), 2)],
         [(1, (0, 1), 1), (1, (1, 2), 1), (1, (1, 3), 2), (1, (1, 4), 2)],
         [(2, (1, 2), 1), (2, (2, 3), 2), (2, (2, 4), 2)],
         [(3, (1, 2), 0), (3, (2, 3), 2), (3, (2, 4), 2)]]
        sage: Gamma1 = graphs.PathGraph(2)                                                                                                         
        sage: Gamma2 = graphs.CycleGraph(6)                                                                                                        
        sage: V2 = Gamma2.vertices(sort=True)                                                                                                               
        sage: f21_0 = [0,0,0,1,1,1]                                                                                                                
        sage: f21 = [V2, f21_0]                                                                                                                    
        sage: Gamma3 = graphs.PathGraph(2)                                                                                                         
        sage: Gamma4 = graphs.CycleGraph(4)                                                                                                        
        sage: f43_0 = [0,1,1,0]                                                                                                                    
        sage: f43 = [V4, f43_0]                                                                                                                    
        sage: V4 = Gamma4.vertices(sort=True)                                                                                                               
        sage: f43 = [V4, f43_0]                                                                                                                    
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f21, v) for v in V2]                                                        
        [1, 0, 1, 1, 0, 1]
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma3, Gamma4, f43, v) for v in V4]                                                        
        [1, 1, 1, 1]
        sage: Gamma_2join4 = graph_convert_to_standard(Gamma2.join(Gamma4))                                                                        
        sage: Gamma_1join3 = graph_convert_to_standard(Gamma1.join(Gamma3))                                                                        
        sage: V_2join4 = Gamma_2join4.vertices(sort=True)                                                                                                   
        sage: f21_join_f43_0 = CL_of_join_of_morphisms(Gamma1, Gamma2, f21, Gamma3, Gamma4, f43)                                                   
        sage: f21_join_f43 = [V_2join4, f21_join_f43_0]; f21_join_f43                                                                              
        [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 0, 0, 1, 1, 1, 2, 3, 3, 2]]
        sage: is_harmonic_graph_morphism(Gamma_1join3, Gamma_2join4, f21_join_f43, verbose=True)                                                   
        Gamma1 = (V1, E1) =  [0, 1, 2, 3] [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        Gamma2 = (V2, E2) =  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] [(0, 1), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 2),
                                                             (1, 6), (1, 7), (1, 8), (1, 9), (2, 3), (2, 6), (2, 7),
                                                              (2, 8), (2, 9), (3, 4), (3, 6), (3, 7), (3, 8), (3, 9), (4, 5),
                                                              (4, 6), (4, 7), (4, 8), (4, 9), (5, 6), (5, 7), (5, 8), (5, 9),
                                                              (6, 7), (6, 9), (7, 8), (8, 9)]
        f = [V2, f0], where f0 =  [0, 0, 0, 1, 1, 1, 2, 3, 3, 2]
        The edge e =  (0, 1)  is vertical under f.
        The edge e =  (1, 2)  is vertical under f.
        The edge e =  (3, 4)  is vertical under f.
        The edge e =  (4, 5)  is vertical under f.
        The edge e =  (6, 9)  is vertical under f.
        The edge e =  (7, 8)  is vertical under f.
        This [<vertex>, <intersection sizes>]] fails the check: [0, [1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [1, [0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [2, [1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [3, [1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [4, [0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [5, [1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [6, [3, 3, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [7, [3, 3, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [8, [3, 3, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [9, [3, 3, 1]]
        False
        sage: table_of_local_horizontal_multiplicities(Gamma_1join3, Gamma_2join4, f21_join_f43)                                                   
        [[(0, (0, 1), 1), (0, (0, 2), 2), (0, (0, 3), 2)],
         [(1, (0, 1), 0), (1, (0, 2), 2), (1, (0, 3), 2)],
         [(2, (0, 1), 1), (2, (0, 2), 2), (2, (0, 3), 2)],
         [(3, (0, 1), 1), (3, (1, 2), 2), (3, (1, 3), 2)],
         [(4, (0, 1), 0), (4, (1, 2), 2), (4, (1, 3), 2)],
         [(5, (0, 1), 1), (5, (1, 2), 2), (5, (1, 3), 2)]]

 
    """
    f0 = f[1]
    g0 = g[1]
    V2 = Gamma2.vertices(sort=True)
    V02 = [(0,v) for v in V2]
    V4 = Gamma4.vertices(sort=True)
    V14 = [(1,v) for v in V4]
    V_2join4 = V02+V14                   # join(Gamma2,Gamma4) vertices
    #print(V_2join4)
    n2 = len(V2)
    n4 = len(V4)
    E2 = Gamma2.edges(labels=None,sort=True)
    E02 = [((0,e[0]),(0,e[1])) for e in E2]  # Gamma2 edges
    E4 = Gamma4.edges(labels=None,sort=True)
    E14 = [((1,e[0]),(1,e[1])) for e in E4]  # Gamma4 edges
    E01_24 = [((0,v),(1,w)) for w in V4 for v in V2]  # Gamma2-Gamma4 edges
    E_2join4 = E02+E14+E01_24                   # join(Gamma2,Gamma4) edges
    ##    join(Gamma2,Gamma4) = Graph([V_2join4,E_2join4])
    V1 = Gamma1.vertices(sort=True)
    V01 = [(0,v) for v in V1]
    V3 = Gamma4.vertices(sort=True)
    V13 = [(1,v) for v in V3]
    V_1join3 = V01+V13                   # join(Gamma1,Gamma3) vertices
    #print(V_1join3)
    n1 = len(V1)
    n3 = len(V3)
    E1 = Gamma1.edges(labels=None,sort=True)
    E01 = [((0,e[0]),(0,e[1])) for e in E1]  # Gamma1 edges
    E3 = Gamma3.edges(labels=None,sort=True)
    E13 = [((1,e[0]),(1,e[1])) for e in E3]  # Gamma3 edges
    E01_13 = [((0,v),(1,w)) for w in V3 for v in V1]  # Gamma1-Gamma3 edges
    E_1join3 = E01+E13+E01_13                   # join(Gamma1,Gamma3) edges
    ##    join(Gamma1,Gamma3) = Graph([V_1join3,E_1join3])
    image_of_f = [(0,image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v)) for v in V2]
    image_of_g = [(1,image_of_vertex_under_graph_morphism(Gamma3, Gamma4, g, v)) for v in V4]
    #print(image_of_f, image_of_g)
    image_of_f_join_g = image_of_f+image_of_g
    f_join_g_CL = [V_1join3.index(x) for x in image_of_f_join_g]
    return f_join_g_CL



def CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g):
    """
    Returns the CL associated to fxg going from
          Gamma2 x Gamma4 -> Gamma1 x Gamma3
    in the lexicographical ordering.

    NOTE: Does not depend on which product (Cartesian, tensor, etc) is used.

    Notation: f represents a harmonic morphism Gamma2 -> Gamma1
              g represents a harmonic morphism Gamma4 -> Gamma3
    (all these graphs use the standard ordering, so Gamma_i has vertices
    0, 1, ...., n_i - 1). Order the vertices of Gamma2 x Gamma4 
    and of Gamma1 x Gamma3 in the lexicographical ordering. The
    CL for fxg is returned using this ordering.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)    
        sage: Gamma2 = graphs.PathGraph(4)     
        sage: f0 = [0,1,2,2]     
        sage: V2 = Gamma2.vertices(sort=True)  
        sage: f = [V2, f0]         
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)    
        True
        sage: Gamma3 = graphs.PathGraph(2)   
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: g0 = [0,1,1,0]   
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g = [V4, g0]   
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g)  
        True
        sage: CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)    
        [0, 1, 1, 0, 2, 3, 3, 2, 4, 5, 5, 4, 4, 5, 5, 4]

    """
    f0 = f[1]
    g0 = g[1]
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    #E1 = Gamma1.edges(labels=None,sort=True)
    #E2 = Gamma2.edges(labels=None,sort=True)
    V3 = Gamma3.vertices(sort=True)
    V4 = Gamma4.vertices(sort=True)
    n3 = len(V3)
    n4 = len(V4)
    #E3 = Gamma3.edges(labels=None,sort=True)
    #E4 = Gamma4.edges(labels=None,sort=True)
    V1x3 = [(i,j) for i in V1 for j in V3]
    V1x3.sort()
    #print(V1x3)
    V2x4 = [(i,j) for i in V2 for j in V4]
    V2x4.sort()
    fxg = [(f0[x[0]], g0[x[1]]) for x in V2x4]
    #print(fxg)
    fxg_CL = [V1x3.index(x) for x in fxg]
    #V13 = list(range(n1*n3))
    #V24 = list(range(n2*n4))
    return fxg_CL


def matrix_of_graph_of_product_of_morphisms_vertices(Gamma1, Gamma2, f, Gamma3, Gamma4, g):
    """
    Returns the vertex matrix map associated to fxg going from
          Gamma2 x Gamma4 -> Gamma1 x Gamma3
    in the lexicographical ordering.

    Notation: f represents a harmonic morphism Gamma2 -> Gamma1
              g represents a harmonic morphism Gamma4 -> Gamma3
    (all these graphs use the standard ordering, so Gamma_i has vertices
    0, 1, ...., n_i - 1). Order the vertices of Gamma2 x Gamma4 
    and of Gamma1 x Gamma3 in the lexicographical ordering. The
    CL for fxg is returned using this ordering.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: f0 = [0,1,1]       
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]     
        sage: Phi = matrix_of_graph_morphism_vertices(Gamma1, Gamma2, f)
        [1 0]
        [0 1]
        [0 1]
        sage: Gamma3 = graphs.PathGraph(2) 
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g0 = [0,1,1,0]     
        sage: g = [V4, g0]  
        sage: Phi_g = matrix_of_graph_morphism_vertices(Gamma3, Gamma4, g)
        [1 0]
        [0 1]
        [0 1]
        [1 0]
        sage: matrix_of_graph_of_product_of_morphisms_vertices(Gamma1, Gamma2, f, Gamma3, Gamma4, g)              
        [1 0 0 0]
        [0 1 0 0]
        [0 1 0 0]
        [1 0 0 0]
        [0 0 1 0]
        [0 0 0 1]
        [0 0 0 1]
        [0 0 1 0]
        [0 0 1 0]
        [0 0 0 1]
        [0 0 0 1]
        [0 0 1 0]

    """
    Gamma13 = Gamma1.cartesian_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.cartesian_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    fxg = [V2x4, fxg0]
    Phi = matrix_of_graph_morphism_vertices(Gamma1x3, Gamma2x4, fxg)
    return  Phi


## new
def CL_product_projection1_harmonic(Gamma1, Gamma2):
    r"""
    Returns CL in the form [V2, f0] of pr_1 (proj of product onto 1st factor) from 
    Gamma1xGamma2 to Gamma1, and False otherwise, where V2 is the list of vertices
    of Gamma1xGamma2 in standard form.

    Assumes Gamma1, Gamma2 are in standard form.

    NOTE: While Cartesian product is used below, this CL does not depend 
    on which product (Cartesian, tensor, strong, etc) is used.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: CL_product_projection1_harmonic(Gamma1, Gamma2) 
        [[0, 1, 2, 3, 4, 5], [0, 0, 0, 1, 1, 1]]
	sage: f = CL_product_projection1_harmonic(Gamma1, Gamma2)
	sage: Gamma12 = Gamma1.cartesian_product(Gamma2)
	sage: Gamma12_0 = graph_convert_to_standard(Gamma12)  
        sage: is_harmonic_graph_morphism(Gamma1, Gamma12_0, f) 
        True

        sage: is_cartesian_product_projection1_harmonic(Gamma1, Gamma2, f) 

        sage: Gamma1 = graphs.PathGraph(2) 
        sage: Gamma2 = graphs.CycleGraph(4)
	sage: CL_product_projection1_harmonic(Gamma1, Gamma2) 
        [[0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 1, 1, 1, 1]]
	sage: f = CL_product_projection1_harmonic(Gamma1, Gamma2)
	sage: Gamma12 = Gamma1.cartesian_product(Gamma2)
	sage: Gamma12_0 = graph_convert_to_standard(Gamma12)  
        sage: is_harmonic_graph_morphism(Gamma1, Gamma12_0, f) 
        True

    """
    ## build the CL of pr_1
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    Gamma12 = Gamma1.cartesian_product(Gamma2)  ## need this in standard form
    V1x2 = Gamma12.vertices(sort=True)
    f0 = [v[0] for v in V1x2]
    f_nst = [V1x2, f0]    ## this is the CL of pr_1, not in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    V1x2_0 = Gamma12_0.vertices(sort=True)
    f_st = [V1x2_0, f0]    ## this is the CL of pr_1, in standard form
    return f_st


## new
def CL_product_projection2_harmonic(Gamma1, Gamma2):
    r"""
    Returns CL in the form [V2, f0] of pr_2 (proj of product onto 2nd factor) from 
    Gamma1xGamma2 to Gamma1, and False otherwise, where V2 is the list of vertices
    of Gamma1xGamma2 in standard form.

    Assumes Gamma1, Gamma2 are in standard form.

    NOTE: While Cartesian product is used below, this CL does not depend 
    on which product (Cartesian, tensor, strong, etc) is used.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: CL_product_projection2_harmonic(Gamma1, Gamma2) 
        [[0, 1, 2, 3, 4, 5], [0, 1, 2, 0, 1, 2]]
	sage: f = CL_product_projection2_harmonic(Gamma1, Gamma2)
	sage: Gamma12 = Gamma1.cartesian_product(Gamma2)
	sage: Gamma12_0 = graph_convert_to_standard(Gamma12)  
        sage: is_harmonic_graph_morphism(Gamma2, Gamma12_0, f) 
        True
        sage: Gamma1 = graphs.PathGraph(2) 
        sage: Gamma2 = graphs.CycleGraph(4)
	sage: CL_product_projection2_harmonic(Gamma1, Gamma2) 
        [[0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 0, 1, 2, 3]]
	sage: f = CL_product_projection2_harmonic(Gamma1, Gamma2)
	sage: Gamma12 = Gamma1.cartesian_product(Gamma2)
	sage: Gamma12_0 = graph_convert_to_standard(Gamma12)  
        sage: is_harmonic_graph_morphism(Gamma2, Gamma12_0, f) 
        True

    """
    ## build the CL of pr_1
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    Gamma12 = Gamma1.cartesian_product(Gamma2)  ## need this in standard form
    V1x2 = Gamma12.vertices(sort=True)
    f0 = [v[1] for v in V1x2]
    f_nst = [V1x2, f0]    ## this is the CL of pr_2, not in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    V1x2_0 = Gamma12_0.vertices(sort=True)
    f_st = [V1x2_0, f0]    ## this is the CL of pr_2, in standard form
    return f_st


## new
def is_cartesian_product_projection1_harmonic(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_1 (proj of cartesian product onto 1st factor) defines a 
    harmonic morphism from Gamma1xGamma2 to Gamma1, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_cartesian_product_projection1_harmonic(Gamma1, Gamma2) 
        True
        sage: is_cartesian_product_projection1_harmonic(Gamma1, Gamma2, verbose=True) 
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [4, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [5, [1]]
        True

    """
    ## build the CL of pr_1
    f_st = CL_product_projection1_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.cartesian_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st) 
    else:
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st, verbose = True) 


def is_cartesian_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False):
    r"""
    Returns True if fxg (cartesian product) defines a graph-theoretic mapping
    from Gamma2xGamma4 to Gamma1xGamma3 that is harmonic, and False otherwise. 

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: f0 = [0,1,1]       
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]     
        sage: Gamma3 = graphs.PathGraph(2) 
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g0 = [0,1,1,0]     
        sage: g = [V4, g0]  
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]  
        [1, 1, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4] 
        [1, 1, 1, 1]
        sage: is_cartesian_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g) 
        False
        sage: Gamma1 = graphs.PathGraph(2) 
        sage: Gamma2 = graphs.CycleGraph(4) 
        sage: f0 = [0,1,1, 0]    
        sage: V2 = Gamma2.vertices(sort=True)    
        sage: f = [V2, f0]                         
        sage: is_cartesian_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g)  
        True
        sage: Gamma13 = Gamma1.cartesian_product(Gamma3) 
        sage: Gamma1x3 = graph_convert_to_standard(Gamma13)
        sage: Gamma24 = Gamma2.cartesian_product(Gamma4)   
        sage: Gamma2x4 = graph_convert_to_standard(Gamma24) 
        sage: V2x4 = Gamma2x4.vertices(sort=True)
        sage: fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g) 
        sage: fxg = [V2x4, fxg0]  
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1x3, Gamma2x4, fxg, v) for v in V2x4]  
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1x3, Gamma2x4, fxg, v) for v in V2x4] 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    """
    Gamma13 = Gamma1.cartesian_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.cartesian_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    fxg = [V2x4, fxg0]
    if verbose:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose=True)
    else:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg)


def is_cartesian_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False):
    r"""
    Returns True if fxg (Cartesian product map) defines a graph-theoretic mapping
    from Gamma2xGamma4 to Gamma1xGamma3 that is a morphism, and False otherwise. 

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: f0 = [0,1,1]       
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]     
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [0, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [1, 1, 0]
        sage: Gamma3 = graphs.PathGraph(2) 
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g0 = [0,1,1,0]     
        sage: g = [V4, g0]  
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4] 
        [1, 1, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]  
        [1, 1, 1, 1]
        sage: is_cartesian_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=True)  
        (0, 2) [(0, 1), (0, 3), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5)]
        Does not send edges to {edges} union {vertices}
        False
        sage: is_cartesian_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g) 
        False

    """
    Gamma13 = Gamma1.cartesian_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.cartesian_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    fxg = [V2x4, fxg0]
    if verbose:
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose=True)
    else:
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg)


## new
def is_tensor_product_projection1_harmonic(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_1 (proj of tensor product onto 1st factor) defines a 
    harmonic morphism from Gamma1xGamma2 to Gamma1, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_tensor_product_projection1_harmonic(Gamma1, Gamma2) 
        True
        sage: is_tensor_product_projection1_harmonic(Gamma1, Gamma2, verbose=True) 
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [4, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [5, [1]]
        True

    """
    ## build the CL of pr_1
    f_st = CL_product_projection1_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.tensor_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st) 
    else:
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st, verbose = True)
        

def is_tensor_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False):
    r"""
    Returns True if fxg (tensor product) defines a graph-theoretic mapping
    from Gamma2xGamma4 to Gamma1xGamma3 that is harmonic, and False otherwise. 

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.

    EXAMPLES:
       sage: V2 = [0, 1, 2, 3, 4, 5]                                                                            
       sage: E2 = [(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (2, 3), (2, 5), (3, 4), (3, 5), (4, 5)] 
       sage: Gamma2 = Graph([V2,E2]) # d4r6a                                                                     
       sage: Gamma2.chromatic_number()                                                                           
       3
       sage: Gamma1 = graphs.CycleGraph(3)                                                                       
       sage: f0 = [2, 0, 1, 2, 1, 0]                                                                             
       sage: f = [V2, f0]   
       sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                          
       [2, 2, 2, 2, 2, 2]
       sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                           
       [0, 0, 0, 0, 0, 0]                                                                 
       sage: is_tensor_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma1, Gamma2, f) 
       True
       sage: is_tensor_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma1, Gamma2, f)   
       True
       sage: Gamma13 = Gamma1.tensor_product(Gamma1)                                                             
       sage: Gamma24 = Gamma2.tensor_product(Gamma2)                                                             
       sage: V24 = Gamma24.vertices(sort=True)                                                                            
       sage: fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma1, Gamma2, f)                             
       sage: Gamma2x4 = graph_convert_to_standard(Gamma24)                                                       
       sage: Gamma1x3 = graph_convert_to_standard(Gamma13)                                                       
       sage: V2x4 = Gamma2x4.vertices(sort=True)                                                                          
       sage: fxg = [V2x4, fxg0]                                                                                  
       sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)                                                       
       True
       sage: is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg)                                                 
       True

    """
    Gamma13 = Gamma1.tensor_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.tensor_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    fxg = [V2x4, fxg0]
    if verbose:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose=True)
    else:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg)


def is_tensor_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False):
    r"""
    Returns True if fxg (tensor product map) defines a graph-theoretic mapping
    from Gamma2xGamma4 to Gamma1xGamma3 that is a morphism, and False otherwise. 

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: f0 = [0,1,1]       
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]     
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [0, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [1, 1, 0]
        sage: Gamma3 = graphs.PathGraph(2) 
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g0 = [0,1,1,0]     
        sage: g = [V4, g0]  
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4] 
        [1, 1, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]  
        [1, 1, 1, 1]
        sage: is_tensor_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=True)  
        The Gamma2 edge (0, 2)  does not map to Gamma1 edge set 
          [(0, 1), (0, 3), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5)]  or vertex set  [0, 1, 2, 3, 4, 5]
        Error: Does not send edges to {edges} union {vertices}
        False
        sage: is_tensor_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g) 
        False

    """
    Gamma13 = Gamma1.tensor_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.tensor_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    #print(V2x4)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    #print(fxg0)
    fxg = [V2x4, fxg0]
    if verbose:
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose=True)
    else:
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg)

## new
def is_strong_product_projection1_harmonic(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_1 (proj of strong product onto 1st factor) defines a 
    harmonic morphism from Gamma1xGamma2 to Gamma1, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_strong_product_projection1_harmonic(Gamma1, Gamma2) 
        True
        sage: is_strong_product_projection1_harmonic(Gamma1, Gamma2, verbose=True) 
        This [<vertex>, <intersection sizes>]] passes the check: [0, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [3]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [4, [3]]
        This [<vertex>, <intersection sizes>]] passes the check: [5, [2]]
        True

    """
    ## build the CL of pr_1
    f_st = CL_product_projection1_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.strong_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st) 
    else:
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st, verbose = True)


def is_strong_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False):
    r"""
    Returns True if fxg (strong product) defines a graph-theoretic mapping
    from Gamma2 to Gamma1 that is harmonic, and False otherwise. 

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: Gamma3 = graphs.CycleGraph(4)
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: V2 = Gamma2.vertices(sort=True)
        sage: V4 = Gamma4.vertices(sort=True)
        sage: f0 = [0, 1, 1]
        sage: g0 = [0,1,2,3] 
        sage: f = [V2, f0] 
        sage: g = [V4, g0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g)
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [1, 1, 0]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [0, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]
        [1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]
        [0, 0, 0, 0]
        sage: is_strong_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)  
        False
        sage: is_strong_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=True)   
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [4, [1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [5, [1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [6, [1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [7, [1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [8, [0, 0, 0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [9, [0, 0, 0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [10, [0, 0, 0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [11, [0, 0, 0, 2, 2]]
        False
        sage: is_strong_product_of_graph_morphisms_harmonic(Gamma3, Gamma4, g, Gamma3, Gamma4, g)                 
        True
        sage: Gamma1 = graphs.CycleGraph(3)                                                                       
        sage: Gamma2 = graphs.CycleGraph(6)                                                                       
        sage: V2 = Gamma2.vertices(sort=True)                                                                              
        sage: f0 = [0, 1, 2, 0, 1, 2]                                                                             
        sage: f = [V2, f0]                                                                                        
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)                                                       
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]   
        [0, 0, 0, 0, 0, 0]
        sage: Gamma3 = graphs.CycleGraph(4)                                                                       
        sage: Gamma4 = graphs.CycleGraph(8)                                                                       
        sage: V4 = Gamma4.vertices(sort=True)                                                                              
        sage: g0 = [0,1,2,3,0,1,2,3]                                                                              
        sage: g = [V4, g0]                                                                                        
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g)                                                       
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                          
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                           
        [0, 0, 0, 0, 0, 0]
        sage: is_strong_product_of_graph_morphisms_harmonic(Gamma3, Gamma4, g, Gamma3, Gamma4, g)                 
        True
        sage: is_strong_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g)   
        True

    """
    Gamma13 = Gamma1.strong_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.strong_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    fxg = [V2x4, fxg0]
    if verbose:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose=True)
    else:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg)


def is_strong_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False):
    r"""
    Returns True if fxg (strong product map) defines a graph-theoretic mapping
    from Gamma2 to Gamma1 that is a morphism, and False otherwise. 

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: f0 = [0,1,1]       
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]     
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [0, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [1, 1, 0]
        sage: Gamma3 = graphs.PathGraph(2) 
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g0 = [0,1,1,0]     
        sage: g = [V4, g0]  
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4] 
        [1, 1, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]  
        [1, 1, 1, 1]
        sage: is_strong_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g) 
        False
        sage: is_strong_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=True)
        The edge e =  (0, 3)  has no image in Gamma1 under f.
        False

    """
    Gamma13 = Gamma1.strong_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.strong_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    #print(V2x4)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    #print(fxg0)
    fxg = [V2x4, fxg0]
    if verbose:
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose=True)
    else:
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg)

def is_lexicographic_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False):
    r"""
    Returns True if fxg (lexicographic product) defines a graph-theoretic mapping
    from Gamma2xGamma4 to Gamma1xGamma3 that is harmonic, and False otherwise. 

    The lex product is not symmetric.

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)                                                                        
        sage: Gamma2 = graphs.PathGraph(3)                                                                        
        sage: Gamma3 = graphs.CycleGraph(4)                                                                       
        sage: Gamma4 = graphs.CycleGraph(4)                                                                       
        sage: V2 = Gamma2.vertices(sort=True)                                                                              
        sage: V4 = Gamma4.vertices(sort=True)                                                                              
        sage: f0 = [0, 1, 1]                                                                                      
        sage: g0 = [0,1,2,3]                                                                                      
        sage: f = [V2, f0]                                                                                        
        sage: g = [V4, g0]                                                                                        
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)                                                       
        True
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g)                                                       
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                          
        [1, 1, 0]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                           
        [0, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]                          
        [1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]                           
        [0, 0, 0, 0]
        sage: is_lexicographic_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=False)  
        False
        sage: is_lexicographic_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose=True)   
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1, 1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [1, 1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [1, 1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [1, 1, 1, 1, 1, 1]]
        This [<vertex>, <intersection sizes>]] fails the check: [4, [1, 1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [5, [1, 1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [6, [1, 1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [7, [1, 1, 1, 1, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [8, [0, 0, 0, 0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [9, [0, 0, 0, 0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [10, [0, 0, 0, 0, 2, 2]]
        This [<vertex>, <intersection sizes>]] fails the check: [11, [0, 0, 0, 0, 2, 2]]
        False
        sage: is_lexicographic_product_of_graph_morphisms_harmonic(Gamma3, Gamma4, g, Gamma3, Gamma4, g)                 
        True
        sage: Gamma1 = graphs.CycleGraph(3)                                                                       
        sage: Gamma2 = graphs.CycleGraph(6)                                                                       
        sage: V2 = Gamma2.vertices(sort=True)                                                                              
        sage: f0 = [0, 1, 2, 0, 1, 2]                                                                             
        sage: f = [V2, f0]                                                                                        
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)                                                       
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]   
        [0, 0, 0, 0, 0, 0]
        sage: Gamma3 = graphs.CycleGraph(4)                                                                       
        sage: Gamma4 = graphs.CycleGraph(8)                                                                       
        sage: V4 = Gamma4.vertices(sort=True)                                                                              
        sage: g0 = [0,1,2,3,0,1,2,3]                                                                              
        sage: g = [V4, g0]                                                                                        
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g)                                                       
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                          
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]                           
        [0, 0, 0, 0, 0, 0]
        sage: is_lexicographic_product_of_graph_morphisms_harmonic(Gamma3, Gamma4, g, Gamma3, Gamma4, g)                 
        False
        sage: is_lexicographic_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma3, Gamma4, g)   
        False
        sage: Gamma1 = graphs.CompleteGraph(4)
        sage: V2 = [0, 1, 2, 3, 4, 5, 6, 7] 
        sage: E2 = [(0, 1), (0, 2), (0, 7), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7)]
        sage: Gamma2 = Graph([V2,E2]) # d3reg8a
        sage: Gamma3 = graphs.WheelGraph(4)
        sage: V3 = Gamma3.vertices(sort=True)
        sage: g0 = [1,2,3,0]
        sage: g = [V3,g0]
        sage: f0 = [0,1,2,3,0,2,1,3]
        sage: f = [V2, f0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: is_harmonic_graph_morphism(Gamma3, Gamma1, g)
        True                   
        sage: is_lexicographic_product_of_graph_morphisms_harmonic(Gamma1, Gamma2, f, Gamma1, Gamma3, g, verbose = False)
        True 

    """
    Gamma13 = Gamma1.lexicographic_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.lexicographic_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    fxg = [V2x4, fxg0]
    if verbose:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose=True)
    else:
        return is_harmonic_graph_morphism(Gamma1x3, Gamma2x4, fxg)


def is_lexicographic_product_projection1_harmonic(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_1 (proj of lexicographic product onto 1st factor) defines a 
    harmonic morphism from Gamma1xGamma2 to Gamma1, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_lexicographic_product_projection1_harmonic(Gamma1, Gamma2) 
        True
        sage: is_lexicographic_product_projection1_harmonic(Gamma1, Gamma2, verbose=True) 
        This [<vertex>, <intersection sizes>]] passes the check: [0, [3]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [3]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [3]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [3]]
        This [<vertex>, <intersection sizes>]] passes the check: [4, [3]]
        This [<vertex>, <intersection sizes>]] passes the check: [5, [3]]
        True

    """
    ## build the CL of pr_1
    f_st = CL_product_projection1_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.lexicographic_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st) 
    else:
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st, verbose = True)


def is_lexicographic_product_projection2_harmonic(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_2 (proj of lexicographic product onto 2nd factor) defines a 
    harmonic morphism from Gamma1xGamma2 to Gamma2, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_lexicographic_product_projection2_harmonic(Gamma1, Gamma2) 
        True
        sage: is_lexicographic_product_projection2_harmonic(Gamma1, Gamma2, verbose=True) 
        This [<vertex>, <intersection sizes>]] passes the check: [0, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [2, 2]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [2]]
        This [<vertex>, <intersection sizes>]] passes the check: [4, [2, 2]]
        This [<vertex>, <intersection sizes>]] passes the check: [5, [2]]
        True

    """
    ## build the CL of pr_1
    f_st = CL_product_projection2_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.lexicographic_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_harmonic_graph_morphism(Gamma2, Gamma12_0, f_st) 
    else:
        return is_harmonic_graph_morphism(Gamma2, Gamma12_0, f_st, verbose = True)


def is_disjunctive_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose = False):
    r"""
    Returns True if fxg (disjunctive product map) defines a graph-theoretic mapping
    from Gamma2xGamma4 to Gamma1xGamma3 that is a morphism, and False otherwise. 

    Assumes Gamma1, Gamma2, Gamma3, Gamma4 are in standard form.
    Converts Gamma2xGamma4 and Gamma1xGamma3 to standard form (eg, for verbose=True output).

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: f0 = [0,1,1]       
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]     
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [0, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [1, 1, 0]
        sage: Gamma3 = graphs.PathGraph(2) 
        sage: Gamma4 = graphs.CycleGraph(4) 
        sage: V4 = Gamma4.vertices(sort=True) 
        sage: g0 = [0,1,1,0]     
        sage: g = [V4, g0]  
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4] 
        [1, 1, 1, 1]
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]  
        [1, 1, 1, 1]
        sage: is_disjunctive_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g) 
        False
        sage: is_disjunctive_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma3, Gamma4, g, verbose = True) 
        The edge e =  (0, 3)  has no image in Gamma1 under f.
        False
        sage: Gamma1 = graphs.CompleteGraph(4)
        sage: V2 = [0, 1, 2, 3, 4, 5, 6, 7] 
        sage: E2 = [(0, 1), (0, 2), (0, 7), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7)]
        sage: Gamma2 = Graph([V2,E2]) # d3reg8a
        sage: Gamma3 = graphs.WheelGraph(4)
        sage: V3 = Gamma3.vertices(sort=True)
        sage: g0 = [1,2,3,0]
        sage: g = [V3,g0]
        sage: f0 = [0,1,2,3,0,2,1,3]
        sage: f = [V2, f0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: is_harmonic_graph_morphism(Gamma3, Gamma1, g)
        True
        sage: is_disjunctive_product_of_graph_morphisms_a_morphism(Gamma1, Gamma2, f, Gamma1, Gamma3, g, verbose = False)
        True

    """
    Gamma13 = Gamma1.disjunctive_product(Gamma3)
    Gamma1x3 = graph_convert_to_standard(Gamma13)
    Gamma24 = Gamma2.disjunctive_product(Gamma4)
    Gamma2x4 = graph_convert_to_standard(Gamma24)
    V2x4 = Gamma2x4.vertices(sort=True)
    #print(V2x4)
    fxg0 = CL_of_product_of_morphisms(Gamma1, Gamma2, f, Gamma3, Gamma4, g)
    #print(fxg0)
    fxg = [V2x4, fxg0]
    if not(verbose):
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg)
    else:
        return is_graph_morphism(Gamma1x3, Gamma2x4, fxg, verbose = True)
	

def is_disjunctive_product_projection1_morphism(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_1 (proj of disjunctive product onto 1st factor) defines a 
    graph morphism from Gamma1xGamma2 to Gamma1, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    Converts Gamma1xGamma2 to standard form (eg, for verbose=True output).

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_disjunctive_product_projection1_morphism(Gamma1, Gamma2) 
        False
        sage: is_disjunctive_product_projection1_morphism(Gamma1, Gamma2, verbose=True) 
        The edge e =  (0, 1)  has no image in Gamma1 under f.
        False

    """
    ## build the CL of pr_1
    f_st = CL_product_projection1_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.disjunctive_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_graph_morphism(Gamma1, Gamma12_0, f_st) 
    else:
        return is_graph_morphism(Gamma1, Gamma12_0, f_st, verbose = True)


def is_disjunctive_product_projection2_morphism(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_2 (proj of disjunctive product onto 2nd factor) defines a 
    graph morphism from Gamma1xGamma2 to Gamma2, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    Converts Gamma1xGamma2 to standard form (eg, for verbose=True output).

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_disjunctive_product_projection2_morphism(Gamma1, Gamma2) 
        False
        sage: is_disjunctive_product_projection2_morphism(Gamma1, Gamma2, verbose=True) 
        The edge e =  (0, 3)  has no image in Gamma1 under f.
        False

    """
    ## build the CL of pr_2
    f_st = CL_product_projection2_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.disjunctive_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_graph_morphism(Gamma2, Gamma12_0, f_st) 
    else:
        return is_graph_morphism(Gamma2, Gamma12_0, f_st, verbose = True)


def is_disjunctive_product_projection1_harmonic(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_1 (proj of disjunctive product onto 1st factor) defines a 
    harmonic morphism from Gamma1xGamma2 to Gamma1, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    Converts Gamma1xGamma2 to standard form (eg, for verbose=True output).

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_disjunctive_product_projection1_harmonic(Gamma1, Gamma2) 
        False
        sage: is_disjunctive_product_projection1_harmonic(Gamma1, Gamma2, verbose=True) 
        False

    """
    ## build the CL of pr_1
    f_st = CL_product_projection1_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.disjunctive_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st) 
    else:
        return is_harmonic_graph_morphism(Gamma1, Gamma12_0, f_st, verbose = True)


def is_disjunctive_product_projection2_harmonic(Gamma1, Gamma2, verbose=False):
    r"""
    Returns True if pr_2 (proj of disjunctive product onto 2nd factor) defines a 
    harmonic morphism from Gamma1xGamma2 to Gamma2, and False otherwise. 

    Assumes Gamma1, Gamma2 are in standard form.

    Converts Gamma1xGamma2 to standard form (eg, for verbose=True output).

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3)
        sage: is_disjunctive_product_projection2_harmonic(Gamma1, Gamma2) 
        False
        sage: is_disjunctive_product_projection2_harmonic(Gamma1, Gamma2, verbose=True) 
        False

    """
    ## build the CL of pr_2
    f_st = CL_product_projection2_harmonic(Gamma1, Gamma2)
    Gamma12 = Gamma1.disjunctive_product(Gamma2)  ## need this in standard form
    Gamma12_0 = graph_convert_to_standard(Gamma12)
    if not(verbose):
        return is_harmonic_graph_morphism(Gamma2, Gamma12_0, f_st) 
    else:
        return is_harmonic_graph_morphism(Gamma2, Gamma12_0, f_st, verbose = True)


def morphism_of_line_graphs(Gamma1, Gamma2, f, verbose=False):
    """
    Returns L(f), the line graph morphism
    L(f): L(Gamma2) -> L(Gamma1) 
    associated to the morphism 
    f: Gamma2 -> Gamma1
    Argument verbose=True to returns (L(f),  L(Gamma1), L(Gamma2)).

    Internally, converts both L(Gamma2), L(Gamma1) to standard form. 

    Gamma1, Gamma2 must be in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(3) 
        sage: f0 = [0,1,1]  
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]    
        sage: morphism_of_line_graphs(Gamma1, Gamma2, f, verbose=True)  
        ([[0, 1], [0, 0]], Graph on 1 vertex, Graph on 2 vertices)
        sage: morphism_of_line_graphs(Gamma1, Gamma2, f)  
        [[0, 1], [0, 0]]
        sage: Gamma1 = graphs.PathGraph(3)   
        sage: Gamma2 = graphs.CycleGraph(4)  
        sage: f0 = [0, 1, 2, 1]    
        sage: V2 = Gamma2.vertices(sort=True)   
        sage: f = [V2, f0]          
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: morphism_of_line_graphs(Gamma1, Gamma2, f, verbose=True) 
        ([[0, 1, 2, 3], [0, 0, 1, 0]], Graph on 2 vertices, Graph on 4 vertices)
        sage: Gamma1 = graphs.CycleGraph(3) 
        sage: Gamma2 = graphs.CycleGraph(6) 
        sage: f0 = [0, 1, 2, 0, 1, 2] 
        sage: V2 = Gamma2.vertices(sort=True)  
        sage: f = [V2, f0]          
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: [horizonal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]  
        [0, 0, 0, 0, 0, 0]
        sage: morphism_of_line_graphs(Gamma1, Gamma2, f, verbose=True) 
        ([[0, 1, 2, 3, 4, 5], [0, 1, 2, 0, 0, 2]],
         Graph on 3 vertices,
         Graph on 6 vertices)
        sage: ans = morphism_of_line_graphs(Gamma1, Gamma2, f, verbose=True) 
        sage: Lf = ans[0] 
        sage: LGamma2_st = ans[2]  
        sage: LGamma1_st = ans[1] 
        sage: is_graph_morphism(LGamma1_st, LGamma2_st, Lf) 
        True
        sage: is_harmonic_graph_morphism(LGamma1_st, LGamma2_st, Lf) 
        True
        sage: is_harmonic_graph_morphism(LGamma1_st, LGamma2_st, Lf, verbose=True) 
        Gamma1 = (V1, E1) =  [0, 1, 2] [(0, 1), (0, 2), (1, 2)]
        Gamma2 = (V2, E2) =  [0, 1, 2, 3, 4, 5] [(0, 1), (0, 2), (1, 5), (2, 3), (3, 4), (4, 5)]
        f = [V2, f0], where f0 =  [0, 1, 2, 1, 0, 2]
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [4, [1, 1]]
        This [<vertex>, <intersection sizes>]] passes the check: [5, [1, 1]]
        True
        sage: VLG2_st = LGamma2_st.vertices(sort=True) 
        sage: [horizonal_multiplicity_of_harmonic_map(LGamma1_st, LGamma2_st, Lf, v) for v in VLG2_st]             
        [1, 1, 1, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(LGamma1_st, LGamma2_st, Lf, v) for v in VLG2_st]              
        [0, 0, 0, 0, 0, 0]

    """
    ## build the CL of L(f)
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    n1 = len(V1)
    n2 = len(V2)
    if V1 != list(range(n1)):
        return "Error! -- Gamma1 must be in standard form."    
    if V2 != list(range(n2)):
        return "Error! -- Gamma2 must be in standard form."      
    LGamma1 = Gamma1.line_graph(labels=False)
    LGamma2 = Gamma2.line_graph(labels=False)
    LV1 = LGamma1.vertices(sort=True)
    LE1 = list(LGamma1.edges(labels=None,sort=True))
    #LE1.sort()
    LV2 = LGamma2.vertices(sort=True)
    LE2 = list(LGamma2.edges(labels=None,sort=True))
    #LE2.sort()
    #print(LV1, LE1)
    #print(LV2, LE2)
    LGamma10 = Graph([LV1, LE1])
    LGamma20 = Graph([LV2, LE2])
    LGamma1_st = graph_convert_to_standard(LGamma10)
    LGamma2_st = graph_convert_to_standard(LGamma20)
    #print(LGamma2_st.vertices(sort=True))
    #print(LGamma2_st.edges(labels=None,sort=True))
    LV1_st = LGamma1_st.vertices(sort=True)
    LV2_st = LGamma2_st.vertices(sort=True)
    CL_Lf = []
    CL_Lf_st = []
    for v in LV2:
        #print(v, v[0], v[1])
        Lfv0 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v[0])
        Lfv1 = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v[1])
        e = (Lfv0, Lfv1)
        ee = (e[1],e[0])
        if e in LV1:
            CL_Lf = CL_Lf+[e]
            CL_Lf_st = CL_Lf_st + [LV1.index(e)]
        if ee in LV1:
            CL_Lf = CL_Lf+[ee]
            CL_Lf_st = CL_Lf_st + [LV1.index(ee)]	    
        if not(e in LV1) and not(ee in LV1):
            print("Error: ", e, " has no image.")
            CL_Lf = CL_Lf+[-1]
            CL_Lf_st = CL_Lf_st + [-1]
    CL = [LV2_st, CL_Lf_st]
    if verbose:
        return CL, LGamma1_st, LGamma2_st
    else:
        return CL

def LC_multipartite_graph(L, cyclic=False):
    r"""
    The function returns what we call a "locally complete 
    multipartite graph", the complete multipartite graph but
    with all "long" edges removed: The vertices are
    V = {0, ..., n-1}, where V = \cup_{j=0}^{k-1} I_j is
    a disjoint partition, where n_j = |I_j| (so that
    n = n_1 + ... + n_{k-1}). Define the edges to be
    (u,v) for u in I_{j_1} and v in I_{j_2}, where
    j_1 \not= j_2, and j_2 = j_1 \pm 1. 

    Here L = [n_1, ... , n_{k-1}]. Each set I_j is
    a set of consecutive integers in V:
    I_0 = [0, ..., n_0-1], ..., [n-n_{k-1}, ..., n-1].
    Each I_j i an independent set of vertices in the graph.

    The option "cyclic = True" constructs the same matrix but where
    there are also edges between I_0 and I_{k-1} (ie, the
    index set {0, ..., k-1} is identified with ZZ/kZZ).

    EXAMPLES:
        sage: Gamma = LC_multipartite_graph([2,3,4])                                       
        sage: Gamma.vertices(sort=True)                                                             
        [0, 1, 2, 3, 4, 5, 6, 7, 8]
        sage: Gamma.edges(labels=None,sort=True)                                                     
        [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), 
         (2, 5), (2, 6), (2, 7), (2, 8), (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (4, 6), (4, 7), (4, 8)]
        sage: 
        sage: Gamma2 = LC_multipartite_graph([2,3,2])  
        sage: V2 = Gamma2.vertices(sort=True)   
        sage: Gamma1 = graphs.PathGraph(3) 
        sage: f0 = [0,0,1,1,1,2,2] 
        sage: f = [V2, f0]       
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [3, 3, 2, 2, 2, 3, 3]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]  
        [0, 0, 0, 0, 0, 0, 0]
        sage: 
        sage: Gamma2 = LC_multipartite_graph([2,2,3]) 
        sage: V2 = Gamma2.vertices(sort=True)  
        sage: Gamma1 = graphs.PathGraph(3) 
        sage: f0 = [0,0,1,1,2,2,2] 
        sage: f = [V2, f0]        
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        False
        sage: is_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [0, 0, 0, 0, 0, 0, 0]
        sage: 
        sage: Gamma2 = LC_multipartite_graph([2,2,2], cyclic = True)
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: Gamma1 = graphs.CycleGraph(3)
        sage: f0 = [0,0,1,1,2,2]
        sage: f = [V2, f0] 
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f)
        True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [2, 2, 2, 2, 2, 2]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [0, 0, 0, 0, 0, 0]
        sage: 
        sage: Gamma2 = LC_multipartite_graph([2,1,2,1], cyclic = True)  
        sage: V2 = Gamma2.vertices(sort=True)  
        sage: Gamma1 = graphs.CycleGraph(4) 
        sage: f0 = [0,0,1,2,2,3] 
        sage: f = [V2, f0] 
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2] 
        [1, 1, 2, 1, 1, 2]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
        [0, 0, 0, 0, 0, 0]

    """
    k = len(L)
    n = sum(L)
    V = list(range(n))
    Is = [list(range(L[0]))]
    j0 = 0
    for i in range(1,k):
        j0 = j0+L[i-1]
        j1 = j0+L[i]
        Is = Is + [list(range(j0,j1))]
    #print(Is)
    E = [(u,v) for u in Is[0] for v in Is[1]]
    if cyclic==False:
        for i in range(1,k-1):
            E = E+[(u,v) for u in Is[i] for v in Is[i+1]]
    else:
        for i in range(1,k-1):
            E = E+[(u,v) for u in Is[i] for v in Is[i+1]]
            E = E + [(u,v) for u in Is[0] for v in Is[k-1]]
    return Graph([V,E])

def blowup_graph(Gamma, L):
    r"""
    This function generalizes blowup_balanced_graph(Gamma, r)
    to a vector-valued argument r. It also generalizes
    LC_multipartite_graph to "base" graphs other than 
    the path graph or the cycle graph.
 
    Here Gamma is a graph with k vertices and 
    L = [n_1, ... , n_{k-1}] is a list of integers > 0. 
    Let n = n_0 + ... + n_{k-1}. Each set I_j is a set 
    of consecutive integers in V2: I_0 = [0, ..., n_0-1], 
    ..., I_{k-1} = [n-n_{k-1}, ..., n-1].
    Each I_j is an independent set of vertices in the graph.
    Let V2 = \cup_{x in V1} I_x.
    Connect a vertex v in I_x \subset V2 to
    each vertex w in I_y by an edge (v,w) in E2
    if and only if (x,y) in E1. This defines
    Gamma2 = (V2, E2).

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(4)      
        sage: L = [2,3,2,3]                         
        sage: Gamma2a = LC_multipartite_graph(L)    
        sage: Gamma2b = blowup_graph(Gamma1, L)              
        sage: Gamma2a == Gamma2b         
        False
        sage: Gamma2a = LC_multipartite_graph(L, cyclic = True)
        sage: Gamma2a == Gamma2b 
        True
        sage: f0 = [0,0,1,1,1,2,2,3,3,3]   
        sage: V2b = Gamma2b.vertices(sort=True)         
        sage: f = [V2b, f0] 
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2b, f) 
        False
        sage: is_graph_morphism(Gamma1, Gamma2b, f)  
        True
        sage: Gamma1 = graphs.DiamondGraph()      
        sage: L = [3,2,3,2]     
        sage: f0 = [0,0,0,1,1,2,2,2,3,3] 
        sage: Gamma2 = blowup_graph(Gamma1, L)                                   
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]    
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        False
        sage: is_graph_morphism(Gamma1, Gamma2, f)  
        True
        sage: Gamma1 = graphs.DiamondGraph() 
        sage: L = [2,2,2,2]      
        sage: f0 = [0,0,1,1,2,2,3,3]   
        sage: Gamma2 = blowup_graph(Gamma1, L)                                   
        sage: V2 = Gamma2.vertices(sort=True)    
        sage: f = [V2, f0]   
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True
        sage: L = [3,3,3,3]   
        sage: Gamma2 = blowup_graph(Gamma1, L)                                   
        sage: f0 = [0,0,0,1,1,1,2,2,2,3,3,3] 
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]  
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f) 
        True

    """
    k = len(L)
    V1 = Gamma.vertices(sort=True)
    E1 = Gamma.edges(labels = None, sort = True)
    if k != len(V1):
        print("Length of list L must equal the number of vertices of Gamma")
        return Gamma
    n = sum(L)
    V2 = list(range(n))
    Is = [list(range(L[0]))]
    j0 = 0
    for i in range(1,k):
        j0 = j0+L[i-1]
        j1 = j0+L[i]
        Is = Is + [list(range(j0,j1))]
    #print(Is)
    E2 = []
    for e in E1:
        i = V1.index(e[0])
        j = V1.index(e[1])
        E2 = E2 + [(u,v) for u in Is[i] for v in Is[j]]
    return Graph([V2, E2])

def blowdown_morphism(Gamma, L):
    r"""
    While blowup_graph(Gamma, L) replaces the i-th vertex of
    Gamma by "copies" indexed by the i-th set L[i], this
    blowdown morphism does the opposite: it sends eany of these
    copies to the original vertex.
 
    Here Gamma is a graph with k vertices and 
    L = [n_0, ... , n_{k-1}] is a list of integers > 0. 
    Let n = n_0 + ... + n_{k-1}. Each set I_j is a set 
    of consecutive integers in V2: I_0 = [0, ..., n_0-1], 
    ..., I_{k-1} = [n-n_{k-1}, ..., n-1].
    Each I_j is an independent set of vertices in the graph.
    Let V2 = \cup_{x in V1} I_x.
    Connect a vertex v in I_x \subset V2 to
    each vertex w in I_y by an edge (v,w) in E2
    if and only if (x,y) in E1. This defines
    Gamma2 = (V2, E2).

    EXAMPLES:
        sage: Gamma = graphs.CycleGraph(4)      
        sage: L = [2,3,2,3]                         
        sage: GammaL = blowup_graph(Gamma, L)              
        sage: blowdown_morphism(Gamma, L)
        [0, 0, 1, 1, 1, 2, 2, 3, 3, 3]

    """
    k = len(L)
    V1 = Gamma.vertices(sort=True)
    E1 = Gamma.edges(labels = None, sort = True)
    if k != len(V1):
        print("Length of list L must equal the number of vertices of Gamma")
        return Gamma
    n = sum(L)
    V2 = list(range(n))
    Is = [list(range(L[0]))]
    j0 = 0
    for i in range(1,k):
        j0 = j0+L[i-1]
        j1 = j0+L[i]
        Is = Is + [list(range(j0,j1))]
    f0 = []
    count = 0
    for s in Is:
        m = len(s)
        f0 = f0+[count]*m
        count = count + 1
    return f0

def degree_of_harmonic_morphism(Gamma1, Gamma2, f):
    """
    Returns the degree of the map phi, computed as the total
    horizontal multiplicity of a fiber.

    Assumes both Gamma1 and Gamma2 are in standard form.

    EXAMPLES:
        sage: Gamma = graphs.CycleGraph(4)
        sage: L = [2,3,2,3]
        sage: GammaL = blowup_graph(Gamma, L)
        sage: VL = GammaL.vertices(sort=True)
        sage: f0 = blowdown_morphism(Gamma, L)
        sage: f = [VL, f0]
        sage: degree_of_harmonic_morphism(Gamma, GammaL, f)
        6

    """
    V2 = Gamma2.vertices(sort=True)
    V2_0 = preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, 0)
    HMs = [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v) for v in V2]
    return sum([HMs[i] for i in V2_0])


def subdivision_graph(Gamma1, e):
    """
    Returns a pair (Gamma2, f), where
     Gamma2 is the subdivision graph of Gamma1 obtained by subdividing the edge e of Gamma1, 
     f is the graph morphism phi: Gamma2 -> Gamma1, where the new vertex of Gamma2
       has been sent to the "tail" (smallest) vertex incident to e. 
       f is written in (vertices, CL) notation
    
    This leaves Gamma1 itself unchanged. 

    This assumes Gamma1 is in standard form.

    EXAMPLES:
        sage: Gamma = graphs.CycleGraph(3)
        sage: e = (0,1)
        sage: Gamma2, f = subdivision_graph(Gamma, e)
        [[0, 1, 2, 3], [0, 1, 2, 0]]
        sage: Gamma2.is_isomorphic(graphs.CycleGraph(4))
        True
        sage: is_harmonic_graph_morphism(Gamma, Gamma2, f, verbose=False)
        False
        sage: is_graph_morphism(Gamma, Gamma2, f, verbose=False)
        True
        sage: Gamma = graphs.PathGraph(3)
        sage: e = (0,1)
        sage: Gamma2, f = subdivision_graph(Gamma, e)
        [[0, 1, 2, 3], [0, 1, 2, 0]]
        sage: is_harmonic_graph_morphism(Gamma, Gamma2, f, verbose=False)
        True
        sage: Gamma2.is_isomorphic(graphs.PathGraph(4))
        True

    """
    Gamma2 = Gamma1.copy()
    #E0 = Gamma0.edges(labels=None,sort=True)
    V1 = Gamma1.vertices(sort=True)
    #print(Gamma1.vertices(sort=True))
    Gamma2.subdivide_edge(e, 1)
    #print(Gamma2.vertices(sort=True))
    E2 = Gamma2.edges(labels=None,sort=True)
    V2 = Gamma2.vertices(sort=True)
    f0 = V1+[min(e)]
    f = [V2, f0]
    #print(f)
    return Graph([V2,E2]),f

def lower_upper_bound_sgon(Gamma):
    """
    Returns the upper UB and lower bound LB on the sgonality of a graph, so
    LB <= sgon(Gamma) <= UB. The bounds are mentioned on pp 2-3 of [1].


    EXAMPLES:
        sage: Gamma = graphs.PathGraph(4)
        sage: lower_upper_bound_sgon(Gamma)
        0.19 1.5
        sage: Gamma = graphs.CycleGraph(5)
        sage: lower_upper_bound_sgon(Gamma)
        0.41 2.0
        sage: Gamma = graphs.DiamondGraph()
        sage: lower_upper_bound_sgon(Gamma)
        0.44 2.5
        sage: Gamma = graphs.CubeGraph(3)
        sage: lower_upper_bound_sgon(Gamma)
        0.44 4.0
        sage: Gamma = flower_graph([4,5])
        sage: lower_upper_bound_sgon(Gamma)
        0.18 2.5


    REFERENCES
        [1] Gijswijt, Smit, van der Wegen, "Computing graph gonality is hard", 
            ArXiV preprint, 2019.

    """
    V = Gamma.vertices(sort=True)
    Q = Gamma.laplacian_matrix()
    lambda1 = min([x for x in Q.eigenvalues() if x != 0])
    D = max(Gamma.degree_sequence())
    #print(lambda1, D)
    UB = (genus(Gamma)+3)/2.0
    LB =  1.0*len(V)*lambda1/(lambda1+4*(D+1))
    print(LB.numerical_approx(digits=2), UB.numerical_approx(digits=2))

def subdivision_graph_morphism(Gamma1, Gamma2, f, s):
    """
    Here s is an edges of Gamma1, f is a morphism from Gamma2 -> Gamma1,
    in CL notation.

    Returns a triple (Gamma3, Gamma4, g), where
     Gamma3 is the subdivision graph of Gamma1 obtained by subdividing the edge s of Gamma1, 
     Gamma4 is the subdivision graph of Gamma2 obtained by subdividing the edges e of Gamma2
      in the fiber of s, 
     g is the graph morphism from Gamma4 -> Gamma3, corresponding to f.
    
    This leaves Gamma1, Gamma2, f unchanged and assumes Gamma1, Gamma2 are in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(3)
        sage: Gamma2 = graphs.PathGraph(4)
        sage: f21_0 = [0,1,2,2]
        sage: V2 = Gamma2.vertices(sort=True)
        sage: f21 = [V2, f21_0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f21, verbose=False)
        True
        sage: E1 = Gamma1.edges(labels=None,sort=True)
        sage: s = E1[0]; s
        (0, 1)
        sage: Gamma3, Gamma4, f43 = subdivision_graph_morphism(Gamma1, Gamma2, f21, s)
        sage: f43
        [[0, 1, 2, 3, 4], [0, 1, 2, 2, 3]]
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, f43, verbose=False)
        True

    """
    Gamma3 = Gamma1.copy()
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    Gamma4 = Gamma2.copy()
    V2 = Gamma2.vertices(sort=True)
    Gamma3.subdivide_edge(s, 1)
    V3 = Gamma3.vertices(sort=True)
    E3 = Gamma3.edges(labels=None,sort=True)
    Gamma30 = Graph([V3, E3])
    S = preimage_of_edge_under_graph_morphism(Gamma1, Gamma2, f, s)
    for e in S:
        Gamma4.subdivide_edge(e, 1)
    E4 = Gamma4.edges(labels=None,sort=True)
    V4 = Gamma4.vertices(sort=True)
    Gamma40 = Graph([V4, E4])
    g0 = f[1]+[n1]*len(S) ## ????
    g = [V4, g0]
    #print(f)
    return Gamma30, Gamma40, g

def is_smooth_vertex(Gamma, v0):
    """
    The function checks if vertex v0
     (a) has exactly 2 neighbors, say u and w, and
     (b) those two neighbors are not adjacent in Gamma.
    If these conditions hold, v0 is smooth.

    Returns True if v0 is smooth and False otherwise.
    
    Assumes Gamma is a simple graph.

    EXAMPLES:
        sage: Gamma = graphs.PathGraph(4)
        sage: V = Gamma.vertices(sort=True); V
         [0, 1, 2, 3]
        sage: v0 = V[0]; is_smooth_vertex(Gamma, v0)
         False
        sage: v0 = V[1]; is_smooth_vertex(Gamma, v0)
         True

    """
    V = Gamma.vertices(sort=True)
    if not(v0 in V):
        print("Vertex v0 must be a vertex of Gamma.")
        return False
    N_v0 = Gamma.neighbors(v0)  # deg(v0)=len(N_v0) 
    E = Gamma.edges(labels=None,sort=True)
    if len(N_v0) != 2:
        return False
    if (N_v0[0], N_v0[1]) in E:
        return False
    return True

def smooth_graph(Gamma, v0):
    """
    Assumes Gamma is in standard form and, if v0 is a smooth vertex
    of Gamma, returns the smoothing of Gamma at v0, as a graph in
    standard form. (The labeling of vertices changes by relabeling
    the vertices v0+1, ..., n-1 to v0, ..., n-2.)

    If v0 is not smooth, it returns Gamma. 

    EXAMPLES:
        sage: V1 = [0,1,2,3,4]
        sage: E1 = [(0,1),(0,2),(1,3),(2,3),(2,4),(3,4)]
        sage: Gamma1 = Graph([V1,E1])  # 4 is the "tip of the roof", (0,1) is the "base"
        sage: Gamma2 = smooth_graph(Gamma1, 4)
         v0 is not a smooth vertex of Gamma.
        sage: Gamma2 == Gamma1
         True
        sage: Gamma2 = smooth_graph(Gamma1, 0)
        sage: Gamma2.is_isomorphic(graphs.DiamondGraph())
         True

    """
    #Gamma.show()
    if not(is_smooth_vertex(Gamma, v0)):
        print("v0 is not a smooth vertex of Gamma.")
        return Gamma
    V = Gamma.vertices(sort=True)
    n = len(V)
    if not(V == srange(n)):
        print("Gamma must be in standard form.")
        return Gamma
    G = SymmetricGroup(V)
    g = G([(0,n-1)])
    V0 = [g(x) for x in V]
    Gamma.relabel(V0) # so v0-> n-1
    #Gamma.show()
    v00 = n-1
    N_v0 = Gamma.neighbors(v00) # size 2
    #print(v0, v00, N_v0, Gamma.neighbors(v0))
    E0 = Gamma.edges(labels=None,sort=True)
    E0_v0 = [e for e in E0 if not(v00 in e)]
    E2 = E0_v0+[(N_v0[0], N_v0[1])]
    V2 = srange(n-2)
    #print(N_v0,V2, E2)
    return Graph([V2, E2])


def smooth_graph_morphism(Gamma1, Gamma2, f, x0):
    """
    Here x0 is a vertex of Gamma1, f is a morphism from Gamma2 -> Gamma1,
    in CL notation.

    Returns a triple (Gamma3, Gamma4, g), where
     Gamma3 is the graph obtained by smoothing Gamma1 at x0, 
     Gamma4 is the graph obtained by smoothing Gamma2 at the vertices in the fiber over x0, 
     g is the graph morphism from Gamma4 -> Gamma3, corresponding to f.
    
    This leaves Gamma1, Gamma2, f unchanged and assumes Gamma1, Gamma2 are in standard form.
    This assumes x0 is a smooth vertex of Gamma1 and that all the vertices in the
    fiber over x0 are smooth. If not, it returns Gamma1, Gamma2, f and prints a 
    message.

    In some examples, this construction can produce a non-simple graph
    (with repeated edges). In this case, the graph returned by this function is the
    "simplified" version.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(4)
        sage: Gamma2 = graphs.CycleGraph(8)
        sage: f21_0 = [0, 1, 2, 3, 0, 1, 2, 3]
        sage: V2 = Gamma2.vertices(sort=True)
        sage: f21 = [V2, f21_0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f21, verbose=False)
         True
        sage: Gamma3, Gamma4, f43 = smooth_graph_morphism(Gamma1, Gamma2, f21, 1)
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, f43, verbose=False)
         True

    """
    V2 = Gamma2.vertices(sort=True)
    if not(is_smooth_vertex(Gamma1, x0)):
        print("x0 must be a smooth vertex of Gamma1.")
        return Gamma1, Gamma2, f
    Gamma3 = smooth_graph(Gamma1, x0)
    Gamma4 = Gamma2.copy()
    S = preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, x0)
    for v in S:
        Gamma4 = smooth_graph(Gamma4, v)
    V4 = Gamma4.vertices(sort=True)
    V20 = copy(V2)
    for v in S:
        V20.remove(v)
    #print(V20)
    f43_0 = [f21_0[i] for i in V20]
    g = [V4, compactify_list(f43_0)]
    #print(f43_0, compactify_list(f43_0))
    return Gamma3, Gamma4, g

def delete_vertex_graph_morphism(Gamma1, Gamma2, f, x0):
    """
    Here x0 is a vertex of Gamma1, f is a morphism from Gamma2 -> Gamma1,
    in CL notation.

    Returns a triple (Gamma3, Gamma4, g), where
     Gamma3 is the graph obtained by deleting x0 from Gamma1,
          assuming the resulting graph is connected, 
     Gamma4 is the graph obtained by deleting the fiber over x0 from Gamma2,
          assuming the resulting graph is connected, 
     g is the graph morphism from Gamma4 -> Gamma3, corresponding to the restriction of f.
    
    This leaves Gamma1, Gamma2, f unchanged and assumes Gamma1, Gamma2 are in standard form.
    If the result of a deletion leaves a disconnected graph then it returns 
    Gamma1, Gamma2, f and prints a message.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(3)
        sage: Gamma2 = graphs.ButterflyGraph()
        sage: V2 = Gamma2.vertices(sort=True)
        sage: f21_0 = [1,2,1,2,0]
        sage: f21 = [V2, f21_0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f21, verbose=False)
        True
        sage: Gamma3, Gamma4, f43 = delete_vertex_graph_morphism(Gamma1, Gamma2, f21, 1)
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, f43, verbose=False)
        True
        sage: V3 = Gamma3.vertices(sort=True); V3
        [0, 1]
        sage: V4 = Gamma4.vertices(sort=True); V4
        [0, 1, 2]
        sage: f43
        [[0, 1, 2], [1, 1, 0]]
        sage: Gamma3, Gamma4, f43 = delete_vertex_graph_morphism(Gamma1, Gamma2, f21, 0)
        preimage of x0 under f must not contain a disconnecting vertex of Gamma2.
        sage: Gamma3==Gamma1
        True
        sage: Gamma4==Gamma2
        True
        sage: f43==f21
        True

    """
    V2 = Gamma2.vertices(sort=True)
    Gamma3 = copy(Gamma1)
    Gamma4 = copy(Gamma2)
    Gamma3.delete_vertex(x0)
    if not(Gamma3.is_connected()):
        print("x0 must not be a disconnecting vertex of Gamma1.")
        return Gamma1, Gamma2, f
    S = preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, x0)
    for v in S:
        Gamma4.delete_vertex(v)
        if not(Gamma4.is_connected()):
            print("preimage of x0 under f must not contain a disconnecting vertex of Gamma2.")
            return Gamma1, Gamma2, f
    V4 = Gamma4.vertices(sort=True)
    V20 = copy(V2)
    for v in S:
        V20.remove(v)
    #print(V20)
    f43_0 = [f21_0[i] for i in V20]
    g = [compactify_list(V4), compactify_list(f43_0)]
    #print(f43_0, compactify_list(f43_0))
    return graph_convert_to_standard(Gamma3), graph_convert_to_standard(Gamma4), g

def table_of_local_horizontal_multiplicities(Gamma1, Gamma2, f):
    """
    Self-explanatory.

    EXAMPLES:
        sage: Gamma1 = graphs.PathGraph(2)
        sage: Gamma2 = graphs.PathGraph(4)
        sage: V2 = Gamma2.vertices(sort=True)
        sage: f21_0 = [0,1,1,0]
        sage: f21 = [V2, f21_0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f21, verbose=True)
        Gamma1 = (V1, E1) =  [0, 1] [(0, 1)]
        Gamma2 = (V2, E2) =  [0, 1, 2, 3] [(0, 1), (1, 2), (2, 3)]
        f = [V2, f0], where f0 =  [0, 1, 1, 0]
        The edge e =  (1, 2)  is vertical under f.
        This [<vertex>, <intersection sizes>]] passes the check: [0, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [1, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [2, [1]]
        This [<vertex>, <intersection sizes>]] passes the check: [3, [1]]
        True
        sage: table_of_local_horizontal_multiplicities(Gamma1, Gamma2, f21)
        [[(0, (0, 1), 1)], [(1, (0, 1), 1)], [(2, (0, 1), 1)], [(3, (0, 1), 1)]]

    """
    T = [[(v,e,local_horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, v, e)) for e in Gamma1.edges(labels=None,sort=True) if image_of_vertex_under_graph_morphism(Gamma1,Gamma2,f,v) in e] for v in V2]
    return T

def is_harmonic_graphWB_morphism(Gamma1, Gamma2, f, B1, B2, verbose = False):
    r"""
    Returns 
      True if f defines a graph-theoretic mapping
           from a graph Gamma2 with boundary B2 to another graph Gamma1
           with boundary B1 that is a harmonic morphism on the interior, and 
      False, otherwise. 

    Assumes Gamma1, Gamma2 are in standard form. Assumes B2 = [s2,t2],
    B1 = [s1, t1] and f must send B2 to B1.

    Suppose Gamma2 has n vertices. A morphism 
              f: Gamma2 -> Gamma1
    is represented by a pair of lists [L2, L1],
    where L2 = V2 is the list of all n vertices of Gamma2,
    and L1 is the list of length n of the vertices
    in Gamma1 that form the corresponding image under
    the map f.

    EXAMPLES:
        sage: V1 = [0,1,2,3,4]
        sage: E1 = [(0,3),(0,1),(1,2),(2,4)] 
        sage: B1 = [3,4]   
        sage: Gamma1 = Graph([V1,E1]) # P3+s1+t1=P5 
        sage: V2 = [0,1,2,3,4,5]  
        sage: E2 = [(0,4),(0,1),(0,2),(1,3),(2,3),(3,5)] 
        sage: B2 = [4,5]  
        sage: Gamma2 = Graph([V2,E2]) # C4+s2+t2 
        sage: f0_21 = [0,1,1,2,3,4] 
        sage: f21_0 = [0,1,1,2,3,4] 
        sage: f21 = [V2, f21_0] 
        sage: is_harmonic_graphWB_morphism(Gamma1, Gamma2, f_21, B1, B2, verbose = True) 
         Gamma1 = (V1, E1) =  [0, 1, 2, 3, 4] [(0, 1), (0, 3), (1, 2), (2, 4)]
         Boundary of Gamma1 =  [3, 4]
         Gamma2 = (V2, E2) =  [0, 1, 2, 3, 4, 5] [(0, 1), (0, 2), (0, 4), (1, 3), (2, 3), (3, 5)]
         Boundary of Gamma2 =  [4, 5]
         interior of Gamma1: Gamma3 = (V3, E3) =  [0, 1, 2] [(0, 1), (1, 2)]
         interior of Gamma2: Gamma4 = (V4, E4) =  [0, 1, 2, 3] [(0, 1), (0, 2), (1, 3), (2, 3)]
         Gamma1 = (V1, E1) =  [0, 1, 2, 3, 4] [(0, 1), (0, 3), (1, 2), (2, 4)]
         Gamma2 = (V2, E2) =  [0, 1, 2, 3, 4, 5] [(0, 1), (0, 2), (0, 4), (1, 3), (2, 3), (3, 5)]
         f = [V2, f0], where f0 =  [0, 1, 1, 2, 3, 4]
         Gamma1 = (V1, E1) =  [0, 1, 2] [(0, 1), (1, 2)]
         Gamma2 = (V2, E2) =  [0, 1, 2, 3] [(0, 1), (0, 2), (1, 3), (2, 3)]
         f = [V2, f0], where f0 =  [0, 1, 1, 2]
         This [<vertex>, <intersection sizes>]] passes the check: [0, [2]]
         This [<vertex>, <intersection sizes>]] passes the check: [1, [1, 1]]
         This [<vertex>, <intersection sizes>]] passes the check: [2, [1, 1]]
         This [<vertex>, <intersection sizes>]] passes the check: [3, [2]]
         True
        sage: is_harmonic_graphWB_morphism(Gamma1, Gamma2, f_21, B1, B2, verbose = False) 
         True

    """
    V1 = Gamma1.vertices(sort=True)
    # B1 is a sublist of V1
    n1 = len(V1)
    if V1 != list(range(n1)):
        return "Error! -- Gamma1 must be in standard form."
    Gamma3 = copy(Gamma1)                  
    Gamma3.delete_vertices(B1)
    V3 = Gamma3.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    # B2 is a sublist of V2
    n2 = len(V2)
    if V2 != list(range(n2)):
        return "Error! -- Gamma2 must be in standard form."
    Gamma4 = copy(Gamma2)                  
    Gamma4.delete_vertices(B2)
    V4 = Gamma4.vertices(sort=True)
    if verbose:
        print("Gamma1 = (V1, E1) = ", V1, Gamma1.edges(labels=None,sort=True))
        print("Boundary of Gamma1 = ", B1)
        print("Gamma2 = (V2, E2) = ", V2, Gamma2.edges(labels=None,sort=True))
        print("Boundary of Gamma2 = ", B2)
        print("interior of Gamma1: Gamma3 = (V3, E3) = ", V3, Gamma3.edges(labels=None,sort=True))
        print("interior of Gamma2: Gamma4 = (V4, E4) = ", V4, Gamma4.edges(labels=None,sort=True))
    for v2 in V2:
        w = image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v2)
        if w in B1 and not(v2 in B2):
            print( "This map does not respect the boundaries: image ",w," of interior vertex ",v2," is in boundary", B1)
            return False
    f0_43 = [f[1][i] for i in V4]
    f43 = [V4, f0_43]
    for b2 in B2:
        if not(image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, b2) in B1):
            print( "This map does not respect the boundaries: image of ",b2," is not in boundary", B1)
            return False
    E1 = Gamma1.edges(labels=None,sort=True)
    m1 = len(E1)
    E2 = Gamma2.edges(labels=None,sort=True)
    m2 = len(E2)
    edges_in_common = []
    if not(is_graph_morphism(Gamma1, Gamma2, f, verbose)):
        return False
    if not(is_graph_morphism(Gamma3, Gamma4, f43, verbose)):
        return False
    for v in V4:
        w = image_of_vertex_under_graph_morphism(Gamma3, Gamma4, f43, v)
        star3w = star_subgraph(Gamma3, w)
        E3w = star3w.edges(labels = None, sort = True)
        star4v = star_subgraph(Gamma4, v)
        E4v = star4v.edges(labels = None, sort = True)
        sizes = []
        for e in E3w:
            sizes.append(local_horizontal_multiplicity_of_harmonic_map(Gamma3, Gamma4, f43, v, e))
        edges_in_common.append([v, sizes]) # these common values = horiz. mult.
    ans = True
    for x in edges_in_common:
        sizesx = x[1]
        S = Set(sizesx)
        if S.cardinality() != 1:
            ans = False
            if verbose:
                print( "This [<vertex>, <intersection sizes>]] fails the check:", x)
        if verbose and ans==True:
            print( "This [<vertex>, <intersection sizes>]] passes the check:", x)
    return ans

def partial_join_graph(Gamma, S):
    """
    Here Gamma is a graph with n vertices (assumed to be in standard form),
         S is a subset of vertices of Gamma.
    Returns a graph obtained by adding a vertex w and edges (v, w), for v in S, to Gamma.

    EXAMPLES:
        sage: Gamma = graphs.CycleGraph(4)
        sage: S = [2,3]
        sage: Gamma2 = partial_join_graph(Gamma, S)
        sage: Gamma2.is_isomorphic(graphs.HouseGraph())
         True
        sage: Gamma = graphs.CycleGraph(4)
        sage: S = [0,1,2,3]
        sage: Gamma2 = partial_join_graph(Gamma, S)
        sage: Gamma2.is_isomorphic(graphs.WheelGraph(5))
         True

    """
    V = list(Gamma.vertices(sort=True))
    E = list(Gamma.edges(labels=None,sort=True))
    n = len(V)
    V2 = V+[n]
    E2 = E+[(v,n) for v in S]
    Gamma2 = Graph([V2,E2])
    return Gamma2


def leaf_addition_graph_morphism(Gamma1, Gamma2, f, x0):
    """
    Here x0 is a vertex of Gamma1 that is not the image of an edge under f, 
    f is a harmonic morphism from Gamma2 -> Gamma1, in CL notation.
    Assumes 
        * Gamma1, Gamma2 are in standard form, with V1 = [0,...,n1-1],
          V2 = [0,...,n2-1]. 
        * x0 is not the image of an edge.
        * f is harmonic.

    Returns a triple (Gamma3, Gamma4, g), where
     Gamma3 is the leaf-addition Gamma1 obtained by adding a leaf (x0, n1) to Gamma1, 
     Gamma4 is the graph obtained by adding, for each v in f^(-1)(x0), 
      mu(v) leafs attached to v. If f^(-1)(x0) = [v_1,...,v_k] (v_1<v_2<...<v_k) then 
      these new vertices and edges are labeled 
       V21 = [n2,...,n2+mu(v_1)-1], (v1,w) for w in V21,
       V22 = [n2+mu(v_1),..., n2+mu(v_1)+mu(v_2)-1], (v2,w) for w in V22,
       ..., 
       V2k = [n2+mu(v_1)+...+mu(v_{k-1}),..., n2+mu(v_1)+...+mu(v_k)-1], (vk,w) for w in V2k.
     g is the graph morphism from Gamma4 -> Gamma3, corresponding to this extention of f.
    
    This leaves Gamma1, Gamma2, f unchanged.

    EXAMPLES:
        sage: Gamma2 = graphs.CycleGraph(4)
        sage: Gamma1 = graphs.PathGraph(3)
        sage: V2 = Gamma2.vertices(sort=True)
        sage: f21_0 = [0,1,2,1]
        sage: f21 = [V2, f21_0]
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f21, verbose=False)
         True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f21, v) for v in V2]
         [2, 1, 2, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma1, Gamma2, f21, v) for v in V2]
         [0, 0, 0, 0]
        sage: Gamma3,Gamma4,g = leaf_addition_graph_morphism(Gamma1, Gamma2, f21, 1)
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g, verbose=False)
         True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]
         [2, 1, 2, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]
         [0, 0, 0, 0, 0, 0]
        sage: degree_of_harmonic_morphism(Gamma3, Gamma4, g)
         2
        sage: degree_of_harmonic_morphism(Gamma1, Gamma2, f21)
         2
        sage: is_harmonic_graph_morphism(Gamma3, Gamma4, g, verbose=False)
         True
        sage: [horizontal_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]
         [2, 1, 2, 1, 1, 1]
        sage: [vertical_multiplicity_of_harmonic_map(Gamma3, Gamma4, g, v) for v in V4]
         [0, 0, 0, 0, 0, 0]
        sage: degree_of_harmonic_morphism(Gamma3, Gamma4, g)
         2

    """
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    E1 = Gamma1.edges(labels=None,sort=True)
    for e in E1:
        if x0 == image_of_edge_under_graph_morphism(Gamma1, Gamma2, f, e, verbose=False):
            print("vertex ", x0, " is the image of an edge")
            return Gamma1, Gamma2, f
    V2 = Gamma2.vertices(sort=True)
    n2 = len(V2)
    E2 = Gamma2.edges(labels=None,sort=True)
    Gamma3 = partial_join_graph(Gamma1, [x0])
    V4 = V2      ## initialize
    E4 = E2      ## initialize
    S = preimage_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, x0)
    k = len(S)
    ll = len(V4) ## initialize
    g0 = f[1]    ## initialize
    for i in range(k):
        m = horizontal_multiplicity_of_harmonic_map(Gamma1, Gamma2, f, S[i])
        Vnew = [ll+j for j in range(m)]
        V4 = V4+Vnew
        g0 = g0 + [n1]*len(Vnew)
        E4 = E4+[(S[i],w) for w in Vnew]
        ll = len(V4)
        #print(i, V4, [(S[i],w) for w in Vnew],Vnew,g0)
    Gamma4 =  Graph([V4,E4])
    g = [V4, g0]
    return Gamma3, Gamma4, g

def sub_graph4edge(Gamma1, e0, Gamma, a, b):
    """
    Here:
     * Gamma1, and Gamma are connected graphs in standard form,
     * e0 = (x0, y0) is an edge of Gamma1, x0<y0.
     * a,b are vertices in Gamma, not necessarily adjacent, a<b.
    Returns a pair (Gamma2, f), where
     Gamma2 is the graph obtained by replacing the edge e0=(x0,y0) of Gamma1 
     by the graph Gamma, where a is attached at x0 and b is attached at
     y0 (so in the new graph a=x0, b=y0).
    
    This leaves Gamma1 itself unchanged. This should agree with the function
    subdivision in the case Gamma=P3 and a,b are the degree 1 vertices.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(3)    
        sage: Gamma = graphs.CycleGraph(3)     
        sage: Gamma2 = sub_graph4edge(Gamma1, (0,1), Gamma, 0, 1) 
        sage: Gamma2.is_isomorphic(graphs.DiamondGraph())
         True
        sage: Gamma1 = graphs.CycleGraph(3)    
        sage: Gamma = graphs.CycleGraph(4)     
        sage: Gamma2 = sub_graph4edge(Gamma1, (0,1), Gamma, 0, 1)
        sage: Gamma2.is_isomorphic(graphs.HouseGraph()) 
         True
        sage: Gamma1 = graphs.CycleGraph(3)    
        sage: Gamma = graphs.PathGraph(3)     
        sage: Gamma2 = sub_graph4edge(Gamma1, (1,2), Gamma, 0, 2) 
        sage: Gamma2.is_isomorphic(graphs.CycleGraph(4))  
         True
        sage: Gamma3,f = subdivision_graph(Gamma1, (1,2)) 
        sage: Gamma2.is_isomorphic(Gamma3)     
         True

    """
    E = Gamma.edges(labels=None,sort=True)
    V = Gamma.vertices(sort=True)
    n = len(V)
    if not(a in V):
        print("Vertex ",a," must belong to Gamma.")
        return Gamma1
    if not(b in V):
        print("Vertex ",b," must belong to Gamma.")
        return Gamma1	
    E1 = Gamma1.edges(labels=None,sort=True)
    V1 = Gamma1.vertices(sort=True)
    n1 = len(V1)
    if not(e0 in E1):
        print("Edge ",e0," must belong to Gamma1.")
        return Gamma1    
    x0 = e0[0]
    y0 = e0[1]
    Vnx0y0 = [v+n1 for v in V if not(v in [a,b])]
    V2 = V1+Vnx0y0   ## vertices of new graph Gamma2
    #print(V2," = V2")
    E1me0 = [e for e in E1 if e!=e0]
    #print(E1me0, " = E1me0")
    E2ab = [(x0,y0) for e in E if ((a in e) and (b in e))]        ##  = [(x0,y0)] if (a,b) in E, =[] otherwise
    #print(E2ab, " = E2ab")
    Eab = [e for e in E if (a in e and not(b in e))]        ## edges in Gamma incident to a not b
    #print(Eab, " = Eab")
    Eba = [e for e in E if (not(a in e) and b in e)]        ## edges in Gamma incident to b not a
    #print(Eba, " = Eba")
    Enab = [e for e in E if (not(a in e) and not(b in e))]  ## edges in Gamma incident to neither a nor b
    #print(Enab, " = Enab")
    E2 = E2ab+E1me0+[(e[0]+n1,e[1]+n1) for e in Enab] # first step to build E2
    #print(E2, " = E2, step 1")
    E2 = E2+[(x0,e[1]+n1) for e in Eab if e[0]==a]+[(e[0]+n1,x0) for e in Eab if e[1]==a] # 2nd step to build E2
    #print(E2, " = E2, step 2")
    E2 = E2+[(y0,e[1]+n1) for e in Eba if e[0]==b]+[(e[0]+n1,y0) for e in Eba if e[1]==b] # 3rd/last step to build E2
    #print(E2, " = E2, step 3/last step")
    return graph_convert_to_standard(Graph([V2,E2]))

def has_harmonic_quotient(Gamma, verbose=False):
    r"""
    This function returns the list (possibly empty) of harmonic 
    graph quotient morphisms, 
                   f: Gamma -> Gamma/G,
    where G is a subgroup of Aut(Gamma), where f is in CL format.

    Input: Gamma - a graph in standard form,
    Output: The harmonic quotient graph morphisms.

    EXAMPLES:
        sage: Gamma2 = graphs.LCFGraph(12, [6, -2, 2], 4) # trunc tetrahedron, d3reg12-12? 
        sage: L = has_harmonic_quotient(Gamma2, verbose=True)  
         10  non-trivial harmonic quotient morphism(s) found.
        sage: f0 = L[3][0]; f0     
         [2, 1, 1, 2, 0, 0, 2, 1, 1, 2, 0, 0]
        sage: G0 = L[3][1]; G0.cardinality()            
         4
        sage: Gamma1 = L[3][2]   
        sage: Gamma1.is_isomorphic(graphs.CycleGraph(3))    
         True
        sage: V2 = Gamma2.vertices(sort=True); V2 
         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        sage: f = [V2, f0]   
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose=False)   
         True

    """
    Gamma2 = graph_convert_to_standard(Gamma)
    V2 = Gamma2.vertices(sort=True)
    #print(V2)
    AutG = Gamma2.automorphism_group()
    AutG_subgroups = [X for X in AutG.subgroups() if (X.cardinality()>1 and X.cardinality()<AutG.cardinality())]
    L = []
    for G in AutG_subgroups:
       #print(V2, G.gens())
       #Gamma1, f0 = quotient_graph(Gamma2, G, verbose=False, morphism=True)
       Gamma1 = quotient_graph(Gamma2, G, verbose=False, morphism=False)
       #print(Gamma1)
       f0 = quotient_graph_morphism(Gamma2, G)
       #print(f0, G.gens())
       if len(Gamma1.vertices(sort=True))>1:
           f = [V2, f0]
           ans = is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose=False)
           if ans==True:
               if verbose:
                   L = L+[(f0, G, Gamma1)]
               else:
                   L = L+[(f0, G)]
    print(len(L), " non-trivial harmonic quotient morphism(s) found.\n")
    return L

def double_point_construction(Gamma):
   """
   Gamma is a k-regular graph with n vertices, assumed to be
   in standard form. We also assume k<n-1. This adds another vertex, 
   which we connect to k+1 vertices of Gamma by an edge. 
   Call this Gamma2. Make a copy of Gamma2. Connect each 
   vertex of degree k on one copy to its corresponding vertex 
   on the other copy. This new graph is (k+1)-regular, with 
   2n+2 vertices.

   EXAMPLES:
       sage: Gamma1 = graphs.CycleGraph(4)
       sage: Gamma1.is_regular(2)
        True
       sage: Gamma2 = double_point_construction(Gamma1)
       sage: Gamma2.is_regular(3)
        True
       sage: Gamma1 = graphs.CompleteBipartiteGraph(3,3)
       sage: Gamma1.is_regular(3)
        True
       sage: Gamma2 = double_point_construction(Gamma1)
       sage: Gamma2.is_regular(4)
        True

   """
   V = Gamma.vertices(sort=True)
   n = len(V)
   if Gamma.is_regular():
       k = Gamma.degree_sequence()[0]
       if k>=n-1:
           print("Graph regularity is too small.")
           return Gamma
   else:
       print("Graph must be regular.")
       return Gamma
   E = Gamma.edges(labels=None,sort=True)
   E2 = E+[(e[0]+n+1,e[1]+n+1) for e in E]
   V1a = V+[n]
   V1b = list(range(n+1,2*n+2))
   for i in range(k+1): ## adding k+1 new edges
       E2=E2+[(i,n)]
   #print(len(E2))
   for j in range(n+1,n+k+2): ## adding k+1 new edges
       E2=E2+[(j,2*n+1)]
       #print(j,2*n+1)
   V2 = V1a+V1b
   #print(len(V2), len(E2))
   for i in range(k+1,n): ## adding n-k new edges
       E2=E2+[(i,n+i+1)]
   #print(len(E2))
   Gamma2 = Graph([V2,E2])
   return Gamma2


def graph_id_graph6(Gamma, verbose=False):
    """
    Returns the graph6 id of Gamma = (V,E). 
    If verbose then it also displays the table of all graphs with 
    |V| vertices and |E| edges.

    Assumes Gamma is a "small" graph.

    EXAMPLES:
        sage: Gamma = graphs.HouseGraph()
        sage: graph_id_graph6(Gamma, verbose=False)
        'Dbk'
        sage: graph_id_graph6(Gamma, verbose=True)

         graphs with 5 vertices and 6 edges:

        Graph6               Aut Grp Size         Degree Sequence     
        ------------------------------------------------------------
        DB{                  2                    [1, 2, 2, 3, 4]     
        DFw                  12                   [2, 2, 2, 3, 3]     
        DJ[                  24                   [0, 3, 3, 3, 3]     
        DJk                  2                    [1, 2, 3, 3, 3]     
        DK{                  8                    [2, 2, 2, 2, 4]     
        Dbk                  2                    [2, 2, 2, 3, 3]     


        'Dbk'

    """
    n = len(Gamma.vertices(sort=True))
    m = len(Gamma.edges(sort=True))
    ds = Gamma.degree_sequence()
    if verbose:
         print("\n #vertices = ", n," #edges = ",m, "degree sequence = ",ds,"\n")
    Q = GraphQuery(display_cols=['graph6', 'aut_grp_size', 'degree_sequence'], num_edges=['=', m], num_vertices=["=", n])
    for g in Q:
        if g.is_isomorphic(Gamma):
            if verbose:
                print("\n graphs with %s vertices"%n+" and %s edges:\n"%m)
                Q.show()
                print("\n")
            return g.graph6_string()
    print("None found")

def effective_resistance_matrix(Gamma):
    """
    Returns the effective resistance matrix, even when Gamma is
    edge-weighted.

    Gamma is assumed to be in standard form. The default weight of
    each edge is 1 for each edge.

    EXAMPLES:
        sage: C3 = graphs.CycleGraph(3)
        sage: effective_resistance_matrix(C3) 
         [  0 2/3 2/3]
         [2/3   0 2/3]
         [2/3 2/3   0]

    """
    V = Gamma.vertices(sort=True)
    n = len(V)
    E = Gamma.edges(sort=True)
    m = len(E)
    wts = []
    for e in E:
       if e[2]==None:
           wts = wts+[1]
       else:
           wts = wts+[e[2]]
    Ew = [(E[i][0], E[i][1], wts[i]) for i in range(m)]
    Q = Graph([V,Ew], weighted=True).laplacian_matrix()
    Qplus = Q.pseudoinverse()
    DQplus = Qplus.diagonal()
    MSn1 = MatrixSpace(QQ, n, 1)
    MS1n = MatrixSpace(QQ, 1, n)
    R = MSn1(DQplus)*MS1n([1]*n) + MSn1([1]*n)*MS1n(DQplus) - 2*Qplus
    return R


def intersection_number_of_vertex_subset(Gamma, C, v):
    r"""
    Returns the number of neighbors of v in C.

    Gamma =(V, E) must be in standard form.

    C is represented as a sublist of V.
    v is an element of V.
    
    EXAMPLES:
        sage: Gamma = graphs.PathGraph(5)
        sage: C = [1,2]
        sage: intersection_number_of_vertex_subset(Gamma, C, 0)
        1

    """
    V = Gamma.vertices(sort=True)
    NCv = [x for x in Gamma.neighbors(v) if x in C]
    return len(NCv)
    
def is_equitable_partition(Gamma, P, verbose=False):
    r"""
    Returns True if P defines an equitable partition of the vertices
    of Gamma. If, in addiiton, verbose=True then it also returns the
    intersection matrix. It returns False otherwise.

    Gamma must be in standard form.

    P is represented as a list of disjoint lists.

    EXAMPLES:
        sage: Gamma = graphs.PathGraph(5)
        sage: P = [[0,4],[1,3],[2]]
        sage: is_equitable_partition(Gamma, P)
	True
        sage: is_equitable_partition(Gamma, P, verbose=True)
        (
               [0 1 0]
               [1 0 1]
         True, [0 2 0]
         )
        sage: Gamma2 = graphs.HouseGraph()   
        sage: V2 = Gamma2.vertices(sort=True); V2
         [0, 1, 2, 3, 4]
        sage: P = [[0,2],[1,3],[4]] 
        sage: is_equitable_partition(Gamma2, P, verbose=True)   
         Fails to be equitable because deg( [4] [0, 2] ) isn't defined.
         False

    """
    V = Gamma.vertices(sort=True)
    C = []
    for C1 in P:
        L = []
        for C2 in P:
            L = [intersection_number_of_vertex_subset(Gamma, C1, v) for v in C2]
            if len(list(Set(L)))>1:
                if verbose:
                    print("Fails to be equitable because deg(",C1, C2,") isn't defined.")
                return False
            else:
                C = C+list(Set(L))
    p = len(P)
    if verbose:
        return True, matrix(p,p,C).transpose()
    else:
        return True

def associated_partition_to_morphism(Gamma1, Gamma2, f):
    r"""
    Each surjective graph morphism
             phi: Gamma2 = (V2, E2) -> Gamma1 = (V1, E1)
    determines a partition
                        P = P_{phi}
    by letting the cels of P be the fibers phi^{-1}(x), x in V1.

    Returns the partition of the vertices of Gamma2 associated to f.

    Gamma1, Gamma2 must be in standard form and f must be surjective.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(3) 
        sage: Gamma2 = graphs.HouseGraph()   
        sage: V2 = Gamma2.vertices(sort=True); V2  
         [0, 1, 2, 3, 4]
        sage: f0 = [0,1,0,1,2]     
        sage: f = [V2, f0]         
        sage: associated_partition_equitable(Gamma1, Gamma2, f) 
         [[0, 2], [1, 3], [4]]

    """
    V1 = Gamma1.vertices(sort=True)
    V2 = Gamma2.vertices(sort=True)
    P =[[v for v in V2 if image_of_vertex_under_graph_morphism(Gamma1, Gamma2, f, v)==x] for x in V1]
    return P

def is_associated_partition_equitable(Gamma1, Gamma2, f, verbose=False):
    r"""
    Returns True if the fibers of f defines an equitable partition of the vertices
    of Gamma2. If, in addition, verbose=True then it also returns the
    intersection matrix. It returns False otherwise (and, if verbose=True) then it 
    returns cells where the equitable condition fails.

    Gamma1, Gamma2 must be in standard form.

    EXAMPLES:
        sage: Gamma1 = graphs.CycleGraph(3) 
        sage: Gamma2 = graphs.HouseGraph()      
        sage: V2 = Gamma2.vertices(sort=True); V2 
         [0, 1, 2, 3, 4]
        sage: f0 = [0,1,0,1,2]      
        sage: f = [V2, f0]          
        sage: is_associated_partition_equitable(Gamma1, Gamma2, f, verbose=False)   
         False
        sage: is_associated_partition_equitable(Gamma1, Gamma2, f, verbose=True)   
         Fails to be equitable because deg( [4] [0, 2] ) isn't defined.
         False
        sage: Gamma1 = graphs.PathGraph(3) 
        sage: Gamma2 = graphs.PathGraph(4) 
        sage: f0 = [0,1,2,2] 
        sage: V2 = Gamma2.vertices(sort=True) 
        sage: f = [V2, f0]                                                                                                    
        sage: is_associated_partition_equitable(Gamma1, Gamma2, f, verbose=True) 
         Fails to be equitable because deg( [1] [2, 3] ) isn't defined.
         False
        sage: is_harmonic_graph_morphism(Gamma1, Gamma2, f, verbose=False) 
         True

    """
    P = associated_partition_to_morphism(Gamma1, Gamma2, f)
    return is_equitable_partition(Gamma2, P, verbose)


def partition_cell_edges(Gamma, C1, C2):
    """
    Returns the collection of edges in Gamma from a vertex in C1 to one in C2.
    Here, C1, C2 are disjoint sublists of V.

    EXAMPLES:
        sage: V2 = [0,1,2,3,4,5]
        sage: E2 = [(0,1),(0,5),(1,2),(1,4),(2,3),(3,4),(4,5)]
        sage: Gamma2 = Graph([V2,E2])
        sage: C1 = [0,4]
        sage: C2 = [1,3]
        sage: partition_cell_edges(Gamma2, C1, C2)
         [(0, 1), (1, 4), (3, 4)]

    """
    edgs = []
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(sort=True, labels=None)
    for v in C1:
        for w in C2:
            if ((v,w) in E) and not((v,w) in edgs) and not((w,v) in edgs):
                if v<w:
                    edgs = edgs + [(v,w)]
                else:
                    edgs = edgs + [(w,v)]
    return edgs

def weights_of_vertex_to_cell(woGamma, C, v):
    r"""
    Returns the list if weights of the edges from vertex v to cell C,
    where C is a sublist of V.

    EXAMPLES:
        sage: V2 = [0,1,2,3,4,5]
        sage: E2 = [(0,1),(0,5),(1,2),(1,4),(2,3),(3,4),(4,5)]
        sage: Gamma2 = Graph([V2,E2])
        sage: C1 = [0,4]
        sage: C2 = [1,3]
        sage: w2 = [1, 4, 2, 2, 3, 2, 1]
        sage: w20 = [E2, w2]
        sage: e20 = [E2, [1]*len(E2)]
        sage: woGamma2 = [Gamma2, e20, w20]
        sage: weights_of_vertex_to_cell(woGamma2, C2, 0)
         [1]
        sage: weights_of_vertex_to_cell(woGamma2, C2, 4)
         [2, 2]


    """
    Gamma = woGamma[0]
    e0 = woGamma[1]
    wt = woGamma[2]
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(sort=True, labels=None)
    Ew = [(E[j][0], E[j][1], wt[1][j]) for j in range(len(E))]
    Gammaw = Graph([V,Ew], weighted=True)
    L = []
    edgs = []
    for w in C:
        if ((v,w) in E) and not((v,w) in edgs) and not((w,v) in edgs):
            if v<w:
                edgs = edgs + [(v,w)]
            else:
                edgs = edgs + [(w,v)]
        if ((w,v) in E) and not((v,w) in edgs) and not((w,v) in edgs):
            if v>w:
                edgs = edgs + [(w,v)]
            else:
                edgs = edgs + [(v,w)]
    #print(edgs)
    for e in edgs:
        L = L + [weight_at_edge(Gammaw, wt, e)]
    return L

def is_weighted_equitable_partition(woGamma, P, verbose=False):
    r"""
    Returns True if P defines an equitable partition of the vertices
    of the given weighted oriented graph woGamma.
    It returns False otherwise.
    
     woGamma is a triple: [Gamma = (V, E), epsilon, wt], where 
                           epsilon is a pair [E,eps0], 
                            and eps0 is a list of |E| edge orientations,
                           wt is a pair [E,w],   
                            and w is a list of |E| edge weights > 0.
    If, in addition, verbose=True then it also returns the intersection matrix. 

    Gamma must be in standard form.

    P is represented as a list of disjoint lists.

    EXAMPLES:
        sage: V2 = [0,1,2,3,4,5]
        sage: E2 = [(0,1),(0,5),(1,2),(1,4),(2,3),(3,4),(4,5)]
        sage: Gamma2 = Graph([V2,E2])
        sage: C1 = [0,4]
        sage: C2 = [1,3]
        sage: w2 = [1, 4, 2, 2, 3, 2, 1]
        sage: w20 = [E2, w2]
        sage: e20 = [E2, [1]*len(E2)]
        sage: woGamma2 = [Gamma2, e20, w20]
	sage: P = [[0,1],[2,3],[4,5]]
        sage: is_weighted_equitable_partition(woGamma2, P, verbose=False)
         False
        sage: is_weighted_equitable_partition(woGamma2, P, verbose=True)
         At vertex  2  the weights to  [0, 1]  are  [2]
         At vertex  3  the weights to  [0, 1]  are  []
         False
    """
    Gamma = woGamma[0]
    e0 = woGamma[1]
    wt = woGamma[2]
    V = Gamma.vertices(sort=True)
    E = Gamma.edges(sort=True, labels=None)
    #Wts = [sum(weights_of_vertex_to_cell(woGamma, C, v)) for v in C]
    C = []
    for C1 in P:
        for C2 in P:
            L = [sum(weights_of_vertex_to_cell(woGamma, C1, v)) for v in C2]
            if len(list(Set(L)))>1:
                if verbose:
                    for v in C2:
                        print("At vertex ", v, " the weights to ", C1, " are ", weights_of_vertex_to_cell(woGamma, C1, v))
                return False
    if verbose:
        for v in C2:
            print("At vertex ", v, " the weights to ", C1, " are ", weights_of_vertex_to_cell(woGamma, C1, v))
    return True

def weighted_cayley_graph(gp, symm_gp_gens, verbose=False):
    """
    Assumes gp is a permutation gp (a subgp of Sn, some n)
    with a symmetric set of generators, symm_gp_gens.
    Returns 1) a simple weighted Cayley graph in standard form,
            whose edges (u,v) are weighted by the order ord_gp(g_
	    of the generator g such that v = g*u, 
            2) a list of pairs of the vertices of the current
	    graph with the corresponding vertex of the original
	    graph gp.cayley_graph(generators = symm_gp_gens, simple = True)

    EXAMPLES:
        sage: gp = S3xC3; symm_gp_gens = [(1,2),(2,3),(4,5,6),(4,6,5)]
        sage: weighted_cayley_graph(gp, symm_gp_gens)
         Graph on 18 vertices

    """
    Gamma2a = gp.cayley_graph(generators = symm_gp_gens, simple = True)
    A2a = Gamma2a.adjacency_matrix()
    #Gamma2b = graph_convert_to_standard(Gamma2a)
    Gamma2b = Graph(A2a)
    V2a = Gamma2a.vertices()
    V2b = Gamma2b.vertices()
    n = len(V2a)
    vertex_pairs = [(V2b[i], V2a[i]) for i in range(n)]
    if verbose:
        print("Vertices (a): ", V2a,"\n", "Vertices (b): ", V2b, "\n", "Pairs of vertices: ", vertex_pairs)
    E2w = [(V2b[i], V2b[j], gp(g).order()) for i in range(n) for j in range(n) for g in symm_gp_gens if (i != j) and (gp(V2a[i])*gp(g) == gp(V2a[j]))]
    if verbose:
        print("weighted edges: ", E2w)
    #Gamma2w = Graph([V2b, E2w], weighted = True)
    Gamma2w = Graph([V2b, E2w], weighted = True)
    return Gamma2w


def convolve_function_with_filter(g, h, S):
    """
    Notation:
     *  g is a function on the vertices V of a graph Gamma = (V, E) in standard form,
        represented as a list of length n = |V|,
     * h is a fixed filter function, represented as a polynomial, h(x).
     * S is a shift operator on Gamma represented by a symmetric nxn matrix, 
       S = (s_{ij}), where s_{ij} = 0 if (i,j) is not an edge in Gamma.
 
    We assume everything has coefficients in QQ.

    Returns the graph convolution

          h *_S g = h(S)g,

    another vector of length n.

    EXAMPLES:
        sage: Gamma = graphs.DiamondGraph()
        sage: V = Gamma.vertices(); n = len(V); n
         4
        sage: g = [2,1,0,-1]
        sage: h(x) = 1+2*x+3*x^2+5*x^7
        sage: S = Gamma.adjacency_matrix()
        sage: convolve_function_with_filter(g, h, S)
         (13, 15, 13, 10)
        sage: g = [1,0,0,0]; g; convolve_function_with_filter(g, h, S)
        [1, 0, 0, 0]
        (11, 8, 8, 10)
        sage: g = [0,1,0,0]; g; convolve_function_with_filter(g, h, S)
        [0, 1, 0, 0]
        (8, 16, 13, 8)
        sage: g = [0,0,1,0]; g; convolve_function_with_filter(g, h, S)
        [0, 0, 1, 0]
        (8, 13, 16, 8)
        sage: g = [0,0,0,1]; g; convolve_function_with_filter(g, h, S)
        [0, 0, 0, 1]
        (10, 8, 8, 11)


    """
    n = len(S.rows())
    d = h(x).degree(x)
    h_coeffs = [ZZ(h.coefficient(x,i)) for i in range(d+1)]
    hS = sum([h_coeffs[i]*S^i for i in range(d)])
    cnv = hS*vector(g)
    return cnv
    