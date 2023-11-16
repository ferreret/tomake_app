import streamlit as st

from data.data_repo import get_tintes


def get_tinte_selector() -> str:
    return st.selectbox("Selección de tinte:", get_tintes())


def get_cantidad_tinte() -> int:
    return st.number_input(
        "Cantidad de tinte a producir (Kg):",
        min_value=1,
        max_value=3000,
        value=1,
    )


def get_rango(cantidad: int) -> int:
    if cantidad <= 10:
        return st.slider(
            "Rango de cantidad:", min_value=0, max_value=cantidad, value=0, step=1
        )

    maximo = int(cantidad * 1.2)
    rango_maximo = maximo - cantidad

    return st.slider(
        "Rango de cantidad:", min_value=0, max_value=rango_maximo, value=0, step=1
    )
