import json
from datetime import datetime

import streamlit as st
from streamlit_calendar import calendar

from crud import le_todos_usuarios

def verifica_e_adiciona_ferias(data_inicio, data_fim):
    usuario = st.session_state['usuario']
    total_dias = (
        datetime.strptime(data_fim, '%Y-%m-%d')
        - datetime.strptime(data_inicio, '%Y-%m-%d')
    ).days + 1
    dias_solicitar = usuario.dias_para_solicitar()
    if total_dias < 5:
        st.error('Quantidade de dias inferior a 5')
    elif dias_solicitar < total_dias:
        st.error(f'Usuario solicitou {total_dias} mas tem apenas {dias_solicitar} para solicitar')
    else:
        usuario.adiciona_ferias(data_inicio, data_fim)
        limpar_datas()

def limpar_datas():
    del st.session_state['data_inicio']
    del st.session_state['data_final']

def pagina_calendario():

    with open('calendar_options.json') as f:
        calendar_options = json.load(f)

    usuarios = le_todos_usuarios()
    calendar_events = []
    for usuario in usuarios:
        calendar_events.extend(usuario.lista_ferias())

    usuario = st.session_state['usuario']

    with st.expander('Dias para solicitar'):
        dias_para_solicitar = usuario.dias_para_solicitar()
        st.markdown(f'O usurio {usuario.nome} possui **{dias_para_solicitar}** dias para solicitar')

    calendar_widget = calendar(events=calendar_events, options=calendar_options)
    if ('callback' in calendar_widget 
        and calendar_widget['callback'] == 'dateClick'):

        raw_date = calendar_widget['dateClick']['date'].split('T')[0]
        if raw_date != st.session_state['ultimo_clique']:

            st.session_state['ultimo_clique'] = raw_date
            date = calendar_widget['dateClick']['date'].split('T')[0]
            
            if not 'data_inicio' in st.session_state:
                st.session_state['data_inicio'] = date
                st.warning(f'Data de início de férias selecionada {date}')
            else:
                st.session_state['data_final'] = date
                date_inicio = st.session_state['data_inicio']
                cols = st.columns([0.7, 0.3])
                with cols[0]:
                    st.warning(f'Data de início de férias selecionada {date_inicio}')
                with cols[1]:
                    st.button(
                        'Limpar',
                        use_container_width=True,
                        on_click=limpar_datas
                        )
                cols = st.columns([0.7, 0.3])
                with cols[0]:
                    st.warning(f'Data final de férias selecionada {date}')
                with cols[1]:
                    st.button(
                        'Adicionar Férias',
                        use_container_width=True,
                        on_click=verifica_e_adiciona_ferias,
                        args=(date_inicio, date)
                        )





