from typing import List
import numpy as np

def window1d(input_array: List | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> List | np.ndarray:
    """
    Generate overlapping windows of a specified size from a 1D input array.

    Args:
        input_array (Union[List, np.ndarray]): The 1D input array.
        size (int): The size of the window.
        shift (int, optional): The shift value between windows. Default is 1.
        stride (int, optional): The stride value for moving the window. Default is 1.

    Returns:
        List[Union[List, np.ndarray]]: A list of windows, where each window is either a list or a 1D NumPy array.

    Raises:
        TypeError: If the input_array is not a list or a 1D NumPy array.
        ValueError: If the size, shift, or stride is not a positive integer.

    Examples:
        >>> input_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> size = 3
        >>> shift = 2
        >>> stride = 1
        >>> result = window1d(input_array, size, shift, stride)
        >>> print(result)
        [[1, 2, 3], [3, 4, 5], [5, 6, 7], [7, 8, 9]]

        >>> input_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> size = 4
        >>> shift = 3
        >>> stride = 2
        >>> result = window1d(input_array, size, shift, stride)
        >>> print(result)
        [array([1, 2, 3, 4]), array([4, 5, 6, 7]), array([7, 8, 9])]

    Notes:
        - The input_array should be a 1D array, either a list or a 1D NumPy array.
        - The size represents the length of each window.
        - The shift determines the step size for moving the window starting position.
        - The stride determines the step size for moving the window elements.
        - If the window cannot fit entirely within the input_array, it is skipped.
        - The function returns a list of windows, where each window is either a list or a 1D NumPy array.
    """
    if isinstance(input_array, np.ndarray):
        array_type = np.ndarray
    elif isinstance(input_array, list):
        array_type = list
    else:
        raise TypeError("input_array must be a list or a 1D Numpy array")

    if size <= 0 or shift <= 0 or stride <= 0:
        raise ValueError("size, shift, and stride must be positive integers")

    if not isinstance(size, int) or not isinstance(shift, int) or not isinstance(stride, int):
        raise ValueError("size, shcat ~/.ssh/id_ed25519.pubift, and stride must be integers")

    result = []
    index = 0
    array_length = len(input_array)

    while index + size <= array_length:
        window = input_array[index:index+size:stride]
        result.append(array_type(window))
        index += shift

    return result