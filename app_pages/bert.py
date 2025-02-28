import streamlit as st
import pandas as pd
import numpy as np
import pickle

from funcs.preproc import *

def run():

    st.subheader('Подбор фильма по запросу, но с секретом!')
    nlp, morph = load_models()
    user_text = st.text_input('Введите запрос на желаемый фильм')

    def display_movie_card(row):
            st.markdown(
                f"""
                **{row['title']}**\n
                *Описание:* {row['description']}\n
                *Год:* {row['year']}\n
                *Актеры:* {row['actors']}\n
                *Сходство:* {row['similarity']:.4f}\n
                {"----------"}
                """
            )

    left, middle, right = st.columns(3)
    if middle.button('Получить топ фильмов по-моему запросу', icon="👀", use_container_width=True):
        if user_text:  # Проверяем, что поле ввода не пустое
            result = search_movie(user_text)
            output = sort_by_entities(result, user_text, morph, nlp)
            output = output[['title', 'year', 'actors', 'description', 'similarity']]
        #st.write('Предлагаю посмотреть вам следующие фильмы:')
        #for index, rows in output.iterrows():
        #    st.write(rows)
            for index, row in output.iterrows():
                display_movie_card(row)

        else:
            st.warning("Пожалуйста, введите свой запрос на фильм.")
