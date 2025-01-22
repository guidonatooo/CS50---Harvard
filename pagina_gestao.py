import streamlit as st
import pandas as pd

from crud import (
    le_todos_usuarios,
    cria_usurios,
    modifica_usuario,
    deleta_usuario
    )

def pagina_gestao():
    with st.sidebar:
        tab_gestao_usuarios()
    
    usuarios = le_todos_usuarios()

    for usuario in usuarios:
        with st.container(border=True):
            cols = st.columns(2)
            dias_para_solicitar = usuario.dias_para_solicitar()
            with cols[0]:
                if dias_para_solicitar > 40:
                    st.error(f'### {usuario.nome}')
                else:
                    st.markdown(f'### {usuario.nome}')
            with cols[1]:
                if dias_para_solicitar > 40:
                    st.error(f'#### Dias para solicitar: {dias_para_solicitar}')
                else:
                    st.markdown(f'#### Dias para solicitar: {dias_para_solicitar}')

def tab_gestao_usuarios():
    tab_vis, tab_cria, tab_mod, tad_del = st.tabs(
        ['Visualizar', 'Criar', 'Moldificar', 'Deletar']
    )
    usuarios = le_todos_usuarios()
    with tab_vis:
        data_usuarios = [{
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'acesso_gestor': usuario.acesso_gestor,
            'inicio_na_empresa': usuario.inicio_na_empresa
        } for usuario in usuarios]
        st.dataframe(pd.DataFrame(data_usuarios).set_index('id'))

    with tab_cria:
        nome = st.text_input('Nome do usuário')
        senha = st.text_input('Senha do usuário')
        email = st.text_input('Email do usuário')
        acesso_gestor = st.checkbox('Tem acesso de gestor?', value=False)
        inicio_na_empresa = st.text_input(
            'Data de início na empresa (formato AAAA-MM-DD)'
            )
        if st.button('Criar'):
            cria_usurios(
                nome=nome,
                senha=senha,
                email=email,
                acesso_gestor=acesso_gestor,
                inicio_na_empresa=inicio_na_empresa,
            )
            st.rerun()
    
    with tab_mod:
        usuarios_dict = {usuario.nome: usuario for usuario in usuarios}
        nome_usuario = st.selectbox(
            'Selecione o usuário para modificar',
            usuarios_dict.keys())
        usuario = usuarios_dict[nome_usuario] 
        nome = st.text_input(
            'Nome do usuário para modificar', 
            value=usuario.nome
            )
        senha = st.text_input('Senha do usuário', value='xxxxx')
        email = st.text_input(
            'Email para modificar', 
            value=usuario.email
            )
        acesso_gestor = st.checkbox('Modificar acesso de gestor?', value=usuario.acesso_gestor)
        inicio_na_empresa = st.text_input(
            'Data de início na empresa (formato AAAA-MM-DD)',
            value=usuario.inicio_na_empresa
            )
        if st.button('Modificar'):
            if senha == 'xxxxx':
                modifica_usuario(
                    id=usuario.id,
                    nome=nome,
                    email=email,
                    acesso_gestor=acesso_gestor,
                    inicio_na_empresa=inicio_na_empresa,
                )
            else:
                modifica_usuario(
                    id=usuario.id,
                    nome=nome,
                    senha=senha,
                    email=email,
                    acesso_gestor=acesso_gestor,
                    inicio_na_empresa=inicio_na_empresa,
                )
            st.rerun()
    with tad_del:
        usuarios_dict = {usuario.nome: usuario for usuario in usuarios}
        nome_usuario = st.selectbox(
            'Selecione o usuário para deletar',
            usuarios_dict.keys())
        usuario = usuarios_dict[nome_usuario]
        if st.button('Deletar'):
            deleta_usuario(usuario.id)
            st.rerun()
