import re
import pandas as pd
import numpy as np
from sentence_transformers import util
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
tqdm.pandas()
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import streamlit as st
import spacy
import pymorphy3

if torch.cuda.is_available():
    print("CUDA доступна!")
    device = torch.device("cuda")
else:
    print("CUDA недоступна. Вычисления будут выполняться на CPU.")
    device = torch.device("cpu")

max_length = 512
@st.cache_data
def load_models():
    # Создание объекта для морфологического анализа
    morph = pymorphy3.MorphAnalyzer()
    # Загрузка модели spaCy для русского языка
    nlp = spacy.load("ru_core_news_lg")
    return nlp, morph

def get_df():
    df = pd.read_csv('/home/marena/Elbrus_phase_2/Semantic-Search/data/movie_data.csv')
    df['all_text'] = df.apply(lambda row: f"{row['title']} {row['genre']} {row['director']} {row['actors']} {row['description']}", axis=1)
    df['all_text'][0]
    return df

@st.cache_data
def autobot():
    model = AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').to(device).half()
    return model
@st.cache_data
def token():
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', truncation=True, max_length=max_length)
    return tokenizer

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

@st.cache_data
def get_sentence_embedding(text):
    tokenizer = token()
    model = autobot()
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(device)
    with torch.amp.autocast('cuda'):
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = mean_pooling(outputs, inputs['attention_mask']).cpu().numpy()[0] # Удаление лишней размерности [0]
    return embeddings

@st.cache_data
def get_embs():
    with open('/home/marena/Elbrus_phase_2/Semantic-Search/data/embeddings', 'rb') as file:
        embeddings = pickle.load(file)
    return embeddings

def search_movie(query, top_k=8, year=None):
    query_embedding = get_sentence_embedding(query)
    embeddings = get_embs()
    df = get_df()
    cos_scores = torch.nn.functional.cosine_similarity(torch.tensor(query_embedding), torch.tensor(embeddings))
    df['similarity'] = cos_scores.tolist()
    res = df.sort_values(by='similarity', ascending=False)
    if year:
        res = res[res['year'] == year]
    return res.head(top_k)




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
