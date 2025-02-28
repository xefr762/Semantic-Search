from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage

def ask_gigachat(user_message):
    # Инициализация GigaChat
    giga = GigaChat(
    model="GigaChat",  
    credentials="GigaChat API Key",
    verify_ssl_certs=False,
    temperature=0.7,
    MaxTokens=300,
    profanity_check=True
)
    
    # Создание списка сообщений
    messages = [
        {
            "role": "system", 
            "content": 'Ты эксперт по кинематографу. Рекомендуй только лучшие фильмы, под запрос пользователя. Отвечай коротко и лаконично в формате "Название" - короткое описание'
        },
        HumanMessage(
            content=user_message
        )
    ]
    
    # Получение ответа
    response = giga.invoke(messages)
    
    return response.content