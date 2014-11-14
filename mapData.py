####### Map Entities #######
M = "^"       # Mountion/Rocks
G = "&"       # Static Goblin
R = "&"       # Random Goblin
C = "#"       # Treasure Chest
X = "%"       # Guarded Chest
e = " "       # Empty Space
D = u"\u2504" # Door
P = "P"       # Player

# Walls
V = u"\u2551" # vertical
H = u"\u2550" # horizontal
L = u"\u255A" # bottom-left
J = u"\u255D" # bottom-right
F = u"\u2554" # top-left
T = u"\u2557" # top-right
obsticles = [M, V, H, L, J, F, T]

######### Main Map #########
         # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
terMap = [[M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M,], #00
          [M, M, M, M, M, M, M, M, M, M, M, F, H, H, H, H, H, H, H, H, H, H, H, T, M,], #01
          [M, M, M, e, M, M, M, M, M, M, M, V, F, T, e, e, e, e, e, e, e, F, T, V, M,], #02
          [M, M, M, e, e, M, e, e, M, M, M, V, L, J, F, H, H, H, H, H, T, L, J, V, M,], #03
          [M, M, e, e, e, e, e, e, e, M, e, V, F, T, V, F, H, H, H, T, V, F, T, V, M,], #04
          [M, M, e, e, e, e, e, e, e, e, e, V, L, J, V, V, e, e, e, V, V, L, J, V, M,], #05
          [M, M, e, e, e, e, e, e, e, e, M, V, F, T, V, V, e, e, e, V, V, F, T, V, M,], #06
          [M, M, M, e, e, e, e, e, e, M, M, V, L, J, V, V, e, e, e, V, V, L, J, V, M,], #07
          [M, M, e, e, e, e, e, e, e, e, M, V, F, T, V, L, H, H, H, J, V, F, T, V, M,], #08
          [M, M, e, e, e, e, e, e, e, e, e, V, L, J, L, H, H, H, H, H, J, L, J, V, M,], #09
          [M, M, e, e, e, e, e, e, e, e, e, V, F, H, T, e, e, e, e, e, F, H, T, V, M,], #10
          [M, M, M, e, e, e, e, e, e, e, e, V, V, e, V, F, H, D, H, T, V, e, V, V, M,], #11
          [M, M, M, e, e, e, e, e, e, e, e, V, L, H, J, V, e, e, e, V, L, H, J, V, M,], #12
          [M, M, M, e, e, e, e, e, e, e, e, L, H, H, H, J, e, e, e, L, H, H, H, J, M,], #13
          [M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M, M,], #14
          [M, M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M, M,], #15
          [M, M, M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M,], #16
          [M, M, M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M, M,], #17
          [M, M, M, e, e, e, e, e, e, e, e, e, M, M, e, e, e, e, e, e, e, e, e, e, M,], #18
          [M, M, M, e, e, e, e, e, e, e, e, e, M, M, e, e, e, e, e, e, e, e, e, e, M,], #19
          [M, M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M,], #20
          [M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M,], #21
          [M, M, e, e, e, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M, M, M, M,], #22
          [M, M, M, M, M, M, M, e, e, e, e, e, M, M, M, M, e, e, e, e, M, M, M, M, M,], #23
          [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M,]] #24
