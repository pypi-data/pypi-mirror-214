import io
import os
import imghdr
import base64
import streamlit.components.v1 as components
import streamlit.elements.image as image_utils
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Union, cast
import numpy as np
from PIL import GifImagePlugin, Image, ImageFile
from typing_extensions import Final, Literal, TypeAlias

from streamlit import runtime
from streamlit.errors import StreamlitAPIException
from streamlit.logger import get_logger
from streamlit.proto.Image_pb2 import ImageList as ImageListProto
from streamlit.runtime import caching
from streamlit.runtime.metrics_util import gather_metrics


MAXIMUM_CONTENT_WIDTH: Final[int] = 2 * 730

ImageFormat: TypeAlias = Literal["JPEG", "PNG", "GIF"]
PILImage: TypeAlias = Union[
    ImageFile.ImageFile, Image.Image, GifImagePlugin.GifImageFile
]
AtomicImage: TypeAlias = Union[PILImage, io.BytesIO, str]

def _ensure_image_size_and_format(
    image_data: bytes, width: int, image_format: ImageFormat
) -> bytes:
    """Resize an image if it exceeds the given width, or if exceeds
    MAXIMUM_CONTENT_WIDTH. Ensure the image's format corresponds to the given
    ImageFormat. Return the (possibly resized and reformatted) image bytes.
    """
    image = Image.open(io.BytesIO(image_data))
    actual_width, actual_height = image.size

    if width < 0 and actual_width > MAXIMUM_CONTENT_WIDTH:
        width = MAXIMUM_CONTENT_WIDTH

    if width > 0 and actual_width > width:
        # We need to resize the image.
        new_height = int(1.0 * actual_height * width / actual_width)
        image = image.resize((width, new_height), resample=Image.BILINEAR)
        return _PIL_to_bytes(image, format=image_format, quality=90)

    ext = imghdr.what(None, image_data)
    if ext != image_format.lower():
        # We need to reformat the image.
        return _PIL_to_bytes(image, format=image_format, quality=90)

    # No resizing or reformatting necessary - return the original bytes.
    return image_data

def _PIL_to_bytes(
    image: PILImage,
    format: ImageFormat = "JPEG",
    quality: int = 100,
) -> bytes:
    """Convert a PIL image to bytes."""
    tmp = io.BytesIO()

    # User must have specified JPEG, so we must convert it
    if format == "JPEG" and _image_may_have_alpha_channel(image):
        image = image.convert("RGB")

    image.save(tmp, format=format, quality=quality)

    return tmp.getvalue()


_RELEASE = True

def image_to_url(
    image: AtomicImage,
    width: int,
    image_id,
    output_format = "auto",
) -> str:
    """Return a URL that an image can be served from.
    If `image` is already a URL, return it unmodified.
    Otherwise, add the image to the MediaFileManager and return the URL.

    (When running in "raw" mode, we won't actually load data into the
    MediaFileManager, and we'll return an empty URL.)
    """


    image_data: bytes
    if isinstance(image, io.BytesIO):
        image_data = _BytesIO_to_bytes(image)
    else:
        image_data = image

    # Determine the image's format, resize it, and get its mimetype
    image_format = _validate_image_format_string(image_data, output_format)
    image_data = _ensure_image_size_and_format(image_data, width, image_format)
    mimetype = _get_image_format_mimetype(image_format)

    if runtime.exists():
        url = runtime.get_instance().media_file_mgr.add(image_data, mimetype, image_id)
        caching.save_media_data(image_data, mimetype, image_id)
        return url
    else:
        # When running in "raw mode", we can't access the MediaFileManager.
        return ""

def _validate_image_format_string(
    image_data: Union[bytes, PILImage], format: str
) -> ImageFormat:
    """Return either "JPEG", "PNG", or "GIF", based on the input `format` string.

    - If `format` is "JPEG" or "JPG" (or any capitalization thereof), return "JPEG"
    - If `format` is "PNG" (or any capitalization thereof), return "PNG"
    - For all other strings, return "PNG" if the image has an alpha channel,
    "GIF" if the image is a GIF, and "JPEG" otherwise.
    """
    format = format.upper()
    if format == "JPEG" or format == "PNG":
        return cast(ImageFormat, format)

    # We are forgiving on the spelling of JPEG
    if format == "JPG":
        return "JPEG"

    if isinstance(image_data, bytes):
        pil_image = Image.open(io.BytesIO(image_data))
    else:
        pil_image = image_data

    if _image_may_have_alpha_channel(pil_image):
        return "PNG"

    return "JPEG"

def _get_image_format_mimetype(image_format: ImageFormat) -> str:
    """Get the mimetype string for the given ImageFormat."""
    return f"image/{image_format.lower()}"

def _image_may_have_alpha_channel(image: PILImage) -> bool:
    if image.mode in ("RGBA", "LA", "P"):
        return True
    else:
        return False
    
def _BytesIO_to_bytes(data: io.BytesIO) -> bytes:
    data.seek(0)
    return data.getvalue()


if not _RELEASE:
    _component_func = components.declare_component(
        "st_line_plotter",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_line_plotter", path=build_dir)


def st_line_plotter(fig, changed, width = None, height = None, lines=[],  key=None):
    size = fig.get_size_inches()*fig.dpi

    buffer = BytesIO()
    options = {"bbox_inches": "tight", "dpi": 200, "format": "png"}
    fig.savefig(buffer, **options)

    image_width = (
        image_utils.WidthBehaviour.ORIGINAL
    )

    url = image_to_url(buffer,image_width, "1","PNG")


    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_url = f"data:image/png;base64,{base64_image}"

    width = width if width != None else size[0]
    height = height if height != None else size[1]

    print(width, height)

    component_value = _component_func(lines=lines, image=data_url, changed=changed, width=width, height=height, key=key, default=0)
    return component_value


# Test code
if not _RELEASE:
    import streamlit as st
    st.set_page_config(layout="wide")

    fig = plt.figure()
    #print("Fig1",fig)

    plt.plot(range(10)) 
    #size = fig.get_size_inches()*fig.dpi

    #buffer = BytesIO()
    #fig.savefig(buffer, format='PNG')
    #base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    #data_url = f"data:image/png;base64,{base64_image}"

    #scale = 2

    #v_camera = "/static/media/v_camera.ed53386f.png"
    #v_ground = "/static/media/v_ground.e2660b07.png"
    if "lines" not in st.session_state:
        st.session_state.lines = []
    #if "changed" not in st.session_state:
    #    st.session_state.changed = 0
    #if st.button("Edit 1"):
    #    st.session_state.changed = 1
    #if st.button("Edit 2"):
    #    st.session_state.changed = 2

    #print(st.session_state.changed)
    lines1 = st_line_plotter(lines=st.session_state["lines"], changed=1, fig=fig, key=1)
    if lines1 != 0:
        st.session_state["lines"] = lines1
    st.pyplot(fig=fig)
