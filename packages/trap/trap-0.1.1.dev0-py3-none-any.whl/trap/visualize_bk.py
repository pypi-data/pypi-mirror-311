import astropy
import matplotlib.pylab as pl
import numpy as np
import pandas as pd
import pygfx as gfx
from astropy.io import fits
from astropy.wcs import WCS
from wgpu.gui.auto import WgpuCanvas, run

from .log import logger

image_counter = 0

points = None
dead_points = None
new_points = None


def sample_colormap(values, cmap="viridis", vmin_percentile=2, vmax_percentile=98):
    """Turn data values into rgba colors based on a colormap of choice.
    The colormap range is determined dynamically based on `values` but
    can be influenced using `vmin_percentile` and `vmax_percentile`.

    Parameters
    ----------
    values: :class:`np.ndarray`
        The data that is to be converted to rgba colors
    cmap: `str`
        The name of the matplotlib colormap from which to sample the colors.
        A full comprehensive overview of available colormaps is given here:
        https://matplotlib.org/stable/users/explain/colors/colormaps.html
    vmin_percentile: float
        The bottom percentile of the data to use as bottom of the colormap.
        Any value that is below this percentile will be given the color corresponding
        to the lower bound of the colormap.
    vmax_percentile: float
        The upper percentile of the data to use as top of the colormap.
        Any value that is larger than this percentile will be given the color corresponding
        to the upper bound of the colormap.

    Returns
    -------
    :class:`np.ndarray`
        The rgba values corresponding to the supplied values
    """
    cmap = getattr(pl.cm, cmap)
    vmin = np.nanpercentile(values, vmin_percentile)
    values_normalized = values - vmin
    values_normalized = values_normalized / np.nanpercentile(values, vmax_percentile)
    colors = cmap(values_normalized).squeeze()
    return colors


def im_2_rgba(im, cmap="viridis", vmin_percentile=2, vmax_percentile=98):
    """Obtain rgba color values from the data in a fits image.

    The colormap range is determined dynamically based on `values` but
    can be influenced using `vmin_percentile` and `vmax_percentile`.

    Parameters
    ----------
    im: :class:`astropy.io.fits.hdu.image.PrimaryHDU`
        The fits image that is to be converted to rgba colors
    cmap: `str`
        The name of the matplotlib colormap from which to sample the colors.
        A full comprehensive overview of available colormaps is given here:
        https://matplotlib.org/stable/users/explain/colors/colormaps.html
    vmin_percentile: float
        The bottom percentile of the data to use as bottom of the colormap.
        Any value that is below this percentile will be given the color corresponding
        to the lower bound of the colormap.
    vmax_percentile: float
        The upper percentile of the data to use as top of the colormap.
        Any value that is larger than this percentile will be given the color corresponding
        to the upper bound of the colormap.

    Returns
    -------
    :class:`np.ndarray`
        The rgba values corresponding to the values in the fits image
    """
    data = im.data[0, 0].astype("float32")
    colors = (
        sample_colormap(data.ravel(), cmap, vmin_percentile, vmax_percentile)
        .reshape((*data.shape, -1))
        .astype("float32")
    )
    return colors


def read_fits(path):
    """Use astropy to read a fits image.

    Parameters
    ----------
    path: str
        The path to the .fits file.

    Returns
    -------
    :class:`astropy.io.fits.hdu.image.PrimaryHDU`
        The astropy image object
    """
    im = fits.open(path)[0]
    return im


def fits_to_gfx(path):
    """Read a .fits file and convert it to a py-gfx image object.
    The image header as metadata alongside the image.

    Parameters
    ----------
    path: str
        The path to the .fits file.

    Returns
    -------
    :class:`gfx.Image`
        The py-gfx image object.
    :class:`astropy.io.fits.header.Header`
        The astropy header associated with the image.
    """
    im = read_fits(path)
    im_rgb = im_2_rgba(im, vmax_percentile=99.7)[:, :, :3]
    im_gfx = gfx.Image(
        gfx.Geometry(grid=gfx.Texture(im_rgb, dim=2)),
        gfx.ImageBasicMaterial(
            clim=(0, 1), interpolation="nearest", map_interpolation="nearest"
        ),
    )
    return im_gfx, im.header


