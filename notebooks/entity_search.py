import pandas as pd
import streamlit as st
import spacy
import pymorphy3


@st.cache_data
def load_models():
    # Создание объекта для морфологического анализа
    morph = pymorphy3.MorphAnalyzer()
    # Загрузка модели spaCy для русского языка
    nlp = spacy.load("ru_core_news_lg")
    return nlp, morph


def sort_by_entities(df: pd.DataFrame, text: str, morph: pymorphy3.analyzer.MorphAnalyzer, nlp):
    genres = {'аниме',
              'биография',
              'боевик',
              'вестерн',
              'военный',
              'детектив',
              'детский',
              'документальный',
              'драма',
              'исторический',
              'комедия',
              'короткометражный',
              'криминал',
              'мелодрама',
              'музыкальный',
              'мультфильмы',
              'мюзикл',
              'приключения',
              'семейный',
              'спорт',
              'триллер',
              'ужасы',
              'фантастика',
              'фэнтези',
              'эротика'}
    # Обработка текста
    doc = nlp(text)

    # Извлечение сущностей
    entities = [entity.text for entity in doc.ents if entity.label_ == "PER"]

    persons = []
    for entity in entities:
        persons.append(" ".join([morph.parse(person)[0].normal_form for person in entity.split()]))

    conditions = []
    for person in persons:
        for word in person.split(" "):
            if len(word) > 3:
                word = word[:-1]
            conditions.append(df["actors"].str.contains(word, na=False, case=False))
            conditions.append(df["director"].str.contains(word, na=False, case=False))

    combined_condition = pd.Series([False] * len(df), index=df.index)
    if len(conditions) > 1:
        combined_condition = conditions[0]
        for condition in conditions[1:]:
            combined_condition |= condition

    search_genre = []
    for genre in genres:
        if genre in text.lower():
            search_genre.append(df[genre] == 1)

    if len(search_genre) > 0:
        for condition in search_genre:
            combined_condition |= condition

    if len(search_genre) + len(persons) > 0:
        filtered = pd.concat([df[combined_condition], df[~combined_condition]])
    else:
        filtered = df
    return filtered
