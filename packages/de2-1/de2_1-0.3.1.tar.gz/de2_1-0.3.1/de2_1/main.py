from typing import List
import numpy as np


def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    """
    Transposes a 2D matrix by flipping its rows and columns.

    Args:
        input_matrix (List[List[float]]): The input matrix to be transposed.
            It is expected to be a 2D list of floats.

    Returns:
        List[List[float]]: The transposed matrix as a 2D list of floats.



    Notes:
        - The input_matrix should be a 2D list of floats.
        - The function uses the `zip(*input_matrix)` expression to perform the transpose operation.
        - The rows of the input_matrix become the columns of the transposed matrix, and vice versa.
        - The resulting transposed matrix has dimensions (number of columns, number of rows) compared to the input matrix.
        - The function returns the transposed matrix as a 2D list of floats.
    """
    return list(map(list, zip(*input_matrix)))

def window1d(input_array: List | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> List | np.ndarray:
    """
    Generate overlapping windows of a specified size from a 1D input array.

    Args:
        input_array List or np.ndarray The 1D input array.
        size (int): The size of the window.
        shift (int, optional): The shift value between windows. Default is 1.
        stride (int, optional): The stride value for moving the window. Default is 1.

    Returns:
        List or  np.ndarray: A list of windows, where each window is either a list or a 1D NumPy array.

    Raises:
        TypeError: If the input_array is not a list or a 1D NumPy array.
        ValueError: If the size, shift, or stride is not a positive integer.

    Notes:
        - The input_array should be a 1D array, either a list or a 1D NumPy array.
        - The size represents the length of each window.
        - The shift determines the step size for moving the window starting position.
        - The stride determines the step size for moving the window elements.
        - If the window cannot fit entirely within the input_array, it is skipped.
        - The function returns a list of windows, where each window is either a list or a 1D NumPy array.
    """
    if isinstance(input_array, np.ndarray):
        array_type = np.array
    elif isinstance(input_array, list):
        array_type = list
    else:
        raise TypeError("input_array must be a list or a 1D Numpy array")

    if size <= 0 or shift <= 0 or stride <= 0:
        raise ValueError("size, shift, and stride must be positive integers")

    if not isinstance(size, int) or not isinstance(shift, int) or not isinstance(stride, int):
        raise ValueError("size, shcat ~/.ssh/id_ed25519.pubift, and stride must be integers")

    if array_type == list : input_array = np.array(input_array)

    n_records = len(input_array)
    num_windows = (n_records - size) // shift + 1

    new_view_structure = np.lib.stride_tricks.as_strided(
        input_array,
        shape=(num_windows, size),
        strides=(input_array.itemsize * shift * stride, input_array.itemsize * stride),
        writeable=False
    )

    result = [array_type(window) for window in new_view_structure]
    return result


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Perform 2D convolution on an input matrix using a given kernel.

    Args:
        input_matrix (np.ndarray): The input matrix to convolve.
        kernel (np.ndarray): The convolution kernel.
        stride (int, optional): The stride value for the sliding window. Default is 1.

    Returns:
        np.ndarray: The convolved output matrix.

    Raises:
        ValueError: If the dimensions of the input matrix and kernel are incompatible.

    Notes:
        - The input_matrix and kernel should be two-dimensional NumPy arrays.
        - The stride determines the step size for moving the kernel across the input_matrix.
        - The function performs valid convolution, meaning the output size is determined by the input size,
        kernel size, and stride. No padding is applied.

    Examples:
        >>> input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> kernel = np.array([[0, 1], [1, 0]])
        >>> stride = 1
        >>> result = convolution2d(input_matrix, kernel, stride)
        >>> print(result)
        [[13. 18.]
        [24. 29.]]
    """
    
    input_shape = input_matrix.shape
    kernel_shape = kernel.shape
    if input_shape[0] < kernel_shape[0] or input_shape[1] < kernel_shape[1]:
        raise ValueError("Dimensions of the input matrix and kernel are incompatible.")
    

    output_rows = (input_shape[0] - kernel_shape[0]) // stride + 1
    output_cols = (input_shape[1] - kernel_shape[1]) // stride + 1
    
    output = np.zeros((output_rows, output_cols), dtype=np.float64)
    
    for i in range(output_rows):
        for j in range(output_cols):
            window = np.lib.stride_tricks.as_strided(input_matrix[
                i * stride : i * stride + kernel_shape[0],
                j * stride : j * stride + kernel_shape[1]
            ].astype(np.float64),
            shape=kernel_shape)

            output[i, j] = np.sum(window * kernel)
    
    return output


