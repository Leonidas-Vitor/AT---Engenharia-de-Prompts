import streamlit as st
import yaml
import json
#from streamlit_extras.app_logo import add_logo
from services import APP_Pages

st.set_page_config(
        page_title="AT - Engenharia de Prompts",
        page_icon="images/Infnet_logo.png",
        layout="wide",
        initial_sidebar_state = "expanded")

#Carregar configurações
APP_Pages.LoadConfigs()

#pg = st.navigation()

#add_logo("images/infnet-30-horizontal-branco.png", height=156)

#pg.run()
intro_container = APP_Pages.ShowIntro()

aplication_container = st.container(border=True)
with aplication_container:
    st.subheader("Aplicação", divider=True)
    tab1, tab2 = st.tabs(['Arquitetura','Textos'])
    with tab1:
        st.write("Arquitetura")
    with tab2:
        st.write("Textos")

misc_container = APP_Pages.ShowMisc()