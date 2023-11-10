import streamlit as st
from api import nav_page

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

def main() :
    nav_page("home")

if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement.
    main()