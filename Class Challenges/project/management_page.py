import streamlit as st
import pandas as pd
from crud import read_all_users, create_user, update_user, delete_user

def tab_usermanagement():
    """Funções de gerenciamento de usuários."""
    tab_vis, tab_creation, tab_modify, tab_del = st.tabs(
        ['Visualizar', 'Criar', 'Modificar', 'Deletar']
    )

    # Obter todos os usuários
    user_vacation = read_all_users()

    # Aba de visualização
    with tab_vis:
        data_user = [{
            'ID': user.id,
            'Nome': user.name,
            'Email': user.email,
            'Gestor': user.manager_access,
            'Data de Início': user.start_in_company,
            'Profissão': user.profession
        } for user in user_vacation]
        st.dataframe(pd.DataFrame(data_user).set_index('ID'))

    # Aba de criação de usuário
    with tab_creation:
        name = st.text_input('Nome do Usuário')
        password = st.text_input('Senha do Usuário', type="password")
        email = st.text_input('Email do Usuário')
        manager_access = st.checkbox('Gestor', value=False)
        profession = st.selectbox('Profissão', ['Veterinário', 'Enfermeiro', 'Estagiário'])
        start_in_company = st.text_input(
            'Data de Início na Empresa (formato YYYY-MM-DD)'
        )
        if st.button('Criar Usuário'):
            if name and password and email and profession and start_in_company:
                create_user(
                    name=name,
                    password=password,
                    email=email,
                    manager_access=manager_access,
                    profession=profession,
                    start_in_company=start_in_company
                )
                st.success(f"Usuário '{name}' criado com sucesso!")
                st.stop()
            else:
                st.error("Preencha todos os campos corretamente.")

    # Aba de modificação de usuário
    with tab_modify:
        user_dic = {user.name: user for user in user_vacation}
        name_user = st.selectbox(
            'Selecione o Usuário para Modificar',
            user_dic.keys()
        )
        user = user_dic[name_user]

        name = st.text_input('Modificar Nome', value=user.name)
        password = st.text_input('Modificar Senha', value='XXX', type="password")
        email = st.text_input('Modificar Email', value=user.email)
        manager_access = st.checkbox('Gestor', value=user.manager_access)

        professions = ['Veterinário', 'Enfermeiro', 'Estagiário']
        profession_index = professions.index(user.profession) if user.profession in professions else 0
        profession = st.selectbox('Profissão', professions, index=profession_index)

        start_in_company = st.text_input(
            'Modificar Data de Início (formato YYYY-MM-DD)',
            value=user.start_in_company
        )
        if st.button('Modificar Usuário'):
            if password == 'XXX':
                update_user(
                    user_id=user.id,
                    name=name,
                    email=email,
                    manager_access=manager_access,
                    profession=profession,
                    start_in_company=start_in_company
                )
            else:
                update_user(
                    user_id=user.id,
                    name=name,
                    password=password,
                    email=email,
                    manager_access=manager_access,
                    profession=profession,
                    start_in_company=start_in_company
                )
            st.success(f"Usuário '{name}' modificado com sucesso!")
            st.stop()

    # Aba de deleção de usuário
    with tab_del:
        user_dic = {user.name: user for user in user_vacation}
        name_user = st.selectbox(
            'Selecione o Usuário para Deletar',
            user_dic.keys()
        )
        user = user_dic[name_user]

        if st.button(f'Deletar {name_user}'):
            delete_user(user.id)
            st.success(f"Usuário '{name_user}' deletado com sucesso!")
            st.stop()

# Atualizar automaticamente após ações
    if st.button("Atualizar Página", key="update_page", use_container_width=True):
        st.stop()
