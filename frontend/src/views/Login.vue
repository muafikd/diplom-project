<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../services/authService"; // Импортируем API

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);
const router = useRouter();

// Добавляем состояния для сброса пароля
const showResetForm = ref(false);
const resetEmail = ref("");
const resetCode = ref("");
const newPassword = ref("");
const resetMessage = ref("");
const isCodeSent = ref(false);

// Добавляем состояние для уведомлений
const notification = ref({
  show: false,
  message: '',
  type: 'success'
});

// Функция для показа уведомлений
const showNotification = (message, type = 'success') => {
  notification.value = {
    show: true,
    message,
    type
  };
  
  setTimeout(() => {
    notification.value.show = false;
  }, 3000);
};

const login = async () => {
    errorMessage.value = "";
    loading.value = true;

    try {
        const response = await api.post("login/", {
            email: email.value,
            password: password.value,
        });

        localStorage.setItem("access", response.data.access);
        localStorage.setItem("refresh", response.data.refresh);

        window.location.href = "/"; // Перезагружаем страницу для обновления состояния
    } catch (err) {
        errorMessage.value = err.response?.data?.detail || "Ошибка входа";
    } finally {
        loading.value = false;
    }
};

// Добавляем методы для сброса пароля
const requestPasswordReset = async () => {
    try {
        const response = await api.post("password-reset/request/", { email: resetEmail.value });
        resetMessage.value = "Код отправлен на почту.";
        isCodeSent.value = true;
        showNotification('Код отправлен на вашу почту');
    } catch (error) {
        resetMessage.value = error.response?.data?.detail || "Ошибка отправки кода";
        showNotification(error.response?.data?.detail || "Ошибка отправки кода", 'error');
    }
};

const confirmPasswordReset = async () => {
    try {
        await api.post("password-reset/confirm/", {
            email: resetEmail.value,
            code: resetCode.value,
            new_password: newPassword.value,
        });
        
        showResetForm.value = false;
        resetCode.value = '';
        newPassword.value = '';
        isCodeSent.value = false;
        showNotification('Пароль успешно изменен');
    } catch (error) {
        showNotification(error.response?.data?.detail || "Ошибка сброса пароля", 'error');
    }
};
</script>


<template>
    <div class="login-container">
        <!-- Добавляем компонент уведомления -->
        <transition name="notification">
            <div v-if="notification.show" 
                 class="notification" 
                 :class="notification.type">
                <i :class="notification.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                {{ notification.message }}
            </div>
        </transition>

        <div class="login-card">
            <div class="login-header">
                <i class="fas fa-user-circle"></i>
                <h1>Вход в систему</h1>
            </div>

            <form @submit.prevent="login" class="login-form">
                <transition name="fade">
                    <div v-if="errorMessage" class="alert error">
                        <i class="fas fa-exclamation-circle"></i>
                        {{ errorMessage }}
                    </div>
                </transition>

                <div class="input-group">
                    <label>
                        <i class="fas fa-envelope"></i>
                        Email
                    </label>
                    <input 
                        v-model="email" 
                        type="email" 
                        required
                        placeholder="Введите email"
                        :disabled="loading"
                    />
                </div>

                <div class="input-group">
                    <label>
                        <i class="fas fa-lock"></i>
                        Пароль
                    </label>
                    <input 
                        v-model="password" 
                        type="password" 
                        required
                        placeholder="Введите пароль"
                        :disabled="loading"
                    />
                </div>

                <button type="submit" :disabled="loading" class="submit-button">
                    <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-sign-in-alt'"></i>
                    {{ loading ? 'Вход...' : 'Войти' }}
                </button>

                <!-- Добавляем ссылку "Забыли пароль?" -->
                <div class="forgot-password">
                    <a href="#" @click.prevent="showResetForm = true">
                        <i class="fas fa-key"></i>
                        Забыли пароль?
                    </a>
                </div>
            </form>

            <div class="register-link">
                <p>
                    Нет аккаунта? 
                    <router-link to="/register">
                        Зарегистрируйтесь
                        <i class="fas fa-arrow-right"></i>
                    </router-link>
                </p>
            </div>
        </div>

        <!-- Добавляем модальное окно для сброса пароля -->
        <div v-if="showResetForm" class="modal">
            <div class="modal-content">
                <button @click="showResetForm = false" class="close-button">
                    <i class="fas fa-times"></i>
                </button>
                <div class="modal-header">
                    <i class="fas fa-key modal-icon"></i>
                    <h3>Сброс пароля</h3>
                </div>
                
                <div v-if="!isCodeSent" class="modal-body">
                    <div class="input-group">
                        <label>Email:</label>
                        <input v-model="resetEmail" type="email" placeholder="Введите ваш email" />
                    </div>
                    <div class="modal-buttons">
                        <button @click="requestPasswordReset" class="submit-button">
                            <i class="fas fa-paper-plane"></i> Отправить код
                        </button>
                        <button @click="showResetForm = false" class="cancel-button">
                            <i class="fas fa-times"></i> Отмена
                        </button>
                    </div>
                </div>

                <div v-else class="modal-body">
                    <div class="input-group">
                        <label>Код подтверждения:</label>
                        <input v-model="resetCode" type="text" placeholder="Введите код" />
                    </div>
                    <div class="input-group">
                        <label>Новый пароль:</label>
                        <input v-model="newPassword" type="password" placeholder="Введите новый пароль" />
                    </div>
                    <div class="modal-buttons">
                        <button @click="confirmPasswordReset" class="submit-button">
                            <i class="fas fa-check"></i> Подтвердить
                        </button>
                        <button @click="showResetForm = false" class="cancel-button">
                            <i class="fas fa-times"></i> Отмена
                        </button>
                    </div>
                </div>

                <p v-if="resetMessage" class="reset-message" :class="{ 'success': resetMessage.includes('успешно') }">
                    <i :class="resetMessage.includes('успешно') ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                    {{ resetMessage }}
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.login-container {
    min-height: 100vh;
    padding: 2rem;
    background-color: #f5f6fa;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-card {
    width: 100%;
    max-width: 400px;
    padding: 2rem;
    background: white;
    border-radius: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    animation: slideUp 0.5s ease;
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
    color: #2c3e50;
}

