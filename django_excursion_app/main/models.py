from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField("Возраст")

    def clean(self):
        if self.age < 18 or self.age > 100:
            raise ValidationError("Возраст должен быть от 18 до 100 лет.")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (ID: {self.user.id}, Возраст: {self.age})"

class Route(models.Model):
    title = models.CharField("Название маршрута", max_length=200)
    description = models.TextField("Описание")
    length_km = models.PositiveIntegerField("Длина (км)")

    def __str__(self):
        return self.title
    
    
class Excursion(models.Model):
    title = models.CharField("Название экскурсии", max_length=200)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='excursions', verbose_name="Маршрут")
    price = models.DecimalField("Цена (руб.)", max_digits=8, decimal_places=2)
    min_age = models.PositiveIntegerField("Мин. возраст", default=18)
    max_age = models.PositiveIntegerField("Макс. возраст", default=80)
    max_persons = models.PositiveIntegerField("Макс. участников", default=10)

    def clean(self):
        if self.max_age < self.min_age:
            raise ValidationError("Максимальный возраст не может быть меньше минимального.")

    def __str__(self):
        return f"{self.title} ({self.route.title})"
    
    
class Group(models.Model):
    excursion = models.OneToOneField(Excursion, on_delete=models.CASCADE, related_name='group', verbose_name="Экскурсия")
    participants = models.ManyToManyField(User, related_name='joined_excursions', blank=True, verbose_name="Участники")

    def __str__(self):
        return f"Группа экскурсии: {self.excursion.title}"