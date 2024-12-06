import sys

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS

try:
    import matplotlib.pyplot as plt

    MPL_AVAILABLE = True
except ModuleNotFoundError:
    MPL_AVAILABLE = False

from trap.associate import associate
from trap.source_extraction import force_fit, read_pyse_image, sources_from_fits_pyse


def main():
    image_paths = [
        "tests/data/lofar1/GRB201006A_final_2min_srcs-t0000-image-pb.fits",
        "tests/data/lofar1/GRB201006A_final_2min_srcs-t0001-image-pb.fits",
        "tests/data/lofar1/GRB201006A_final_2min_srcs-t0002-image-pb.fits",
    ]

    # import os
    # base_path = "/home/millenaar/software/astron/tkp/projects/trap_demo/Images/GRB201006A/"
    # image_paths = [base_path + f for f in os.listdir(base_path) if f.endswith(".fits")]
    # image_paths.sort()
    # image_paths = image_paths

    dynamic_visualization = 0
    plot_all_sources = 1

    sources = pd.DataFrame(
        {
            "id": [],
            "ra": [],
            "dec": [],
            "ra_fit_err": [],
            "dec_fit_err": [],
            "based_on": [],
            "peak_flux": [],
            "uncertainty_ns": [],
            "uncertainty_ew": [],
        }
    ).set_index("id")

    lightcurves = pd.DataFrame(
        {
            "id": [],
        }
    ).set_index("id")

    image_db = pd.DataFrame(
        {
            "id": [],
            "url": [],
            "found_sources": [],
            "null_detections": [],
            "new_sources": [],
            "acquisition_date": [],
        }
    ).set_index("id")

    for im_id, path in enumerate(image_paths):
        pyse_im = read_pyse_image(path)
        new_sources = sources_from_fits_pyse(pyse_im)

        if sources.empty:
            sources = new_sources
            new_source_ids = sources.index
            null_detection_ids = np.array([])
            persistings_mapping = pd.DataFrame(
                [], columns=["original_id", "new_id", "de_ruiter"]
            )
            found_source_ids = sources.index
            duplicate_mapping = pd.DataFrame(
                {"new_id": [], "original_id": [], "de_ruiter": []}
            )
        else:
            null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = (
                associate(sources, new_sources)
            )
            sources.update(
                new_sources.loc[persistings_mapping["new_id"]].set_index(
                    persistings_mapping["original_id"]
                )
            )
            new_source_ids = [*duplicate_mapping.new_id, *new_ids]
            based_on = np.full(len(new_source_ids), np.nan)
            based_on[: len(duplicate_mapping)] = duplicate_mapping.original_id
            new_ids = new_sources.loc[new_source_ids]
            new_source_ids = sources.index.max() + np.arange(len(new_ids)) + 1
            new_ids = new_ids.set_index(new_source_ids)
            found_source_ids = [*persistings_mapping["original_id"], *new_source_ids]
            sources = pd.concat([sources, new_ids])

        # Update image_db
        with fits.open(path) as im:
            header = im[0].header
            date_time = header.get("DATE-OBS", None)
            date_time = np.datetime64(date_time)
        image_db = pd.concat(
            [
                image_db,
                pd.DataFrame(
                    {
                        "id": [im_id],
                        "url": [path],
                        "found_sources": [tuple(found_source_ids)],
                        "null_detections": [tuple(null_detection_ids)],
                        "new_sources": [new_source_ids],
                        "acquisition_date": [date_time],
                    }
                ).set_index("id"),
            ]
        )

        # Force fit null-detections
        if null_detection_ids.size > 0:
            null_detection_coords = sources.loc[
                null_detection_ids, ["ra", "dec"]
            ].to_numpy()
            null_detection_fluxes, fit_ids = force_fit(
                pyse_im, positions=null_detection_coords
            )
            null_detection_ids = null_detection_ids[fit_ids]
            sources.loc[null_detection_ids, "peak_flux"] = (
                null_detection_fluxes.peak_flux.values
            )

        # Add nans for previous images for every new source. Do this first or the new rows won't be added and only
        # existing rows will be updated.
        lightcurves = pd.concat(
            [lightcurves, pd.DataFrame({"id": new_source_ids}).set_index("id")]
        )
        # For duplicates copy the flux values based on original source
        for (_, duplicate), new_id in zip(
            duplicate_mapping.iterrows(), new_source_ids[: len(duplicate_mapping)]
        ):
            lightcurves.loc[new_id] = lightcurves.loc[duplicate.original_id]
        lightcurves[f"im_{im_id}"] = sources["peak_flux"]

    if dynamic_visualization:
        from trap.visualize import visualize

        visualize(sources, image_db, lightcurves)

    if plot_all_sources:
        if not MPL_AVAILABLE:
            raise ModuleNotFoundError(
                "Unable to import all required visualization dependencies. Please install TraP with the optional visualization dependencies: `pip install trap[view]`"
            )

        im = fits.open(image_paths[-1])[0]
        wmap = WCS(im.header, naxis=2)
        ax = plt.subplot(projection=wmap)
        data = im.data[0, 0]
        ax.imshow(data, vmin=np.percentile(data, 2), vmax=np.percentile(data, 98))
        ax.scatter(
            sources.ra,
            sources.dec,
            marker="o",
            facecolors="none",
            edgecolors="r",
            transform=ax.get_transform("fk5"),
        )
        plt.show()


if __name__ == "__main__":
    sys.exit(main())
