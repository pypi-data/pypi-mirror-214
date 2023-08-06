import os
import streamlit as st
import streamlit.components.v1 as components


_RELEASE = False

if not _RELEASE:
    _chat_box = components.declare_component(
        "chat_box_streamlit",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _chat_box = components.declare_component("chat_box_streamlit", path=build_dir)


def message(isLeft=True, message="", loading=False, loadingText="Loading...", placeholder="Enter your input", height=500, key=None):
    return _chat_box(component="message", isLeft=isLeft, message=message, placeholder=placeholder, loading=loading, loadingText=loadingText, height=height, key=key)

def input(placeholder="Enter your input", loading=False, loadingText="Loading...", rows=1, key=None):
    return _chat_box(component="input", placeholder=placeholder, rows=rows, loading=loading, loadingText=loadingText, key=key)

def display_chat(leftMessages = [], rightMessages=[], height=500, rows=1, key=None):
    return _chat_box(component="", leftMessages=leftMessages, rightMessages=rightMessages, rows=rows, height=height, key=key)

def initialise():
    if 'leftMessages' not in st.session_state:
        st.session_state['leftMessages'] = []
    
    if 'rightMessages' not in st.session_state:
        st.session_state['rightMessages'] = []

    if 'input' not in st.session_state:
        st.session_state['input'] = ""


def main():
    initialise()
    st.header('🗃️ Demo Chat')

    st.session_state.input = input(placeholder="Enter your input", loading=False, loadingText="Loading...", rows=1)
    if st.session_state.input != "" and st.session_state.input is not None:
        st.session_state['leftMessages'].append(st.session_state.input)
        st.session_state['rightMessages'].append("(Response) : " + st.session_state.input)


    display_chat(leftMessages=st.session_state['leftMessages'], rightMessages=st.session_state['rightMessages'], height=600)

if not _RELEASE:
    st.set_page_config(page_title="ChatBox Demo", page_icon=":speech_balloon:")
    st.markdown("## Streamlit ChatBox Demo 💬")
    main()
