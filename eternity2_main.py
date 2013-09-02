from eternity2_functions import *
from dwave_sapi import local_connection, BlackBoxSolver

##------------------------------------------------------------##
##--------------MAIN ROUTINE----------------------------------##
##------------------------------------------------------------##

solver = local_connection.get_solver("c4-sw_sample")
blackbox_parameter = 30 # This parameter sets the strength vs. speed of BlackBox (higher = more powerful/slower).

# How do we construct our bitstring to send to BlackBox?
# Well, the position along the bitstring could be the position on the board,
# and the numbers contained within can specify which piece goes there and its rotation

# For n=16, 265 positions can be described by 8 bits
# For n=4, 16 positions can be described by 4 bits
# Additionally, each piece can have a rotation (2 bit)
# For the full 16x16 puzzle there are 10 bits per board position = 2560 total optimization variables
# For a 4x4 puzzle there are 6 bits per board position = 96 total optimization variables
n = 4
num_vars = 96

# A test bitstring for n=4, no rotation. Piece index (4 bits) then rotation (2 bits)
#test_bitstring =   [0,0,0,0,  0,0,   0,0,0,1,  0,0,   0,0,1,0,  0,0,   0,0,1,1,  0,0,
#                    0,1,0,0,  0,0,   0,1,0,1,  0,0,   0,1,1,0,  0,0,   0,1,1,1,  0,0,
#                    1,0,0,0,  0,0,   1,0,0,1,  0,0,   1,0,1,0,  0,0,   1,0,1,1,  0,0,
#                    1,1,0,0,  0,0,   1,1,0,1,  0,0,   1,1,1,0,  0,0,   1,1,1,1,  0,0]

test_bitstring =   [1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0,\
                    1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0,\
                    1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0,\
                    1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0,  1,0,0,0,  0,0, ]

tile_list = tiles_16_colors
tile_list_string = "tiles_16_colors"

#Here we create the tiles. We only need to do this once.
for i in range(len(tile_list)):
    build_a_piece(tile_list[i], i, tile_list_string)

row_map = compute_row_map(n)
valid_edges = compute_valid_edges(n, row_map)

#This code allows you to test the visualization routine with a "fake" bitstring
#mismatches = calculate_mismatches(test_bitstring, tile_list, valid_edges, n)
#visualize_board(test_bitstring, tile_list_string, n)

#Now we use Blackbox solver to provide the bitstring definition.
mismatch_function = MismatchFunction(tile_list, valid_edges, n)

blackbox_solver = BlackBoxSolver(solver)
blackbox_answer = blackbox_solver.solve(mismatch_function, num_vars, cluster_num = 2, \
                                        min_iter_inner = blackbox_parameter, \
                                        max_iter_outer= blackbox_parameter, \
                                        unchanged_threshold=blackbox_parameter, \
                                        max_unchanged_objective_outer=blackbox_parameter, \
                                        max_unchanged_objective_inner = blackbox_parameter, \
                                        unchanged_best_threshold = blackbox_parameter, verbose=1)
print blackbox_answer
blackbox_answer_bin = [(item+1)/2 for item in blackbox_answer] # converting to 0/1 from -1/+1

print "The best bit string we found was:",blackbox_answer_bin
print "The number of mismatches is:", calculate_mismatches(blackbox_answer_bin, tile_list, valid_edges, n)
print "The number of bad tiles is:", calculate_bad_tile_choice(blackbox_answer_bin, n, verbose=0)/3
print "The number of bad corners is:", calculate_bad_corner_choice(blackbox_answer_bin)/5
print "The number of bad edges is:", calculate_bad_edge_choice(blackbox_answer_bin)/4

visualize_board(blackbox_answer_bin, tile_list_string, n)