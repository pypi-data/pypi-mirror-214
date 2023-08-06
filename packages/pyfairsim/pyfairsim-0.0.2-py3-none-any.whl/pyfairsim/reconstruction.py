import logging
import time

from pyfairsim.sim_algorithm.SIM_Utils import run_reconstruction, plot_img

from pyfairsim.utils.argparse import parse_args_reconstruction
from pyfairsim.utils.load_settings import load_settings, save_settings
from pyfairsim.utils.tif import load_tif, order_images, fft_images, save_tif, tif_basename


def main():
    args = parse_args_reconstruction()

    logging.basicConfig(level=args.level)
    global logger
    logger = logging.getLogger()

    print(f"Running reconstruction for {args.filename}")

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

    logger.info(f"run reconstruction")
    start = time.time()
    result = run_reconstruction(settings, raw_images)
    stop = time.time()
    logger.info(f"reconstruction done in {stop-start:.2f} s.")

    if args.out_filename:
        save_tif(result[0], args.out_filename)
        widefield_filename = tif_basename(args.out_filename) + "_filtered_widefield.tif"
        save_tif(result[1], widefield_filename)
    else:
        plot_img(result[0], "reconstructed image")
        plot_img(result[1], "filtered widefield")


if __name__ == "__main__":
    main()
