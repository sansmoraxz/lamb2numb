"""Functions for loading data from file-like objects."""

from io import IOBase

import numpy as np
from PIL import Image


def load_image(data: IOBase) -> np.ndarray:
    """Load image from file-like object.

    Parameters
    ----------
    data: IOBase
        File-like object

    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    image = Image.open(data)
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

def load_audio(data: IOBase) -> np.ndarray:
    """Load numpy array from file-like object.

    Parameters
    ----------
    data: IOBase
        File-like object

    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    return np.frombuffer(data.read(), dtype=np.int16)

def load_npy(data: IOBase) -> np.ndarray:
    """Load numpy array from file-like object.

    Parameters
    ----------
    data: IOBase
        File-like object

    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    return np.load(data)

def load_txt(data: IOBase) -> np.ndarray:
    """Load numpy array from file-like object.

    Parameters
    ----------
    data: IOBase
        File-like object

    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    return np.loadtxt(data)

def load_csv(data: IOBase) -> np.ndarray:
    """Load numpy array from file-like object.

    Parameters
    ----------
    data: IOBase
        File-like object

    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    return np.loadtxt(data, delimiter=',')

def load_tsv(data: IOBase) -> np.ndarray:
    """Load numpy array from file-like object.

    Parameters
    ----------
    data: IOBase
        File-like object

    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    return np.loadtxt(data, delimiter='\t')


def auto_loader(data: IOBase, name: str) -> np.ndarray:
    """Load numpy array from file-like object based on file extension.

    Parameters
    ----------
    data: IOBase
        File-like object
    name: str
        File name

    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    if name.endswith('.npy'):
        return load_npy(data)
    if name.endswith('.txt'):
        return load_txt(data)
    if name.endswith('.csv'):
        return load_csv(data)
    if name.endswith('.tsv'):
        return load_tsv(data)
    if name.endswith(('.jpg', '.jpeg', '.png')):
        return load_image(data)
    if name.endswith(('.wav', '.mp3')):
        return load_audio(data)
    err_msg = f'Unsupported file extension: {name}'
    raise ValueError(err_msg)
