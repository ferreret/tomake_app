import pandas as pd
import plotly.graph_objs as go
import streamlit as st
import xgboost as xgb
from joblib import load

from data.data_repo import get_components_by_tinte
from settings import CAPACIDAD_REACTORES


def grado_llenado(cantidad: int, show_warning=True) -> tuple[float, float, float]:
    """En esta función validamos la cantidad de tinte a producir,
    a su vez, devolveremos el grado de llenado para cada uno de los reactores.

    Args:
        cantidad (int): Cantidad de tinte a producir en Kg

    Returns:
        tuple[float, float, float]: Grado de llenado para cada uno de los reactores, grande, mediano, pequeño

    """
    grados_llenado = {}
    for reactor, capacidad in CAPACIDAD_REACTORES.items():
        if cantidad <= capacidad:
            grados_llenado[reactor] = round((cantidad / capacidad) * 100, 2)
        else:
            grados_llenado[reactor] = 0
            if show_warning:
                st.warning(
                    f"La cantidad de tinte a producir supera la capacidad del reactor {reactor}"
                )

    return (
        grados_llenado["grande"],
        grados_llenado["mediano"],
        grados_llenado["pequeño"],
    )

def add_features(
    components: pd.DataFrame, grados_llenado: tuple[float, float, float], cantidad: int
) -> list[pd.DataFrame]:
    """
    Genera una lista de DataFrames con características adicionales para cada reactor.

    :param components: DataFrame con los componentes.
    :param grados_llenado: Tuple con los grados de llenado para cada reactor.
    :param cantidad: Cantidad a añadir en cada DataFrame.
    :return: Lista con tres DataFrames, uno para cada reactor.
    """
    # Nombres de las columnas adicionales
    columnas_reactor = ["reactor_mediano", "reactor_pequeño"]

    # Inicializar los DataFrames resultantes
    dfs = []

    for i, grado_llenado in enumerate(grados_llenado):
        df_temp = components.copy()
        # Establecer las columnas del reactor
        df_temp["reactor_mediano"] = int(i == 1)
        df_temp["reactor_pequeño"] = int(i == 2)
        # Añadir grado de llenado y cantidad
        df_temp["grado_llenado"] = grado_llenado
        df_temp["cantidad"] = cantidad
        # Reordenar las columnas
        columnas_ordenadas = ["cantidad", "grado_llenado"] + [
            col for col in df_temp.columns if col not in ["cantidad", "grado_llenado"]
        ]
        dfs.append(df_temp[columnas_ordenadas])

    return dfs

def predecir_viscosidad(dfs, xgb_model, cantidad, rango, grado_llenado):
    """
    Predice la probabilidad de viscosidad para cada reactor y actualiza los DataFrames.

    :param dfs: Lista de DataFrames correspondientes a cada reactor.
    :param xgb_model: Modelo XGBoost para la predicción.
    :param cantidad: Cantidad actual en el reactor.
    :param rango: Rango de variación de la cantidad.
    :param grado_llenado: Función para calcular el grado de llenado.
    """
    for i, df in enumerate(dfs):
        if df is not None:
            # Predecir probabilidad inicial
            df["probabilidad_valor_medio"] = (
                xgb_model.predict_proba(df)[:, 1] * 100
            ).round(2)

            if rango > 0:
                for j in range(cantidad - rango, cantidad + rango + 1):
                    if (
                        i == 0
                        or j <= CAPACIDAD_REACTORES[["mediano", "pequeño"][i - 1]]
                    ):
                        df_temp = df.copy()
                        df_temp["cantidad"] = j
                        df_temp["grado_llenado"] = grado_llenado(j, show_warning=False)[
                            i
                        ]

                        # Concatenar con el DataFrame principal
                        dfs[i] = pd.concat([dfs[i], df_temp])

            # Calcular la probabilidad final
            dfs[i]["probabilidad"] = (
                xgb_model.predict_proba(
                    dfs[i].drop(columns=["probabilidad_valor_medio"])
                )[:, 1]
                * 100
            ).round(2)

    return dfs

