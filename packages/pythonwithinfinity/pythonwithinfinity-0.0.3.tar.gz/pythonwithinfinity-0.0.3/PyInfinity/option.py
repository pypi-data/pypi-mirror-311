from typing import Self, Union

class Option:
    """
    A class to manage options with associated arguments.

    Attributes:
        options (dict): A dictionary to store options and their arguments.
    """
    def __init__(self: Self) -> None:
        """
        Initialize the Option class with an empty dictionary.
        """
        self.options = {}

    def setOption(self: Self, option: str, args: Union[list[str], tuple[str]]) -> None:
        """
        Sets a single option with its arguments.

        Args:
            option (str): The name of the option.
            args (list[str] | tuple[str]): Arguments associated with the option.

        Raises:
            TypeError: If `option` is not a string.
            TypeError: If `args` is not a list or tuple.
            TypeError: If any item in `args` is not a string.
        """
        # Validate that `args` is either a list or a tuple
        if not isinstance(args, (list, tuple)):
            raise TypeError('args must be a list or tuple')
        
        # Validate that `option` is a string
        if not isinstance(option, str):
            raise TypeError('option must be a string')
        
        # Validate that every element in `args` is a string
        for a in args:
            if not isinstance(a, str):
                raise TypeError('args must contain only strings')
        
        # Assign the arguments to the option
        self.options[option] = list(args)

    def setOptions(self: Self, 
                   option: Union[tuple[str], list[str]], 
                   args: Union[tuple[Union[list[str], tuple[str]]], list[Union[list[str], tuple[str]]]]) -> None:
        """
        Sets multiple options with their respective arguments.

        Args:
            option (tuple[str] | list[str]): A collection of option names.
            args (tuple[list[str] | tuple[str]] | list[list[str] | tuple[str]]): Arguments for each option.

        Raises:
            TypeError: If `option` is not a tuple or list.
            TypeError: If `args` is not a tuple or list.
            TypeError: If any item in `option` is not a string.
            TypeError: If any argument group in `args` is not a list or tuple.
            TypeError: If any item within the argument groups is not a string.
        """
        # Validate that `option` is either a tuple or list
        if not isinstance(option, (tuple, list)):
            raise TypeError('option must be a tuple or list')
        
        # Validate that `args` is either a tuple or list
        if not isinstance(args, (tuple, list)):
            raise TypeError('args must be a tuple or list')
        
        # Ensure all items in `option` are strings
        for o in option:
            if not isinstance(o, str):
                raise TypeError('option must contain only strings')
        
        # Validate that all items in `args` are lists or tuples, and contain only strings
        lvl = 0
        for a in args:
            try:
                for ai in a:
                    if not isinstance(ai, str):
                        raise TypeError('args must contain only strings')
            except TypeError:
                raise TypeError(f'args[{lvl}] must be a tuple or list')
            lvl += 1

        # Assign arguments to each option
        for o, a in zip(option, args):
            self.options[o] = list(a)

    def __repr__(self: Self) -> str:
        """
        Provides a string representation of the Option object.

        Returns:
            str: The dictionary of options in string format.
        """
        return repr(self.options)