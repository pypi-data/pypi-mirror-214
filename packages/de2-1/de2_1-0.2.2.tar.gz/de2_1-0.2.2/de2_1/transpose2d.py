from typing import List

def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    """
    Transposes a 2D matrix by flipping its rows and columns.

    Args:
        input_matrix (List[List[float]]): The input matrix to be transposed.
            It is expected to be a 2D list of floats.

    Returns:
        List[List[float]]: The transposed matrix as a 2D list of floats.

    Examples:
        >>> input_matrix = [[1, 2, 3], [4, 5, 6]]
        >>> result = transpose2d(input_matrix)
        >>> print(result)
        [[1, 4], [2, 5], [3, 6]]

        >>> input_matrix = [[1, 2], [3, 4], [5, 6]]
        >>> result = transpose2d(input_matrix)
        >>> print(result)
        [[1, 3, 5], [2, 4, 6]]

    Notes:
        - The input_matrix should be a 2D list of floats.
        - The function uses the `zip(*input_matrix)` expression to perform the transpose operation.
        - The rows of the input_matrix become the columns of the transposed matrix, and vice versa.
        - The resulting transposed matrix has dimensions (number of columns, number of rows) compared to the input matrix.
        - The function returns the transposed matrix as a 2D list of floats.
    """
    return list(map(list, zip(*input_matrix)))