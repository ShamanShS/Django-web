# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote # для декодирования URL
from .gemini_utils import generate_content
from django.http import JsonResponse

# (здесь позже будет код для Gemini)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Сразу логиним пользователя после регистрации
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Остальные views добавим позже
def home_view(request):
    return render(request, 'home.html')

@login_required
def questions_page_view(request):
    """Просто отображает страницу с анимацией загрузки."""
    return render(request, 'questions.html')

@login_required
def get_questions_api(request):
    """
    API-эндпоинт: вызывает Gemini, получает вопросы 
    и возвращает их в формате JSON.
    """
    prompt = "Придумай 3 очень смешных вопроса о Гитлере. Ответь только списком вопросов, без лишних слов. Каждый вопрос на новой строке."
    generated_text = generate_content(prompt)
    

    questions_list = [q.strip() for q in generated_text.split('\n') if q.strip()]
    questions_list = [q.split('. ', 1)[-1] for q in questions_list]

    # Возвращаем данные в формате JSON
    return JsonResponse({'questions': questions_list})

@login_required
def questions_view(request):
    # Промпт для генерации вопросов
    prompt = "Придумай 3 очень смешных вопроса о Гитлере. Ответь только списком вопросов, без лишних слов. Каждый вопрос на новой строке."
    
    generated_text = generate_content(prompt)
    
    # Разделяем текст на отдельные вопросы
    questions_list = [q.strip() for q in generated_text.split('\n') if q.strip()]
    
    # Убираем возможную нумерацию типа "1. "
    questions_list = [q.split('. ', 1)[-1] for q in questions_list]

    return render(request, 'questions.html', {'questions': questions_list})

@login_required
def answer_loading_view(request):
    # Получаем вопрос из GET-параметра, чтобы передать его дальше
    question = request.GET.get('q', '')
    # Эта view ничего не вычисляет, просто рендерит шаблон
    return render(request, 'answer_loading.html', {'question': question})



@login_required
def answer_view(request):
    # Получаем вопрос из GET-параметра
    question = request.GET.get('q', '')
    
    if not question:
        return redirect('questions')
        
    # Декодируем вопрос, если в нем были спецсимволы
    question_decoded = unquote(question)

    # Промпт для генерации ответа
    prompt = f"Дай короткий, абсурдный и смешной ответ на следующий вопрос: '{question_decoded}'"
    
    answer_text = generate_content(prompt)
    
    context = {
        'question': question_decoded,
        'answer': answer_text,
    }
    return render(request, 'answer.html', context)