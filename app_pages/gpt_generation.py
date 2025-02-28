import streamlit as st

###########################
### Пишем функцию работы ГПТ
###########################
from funcs.try_gpt import ask_gigachat

def run():
    ###########################
    ### Блок описания страницы
    ###########################
    st.subheader('Привет, путник! На этой странице ты найдёшь ответы на все свои запросы и пожелания по фильмам, не стесняйся, задавай вопрос ниже!')
    
    user_text = st.text_input('Введите свой запрос на фильм')
    
    # Добавляем кнопку для получения ответа
    left, middle, right = st.columns(3)
    if middle.button('Смотреть фильм', icon="👀", use_container_width=True):
        if user_text:  # Проверяем, что поле ввода не пустое
            resp = ask_gigachat(user_text)
            st.write('Предлагаю посмотреть вам следующие фильмы:')
            st.markdown(f"""
                <h2 style='text-align: center; color:#3262a8; font-size: 30px; font-weight: bold; padding: 10px; border-radius:10px;'>
                {resp}
                </h2>
                """, unsafe_allow_html=True)
        else:
            st.warning("Пожалуйста, введите свой запрос на фильм.")