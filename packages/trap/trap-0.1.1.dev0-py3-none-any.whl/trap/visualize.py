"""The scene children look as follows:

    0: background image
    1: points
    2: legend backround
    3: legend label 1
    4: legend label 2
    5: legend label 3
    6: legend navigate images
    7: legend toggle legend
    8: legend exit app
"""

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS

try:
    import matplotlib.pylab as pl
    import pygfx as gfx
    from wgpu.gui.auto import WgpuCanvas, run
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Unable to import all required visualization dependencies. Please install TraP with the optional visualization dependencies: `pip install trap[view]`"
    )

from trap.log import logger

image_counter = 0  # Used to keep track of the image we are showing
show_legend = True  # Used to keep track on whether the legend should be shown


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


def add_legend(scene, show_legend=True):
    """Add a basic overlay to show the meaning of the visualized elements,
    as well as some key bindings for operating the app.

    Parameters
    ----------
    scene: :class:`gfx.Scene`
        The scene on which to render the legend
    show_legend:
        Whether or not to make the legend invisible.
        If True: legend is visible, if False: legend is made transparent.

    Returns
    -------
    None
    """
    # Define legend point colors and positions
    bbox = scene.children[
        0
    ].geometry.get_bounding_box()  # returns [[minx, miny, minz], [maxx, maxy, maxz]]
    right = bbox[1, 0]
    center = [(bbox[1, 0] - bbox[0, 0]) / 2, (bbox[1, 1] - bbox[0, 1]) / 2]
    legend_colors = {
        "Persistent": [1, 0, 0, 1],
        "New": [1, 0, 1, 1],
        "Null-detection": [0, 0, 0, 1],
    }

    # Create a grey, semi-transparent rectangle as a background for the legend
    rect_width = 1500  # Adjust based on legend content width
    rect_height = 1300  # Adjust based on legend content height
    rect_position = (*center, 9)  # Position behind legend item
    bg_geometry = gfx.plane_geometry(rect_width, rect_height)
    bg_material = gfx.MeshBasicMaterial(
        color=(0.7, 0.7, 0.7, 0.9 if show_legend else 0)
    )
    bg_rect = gfx.Mesh(bg_geometry, bg_material)
    bg_rect.local.position = rect_position
    scene.add(bg_rect)

    # Add text labels
    for i, (label, color) in enumerate(legend_colors.items()):
        text = gfx.Text(
            gfx.TextGeometry(
                label, font_size=130, anchor="middle-center", anchor_offset=0
            ),
            gfx.TextMaterial(
                color=color[:3],
                outline_color="grey",
            ),
        )

        text.local.position = np.array(
            [center[0], center[1] - 240 + i * 120, 11], dtype="float32"
        )
        text.local.scale_y = -1
        text.render_order = 1001  # Render text labels on top of points
        scene.add(text)

    # Add control key explenation
    control_lines = [
        "Cycle images with arrow keys",
        "Toggle legend with 'L'",
        "Hide/show sources with 'space-bar'",
        "Exit with 'q' or 'Esc'",
    ]
    for i, line in enumerate(control_lines):
        text = gfx.Text(
            gfx.TextGeometry(
                line, font_size=80, anchor="middle-center", anchor_offset=0
            ),
            gfx.TextMaterial(
                color="black",
                outline_color="grey",
            ),
        )
        text.local.position = np.array(
            [center[0], center[1] + 250 + i * 95, 11], dtype="float32"
        )
        text.local.scale_y = -1
        text.render_order = 1001  # Render text labels on top of points
        scene.add(text)


