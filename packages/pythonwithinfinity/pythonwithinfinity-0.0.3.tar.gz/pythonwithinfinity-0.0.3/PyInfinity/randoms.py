from PyInfinity.constants import NULL
import random as _random

# Function to generate a random number between `s` and `e`
def rand(s, e, /, *, dtype=int, randnumber=False):
    """
    Returns a random number between s and e.

    Args:
        start (int or float): The start of the range.
        end (int or float): The end of the range.
        
        dtype (tuple[int, int] | list[int, int]): The data type of the random number.
        randnumber (bool): If True, return either `s` or `e` randomly.

    Returns:
        int or float: A random number between start and end.
    """
    # Validate that both `s` (start) and `e` (end) are either integers or floats
    if not (isinstance(s, (int, float)) and isinstance(e, (int, float))):
        raise TypeError('start and end must be int or float')

    # Handle the randnumber flag to directly choose between `s` and `e`
    if isinstance(randnumber, bool):
        if randnumber:
            # Return `s` or `e` randomly
            return s if _random.random(1, 2) == 1 else e
    else:
        # Raise an error if randnumber is not a boolean
        raise TypeError('randnumber must be a bool')

    # Handle cases where dtype is a tuple or list
    if isinstance(dtype, (tuple, list)):
        # Check if dtype specifies integer outputs
        if dtype[0] == int and dtype[1] == int:
            # Ensure both `s` and `e` are integers
            if not (isinstance(s, int) or isinstance(e, int)):
                raise TypeError('start and end must be int')
            return _random.randint(s, e)
        
        # Handle cases where dtype specifies floats or a mix of int and float
        elif (dtype[0] == float and dtype[1] == int) or \
             (dtype[0] == int and dtype[1] == float) or \
             (dtype[0] == float and dtype[1] == float):
            # Ensure both `s` and `e` are either int or float
            if not (isinstance(s, float) or isinstance(e, float)) or \
               not (isinstance(s, int) or isinstance(e, int)):
                raise TypeError('start and end must be int or float')
            return _random.uniform(s, e)
        
        # Raise an error if dtype does not match the expected formats
        else:
            raise TypeError('dtype must be a tuple or list of int and float')
        
    # Handle cases where dtype is directly an integer
    elif dtype == int:
        return _random.randint(s, e)
    
    # Handle cases where dtype is directly a float
    elif dtype == float:
        return _random.uniform(s, e)
    
    # Raise an error for invalid dtype
    else:
        raise TypeError('dtype must be a tuple or list of int and float')


# Function to choose a random object from a list
def choiseObjectInList(list):
    """
    Returns a random object from a list.

    Args:
        list (list): A list of objects.

    Returns:
        object: A random object from the list.
    """
    # Ensure the argument is a list
    if not isinstance(list, list):
        raise TypeError('list must be a list')
    
    # Return NULL if the list is empty
    if len(list) == 0:
        return NULL
    
    # Randomly select and return an object from the list
    return _random.choice(list)


# Function to choose a random object from a tuple
def choiseObjectInTuple(tuple):
    """
    Returns a random object from a tuple.

    Args:
        tuple (tuple): A tuple of objects.

    Returns:
        object: A random object from the tuple.
    """
    # Ensure the argument is a tuple
    if not isinstance(tuple, tuple):
        raise TypeError('tuple must be a tuple')
    
    # Return NULL if the tuple is empty
    if len(tuple) == 0:
        return NULL
    
    # Randomly select and return an object from the tuple
    return _random.choice(tuple)


# Function to recursively choose a random object from a nested list
def randList(list):
    """
    Returns a random object from a list. If the selected object is a list,
    recursively selects an object from it.

    Args:
        list (list): A list of objects.

    Returns:
        object: A random object from the list.
    """
    # Ensure the argument is a list
    if not isinstance(list, list):
        raise TypeError('list must be a list')
    
    # Return NULL if the list is empty
    if len(list) == 0:
        return NULL
    
    # Select a random object from the list
    dt = _random.choice(list)

    # If the selected object is a list, recursively choose from it
    if isinstance(dt, list):
        try:
            return randList(dt)
        except TypeError:
            pass  # Handle cases where recursion fails (no nested list)

    # Return the selected object
    return dt


# Function to generate a random float
def random():
    """
    Generates a random float value. If the float can be represented as an int,
    returns the value as an integer.

    Returns:
        float or int: A random value.
    """
    # Generate a random float
    a = _random.random()
    
    # Check if the float is equivalent to an integer
    if a == int(a):
        return int(a)
    
    # Return the float value
    return a


__all__ = [
    'rand', 
    'choiseObjectInList', 
    'choiseObjectInTuple', 
    'randList', 
    'random'
]