from io import IOBase

import numpy as np
from PIL import Image

def load_image(data: IOBase) -> np.ndarray:
    """
    Load image from file-like object
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
    """
    Load numpy array from file-like object
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
    """
    Load numpy array from file-like object
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
    """
    Load numpy array from file-like object
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
    """
    Load numpy array from file-like object
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
    """
    Load numpy array from file-like object
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
    """
    Load numpy array from file-like object based on file extension
    Parameters
    ----------
    data: IOBase
        File-like object
    Returns
    -------
    numpy.ndarray
        Array refresentation of the image
    """
    if name.endswith('.npy'):
        return load_npy(data)
    elif name.endswith('.txt'):
        return load_txt(data)
    elif name.endswith('.csv'):
        return load_csv(data)
    elif name.endswith('.tsv'):
        return load_tsv(data)
    elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
        return load_image(data)
    elif name.endswith('.wav') or name.endswith('.mp3'):
        return load_audio(data)
    else:
        raise ValueError(f"Unsupported file extension: {name}")