def visualize(sources, image_db, lightcurves):
    """Start up a new window with an interactive visualization.

    Parameters
    ----------
    sources: :class:`pd.DataFrame`
        Table of know sources, with columns:

            - "id" (index of source)
            - "ra" (right-ascension coordinate of source)
            - "dec" (declination coordinate of source))
            - "ra_fit_err" (fit error in direction of right-ascension)
            - "decl_fit_err" (fit error in direction of declination)
            - "based_on" (id of the previous source, used to construct lightcurve)
            - "peak_flux" (the flux value at the peak of the gaussian fit over the source)
            - "uncertainty_ns" (sqare root of quadratic sum of systematic error and error_radius)
            - "uncertainty_ew" (sqare root of quadratic sum of systematic error and error_radius)

    image_db: :class:`pd.DataFrame`
        Table of images, with columns:

            - "id" (index of the image)
            - "url" (location of the image file)
            - "found_sources" (index of sources found in the image, matching the sources DataFrame)
            - "null_detections" (index of null_detections found in the image, matching the sources DataFrame)
            - "new_sources" (index of new sources found in the image, matching the sources DataFrame)
            - "acquisition_date" (date and time of image acquisition)
        }

    lightcurves: :class:`pd.DataFrame`
        Table of flux values per image per source, with columns:

            - "id" (index of the sources, matching the sources DataFrame)
            - "im_0" (The flux values corresponding to image 0)
            - "im_1" (The flux values corresponding to image 1)
            - ... (The flux values corresponding to all subsequent imges)

        }

    Returns
    -------
    None
    """
    global points
    global dead_points
    global new_points

    canvas = WgpuCanvas()
    renderer = gfx.renderers.WgpuRenderer(canvas)
    scene = gfx.Scene()

    bg_im, header = fits_to_gfx(image_db.loc[0, "url"])
    wmap = WCS(header, naxis=2)
    im_shape = bg_im.geometry.grid.data.shape[:2]  # exclude rgb axis

    scene.add(bg_im)

    def update_image(path):
        logger.info(f"Showing image: {path}")
        new_im = read_fits(path)
        new_im = im_2_rgba(new_im, vmax_percentile=99.7)[:, :, :3]
        np.copyto(bg_im.geometry.grid.data, new_im)
        bg_im.geometry.grid.update_range((0, 0, 0), bg_im.geometry.grid.size)

    def update_sources():
        global image_counter

        # Leave child 0 untouched for that is the background image
        try:
            scene.remove(scene.children[1])
        except:
            # Expect points to not be present on first initialization
            pass

        found_sources = image_db.loc[image_counter, "found_sources"]
        new_sources = image_db.loc[image_counter, "new_sources"]
        null_detections = image_db.loc[image_counter, "null_detections"]
        persistent_sources = set(found_sources) - set(new_sources)

        positions = np.ones(
            (len(found_sources) + len(null_detections), 3), dtype="float32"
        )
        source_ids = (*found_sources, *null_detections)
        x_pixels, y_pixels = wmap.world_to_pixel_values(
            *sources.loc[source_ids, ["ra", "dec"]].to_numpy().T
        )
        positions[:, 0] = x_pixels
        positions[:, 1] = y_pixels

        colors = np.full((len(positions), 4), [1, 0, 0, 1], dtype="float32")

        # Color null detections
        # Assme the array is structured such that we have first the persistent sources, then new detections and then null detections
        if len(new_sources) != 0:  # skip slice if there are no new sources
            # Check for case where there are no null detections. Slicing with -0 will refer to the start and not the end of the array.
            end_slice = -len(null_detections) if len(null_detections) != 0 else None
            colors[-len(null_detections) - len(new_sources) : end_slice] = [1, 0, 1, 1]
        # Color new sources
        if len(null_detections) != 0:  # skip slice if there are no null detections
            colors[-len(null_detections) :] = [0, 0, 0, 1]
        points = gfx.Points(
            gfx.Geometry(
                positions=positions,
                colors=colors,
                sizes=25 * np.ones(len(positions), dtype="float32"),
            ),
            gfx.PointsMarkerMaterial(
                size=30,
                color_mode="vertex",
                marker="ring",
                edge_color="#000",
                edge_width=1,
            ),
        )
        scene.add(points)

    @renderer.add_event_handler("key_down")
    def handle_event(event):
        global image_counter
        if event.key == "ArrowRight":
            image_counter += 1
            if image_counter >= len(image_db):
                image_counter -= 1
                print(f"Already showing last image: {image_counter}")
                return
            update_image(image_db.loc[image_counter, "url"])
            update_sources()
        if event.key == "ArrowLeft":
            if image_counter == 0:
                print(f"Already showing first image")
                return
            image_counter -= 1
            update_image(image_db.loc[image_counter, "url"])
            update_sources()

    # Initialize sources
    update_sources()

    camera = gfx.PerspectiveCamera(0)
    camera.local.scale_y = -1
    camera.show_rect(-10, im_shape[1] + 10, -10, im_shape[0] + 10)

    controller = gfx.PanZoomController(camera, register_events=renderer)

    def animate():
        renderer.render(scene, camera, flush=True)
        canvas.request_draw()

    # Visualize
    canvas.request_draw(animate)
    run()
