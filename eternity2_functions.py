from numpy import array
from eternity2_tile_definitions import *
import Image as im
from math import log, ceil

def build_a_piece(piece, piece_index, foldername):
    '''Creates a jpg image of a piece given a piece object (which is a list of 4 triangles)
     a piece index for the filename, and a folder to save the piece images in'''
    [top_piece_number, right_piece_number, bottom_piece_number, left_piece_number] = piece
    test_piece = im.open("piece_images/test_piece.png")
    top_piece = im.open("piece_images/piece" + str(top_piece_number) + ".png")
    right_piece = im.open("piece_images/piece" + str(right_piece_number) + ".png")
    bottom_piece = im.open("piece_images/piece" + str(bottom_piece_number) + ".png")
    left_piece = im.open("piece_images/piece" + str(left_piece_number) + ".png")
    for y in range(0,100):
        for x in range(0,100):
            if y<100-x and y<x: # This is the top triangle in the square
                rotation_0 = (x,y)
                rotation_270 = (y,x)
                rotation_180 = (x,99-y)
                rotation_90 = (99-y,99-x)
                pixels = top_piece.getpixel((x,y))
                test_piece.putpixel(rotation_0, pixels)
                pixels = right_piece.getpixel((x,y))
                test_piece.putpixel(rotation_90, pixels)
                pixels = bottom_piece.getpixel((x,y))
                test_piece.putpixel(rotation_180, pixels)
                pixels = left_piece.getpixel((x,y))
                test_piece.putpixel(rotation_270, pixels)
    test_piece.save("piece_images/" + str(foldername) + "/piece_index"+ str(piece_index) + ".png")

def get_piece_indices_from_bitstring(bitstring, n):
    '''Takes a bitstring and returns the indices and rotations of all pieces in their decimal format'''
    piece_indices = []
    piece_rotations = []
    chunk_length = int(ceil(log(n**2, 2))+2)
#    print "chunk_length", chunk_length
    for i in range(n**2):
        bitstring_index = bitstring[chunk_length*i:chunk_length*i+n]
#        bitstring_index = bitstring[6*i:6*i+n]
#        bitstring_index = bitstring[4*i:4*i+n] # - for 2x2 board

        decimal_index = 0
        for i in range(len(bitstring_index)): # Is there a built in Python function that does this?? :)
            if bitstring_index[i]:
                counter = 2**(len(bitstring_index)-i-1)
                decimal_index += counter
        piece_index = decimal_index

#        piece_index = bitstring_index[0]*8+\
#                      bitstring_index[1]*4+\
#                      bitstring_index[2]*2+\
#                      bitstring_index[3]
#        piece_index = bitstring_index[0]*2+\ # - for 2x2 board
#                      bitstring_index[1]
        piece_indices.append(piece_index)
        bitstring_rotation = bitstring[chunk_length*i+n:chunk_length*i+n+2]
#        bitstring_rotation = bitstring[6*i+n:6*i+n+2]
#        bitstring_rotation = bitstring[4*i+n:4*i+n+4] # - for 2x2 board
        piece_rotation =    bitstring_rotation[0]*2+\
                            bitstring_rotation[1]
        piece_rotations.append(piece_rotation)
    return piece_indices, piece_rotations

def visualize_board(bitstring, tile_description_string, n):
    '''Loads corresponding tiles form the tile_description_string
    folder and places them on the board according to the values given in the bitstring.
    Saves the resulting image to a jpg file'''
    piece_indices_by_position, piece_rotations_by_position = get_piece_indices_from_bitstring(bitstring, n)
    small_tile_size = 50
    board_size = small_tile_size*n
    positions_list = []
    rotations = [0,270,180,90]
    for j in range(n):
        for i in range(n):
            positions_list.append([i*board_size/n,j*board_size/n])
    board = im.new("RGB", (board_size,board_size))
    for piece in range(len(piece_indices_by_position)):
        pic_index =  piece_indices_by_position[piece]
        tile = im.open("piece_images/" + str(tile_description_string)+ "/piece_index"+str(pic_index)+".png")
        small_tile = tile.resize((small_tile_size,small_tile_size))
        rotated_small_tile = small_tile.rotate(rotations[piece_rotations_by_position[piece]])
        board.paste(rotated_small_tile, tuple(positions_list[piece]))
    board.save("e2_board.bmp")

