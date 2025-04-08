import json
import streamlit as st
from streamlit_calendar import calendar
from crud import read_all_users, read_user_by_id

def clear_date():
    """Função para limpar as datas de início e fim das férias."""
    if 'begin_date' in st.session_state:
        del st.session_state['begin_date']
    if 'end_date' in st.session_state:
        del st.session_state['end_date']

def delete_vacation(user, event_id):
    """Função para deletar férias selecionadas."""
    try:
        user.delete_vacation(event_id)
        st.success("Férias removidas com sucesso!")
    except Exception as e:
        st.error(f"Erro ao remover férias: {e}")

def modify_vacation(user, event_id, new_start, new_end):
    """Função para modificar férias selecionadas."""
    try:
        user.modify_vacation(event_id, new_start, new_end)
        st.success("Férias modificadas com sucesso!")
    except Exception as e:
        st.error(f"Erro ao modificar férias: {e}")

def calendar_page():
    """Página principal do calendário."""
    if 'user' not in st.session_state:
        st.error("Usuário não encontrado na sessão. Por favor, faça login novamente.")
        st.stop()

    user = st.session_state['user']

    with open('calendar_options.json') as f:
        calendar_options = json.load(f)

    # Recuperar usuários e eventos de férias
    users = read_all_users()
    calendar_events = []
    for user in users:
        if hasattr(user, "vacation_list") and callable(user.vacation_list):
            try:
                events = user.vacation_list()
                # Garantir que cada evento tenha um ID único
                for event in events:
                    event['id'] = f"{user.id}-{event['start']}-{event['end']}"
                calendar_events.extend(events)
            except Exception as e:
                st.warning(f"Erro ao recuperar a lista de férias do usuário {user.name}: {e}")
        else:
            st.warning(f'Usuário {user.name} não possui método vacation_list implementado ou configurado corretamente.')

    calendar_widget = calendar(events=calendar_events, options=calendar_options)

    # Interação com o calendário
    if 'callback' in calendar_widget:
        callback_type = calendar_widget['callback']

        if callback_type == 'dateClick':
            raw_date = calendar_widget['dateClick']['date']
            date = raw_date.split('T')[0]

            if 'begin_date' not in st.session_state:
                st.session_state['begin_date'] = date
                st.success(f'Data de início selecionada: {date}')
            else:
                st.session_state['end_date'] = date
                begin_date = st.session_state['begin_date']
                end_date = st.session_state['end_date']

                cols = st.columns([0.7, 0.3])
                with cols[0]:
                    st.success(f'Férias de {begin_date} a {end_date} selecionadas.')
                with cols[1]:
                    st.button('Limpar', use_container_width=True, on_click=clear_date)

                if hasattr(user, "manager_access") and user.manager_access:
                    try:
                        st.button(
                            'Adicionar Férias',
                            use_container_width=True,
                            on_click=user.add_vacation,
                            args=(begin_date, end_date)
                        )
                    except Exception as e:
                        st.error(f'Erro ao adicionar férias: {e}')

        elif callback_type == 'eventClick':
            try:
                event = calendar_widget['eventClick']
                event_id = event.get('id')

                if not event_id:
                    st.error("Evento selecionado não possui um ID válido.")
                else:
                    st.warning(f"Evento selecionado: ID {event_id}")

                    with st.expander("Modificar ou Deletar Férias"):
                        new_start = st.text_input("Nova Data de Início (YYYY-MM-DD)", value=event.get('start', ''))
                        new_end = st.text_input("Nova Data de Fim (YYYY-MM-DD)", value=event.get('end', ''))

                        cols = st.columns(2)
                        with cols[0]:
                            if st.button("Modificar Férias", key=f"modify_{event_id}"):
                                modify_vacation(user, event_id, new_start, new_end)
                        with cols[1]:
                            if st.button("Deletar Férias", key=f"delete_{event_id}"):
                                delete_vacation(user, event_id)
            except Exception as e:
                st.error(f"Erro ao manipular evento: {e}")

    # Mostrar número de dias restantes para solicitação de férias
    with st.expander('Dias disponíveis para solicitação'):
        if hasattr(user, 'request_vacation_days') and callable(user.request_vacation_days):
            try:
                vacation_days = user.request_vacation_days()
                st.markdown(f'O usuário **{user.name}** tem **{vacation_days}** dias disponíveis para solicitar.')
            except Exception as e:
                st.error(f'Erro ao calcular os dias de férias disponíveis: {e}')
        else:
            st.error('Não foi possível calcular os dias de férias disponíveis. Verifique a configuração do método request_vacation_days.')

    # Atualizar automaticamente após ações
    if st.button("Atualizar Página", key="update_page"):
        st.stop()

