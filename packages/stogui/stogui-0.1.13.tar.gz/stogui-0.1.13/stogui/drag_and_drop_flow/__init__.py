from distutils.util import strtobool
import os
import streamlit.components.v1 as components

DEBUG = strtobool(os.getenv('STOGUI_DEBUG', 'false'))


if DEBUG:
    _component_func = components.declare_component(
        'drag_and_drop_flow', url='http://localhost:3001',
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, 'frontend/build')
    _component_func = components.declare_component('drag_and_drop_flow', path=build_dir)


def drag_and_drop_flow():
    return _component_func()
