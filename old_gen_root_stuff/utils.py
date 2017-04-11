def get_west(index):
    return index - 1 if index % 64 != 0  else None

def get_east(index):
    return index + 1 if index % 64 != 63 else None
    
def get_north(index, array_size):
    return index - 64 if index - 64 >= 0 else (array_size - 64) + index

def get_south(index, array_size):
    return index + 64 if index + 64 < array_size else index % 64
