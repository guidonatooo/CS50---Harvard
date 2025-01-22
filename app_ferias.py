from time import sleep

import streamlit as st

from crud import le_todos_usuarios
from pagina_gestao import pagina_gestao
from pagina_calendario import pagina_calendario

def login():
    usuarios = le_todos_usuarios()
    usuarios = {usuario.nome: usuario for usuario in usuarios}
    with st.container(border=True):
        st.markdown('Bem-vindos ao AppFerias')
        nome_usuario = st.selectbox(
            'Selecione o seu usuário',
            usuarios.keys()
            )
        senha = st.text_input('Digite sua senha', type='password')
        if st.button('Acessar'):
            usuario = usuarios[nome_usuario]
            if usuario.verifica_senha(senha):
                st.success('Login efetuado com sucesso')
                st.session_state['logado'] = True
                st.session_state['usuario'] = usuario
                sleep(1)
                st.rerun()
            else:
                st.error('Senha incorreta')

def pagina_principal():
    st.title('Bem-vindo ao AppFerias')

    usuario = st.session_state['usuario']
    if usuario.acesso_gestor:
        cols = st.columns(2)
        with cols[0]:
            if st.button(
                'Acessar Gestão de Usuários',
                use_container_width=True):
                st.session_state['pag_gestao_usuarios'] = True
                st.rerun()
        with cols[1]:
            if st.button(
                'Acessar Calendário',
                use_container_width=True
                ):
                st.session_state['pag_gestao_usuarios'] = False
                st.rerun()
        
    if st.session_state['pag_gestao_usuarios']:
        pagina_gestao()
    else:
        pagina_calendario()

def main():

    if not 'logado' in st.session_state:
        st.session_state['logado'] = False
    if not 'pag_gestao_usuarios' in st.session_state:
        st.session_state['pag_gestao_usuarios'] = False
    if not 'ultimo_clique' in st.session_state:
        st.session_state['ultimo_clique'] = ''
    
    if not st.session_state['logado']:
        login()
    else:
        pagina_principal()


if __name__ == '__main__':
    main()