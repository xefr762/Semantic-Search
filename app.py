import streamlit as st

st.set_page_config(page_title="Семантический поиск кино", page_icon="🎦", layout='wide')

if "page" not in st.session_state:
    st.session_state.page = "Главная"

def go_to(page):
    st.session_state.page = page

st.sidebar.title("📌 Меню")
st.sidebar.button("🏠 Главная", on_click=lambda: go_to("Главная"), use_container_width=True)
st.sidebar.button("🎰 Сходить к тарологу", on_click=lambda: go_to("Рандом"), use_container_width=True)
st.sidebar.button("🎬 Подбор фильма по запросу", on_click=lambda: go_to("Подбор"), use_container_width=True)
st.sidebar.button("🤖 Подбор фильма с GPT", on_click=lambda: go_to("Генерация"), use_container_width=True)

if st.session_state.page == "Главная":
    st.title("Семантический поиск кино")
    st.markdown("""
    ## Добро пожаловать на главную страницу приложения по подбору фильмов!

    **Описание:**
    - **Главная страница**: Общая информация и навигация 🌌
    - **Release 1.0**: 🍀 Рандомный выбор 10 фильмов, испытай свою удачу! 🎰
    - **Release 2.0**: Подбор кино по запросу 👀
    - **Release 3.0**: Подбор кино на по запросу с использованием GPT 🥂
    Переключайтесь между страницами через левый сайдбар! 
    """)

elif st.session_state.page == "Рандом":
    from app_pages import random_selection
    random_selection.run()
elif st.session_state.page == "Подбор":
    from app_pages import bert
    bert.run()
elif st.session_state.page == "Генерация":
    from app_pages import gpt_generation
    gpt_generation.run()
