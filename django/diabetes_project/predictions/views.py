import os
import json
import numpy as np
import joblib
import io
import random

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reportlab.lib import colors
import io
from reportlab.lib.utils import ImageReader


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from .models import UserProfile, PredictionHistory, PasswordResetCode
from .serializers import (
    PasswordResetRequestSerializer,
    UserSerializer, 
    UserProfileSerializer, 
    RegisterSerializer, 
    LoginSerializer,
    PredictionHistorySerializer,
    PasswordResetConfirmSerializer
)


# Загружаем модель и scaler
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "diabetes_model.pkl")
model, scaler = joblib.load(MODEL_PATH)

#Функция предсказания
class PredictionView(APIView):
    """
    Класс для предсказания диабета, получения истории предсказаний и скачивания PDF.
    """
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]  # Предсказание можно делать без регистрации
        return [IsAuthenticated()]  # История и скачивание PDF только для аутентифицированных пользователей

    def get(self, request):
        """
        Получение истории предсказаний или скачивание PDF, если передан параметр `download`.
        """
        if "download" in request.GET:
            return self.download_pdf(request)

        # Получаем историю предсказаний пользователя
        predictions = PredictionHistory.objects.filter(user=request.user).order_by("-created_at")
        serializer = PredictionHistorySerializer(predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Предсказание диабета и сохранение результата (если пользователь аутентифицирован).
        """
        try:
            data = json.loads(request.body)
            print(data, "Дата")
            print(data, "Дата")
            input_data = list(data.values())
            print(input_data, "Введенные данные")

            if len(input_data) != 8:
                return Response({"error": "Нужно передать 8 числовых значений."}, status=status.HTTP_400_BAD_REQUEST)

            # Преобразуем данные и масштабируем
            input_array = np.array(input_data).reshape(1, -1)
            input_array = scaler.transform(input_array)

            # Делаем предсказание
            prediction = model.predict(input_array)[0]
            probability = model.predict_proba(input_array)[0][1] * 100

            # Определяем результат
            result = "Есть риск диабета" if prediction == 1 else "Маленький риск диабета"
            print("Результат:", result)
            response_data = {
                "prediction": result,
                "probability": probability
            }
            print(f"Authenticated: {request.user.is_authenticated}, User: {request.user}")

            # Если пользователь аутентифицирован – сохраняем результат
            if request.user.is_authenticated:
                PredictionHistory.objects.create(
                    user=request.user,
                    pregnancies=input_data[0],
                    glucose=input_data[1],
                    blood_pressure=input_data[2],
                    skin_thickness=input_data[3],
                    insulin=input_data[4],
                    bmi=input_data[5],
                    diabetes_pedigree_function=input_data[6],
                    age=input_data[7],
                    prediction=result,
                    probability=probability
                )
                response_data["message"] = "Результат сохранен в вашем профиле."

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, prediction_id=None):
        """Удаление одного результата или всей истории"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Необходимо войти в систему"}, status=401)

        if prediction_id:
            # Удаляем конкретный результат
            try:
                prediction = PredictionHistory.objects.get(id=prediction_id, user=request.user)
                prediction.delete()
                return JsonResponse({"message": "Результат успешно удален"})
            except PredictionHistory.DoesNotExist:
                return JsonResponse({"error": "Результат не найден"}, status=404)
        else:
            # Удаляем всю историю пользователя
            PredictionHistory.objects.filter(user=request.user).delete()
            return JsonResponse({"message": "Вся история предсказаний удалена"})

class DownloadPredictionPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Скачивание истории предсказаний в PDF с графиком"""
        predictions = PredictionHistory.objects.filter(user=request.user).order_by('created_at')

        if not predictions.exists():
            return JsonResponse({"error": "У вас нет сохраненных предсказаний"}, status=404)

        # Регистрация русского шрифта
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("История предсказаний")

        pdf.setFont("DejaVuSans", 16)
        pdf.drawString(150, 750, "История предсказаний диабета")
        pdf.setFont("DejaVuSans", 12)

        # Отображение списка предсказаний
        y_position = 720
        dates = []
        probabilities = []

        for prediction in predictions:
            result = "Есть риск диабета" if prediction.prediction == 1 else "Маленький риск диабета"
            text = f"{prediction.created_at.strftime('%Y-%m-%d %H:%M')} | {result} ({prediction.probability:.2f}%)"
            pdf.drawString(100, y_position, text)

            # Сбор данных для графика
            dates.append(prediction.created_at.strftime('%Y-%m-%d'))
            probabilities.append(prediction.probability)

            y_position -= 20
            if y_position < 150:  # Оставляем место под график
                pdf.showPage()
                pdf.setFont("DejaVuSans", 12)
                y_position = 750

        # === ВАЖНО ===
        # Перед использованием matplotlib отключаем GUI backend
        # matplotlib.use('Agg') <- я уже добавил это вверху

        dates.append(prediction.created_at.strftime('%Y-%m-%d %H:%M'))
        probabilities.append(prediction.probability * 100)
        # Рисование графика
        plt.figure(figsize=(8, 3))
        plt.plot(dates, probabilities, marker='o', linestyle='-', color='blue')
        plt.xlabel('Дата и время')
        plt.ylabel('Риск (%)')
        plt.title('Изменение риска диабета со временем')
        plt.xticks(rotation=45)
        plt.ylim(0, 100)
        plt.grid(True)
        plt.tight_layout()

        # Сохраняем график в буфер
        graph_buffer = io.BytesIO()
        plt.savefig(graph_buffer, format='PNG')
        plt.close()
        graph_buffer.seek(0)

        # Вставляем график в PDF
        image = ImageReader(graph_buffer)
        pdf.drawImage(image, 100, 100, width=400, height=200)

        # Завершаем PDF
        pdf.save()
        buffer.seek(0)  # ОЧЕНЬ ВАЖНО: отматываем PDF буфер перед отправкой

        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="prediction_history.pdf"'
        return response


#Функция регистрации пользователя
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create the user using the serializer
            
            # Now create the profile for the user
            UserProfile.objects.create(user=user)  # Automatically create a profile
            
            return Response({"message": "User registered successfully!"}, status=201)
        
        return Response(serializer.errors, status=400)

#Функция входа по юзернейму и паролю
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Функция выхода
class LogoutView(APIView):
    permission_classes = [AllowAny]  # Можно вызвать без токена

    def post(self, request):
        return Response({"message": "Logged out successfully."}, status=200)

        
#Функция просмотра профиля пользователя
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Получение данных профиля"""
        try:
            profile = request.user.userprofile
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

    def put(self, request):
        """Обновление данных профиля"""
        try:
            profile = request.user.userprofile
            data = request.data.copy()

            # Приведение числовых полей к float
            for field in ["weight", "height"]:
                if field in data and data[field] != "":
                    try:
                        data[field] = float(data[field])
                    except ValueError:
                        return Response({field: "Должно быть числом"}, status=400)

            serializer = UserProfileSerializer(profile, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)

        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        
#Отправка кода на почту для сброса
class PasswordResetRequestView(APIView):
    """Генерация кода и отправка на почту"""

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = get_object_or_404(User, email=email)

            # Генерируем код
            code = f"{random.randint(100000, 999999)}"

            # Сохраняем в базе
            PasswordResetCode.objects.update_or_create(user=user, defaults={"code": code})

            # Отправляем код на почту
            send_mail(
                "Сброс пароля",
                f"Ваш код для сброса пароля: {code}",
                "diabetesprediction@gmail.com",
                [email],
                fail_silently=False,
            )

            return Response({"message": "Код отправлен на вашу почту."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Подтверждение кода и смена пароля
class PasswordResetConfirmView(APIView):
    """Подтверждение кода и смена пароля"""

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data["code"]
            new_password = serializer.validated_data["new_password"]

            user = get_object_or_404(User, email=email)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()

            if not reset_code or not reset_code.is_valid():
                return Response({"error": "Неверный или истекший код."}, status=status.HTTP_400_BAD_REQUEST)

            # Меняем пароль и удаляем код
            user.set_password(new_password)
            user.save()
            reset_code.delete()

            return Response({"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def send_test_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            recipient_email = data.get("email")  # Кому отправить письмо

            if not recipient_email:
                return JsonResponse({"error": "Укажите email получателя"}, status=400)

            # Отправляем письмо
            send_mail(
                subject="Тестовое письмо",  # Тема письма
                message="Привет! Это тестовое письмо из Django. 🎉",  # Сам текст
                from_email="muafikd@gmail.com",  # Твой email
                recipient_list=[recipient_email],  # Кому отправить
                fail_silently=False,
            )

            return JsonResponse({"message": f"Письмо отправлено на {recipient_email}"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Используйте POST-запрос"}, status=400)