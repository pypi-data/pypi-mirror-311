# Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pandas as pd
from sourcefinder import image
from sourcefinder.accessors import open as pyse_open
from sourcefinder.accessors import sourcefinder_image_from_accessor

from trap.log import log_time, logger

# Use SEP for faster but less accurate rmse maps
image.SEP = True
# Set VECTORIZED for faster source association but no gaussian fitting
# This only works if force_beam is False when alling pyse_im.extract
image.VECTORIZED = True

PYSE_OUT_COLUMNS = [
    "ra",
    "dec",
    "ra_fit_err",
    "decl_fit_err",
    "peak_flux",
    "peak_flux_err",
    "int_flux",
    "int_fulx_err",
    "significance_detection_level",
    "beam_width",
    "minor_width",
    "parallactic_angle",
    "ew_sys_err",
    "ns_sys_err",
    "err_radius",
    "gaussian_fit",
    "chisq",
    "reduced_chisq",
]


@log_time()
def read_pyse_image(
    path,
    margin=None,
    radius=1500,
    back_size_x=50,
    back_size_y=50,
):
    """
    Read an image with PySE that can be used in functions like :func:`sources_from_fits_pyse` and :func:`force_fit`

    Parameters
    ----------
        fits_path: str
            The path to the .fits file containing the image of which the sources are to be extracted.
        margin: int
            The margin in pixels from the edge of the image within which sources are ignored.
            This exclusion area combines with radius.
        radius: int,
            The radius in pixels around the center of the image, outside of which sources are ignored.
            This exclusion area combines with margin.
        back_size_x: int
            Widht of the background boxes as use in SEP.
            See https://sep.readthedocs.io/en/v1.1.x/api/sep.Background.html#sep.Background
        back_size_y: int
            Height of the background boxes as use in SEP.
            See https://sep.readthedocs.io/en/v1.1.x/api/sep.Background.html#sep.Background

    Returns: sourcefinder.image.ImageData
        A PySE image that can be used for source extraction
    """
    im = pyse_open(path)
    pyse_im = sourcefinder_image_from_accessor(
        im,
        margin=margin,
        radius=radius,
        back_size_x=back_size_x,
        back_size_y=back_size_y,
    )
    return pyse_im


