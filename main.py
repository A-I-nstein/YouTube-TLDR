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

# program variables and functions

process_video = None
process_question = None
go_to_timestamp = None

@st.cache_data
def call_get_summary(video_link):
    return get_summary(video_link)
@st.cache_data
def call_get_answer(question):
    return get_answer(question)

# session state management

if 'process_video_clicked' not in st.session_state:
    st.session_state.process_video_clicked = False
if 'process_question_clicked' not in st.session_state:
    st.session_state.process_question_clicked = False
if 'go_to_timestamp_clicked' not in st.session_state:
    st.session_state.go_to_timestamp_clicked = False
if 'timestamp' not in st.session_state:
    st.session_state.timestamp = 0

def process_video_callback():
    st.session_state.process_video_clicked = True
    st.session_state.process_question_clicked = False
def process_question_callback():
    st.session_state.process_question_clicked = True
    st.session_state.go_to_timestamp_clicked = False
def go_to_timestamp_callback():
    st.session_state.go_to_timestamp_clicked = True


# video link input container

st.divider()
container_1 = st.container()
with container_1:
    st.text('Paste the link to the YouTube video here: ')
    col_1, col_2 = st.columns([0.8, 0.2])
    with col_1:
        video_link = st.text_input(
            label = 'Video Link',
            label_visibility = 'collapsed',
            placeholder = 'https://www.youtube.com/watch?v=0CmtDk-joT4',
            value = 'https://www.youtube.com/watch?v=0CmtDk-joT4'
            )
    with col_2:
        process_video = st.button('Process Video', on_click=process_video_callback)

# processed output container

if process_video or st.session_state.process_video_clicked:
    st.session_state.process_video_clicked = True
    st.divider()
    container_2 = st.container()
    with container_2:
        col_1, col_2 = st.columns([0.6, 0.4])
        with col_1:
            if 'shorts' in video_link:
                video_link = video_link.replace('shorts', 'embed')
            video = st.video(video_link, start_time = st.session_state.timestamp)
        with col_2:
            with st.spinner('Generating summary...'):
                status, data = call_get_summary(video_link)
            if status != 'success':
                st.error(data)
                exit(0)
            else:
                st.text('Summary of the video:')
                summary_box = st.text_area(
                    label = 'Summary',
                    label_visibility = 'collapsed',
                    value = data,
                    disabled = True,
                    height = 300
                )
        st.divider()
        st.text('Type your question here: ')
        col_1, col_2 = st.columns([0.8, 0.2])
        with col_1:
            question = st.text_input(
                label = 'Question',
                label_visibility = 'collapsed',
                )
        with col_2:
            process_question = st.button('Get Answer', on_click=process_question_callback)

# answer container

if process_question or st.session_state.process_question_clicked:
    container_3 = st.container()
    with container_3:
        with st.spinner('Finding answer...'):
            status, data = call_get_answer(question)
            if status != 'success':
                st.error(data)
                exit(0)
            else:
                answer, st.session_state.timestamp = data[0], data[1]
        st.text('The answer to your question: ')
        col_1, col_2 = st.columns([0.8, 0.2])
        with col_1:
            answer_box = st.text_area(
                label = 'Answer',
                label_visibility = 'collapsed',
                value = answer
                )
        with col_2:
            go_to_timestamp = st.button('Go To Timestamp', on_click=go_to_timestamp_callback)
