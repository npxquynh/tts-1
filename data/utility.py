import math

def calculate_square(dictionary):
    """
    sqrt(a1 ^ 2 + a2 ^ 2 + ...)
    """
    result = 0
    for value in dictionary.values():
        result += value

    return math.sqrt(result)