@log_time()
def sources_from_fits_pyse(
    pyse_im,
    ew_sys_err=10,
    ns_sys_err=10,
    detection_threshold=8,
    analysis_threshold=3,
    deblend_nthresh=0,
    force_beam=False,
):
    """Extract sources from an image using PySE.

    Parameters
    ----------
    pyse_im: sourcefinder.image.ImageData
        The pyse image as read using :func:`read_pyse_image`
    ew_sys_err: float
        Systematic errors in units of arcseconds which augment the sourcefinder-measured errors on source positions when performing source association. These variables refer to an absolute angular error along an east-west and north-south axis respectively. (NB Although these values are stored during the source-extraction process, they affect the source-association process.)
    ns_sys_err: float
        Same as ew_sys_err but in perpendicular direction
    detection_threshold: float
        The detection threshold, as a multiple of the RMS
        noise. At least one pixel in a source must exceed this value
        for it to be regarded as significant.
    analysis_threshold: float
        Analysis threshold, as a multiple of the RMS
        noise. All the pixels within the island that exceed
        this will be used when fitting the source.
    deblend_nthresh: int
        Number of subthresholds to use for
        deblending. Set to 0 to disable.
    force_beam: bool
        Force all extractions to have major/minor axes
        equal to the restoring beam.
        If force_beam is False, vecortize=True is ignored.

    Returns
    -------
    `pandas.DataFrame`
        A dataframe where each row is an obtained source.
        The columns contain the attributes of the corces.

        Column names with explenation:

            ra [deg]: float
                Right ascension coordinate of the source
            dec [deg]: float
                Declination coordinate of the source
            ra_fit_err [deg]: float
                1-sigma error from the gaussian fit in right ascension.
                Note that for a source located towards the poles the ra_fit_err
                increases with absolute declination.
            decl_fit_err [deg]: float
                1-sigma error from the gaussian fit in declination
            peak_flux [Jy]: float
            peak_flux_err [Jy]: float
            int_flux [Jy]: float
            int_fulx_err [Jy]: float
            significance_detection_level: float
            beam_width [arcsec]: float
            minor_width [arcsec]: float
            parallactic_angle [deg]: float
            ew_sys_err [arcsec]: float
                Telescope dependent systematic error in east-west direction.
            ns_sys_err [arcsec]: float
                Telescope dependent systematic error in north-south direction.
            err_radius [arcsec]: float
                A pessimistic on-sky position error estimate in arcsec.
            gaussian_fit: bool
            chisq: float
            reduced_chisq: float
    """
    # Note: for explanation of variables see tkp/db/general.py::insert_extracted_sources:
    #       https://github.com/transientskp/tkp/blob/b34582712b82b888a5a7b51b3ee371e682b8c349/tkp/db/general.py#L106
    extraction_results = pyse_im.extract(
        det=detection_threshold,
        anl=analysis_threshold,
        deblend_nthresh=deblend_nthresh,
        force_beam=force_beam,
    )
    extraction_results = [
        r.serialize(ew_sys_err, ns_sys_err) for r in extraction_results
    ]

    sources = pd.DataFrame(extraction_results, columns=PYSE_OUT_COLUMNS)
    # uncertainty_ew: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    sources["uncertainty_ew"] = (
        np.sqrt(sources["ew_sys_err"] ** 2 + sources["err_radius"] ** 2) / 3600.0
    )
    # uncertainty_ns: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    sources["uncertainty_ns"] = (
        np.sqrt(sources["ns_sys_err"] ** 2 + sources["err_radius"] ** 2) / 3600.0
    )

    logger.info(f"Found {len(sources)} sources")

    sources.index.name = "id"
    return sources


def force_fit(pyse_im, positions, ew_sys_err=10, ns_sys_err=10):
    """
    Fit the specified locations using PySE.

    Parameters
    ----------
    pyse_im: sourcefinder.image.ImageData
        The pyse image as read using :func:`read_pyse_image`
    positions: np.ndarray
        A numpy array with the positions of the sources to be force fitted in the form [[ra_1, dec_1], [ra_2, dec_2]]
    ew_sys_err [arcsec]: float
        Telescope dependent systematic error in east-west direction.
    ns_sys_err [arcsec]: float
        Telescope dependent systematic error in north-south direction.
    Returns
    -------
    pd.DataFrame
        A dataframe with the force-fitted sources
    """
    box_in_beampix = 10
    boxsize = box_in_beampix * max(pyse_im.beam[0], pyse_im.beam[1])
    ids = np.arange(len(positions))
    # Some fits could have been dropped by PySE. Also return the fit_ids so the caller can know what ids were dropped
    forced_fits, fit_ids = pyse_im.fit_fixed_positions(
        positions, boxsize, ids=range(len(positions))
    )

    force_fit_results = [r.serialize(ew_sys_err, ns_sys_err) for r in forced_fits]
    forced_sources = pd.DataFrame(force_fit_results, columns=PYSE_OUT_COLUMNS)

    # uncertainty_ew: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    forced_sources["uncertainty_ew"] = (
        np.sqrt(forced_sources["ew_sys_err"] ** 2 + forced_sources["err_radius"] ** 2)
        / 3600.0
    )
    # uncertainty_ns: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    forced_sources["uncertainty_ns"] = (
        np.sqrt(forced_sources["ns_sys_err"] ** 2 + forced_sources["err_radius"] ** 2)
        / 3600.0
    )

    logger.info(f"Forced fit for {len(forced_sources)} sources")

    return forced_sources, fit_ids
