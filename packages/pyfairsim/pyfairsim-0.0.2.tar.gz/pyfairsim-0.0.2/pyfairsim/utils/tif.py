import logging
import os
import math
import numpy as np
import numpy.typing as npt
import PIL
from PIL.TiffTags import TAGS
from typing import List, Tuple, Dict

# from sim_algorithm.SIM_Parameters import SIM_Parameters
SIM_Parameters = "SIM_Parameters"

logger = logging.getLogger(__name__)


def find_tifs(destination: str) -> List[str]:
    files = []
    for path in os.walk(destination):
        for filename in path[2]:
            if filename.endswith(".tif") or filename.endswith(".tiff"):
                files.append(path[0] + "\\" + filename)
    return files


def tif_basename(filename: str) -> str:
    if filename.endswith(".tiff"):
        return filename[:-5]
    elif filename.endswith(".tif"):
        return filename[:-4]
    else:
        raise ValueError(f"file {filename} dosent end with .tif/.tiff")


def load_tif(image_path: str) -> Tuple[List, Dict]:
    # load image and metadata from file
    with PIL.Image.open(image_path) as tif:
        # assinge the human readable tags to the meta data dict
        meta_data = {
            TAGS[key]: tif.tag[key] for key in tif.tag.keys() if key in TAGS.keys()
        }

        # load images and save them as np arrays in a list
        images = []
        for image_count in range(tif.n_frames):
            tif.seek(image_count)
            images.append(np.array(tif))

        return images, meta_data


def save_tif(image: npt.ArrayLike, path: str) -> None:
    im = PIL.Image.fromarray(image)
    im.save(path)


def order_images(
    images, number_dirs: int, number_phases: int, ordering: str, z_slice: int
):
    length = len(images)
    if (length % (number_dirs * number_phases)) != 0:
        logger.warning(f"the provieded imagestack has missing images.")
    ordering = ordering
    ordered_images = []
    z_slice = z_slice  # 2 for beads, 4 for Lsec
    if ordering == "pza":
        t = length // number_dirs
        for angle in range(number_dirs):
            for phase in range(number_phases):
                ordered_images.append(
                    images[angle * t + phase + z_slice * number_phases]
                )
    elif ordering == "paz":  # this is what we want
        ordered_images = images
    elif ordering == "apz":
        raise NotImplementedError
    elif ordering == "azp":
        raise NotImplementedError
    elif ordering == "zap":
        raise NotImplementedError
    elif ordering == "zpa":
        raise NotImplementedError
    else:
        raise NotImplementedError(f"ordering {ordering} not supported.")
    return ordered_images


def pad_image(image: npt.ArrayLike) -> npt.ArrayLike:
    """
    takes a rectangular image and transforms it into a quadratic
    image with dimensions that are a power of 2 for faster fft.
    @param image numpy array of the image that needs padding"""
    pass  # ToDo


def fade_border_cos(image: np.array, pixels: int) -> np.array:
    """
    Fades borders (sizes px) of the input to zero.
    Done by multiplying sin^2(x) mapped [0..px] to [pi/2..0].
    Good step before zero-padding data for high-res FFT.
    @param image numpy array to fade borders
    @param pixels Size of faded region in pixels
    """
    h, w = image.shape
    fac = 1.0 / pixels * math.pi / 2

    # vertical
    for x in range(w):
        # top
        for y in range(pixels):
            image[y][x] *= math.pow(math.sin(y * fac), 2)
        # bottom
        for y in range(h - pixels, h):
            image[y][x] *= math.pow(math.sin((h - y - 1) * fac), 2)
    # horizontal
    for y in range(h):
        # left
        for x in range(pixels):
            image[y][x] *= math.pow(math.sin(x * fac), 2)
        # right
        for x in range(w - pixels, w):
            image[y][x] *= math.pow(math.sin((w - x - 1) * fac), 2)

    return image


def fft_images(images, number_directions: int, number_phases: int, background: float):
    """
    takes a flat list/array, removes background and fade borders with a cos^2 and then ffts the image.
    returns a array with angle in the first component and phase in the second
    """
    raw_images = np.zeros(
        (
            number_directions,
            number_phases,
            images[0].shape[0],
            images[0].shape[1],
        ),
        dtype=complex,
    )

    for angle in range(number_directions):
        for phase in range(number_phases):
            # select current image
            tmp = images[angle * number_phases + phase]
            

            # convert to float to avoid overflow when substracting
            tmp = tmp.astype(float, copy=True)
            # substract background
            tmp -= background
            tmp[tmp < 0] = 0
            #print(f" input flt {angle} {phase} {np.sum(tmp * tmp)}")

            # apply simple windowing
            tmp = fade_border_cos(tmp, 15)
            #print(f"before fft {angle} {phase} {np.sum(tmp * tmp)}")

            # fft the image
            tmp = np.fft.fft2(tmp, norm="backward")
            #print(f"after fft {angle} {phase} {np.sum(np.abs(tmp * tmp))}")

            # save the image
            raw_images[angle][phase] = tmp

    return raw_images