def compute_row_map(n):
    '''Compute simple list describing which row pieces belong to, e.g. [0,0,0,1,1,1,2,2,2] for 3x3 board'''
    row_map = []
    for i in range(n):
        the_row = [i]*n
        for each in the_row:
            row_map.append(each)
    return row_map

def get_piece_adjacency(piece_index, row_map, n):
    '''Returns the neighbours of a given piece index, in the format [above, right, below, left]'''
    piece_above_index = n*(row_map[piece_index]-1) + piece_index%n
    if piece_index < n:
        piece_above_index = -1
    piece_right_index = piece_index +1
    if piece_index % n == (n-1):
        piece_right_index = -1
    piece_below_index = n*(row_map[piece_index]+1) + piece_index%n
    if piece_below_index >= n**2-n:
        piece_below_index = -1
    piece_left_index = piece_index -1
    if not piece_index % n:
        piece_left_index = -1
    return [piece_above_index, piece_right_index, piece_below_index, piece_left_index]

def compute_valid_edges(n, row_map):
    '''Computes the edgeset of an nxn eternity 2 board, by examining
    each piece in turn and computing the positions of its top and left neighbours (we only do 2
    edges so that we do not double count). The remaining uncounted bottom right
    edges are added on separately. Outer edges are included in the edgeset and their
    neighbouring edge outside the board area is denoted by the a special '-1' status.'''
    valid_edges = []
    for position in range(n**2):
        adjacency = get_piece_adjacency(position, row_map, n)
        valid_edges.append([position, 0, adjacency[0], 2]) # 0 (top) edge matches 2 (bottom) edge of neighbour
        valid_edges.append([position, 3, adjacency[3], 1]) # 3 (left) edge matches 1 (right) edge of neighbour
        if position % n == (n-1):
            valid_edges.append([position, 1,adjacency[1], 3])
    for position in range(n**2-n,n**2):
        adjacency = get_piece_adjacency(position, row_map, n)
        valid_edges.append([position, 2,adjacency[2], 0])
    return valid_edges

def calculate_mismatches(bitstring, tile_list, valid_edges, n):
    '''Returns a penalty corresponding to the number of mismatched edges in the whole puzzle
    including outer edges. Handles tile rotations'''
    piece_indices_by_position, piece_rotations_by_position = get_piece_indices_from_bitstring(bitstring, n)
    mismatches = 0
    for i in range(len(valid_edges)):
        # piece_rotations are [0,1,2,3] format
        # if it is rotated 0 degrees, you want to add 0 to the edge
        # if it is rotated 90 degrees, you want to add 1 to the edge
        # if it is rotated 180 degrees, you want to add 2 to the edge
        # if it is rotated 270 degrees, you want to add 3 to the edge]
        # but it has to be modulo arithmetic too

        #Then get the positions of the pieces to check
        piece_1_position = valid_edges[i][0]
        piece_2_position = valid_edges[i][2]

        #Then get the 2 edges to check from these pieces after they have been adequately rotated
        edge_to_check_1 = (valid_edges[i][1]-(piece_rotations_by_position[piece_1_position])) % 4
        edge_to_check_2 = (valid_edges[i][3]-(piece_rotations_by_position[piece_2_position])) % 4

        #Now get the tiles that are at these positions:
        tile1 = piece_indices_by_position[piece_1_position]
        tile2 = piece_indices_by_position[piece_2_position]

        # Now get the patterns that are at the relevant edge of both tiles (if the second tile is
        # overflowing the board edge, we check against the "all grey" tile):
        if piece_2_position == -1: #Check for the grey edges
            pattern1 = tile_list[tile1][edge_to_check_1]
            pattern2 = all_grey_tile[edge_to_check_2]
            if pattern1 != pattern2:
                mismatches +=1
        else:
            pattern1 = tile_list[tile1][edge_to_check_1]
