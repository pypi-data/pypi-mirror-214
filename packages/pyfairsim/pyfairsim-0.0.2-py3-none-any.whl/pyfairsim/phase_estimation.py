import logging
import time

import numpy as np

from pyfairsim.sim_algorithm.SIM_Utils import (
    estimate_absolute_phases,
    estimate_absolute_phases_parallel,
)

from pyfairsim.utils.argparse import parse_args_phase_estimation
from pyfairsim.utils.load_settings import load_settings, save_settings
from pyfairsim.utils.tif import load_tif, order_images, fft_images


def main():
    args = parse_args_phase_estimation()

    logging.basicConfig(level=args.level)
    global logger
    logger = logging.getLogger()

    print(f"Running phase estimation for {args.filename}")

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

    logger.info(f"run phase estimation")
    start = time.time()
    estimate_absolute_phases_parallel(settings, raw_images)
    stop = time.time()
    logger.info(f"phase estimation done in {stop-start:.2f} s.")

    if args.out_filename:
        save_settings(settings, args.out_filename, overwrite=True)
    else:
        print("Relative phases (difference from phase to phase):")
        for direction in settings.directions:
            phase_offset = direction.phases[-1]
            for phase in direction.phases:
                phase_difference = phase - phase_offset
                # print(phase_difference, end=" converts to ")
                while True:
                    if phase_difference < 0:
                        phase_difference += 2 * np.pi
                    elif phase_difference > 2 * np.pi:
                        phase_difference -= 2 * np.pi
                    else:
                        break
                print(phase_difference, end=" ")
                phase_offset = phase
            print()


if __name__ == "__main__":
    main()
