from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

#Модель юзера
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("male", "Мужской"),
        ("female", "Женский"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)  # Вес (кг)
    height = models.FloatField(null=True, blank=True)  # Рост (м)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)  # Пол

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        """Вычисляем возраст на основе даты рождения"""
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    @property
    def bmi(self):
        """Вычисляем ИМТ (индекс массы тела)"""
        if self.weight and self.height:
            return round(self.weight / (self.height ** 2), 2)
        return None


#Модель результатов пользователя
class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Может быть null для анонимных
    pregnancies = models.IntegerField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree_function = models.FloatField()
    age = models.IntegerField()
    prediction = models.CharField(max_length=50)  # Увеличиваем размер поля
    probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи

    def __str__(self):
        return f"Prediction for {self.user.username if self.user else 'Anonymous'} - {self.prediction}"
    
#Модель сброса пароля по почте
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Код действителен в течение 10 минут"""
        return (now() - self.created_at).seconds < 600