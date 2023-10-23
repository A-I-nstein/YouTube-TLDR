# imports

import streamlit as st
from backend import get_summary, get_answer

# page config

st.set_page_config(
    page_title = 'YouTube Q & A',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
    )

# side bar

with st.sidebar:
    with open('sidebar.txt') as fb:
        text = fb.read()
    st.write(text)

# main page

st.title(":video_camera: YouTube Video Q and A")

# UI Elements

st.subtitle("Sorry! We're working on improving this site! Here's a demo video in the meanwhile (Thanks to Weaviate!)")
st.video("video.mp4")
