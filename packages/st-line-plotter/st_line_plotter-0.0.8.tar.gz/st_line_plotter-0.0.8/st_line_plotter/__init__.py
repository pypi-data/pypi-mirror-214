import io
import os
import base64
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

_RELEASE = True


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
    fig.savefig(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_url = f"data:image/png;base64,{base64_image}"

    width = width if width != None else size[0]
    height = height if height != None else size[1]

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
