# core/views.py
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote # для декодирования URL
from .gemini_utils import generate_content
from django.http import JsonResponse
from .models import FavoriteAnswer



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')

@login_required
def questions_page_view(request):
    return render(request, 'questions.html')

@login_required
def questions_loading_view(request):
    return render(request, 'questions_loading.html')


@login_required
def questions_view(request):
    prompt = "Придумай 3 очень смешных вопроса о Китайцах. Ответь только списком вопросов, без лишних слов. Каждый вопрос на новой строке."
    generated_text = generate_content(prompt)
    questions_list = [q.strip() for q in generated_text.split('\n') if q.strip()]
    questions_list = [q.split('. ', 1)[-1] for q in questions_list]

    return render(request, 'questions.html', {'questions': questions_list})

@login_required
def answer_loading_view(request):
    question = request.GET.get('q', '')
    return render(request, 'answer_loading.html', {'question': question})



@login_required
def answer_view(request):
    question = request.GET.get('q', '')  
    if not question:
        return redirect('questions')
    question_decoded = unquote(question)
    prompt = f"Дай короткий, абсурдный и смешной ответ на следующий вопрос: '{question_decoded}'"
    
    answer_text = generate_content(prompt)
    
    context = {
        'question': question_decoded,
        'answer': answer_text,
    }
    return render(request, 'answer.html', context)




@login_required
def favorites_list_view(request):

    favorites = FavoriteAnswer.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})


@login_required
def add_to_favorites_view(request):
   
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        
 
        if question and answer:
            FavoriteAnswer.objects.create(
                user=request.user,
                question=question,
                answer=answer
            )
      
        return redirect('favorites_list')

    return redirect('home')


@login_required
def remove_from_favorites_view(request, pk):
    favorite = get_object_or_404(FavoriteAnswer, pk=pk)
    if favorite.user == request.user and request.method == 'POST':
        favorite.delete()
        return redirect('favorites_list')
        
    return redirect('favorites_list') 