import streamlit as st

from pgs.components import get_cantidad_tinte, get_tinte_selector


def groups_page() -> None:
    st.subheader(":microscope: Predicción de viscosidad por grupos funcionales")

    selected_tinte = get_tinte_selector()
    cantidad_tinte = get_cantidad_tinte()
