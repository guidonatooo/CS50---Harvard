from time import sleep

import streamlit as st

from crud import read_all_users
from management_page import tab_usermanagement
from calendar_page import calendar_page

def login():
    user_vacation = read_all_users()
    user_vacation = {user.name: user for user in user_vacation}
    with st.container(border=True):
        st.markdown('Welcome to Web Vacation')
        name_user = st.selectbox(
            'Select user',
            user_vacation.keys()
            )
        password = st.text_input('Password', type="password")
        if st.button('Access'):
            user = user_vacation[name_user]
            if user.verify_password(password):
                st.success('Login successful')
                st.session_state['logged'] = True
                st.session_state['user'] = user
                sleep(1)
                st.rerun()
            else:
                st.error('Incorrect Password')

def main_page():
    st.title('Bem-vindo ao Web Vacation')
    st.divider()

    # Recuperar o usuário atual
    user = st.session_state.get('user')

    # Verificar se o usuário tem acesso de gerente
    if user and user.manager_access:
        # Botões para alternar entre as páginas
        cols = st.columns(2)
        with cols[0]:
            if st.button('Access User Management', use_container_width=True):
                st.session_state['current_page'] = 'user_management'
        with cols[1]:
            if st.button('Access Calendar', use_container_width=True):
                st.session_state['current_page'] = 'calendar'

    # Exibir a página com base no estado atual
    current_page = st.session_state.get('current_page', 'calendar')
    if current_page == 'user_management':
        st.markdown("### User Management")
        tab_usermanagement()
    elif current_page == 'calendar':
        st.markdown("### Calendar")
        calendar_page()


def main():

    if 'logged' not in st.session_state:
        st.session_state['logged'] = False
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'calendar'  # Página padrão
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    if not st.session_state['logged']:
        login()
    else:
        main_page()

if __name__ == '__main__':
    main()
