import streamlit as st

from data.data_repo import get_tintes
from models.predictor import run_components_xgb_prediction
from pgs.components import get_cantidad_tinte, get_rango, get_tinte_selector


def components_page() -> None:
    st.subheader(":test_tube: Predicción viscosidad por proporción de componentes")

    selected_tinte = get_tinte_selector()
    cantidad_tinte = get_cantidad_tinte()

    rango = get_rango(cantidad_tinte)

    predict_btn = st.button("Predecir viscosidad")

    if predict_btn:
        run_components_xgb_prediction(selected_tinte, cantidad_tinte, rango)
