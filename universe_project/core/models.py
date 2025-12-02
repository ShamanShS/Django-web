# core/models.py
from django.db import models
from django.contrib.auth.models import User

class FavoriteAnswer(models.Model):
    # Связь с пользователем, который добавил ответ в избранное.
    # Если пользователь удаляется, все его избранные ответы тоже удаляются.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Текст вопроса и ответа, которые мы сохраняем.
    question = models.TextField()
    answer = models.TextField()
    
    # Дата добавления.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Как будет отображаться объект в админке
        return f'"{self.question[:30]}..." by {self.user.username}'

    class Meta:
        # Сортируем по дате, чтобы новые были сверху
        ordering = ['-created_at']