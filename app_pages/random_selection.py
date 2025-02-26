import streamlit as st
import pandas as pd
import random

#st.set_page_config(page_title="Случайные фильмы", page_icon="🍀", layout='wide')
def run():
    # read df
    path = '/home/marena/Elbrus_phase_2/Semantic-Search/test.csv'
    df = pd.read_csv(path, index_col='Unnamed: 0')

    # Функция генерации и вывода 10 рандомных фильмов из датафрейма
    #l, mid, r = st.columns(3)
    st.subheader('Привет, ты решил испытать удачу, и посмотреть 10 случайных фильмов. Вот твоя топовая подборка на сегодня!')

    def random_generator(df: pd.DataFrame):
        return df.sample(10).reset_index(drop=True)

    if not st.session_state:
        st.session_state['rand_movies'] = random_generator(df)

    left, middle, right = st.columns(3)
    if middle.button('Крутите барабан', icon="🎰", use_container_width=True):
        st.session_state['rand_movies'] = random_generator(df)

    output = st.session_state['rand_movies']

    row1 = st.columns(3)
    row2 = st.columns(4)
    row3 = st.columns(3)

    rows = row1 + row2 + row3

    for i, (col, (_, movie)) in enumerate(zip(rows, output.iterrows())):
        key = f"key_{i}"                                # Уникальный ключ для состояния

        if key not in st.session_state:
            st.session_state[key] = False

        expanded = st.session_state[key]
        height = 250 if expanded else 130
        tile = col.container(height=height)

        tile.subheader(f'🎬 {movie["Title"]}')

        def toggle_description(k=key):                   # Функция, изменяющая "состояние" кнопки
            st.session_state[k] = not st.session_state[k]

        tile.button(
            "🔍 Описание", 
            key=f"btn_{i}",                              # Отдельный ключ под кнопочку
            on_click=toggle_description
        )
        if expanded:
            tile.write(movie["Description"])