.login-header i {
    font-size: 4rem;
    color: #3498db;
    margin-bottom: 1rem;
}

.login-header h1 {
    font-size: 2rem;
    font-weight: 600;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.input-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.input-group label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #666;
    font-weight: 500;
}

.input-group label i {
    color: #3498db;
    width: 20px;
}

.input-group input {
    padding: 0.8rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.input-group input:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    outline: none;
}

.input-group input:disabled {
    background-color: #f8f9fa;
    cursor: not-allowed;
}

.submit-button {
    padding: 1rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
    transition: all 0.3s ease;
}

.submit-button:hover:not(:disabled) {
    background: #2980b9;
    transform: translateY(-2px);
}

.submit-button:disabled {
    background: #95a5a6;
    cursor: not-allowed;
}

.alert {
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    animation: shake 0.5s ease;
}

.alert.error {
    background: #fde8e8;
    color: #e74c3c;
    border-left: 4px solid #e74c3c;
}

.register-link {
    margin-top: 2rem;
    text-align: center;
    color: #666;
}

.register-link a {
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
}

.register-link a:hover {
    color: #2980b9;
    transform: translateX(5px);
}

/* Анимации */
@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@media (max-width: 768px) {
    .login-container {
        padding: 1rem;
    }

    .login-card {
        padding: 1.5rem;
    }

    .login-header h1 {
        font-size: 1.8rem;
    }
}

/* Добавляем стили для "Забыли пароль?" */
.forgot-password {
    text-align: center;
    margin-top: 1rem;
}

.forgot-password a {
    color: #3498db;
    text-decoration: none;
    font-size: 0.9rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
}

.forgot-password a:hover {
    color: #2980b9;
    transform: translateY(-2px);
}

/* Добавляем стили для уведомлений */
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-weight: 500;
    z-index: 2000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.notification.success {
    background: #edfbf3;
    color: #2ecc71;
    border-left: 4px solid #2ecc71;
}

.notification.error {
    background: #fde8e8;
    color: #e74c3c;
    border-left: 4px solid #e74c3c;
}

.notification i {
    font-size: 1.2rem;
}

/* Анимации для уведомлений */
.notification-enter-active,
.notification-leave-active {
    transition: all 0.3s ease;
}

.notification-enter-from {
    transform: translateX(100%);
    opacity: 0;
}

.notification-leave-to {
    transform: translateX(100%);
    opacity: 0;
}

/* Стили для модального окна */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    max-width: 400px;
    width: 90%;
    position: relative;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    animation: slideIn 0.3s ease;
}

.close-button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.2rem;
    color: #666;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.close-button:hover {
    background: #f8f9fa;
    color: #e74c3c;
    transform: rotate(90deg);
}

.modal-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}

.modal-header h3 {
    margin: 0;
    color: #2c3e50;
    font-size: 1.5rem;
}

.modal-icon {
    color: #3498db;
    font-size: 1.8rem;
}

.modal-body {
    margin-bottom: 1.5rem;
}

.modal-body .input-group {
    margin-bottom: 1rem;
}

.modal-body input {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-size: 1rem;
}

.modal-body input:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    outline: none;
}

.modal-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 1.5rem;
}

.modal-buttons button {
    min-width: 140px;
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.modal-buttons .submit-button {
    background: #2ecc71;
    color: white;
}

.modal-buttons .submit-button:hover {
    background: #27ae60;
    transform: translateY(-2px);
}

.modal-buttons .cancel-button {
    background: #95a5a6;
    color: white;
}

.modal-buttons .cancel-button:hover {
    background: #7f8c8d;
    transform: translateY(-2px);
}

.reset-message {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background: #fde8e8;
    color: #e74c3c;
    animation: slideUp 0.3s ease;
}

.reset-message.success {
    background: #edfbf3;
    color: #2ecc71;
}

.reset-message i {
    font-size: 1.2rem;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from {
        transform: translateY(-20px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@keyframes slideUp {
    from {
        transform: translateY(10px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

/* Медиа-запросы для мобильной адаптации */
@media (max-width: 768px) {
    .modal-content {
        width: 95%;
        padding: 1.5rem;
    }

    .modal-header h3 {
        font-size: 1.3rem;
    }

    .modal-buttons {
        flex-direction: column;
    }

    .modal-buttons button {
        width: 100%;
    }
}

@media (max-width: 480px) {
    .modal-content {
        padding: 1.2rem;
    }

    .modal-header h3 {
        font-size: 1.2rem;
    }

    .modal-body input {
        padding: 0.7rem;
        font-size: 0.9rem;
    }

    .modal-buttons button {
        padding: 0.7rem;
        font-size: 0.9rem;
    }
}
</style>
