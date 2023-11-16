import streamlit as st


def home_page() -> None:
    st.markdown(
        "<h1 style='text-align: center; color: black;'>ToMakeUp</h1>",
        unsafe_allow_html=True,
    )

    st.image("images/portada.png")

    st.markdown(
        """
        ## Aplicación de Predicción de Viscosidad para Fabricación de Tintes de Cabello

        Bienvenido a nuestra aplicación avanzada para la predicción de la viscosidad en el proceso de fabricación de tintes de cabello. 
        Nuestro sistema utiliza tecnología punta para garantizar la calidad y consistencia de los tintes producidos. 
        A continuación, encontrarás cómo nuestra aplicación puede ayudarte a mejorar tus procesos de fabricación.

        ### Características Principales

        #### Selección y Predicción
        - **Selección del Tinte**: Elige el tipo de tinte que deseas producir y la cantidad requerida.
        - **Predicción de Viscosidad**: Calculamos la probabilidad de que la viscosidad no sea la adecuada para cada uno de los tres reactores disponibles 
        en la planta de fabricación.
        
        Hay tres reactores, grande de 3000 Kg, mediano de 1000 Kg y pequeño de 500 Kg.

        #### Métodos de Predicción

        1. **Proporción de Componentes**:
        - Al seleccionar un tinte, nuestro sistema analiza y tiene en cuenta cada uno de los componentes en proporción a sus cantidades. 

        2. **Grupos Funcionales**:
        - Agrupamos las cantidades de componentes según sus grupos funcionales. Estos grupos incluyen:
            - **Colorantes**: Sustancias que proporcionan el color deseado al tinte.
            - **Excipientes**: Componentes que facilitan la aplicación y estabilidad del tinte.
            - **Emulsionantes**: Ayudan a mezclar sustancias que normalmente no se combinan bien, como el aceite y el agua.
            - **Agua**: Utilizada como disolvente y medio de mezcla.

        #### Beneficios de Utilizar Nuestra Aplicación

        - **Optimización de la Producción**: Mejora la eficiencia y reduce los tiempos de inactividad en la producción.
        - **Calidad del Producto**: Asegura la consistencia en la calidad del tinte, satisfaciendo a tus clientes.
        - **Reducción de Desperdicios**: Minimiza los residuos generados por mezclas incorrectas.
    """
    )
