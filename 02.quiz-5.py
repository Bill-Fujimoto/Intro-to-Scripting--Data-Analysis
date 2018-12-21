NUM_ROWS = 25
NUM_COLS = 25

# construct a matrix
my_matrix = []
for row in range(NUM_ROWS):
    new_row = []
    for col in range(NUM_COLS):
        new_row.append(row * col)
    my_matrix.append(new_row)
 
 
def trace(matrix):
    '''Computes the sum of diagonal for square matrix'''
    size = len(matrix[0])
    sum = 0
    for idx in range(size):
        sum += matrix[idx][idx]
         
    return sum

print(trace(my_matrix))