def mostrar_resultado_sin_rango(dfs: list[pd.DataFrame], tinte: str) -> None:
    """
    Muestra la probabilidad de viscosidad para un tinte dado.

    Parameters
    ----------
    dfs : list[pd.DataFrame]
        Una lista de DataFrames que contienen información sobre la probabilidad de viscosidad para el tinte dado.
    tinte : str
        El nombre del tinte para el cual se desea mostrar la probabilidad de viscosidad.

    Returns
    -------
    None
    """
    st.markdown(f"**Probabilidad de viscosidad para el tinte {tinte}**")
    # Concatenamos los DataFrames
    df = pd.concat(dfs)
    # Ordenamos por probabilidad descendente
    df = df.sort_values(by=["probabilidad"])

    # Si reactor_mediano y reactor_pequeño son 0, creamos una columna de nombre reactor que tenga el valor Grande
    # Si reactor_mediano es 1, creamos una columna de nombre reactor que tenga el valor Mediano
    # Si reactor_pequeño es 1, creamos una columna de nombre reactor que tenga el valor Pequeño
    df["reactor"] = df.apply(
        lambda x: ["Grande", "Mediano", "Pequeño"][
            int(x["reactor_mediano"]) + int(x["reactor_pequeño"]) * 2
        ],
        axis=1,
    )

    for i, row in enumerate(df.itertuples(index=False)):
        message = f"Reactor {row.reactor}: {row.probabilidad:.2f}% de probabilidad de viscosidad negativa"
        if i == 0:
            st.success(message)
        else:
            st.info(message)

def mostrar_resultado_con_rango(dfs: list[pd.DataFrame], tinte: str) -> None:
    """
    Plots the probability of negative viscosity for a given dye, based on the amount produced.

    Args:
        dfs (list[pd.DataFrame]): A list of pandas DataFrames containing the probability of negative viscosity
            for each reactor, sorted by the amount of dye produced.
        tinte (str): The name of the dye being produced.

    Returns:
        None
    """
    # Ordenamos por cantidad
    for i, df in enumerate(dfs):
        if df is not None:
            dfs[i] = df.sort_values(by=["cantidad"])

    trace1 = go.Scatter(
        x=dfs[0]["cantidad"],
        y=dfs[0]["probabilidad"],
        mode="lines",
        name="Reactor Grande",
    )
    if dfs[1] is not None:
        trace2 = go.Scatter(
            x=dfs[1]["cantidad"],
            y=dfs[1]["probabilidad"],
            mode="lines",
            name="Reactor Mediano",
        )
    if dfs[2] is not None:
        trace3 = go.Scatter(
            x=dfs[2]["cantidad"],
            y=dfs[2]["probabilidad"],
            mode="lines",
            name="Reactor Pequeño",
        )
    if dfs[1] is not None and dfs[2] is not None:
        fig = go.Figure(data=[trace1, trace2, trace3])
    elif dfs[1] is not None:
        fig = go.Figure(data=[trace1, trace2])
    else:
        fig = go.Figure(data=[trace1])

    fig.update_layout(
        title=f"Probabilidad de viscosidad para el tinte {tinte}",
        xaxis_title="Cantidad de tinte a producir (Kg)",
        yaxis_title="Probabilidad de viscosidad negativa (%)",
        legend_title="Reactor",
    )

    st.plotly_chart(fig, use_container_width=True)

def run_components_xgb_prediction(tinte: str, cantidad: int, rango: int):
    """
    Runs the XGBoost model to predict the viscosity probability for each reactor based on the given tinte, cantidad, and rango.

    Args:
        tinte (str): The tinte to use for the prediction.
        cantidad (int): The amount of tinte to use for the prediction.
        rango (int): The range of the prediction.

    Returns:
        None
    """
    # El código de tinte son los 6 primeros caracteres del tinte
    components = get_components_by_tinte(int(tinte[:6]))

    if len(components) == 0:
        st.error("No se encontraron componentes para el tinte seleccionado")
        return

    grados_llenado = grado_llenado(cantidad)

    # Creo un dataframe para cada reactor
    dfs = add_features(components, grados_llenado, cantidad)

    # Cargamos el modelo
    xgb_model = load("models/xgb_viscosity.joblib")

    # Predecimos la probabilidad de viscosidad para cada reactor
    predecir_viscosidad(dfs, xgb_model, cantidad, rango, grado_llenado)

    if rango > 0:
        mostrar_resultado_con_rango(dfs, tinte)
    else:
        mostrar_resultado_sin_rango(dfs, tinte)
