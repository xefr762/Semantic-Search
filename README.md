# Semantic-Search
Семантический поиск фильмов
https://...streamlit.app/...

## Описание
Разработать систему поиска фильма по пользовательскому запросу. Сервис должен принимать на вход описание фильма от пользователя и возвращать заданное количество подходящих вариантов.

Совет от LLM к просмотру фильма, возможность получать краткое содержание сюжета фильма (Sber GigaChat)

Случайные фильмы - возвращает случайные 10 позиций из csv-файла формате: название фильма – описание

## Структура проекта

(Основная структура на данный момент - будет докручиваться по мере дальнейшего развития проекта)

- **data/** - папка с данными парсинга и эмбедингами
- **images/** - папка с используемыми в streamlit иллюстрациями
- **notebooks/** - папка с кодом создания и настройки моделей
- **app_pages/** - папка со страницами для Streamlit
- **funcs/** - папка со вспомогательными функциями для Streamlit
- **main.py** - основной файл для запуска приложения Streamlit
- **README.md** - файл описания проекта
- **.gitignrore** - игнорируемые для загрузки файлы
- **requirements.txt** - файл с зависимостями для установки окружения

## Команда
 - [Нанзат](https://github.com/nanzat)
 - [Илья](https://github.com/xefr762)
 - [Миша](https://github.com/allspicepaege)

## Установка

1. Клонируйте репозиторий:

   git clone https://github.com/xefr762/Semantic-Search
   cd Semantic-Search

2. Создайте виртуальное окружение:

   python -m venv .myenv
   source .myenv/bin/activate


3. Установите необходимые зависимости:

   pip install -r requirements.txt


4. Установите Git LFS:

   git lfs install
   git lfs track '*.pt'

##  Использование

1. Запустите приложение Streamlit:

   streamlit run main.py
