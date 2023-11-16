import pandas as pd
import streamlit as st


@st.cache_data
def get_tintes() -> list[str]:
    try:
        with open("data/tintes.txt") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        st.error("No se encontró el archivo tintes.txt")
        return []
    except Exception as e:
        st.error(f"Error desconocido: {e}")
        return []


@st.cache_data
def read_components() -> pd.DataFrame:
    return pd.read_csv("data/componentes.csv")


def get_components_by_tinte(codigo_tinte: int) -> pd.DataFrame:
    df_components = read_components()
    df_tinte = df_components[df_components["material"] == codigo_tinte]
    # Borramos la columna material porque ya sabemos que es el tinte
    df_tinte = df_tinte.drop("material", axis=1)
    return df_tinte