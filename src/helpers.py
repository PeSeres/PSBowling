
def is_valid_input(value):
    return value in ['', 'X', 'x', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def is_strike(value):
    return value in ['X', 'x']


def is_spare(value):
    return value == '/'
