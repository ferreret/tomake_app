import streamlit as st
from streamlit_option_menu import option_menu

import settings
from pgs.components_page import components_page
from pgs.groups_page import groups_page
from pgs.home_page import home_page


def create_menu() -> None:
    """
    Creates a menu using Streamlit's sidebar and displays different pages based on the user's selection.

    Returns:
        None
    """
    with st.sidebar:
        selected = option_menu(
            settings.MENU_NAME,
            settings.MENU_OPTIONS,
            icons=settings.MENU_ICONS,
            menu_icon=settings.MENU_ICON,
            default_index=0,
        )

    if selected == settings.MENU_OPTIONS[0]:
        home_page()
    elif selected == settings.MENU_OPTIONS[1]:
        components_page()
    elif selected == settings.MENU_OPTIONS[2]:
        groups_page()


def config_app() -> None:
    """
    Configures the ToMakeUp app with Streamlit's `set_page_config` function.

    Sets the page title to "ToMakeUp", the page icon to ":haircut:", the layout to "wide",
    and the initial sidebar state to "expanded".
    """
    st.set_page_config(
        page_title="ToMakeUp",
        page_icon=":haircut:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def main() -> None:
    """
    This function initializes the application by configuring the app and creating the menu.
    """
    config_app()
    create_menu()


if __name__ == "__main__":
    main()
