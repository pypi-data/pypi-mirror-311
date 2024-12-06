from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import numpy as np
import pct_tools._ext
from scipy.sparse import csr_matrix

if TYPE_CHECKING:
    from typing import Any


class ShuffleMethod(int, Enum):
    BLOSC_SHUFFLE = 1
    BLOSC_BITSHUFFLE = 2


def construct_matrix(
    filename: str,
    row_indexes: np.ndarray[Any, np.dtype[np.int32]],
    col_indexes: np.ndarray[Any, np.dtype[np.int32]],
    values: np.ndarray[Any, np.dtype[np.float32]],
    img_shape: tuple[int, int, int],
    compression_level: int = 3,
    shuffle_method: ShuffleMethod = ShuffleMethod.BLOSC_SHUFFLE,
    verbose_level: int = 0,
) -> None:
    """Construct and store a matrix from a list of indices and values.

    Args:
        filename: The filename of the output file.
        row_indexes: The row indices of the matrix elements.
        col_indexes: The column indices of the matrix elements.
        values: The values of the matrix elements.
        img_shape: The expected shape of the image.
        compression_level: The compression level 0-9 to use. Default is 3.
        shuffle_method: The blosc shuffle method to use. Default is byte shuffling.
        verbose_level: The verbosity level.
    """
    pct_tools._ext.construct_matrix(
        filename,
        row_indexes,
        col_indexes,
        values,
        img_shape,
        compression_level,
        shuffle_method,
        verbose_level,
    )


def read_matrix(filename: str) -> csr_matrix:
    """Read compressed Eigen matrix from disk.

    Args:
        filename: Name of the file containing the matrix.

    Returns:
        The matrix as a sparse matrix of 32-bit floats in CSR format.
    """
    return pct_tools._ext.read_matrix(filename)


def read_compressed_matrix(filename: str, verbosity_level: int = 0) -> csr_matrix:
    """Read compressed Eigen matrix from disk.

    Args:
        filename: Name of the file containing the matrix.

    Returns:
        The matrix as a sparse matrix of 32-bit floats in CSR format.
    """
    return pct_tools._ext.read_compressed_matrix(filename, verbosity_level)


def read_compressed_vector(filename: str) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Read compressed Eigen vector from disk.

    Args:
        filename: Name of the file containing the vector.

    Returns:
        The vector as an array of 32-bit floats.
    """
    return pct_tools._ext.read_compressed_vector(filename)


def read_vector(filename: str) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Read an Eigen vector from disk.

    Args:
        filename: Name of the file containing the vector.

    Returns:
        The vector as an array of 32-bit floats.
    """
    return pct_tools._ext.read_vector(filename)


def recompress_matrix(filename: str, compression_level: int) -> None:
    """Read a compressed matrix and store it with a given compression level.

    Args:
        filename: Name of the file containing the matrix.
        compression_level: The compression level to use when storing it.
    """
    return pct_tools._ext.recompress_matrix(filename, compression_level)


def store_compressed_vector(
    vector: np.ndarray[Any, np.dtype[np.float32]],
    filename: str,
    compression_level: int = 1,
    shuffle_method: ShuffleMethod = ShuffleMethod.BLOSC_SHUFFLE,
) -> None:
    """Compress and store a vector.

    Args:
        vector: The vector to compress and store.
        filename: The filename of the output file.
        compression_level: The compression level to use.
        shuffle_method: The blosc shuffle method to use. Default is byte shuffling.
    """
    return pct_tools._ext.store_compressed_vector(vector, filename, compression_level, shuffle_method)


def store_vector(vector: np.ndarray[Any, np.dtype[np.float32]], filename: str) -> None:
    """Store a vector.

    Args:
        x: The vector to store.
        filename: The filename of the output file.
    """
    return pct_tools._ext.store_vector(vector, filename)
