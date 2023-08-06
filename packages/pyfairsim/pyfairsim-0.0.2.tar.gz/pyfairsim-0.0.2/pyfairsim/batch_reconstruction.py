import logging
import time

import numpy as np

from pyfairsim.sim_algorithm.SIM_Utils import estimate_parameters, run_reconstruction

from pyfairsim.utils.argparse import parse_args_batch_reconstruction
from pyfairsim.utils.load_settings import load_settings, save_settings
from pyfairsim.utils.tif import (
    load_tif,
    order_images,
    fft_images,
    find_tifs,
    tif_basename,
    save_tif,
)


def main():
    args = parse_args_batch_reconstruction()

    logging.basicConfig(level=args.level)
    global logger
    logger = logging.getLogger()
    logger.info(
        f"Running batch reconstruction on {args.destination} with settings in {args.settings_filename}"
    )

    if args.settings_filename:
        logger.debug(f"loading settings from {args.settings_filename}")
        settings = load_settings(args.settings_filename)
    else:
        logger.warning(f"no settings provided fall back on default settings")
        settings = load_settings(args.destination)

    files_to_reconstruct = find_tifs(args.destination)

    logger.info(f"found {len(files_to_reconstruct)} to reconstruct")

    for filename in files_to_reconstruct:
        try:
            # load images
            logger.debug(f"loading images from {filename}")
            images, _ = load_tif(filename)
            if (
                len(images)
                < len(settings.directions) * settings.directions[0].number_phases
            ):
                logger.error(
                    f"given image stack has to few images n={len(images)} but at least {len(settings.directions) * settings.directions[0].number_phases} are expected"
                )
                raise ValueError("Provided image stack has to few images")

            # order images
            logger.debug(f"order images")
            ordered_images = order_images(
                images,
                len(settings.directions),
                settings.directions[0].number_phases,
                settings.image_parameters.ordering,
                settings.image_parameters.z_slice,
            )

            # fft images
            logger.debug("fft images")
            raw_images = fft_images(
                ordered_images,
                len(settings.directions),
                settings.directions[0].number_phases,
                settings.image_parameters.background,
            )

            # do k-vector and phase estimation
            logger.info(f"run k-vector estimation")
            start = time.time()
            estimate_parameters(settings, raw_images, False)
            stop = time.time()
            logger.info(f"parameter estimation done in {stop-start:.2f} s.")

            save_settings(
                settings, tif_basename(filename) + "_settings.json", overwrite=False
            )

            logger.info(f"run reconstruction")
            start = time.time()
            result = run_reconstruction(settings, raw_images)
            stop = time.time()
            logger.info(f"reconstruction done in {stop-start:.2f} s.")

            save_tif(result[0], tif_basename(filename) + "_reconstructed.tif")

            widefield_filename = (
                tif_basename(args.out_filename) + "_filtered_widefield.tif"
            )
            save_tif(result[1], widefield_filename)

        except Exception as e:
            logger.error(
                f"Error on {filename} skipped this file because: {e.__class__.__name__}"
            )
            logger.error(str(e))
    return


if __name__ == "__main__":
    main()
