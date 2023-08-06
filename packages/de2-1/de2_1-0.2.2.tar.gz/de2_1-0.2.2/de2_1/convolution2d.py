import numpy as np

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
    
    output_rows = (input_shape[0] - kernel_shape[0]) // stride + 1
    output_cols = (input_shape[1] - kernel_shape[1]) // stride + 1
    
    output = np.zeros((output_rows, output_cols))
    
    for i in range(output_rows):
        for j in range(output_cols):
            window = input_matrix[
                i * stride : i * stride + kernel_shape[0],
                j * stride : j * stride + kernel_shape[1]]
            
            output[i, j] = np.sum(window * kernel)
    
    return output