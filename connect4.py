print("hello world")

meineliste = [21, 11, 79]

for i in meineliste:
    print(i)

reihe = []
gesamt = []

for j in range(0, 8):
    reihe.append("0")
for i in range(0, 7):
    gesamt.append(reihe)

def print_matrix(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i]) - 1):
            print("["+ matrix[i][j]+ "]", end='')
        print("[" + matrix[i][len(matrix[i]) - 1] + "]")

print_matrix(gesamt)

print("len of reihe: ", len(reihe))
print("len of gesamt: ", len(gesamt))

testfeld = (
    [ " ", " ", " ", " ", " ", " ", " ", "1" ],
    [ " ", " ", " ", " ", " ", " ", "1", "0" ],
    [ " ", " ", " ", " ", " ", "1", "0", "1" ],
    [ "1", " ", " ", " ", "1", "1", "0", "0" ],
    [ "0", " ", " ", " ", "0", "1", "1", "0" ],
    [ "1", "1", " ", "1", "0", "0", "1", "0" ],
    [ "1", "0", "0", "1", "0", "0", "0", "1" ]
)

print_matrix(testfeld)

def check_horizontal(matrix, char):
    for i in range(6, -1, -1):
        for j in range(0, 5):
            if matrix[i][j] == char:
                if matrix[i][j + 1] == char:
                    if matrix[i][j + 2] == char:
                        if matrix[i][j + 3] == char:
                            print("won! h")
                            break

def check_vertical(matrix, char):
    for i in range(6, 2, -1):
        for j in range(0, 8):
            if matrix[i][j] == char:
                if matrix[i - 1][j] == char:
                    if matrix[i - 2][j] == char:
                        if matrix[i - 3][j] == char:
                            print("won! v")
                            break


def check_diagonal_ne_to_sw(matrix, char):
    for i in range(0, 4):
        for j in range(0, 4):
            if matrix[i][j] == char:
                if matrix[i + 1][j + 1] == char:
                    if matrix[i + 2][j + 2] == char:
                        if matrix[i + 3][j + 3] == char:
                            print("won! ne2sw")
                            break

# diagonal SW to NE
def check_diagonal_sw_to_ne(matrix, char):
    for i in range(6, 2, -1):
        for j in range(0, 4):
            if matrix[i][j] == char:
                if matrix[i - 1][j + 1] == char:
                    if matrix[i - 2][j + 2] == char:
                        if matrix[i - 3][j + 3] == char:
                            print("won! sw2ne")
                            break

def check_for_win(matrix, char):
    check_horizontal(matrix, char)
    check_vertical(matrix, char)
    check_diagonal_ne_to_sw(matrix, char)
    check_diagonal_sw_to_ne(matrix, char)

check_for_win(testfeld, "1")
