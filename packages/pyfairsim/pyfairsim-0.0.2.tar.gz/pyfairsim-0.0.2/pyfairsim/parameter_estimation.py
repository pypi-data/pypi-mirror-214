import logging
import time

import numpy as np

from pyfairsim.sim_algorithm.SIM_Utils import estimate_parameters

from pyfairsim.utils.argparse import parse_args_k_estimation
from pyfairsim.utils.load_settings import load_settings, save_settings
from pyfairsim.utils.tif import load_tif, order_images, fft_images


def main():
    args = parse_args_k_estimation()

    logging.basicConfig(level=args.level)
    global logger
    logger = logging.getLogger()

    print(f"Running parameter estimation for {args.filename}")

    if args.settings_filename:
        logger.debug(f"loading settings from {args.settings_filename}")
        settings = load_settings(args.settings_filename)
    else:
        logger.warning(f"no settings provided fall back on default settings")
        settings = load_settings(args.filename)

    logger.debug(f"loading images from {args.filename}")
    images, _ = load_tif(args.filename)

    if len(images) < len(settings.directions) * settings.directions[0].number_phases:
        logger.error(
            f"given image stack has to few images n={len(images)} but at least {len(settings.directions) * settings.directions[0].number_phases} are expected"
        )
        return

    logger.debug(f"order images")
    ordered_images = order_images(
        images,
        len(settings.directions),
        settings.directions[0].number_phases,
        settings.image_parameters.ordering,
        settings.image_parameters.z_slice,
    )

    logger.debug("fft images")
    raw_images = fft_images(
        ordered_images,
        len(settings.directions),
        settings.directions[0].number_phases,
        settings.image_parameters.background,
    )

    logger.info(f"run k-vector estimation")
    start = time.time()
    estimate_parameters(settings, raw_images, False)
    stop = time.time()
    logger.info(f"parameter estimation done in {stop-start:.2f} s.")

    if args.out_filename:
        save_settings(settings, args.out_filename, overwrite=True)
    else:
        for direction in settings.directions:
            px, py = direction.px * (
                settings.directions[0].number_bands - 1
            ), direction.py * (settings.directions[0].number_bands - 1)
            if py == 0:  # prevent ZeroDivision error
                py = 1e-14
            print(
                f"kx: {px:.3f}, ky: {py:.3f}, r: {np.hypot(px, py):.3f}, angle: {np.arctan(px/py):.3f}"
            )


if __name__ == "__main__":
    main()