def set_legend_transparency(scene, alpha=0.9):
    """Set the transparency of the legend by updating it in-place.

    Parameters
    ----------
    scene
        The pygfx scene object
    alhpa: float
        The transparency value between 0 (fully transparent) and 1 (fully opaque)
    """
    # Loop over legend components and set transparency to visible.
    scene.children[2].material.color = (*scene.children[2].material.color[:3], alpha)
    for component in scene.children[3:10]:
        component.material.color = (*component.material.color[:3], alpha)


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
    canvas = WgpuCanvas()
    renderer = gfx.renderers.WgpuRenderer(canvas)
    scene = gfx.Scene()

    bg_im, header = fits_to_gfx(image_db.loc[0, "url"])
    wmap = WCS(header, naxis=2)
    im_shape = bg_im.geometry.grid.data.shape[:2]  # exclude rgb axis

    scene.add(bg_im)

    def update_image(path):
        """Inner function that sets the background image based on a supplied filepath."""
        logger.info(f"Showing image: {path}")
        new_im = read_fits(path)
        new_im = im_2_rgba(new_im, vmax_percentile=99.7)[:, :, :3]
        np.copyto(bg_im.geometry.grid.data, new_im)
        bg_im.geometry.grid.update_range((0, 0, 0), bg_im.geometry.grid.size)

    def update_sources(scene, image_counter):
        """Inner function that visualizes the sources corresponding to a certain image id."""
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

        if len(scene.children) < 2:
            alpha = 1
            edge_color = (0, 0, 0, 1)
        else:
            alpha = scene.children[1].geometry.colors.data[0, -1]
            edge_color = scene.children[1].material.edge_color

        colors = np.full((len(positions), 4), [1, 0, 0, alpha], dtype="float32")

        # Color null detections
        # Assme the array is structured such that we have first the persistent sources, then new detections and then null detections
        if len(new_sources) != 0:  # skip slice if there are no new sources
            # Check for case where there are no null detections. Slicing with -0 will refer to the start and not the end of the array.
            end_slice = -len(null_detections) if len(null_detections) != 0 else None
            colors[-len(null_detections) - len(new_sources) : end_slice] = [
                1,
                0,
                1,
                alpha,
            ]
        # Color new sources
        if len(null_detections) != 0:  # skip slice if there are no null detections
            colors[-len(null_detections) :] = [0, 0, 0, alpha]

        geometry = gfx.Geometry(
            positions=positions,
            colors=colors,
            sizes=25 * np.ones(len(positions), dtype="float32"),
        )
        if len(scene.children) < 2:  # Add points geometry (first time only)
            points = gfx.Points(
                geometry,
                gfx.PointsMarkerMaterial(
                    size=30,
                    color_mode="vertex",
                    marker="ring",
                    edge_color=edge_color,
                    edge_width=1,
                ),
            )
            scene.add(points)
        else:  # Update points geometry
            scene.children[1].geometry = geometry
            scene.children[1].geometry.positions.update_range(
                0, geometry.positions.nitems
            )

    @renderer.add_event_handler("key_down")
    def handle_key_press(event):
        global image_counter
        global show_legend
        if event.key == "ArrowRight":
            image_counter += 1
            if image_counter >= len(image_db):
                image_counter -= 1
                logger.info(f"Already showing last image: {image_counter}")
                return
            update_image(image_db.loc[image_counter, "url"])
            update_sources(scene, image_counter)
        if event.key == "ArrowLeft":
            if image_counter == 0:
                logger.info(f"Already showing first image")
                return
            image_counter -= 1
            update_image(image_db.loc[image_counter, "url"])
            update_sources(scene, image_counter)
        if event.key == " ":
            # breakpoint()
            edge_color = list(scene.children[1].material.edge_color)
            edge_color[-1] = 1 - edge_color[-1]
            scene.children[1].material.edge_color = tuple(edge_color)
            scene.children[1].geometry.colors.data[:, -1] = (
                1 - scene.children[1].geometry.colors.data[:, -1]
            )
            scene.children[1].geometry.colors.update_range(
                0, scene.children[1].geometry.colors.nitems
            )
        if event.key == "l" or event.key == "L":
            if show_legend:
                set_legend_transparency(scene, 0)
                show_legend = False
            else:
                set_legend_transparency(scene, 0.9)
                show_legend = True
        if event.key == "q" or event.key == "Q" or event.key == "Escape":
            canvas.close()

    # Initialize sources
    update_sources(scene, image_counter)

    # Add legend to the scene
    # NOTE: Always initialize the legend, also when show_legend is false.
    #       Whether or not the legend is shown is a transparency matter, not one of creation and deletion
    add_legend(scene, show_legend=show_legend)

    # Create the pygfx attributes required to render the scene
    camera = gfx.PerspectiveCamera(0)
    camera.local.scale_y = -1
    camera.show_rect(-10, im_shape[1] + 10, -10, im_shape[0] + 10)

    controller = gfx.PanZoomController(camera, register_events=renderer)

    def animate():
        renderer.render(scene, camera, flush=True)
        canvas.request_draw()

    # Run the visualization
    canvas.request_draw(animate)
    run()