#            print "pattern1 =", pattern1
            pattern2 = tile_list[tile2][edge_to_check_2]
#            print "pattern2 =", pattern2
            if pattern1 != pattern2:
                mismatches +=1
    return mismatches

def calculate_bad_tile_choice(bitstring, n, verbose):
    '''Returns a summed penalty if piece indices are used more than once in the bitstring.'''
    allowed_tile_selection = [  [0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],
                                [0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],
                                [1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],
                                [1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]
    penalty = 0
    for i in range(n**2):
        #Going to hardcode this to 4x4 for now!
        selection_to_check = list(bitstring[6*i:6*i+n])
        if verbose: print len(allowed_tile_selection), allowed_tile_selection
        if selection_to_check in allowed_tile_selection:
            allowed_tile_selection.remove(selection_to_check)
        else:
            penalty +=1
            if verbose: print "penalty added", penalty
    if verbose: print '.....end of loop'
    if verbose: print allowed_tile_selection

    return penalty

def calculate_bad_edge_choice(bitstring):
    '''Returns a summed penalty if edge pieces as described by the bitstring
    are not in valid edge locations.'''
    allowed_edge_pieces = [[0,0,0,1],[0,0,1,0],
                           [0,1,0,0],[0,1,1,1],
                           [1,0,0,0],[1,0,1,1],
                            [1,1,0,1],[1,1,1,0]]
    penalty = 0
    #Going to hardcode this to 4x4 for now!!!
    for i in [[6,10], [12,16], [24,28], [42,46], [48,52], [66,70], [78,82], [84,88]]:
    #decimal values for allowed edge pieces = 1,2,4,7,8,11,13,14
        selection_to_check = list(bitstring[i[0]:i[1]])
        if selection_to_check in allowed_edge_pieces:
            allowed_edge_pieces.remove(selection_to_check)
        else:
            penalty +=1
    return penalty

def calculate_bad_corner_choice(bitstring):
    '''Returns a summed penalty if corner pieces as described by the bitstring
    are not in valid corner locations.'''
    allowed_corner_pieces = [[0,0,0,0],[0,0,1,1],
                            [1,1,0,0],[1,1,1,1]]
    penalty =0
    # Going to hardcode this to 4x4 for now!!!
    for i in [[0,4], [18,22], [72,76], [90,94]]:
    #decimal values for corner pieces = 0,3,12,15
        selection_to_check = list(bitstring[i[0]:i[1]])
        if selection_to_check in allowed_corner_pieces:
            allowed_corner_pieces.remove(selection_to_check)
        else:
            penalty +=1
    return penalty

class MismatchFunction(object):
    ''' procesar la funcion objetivo para ser consumida por el BlackBox 
    usando las 4 terminos de penalidad definidos '''
    def __init__(self, tile_list, valid_edges, n): # These are all the variables needed to compute G(D,w)
        self.tile_list = tile_list
        self.valid_edges = valid_edges
        self.n = n

    def __call__(self, states, numStates):
        states_bin  = [(item+1)/2 for item in states] # --------------------- converting to 0/1 from -1/+1
        stateLen = len(states)/numStates # ------------------------------------ this is the length of each individual state; this should be equal to K
        ret = []
        for state_number in range(numStates):
            bitstring = array(states_bin[state_number*stateLen:(state_number+1)*stateLen])
            ''' P1: Calcular el numero de piezas que no encajan '''
            penalty1 = 3 * calculate_mismatches(bitstring, self.tile_list, self.valid_edges, self.n)
            ''' P2: Penalizar aquellos casos donde una pieza se coloque en el mismo lugar de otra '''
            penalty2 = 3 * calculate_bad_tile_choice(bitstring, self.n, verbose =0)
            ''' P3: Penalizar cuando una pieza lateral no contenga el patron gris '''
            penalty3 = 4 * calculate_bad_edge_choice(bitstring)
            ''' P4: Ademas penalizar cuando una pieza de esquina no sea de patron gris '''
            penalty4 = 5 * calculate_bad_corner_choice(bitstring)
            result = penalty1+penalty2+penalty3+penalty4
            ret.append(result)
        return tuple(ret)


  