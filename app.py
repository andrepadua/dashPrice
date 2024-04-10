import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from yaml.loader import SafeLoader
from streamlit_authenticator.utilities.hasher import Hasher


def main():
    st.set_page_config(layout="wide", page_title="Solaris Systems", page_icon=":chart_with_upwards_trend:")

    #hashed_passwords = stauth.Hasher(['ap123', 'cp123']).generate()

    passwords_to_hash = ['ap123', 'cp123']
    hashed_passwords = Hasher(passwords_to_hash).generate()

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('main')

    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'Bem-vindo *{name}*')
        #st.title('Some content')
        

        st.title("Consulta Preços - Flytec Computers 03/04/2024")
        df = pd.read_excel('prices.xlsx', sheet_name='price')
        with st.sidebar:
            st.image('logo.png')
            st.header("Pesquisa")
            selected_product = st.selectbox(label="Selecione o Produto:", options=set(df['product']))
            del df

        @st.cache_data
        def carrega_dados(product):
            dados = pd.read_excel('prices.xlsx', sheet_name='price')
            if product:
                dados = dados.query("product == '{}'".format(product))
            return dados

        # Mensagem de carga dos dados
        mensagem = st.text('Carregando os dados...')

        # Carrega os dados
        dados = carrega_dados(selected_product)

        # Mensagem de encerramento da carga dos dados
        mensagem.text('Carregando os dados...Concluído!')
        
        with st.sidebar:
            st.markdown("---")
            st.markdown(
                '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by @solarissystems</h6>',
                unsafe_allow_html=True,
            )
            
        st.table(dados)

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

    

if __name__ == "__main__":
    main()
