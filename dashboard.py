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

with st.sidebar:
    st.image("images/infnet-30-horizontal-branco.png", width=400)
    with st.container(border=True):
        st.subheader("Observações", divider=True)
        st.markdown('O trabalho possui duas partes:')
        st.markdown('1. **Aplicação**: Funções e recursos solicitados para a aplicação streamlit')
        st.markdown('2. **Miscelânea**: Fotos e respostas para as demais questão do AT')

        st.divider()

        st.markdown('*As mesmas respostas da parte de miscelânea estão presentes no PDF do AT*')

            

aplication_container = st.container(border=True)
with aplication_container:
    st.subheader("Aplicação", divider=True)
    APP_Pages.criar_tabs()

misc_container = APP_Pages.ShowMisc()