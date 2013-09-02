# This is the file that contains the tile definitions
# For the visualizations to work properly, your tiles MUST be in the
# same order in the tileset as the images are in the corresponding folder of the same name
# This shouldn't be too much of an issue as you use the build_tile routine to create
# the images in the first place.
#
# "Tile Number","Top Edge Design","Right Edge Design","Bottom Edge Design","Left Edge Design"],

# # Design Reference Numbers],
#  0 - Edge (Grey),
#  1 - Red
#  2 - Yellow
#  3 - Bright Green
#  4 - Bright Blue
#  5 - Magenta
#  6 - Cyan
#  7 - Orange
#  8 - Purple
#  9 - Peach
# 10 - Pink
# 11 - Teal
# 12 - Mid green
# 13 - Aubergine
# 14 - Dark Red
# 15 - Pale blue green
# 16 - Apple green
# 17 - Brown
# 18 - Violet
# 19 - Pale yellow
# 20 - Red Pink
# 21 - Racing green
# 22 - Black


tiles_16_test = [\
[1,17,0,0], [1,5,0,0], [9,17,0,0], [17,9,0,0],
[2,1,0,1], [10,9,0,1], [6,1,0,1], [6,13,0,1],
[11,17,0,1], [7,5,0,1], [15,9,0,1], [8,5,0,1],
[8,13,0,1], [21,5,0,1], [10,1,0,9], [18,17,0,9]]

tiles_4_test = [\
[1,17,0,0], [1,5,0,0],
[9,17,0,0], [17,9,0,0]]

tiles_16_test2 = [\
[1,17,0,0], [1,17,0,0], [1,17,0,0], [1,17,0,0],
[1,17,0,0], [1,17,0,0], [1,17,0,0], [1,17,0,0],
[1,17,0,0], [1,17,0,0], [1,17,0,0], [1,17,0,0],
[1,17,0,0], [1,17,0,0], [1,17,0,0], [1,17,0,0],
]

tiles_16_solved = [\
[0,1,9,0],  [0,1,10,1],   [0,9,2,1],   [0,0,9,9],
[9,10,9,0], [10,10,2,10], [2,2,10,10], [9,0,9,2],
[9,10,1,0], [2,2,2,10],   [10,10,2,2], [9,0,1,10],
[1,1,0,0],  [2,1,0,1],    [2,9,0,1],   [1,0,0,9]]

all_grey_tile = [0,0,0,0]

tiles_16_degenerate = [\
[1,1,0,0],  [2,1,0,1],   [2,1,0,1],   [1,1,0,0],
[2,1,0,1], [2,2,2,2], [2,2,2,2], [2,1,0,1],
[2,1,0,1], [2,2,2,2],   [2,2,2,2], [2,1,0,1],
[1,1,0,0],  [2,1,0,1],    [2,1,0,1],   [1,1,0,0]]

tiles_16_colors = [\
[0,1,2,0],  [0,3,1,1],   [0,2,2,3],   [0,0,4,2],
[2,3,4,0],  [1,1,4,3],   [2,4,1,1],   [4,0,2,4],
[4,1,2,0],  [4,2,3,1],   [1,2,2,2],   [2,0,1,2],
[2,3,0,0],  [3,4,0,3],   [2,3,0,4],   [1,0,0,3]]