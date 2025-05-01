<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../services/authService"; // Импортируем API

const username = ref("");
const email = ref("");
const password = ref("");
const passwordConfirm = ref("");
const errorMessage = ref("");
const loading = ref(false);
const notification = ref({
    show: false,
    message: '',
    type: 'success'
});
const router = useRouter();

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

const register = async () => {
    errorMessage.value = "";
    loading.value = true;

    if (password.value !== passwordConfirm.value) {
        errorMessage.value = "Пароли не совпадают";
        loading.value = false;
        return;
    }

    try {
        await api.post("register/", {
            username: username.value,
            email: email.value,
            password: password.value,
        });

        showNotification("Регистрация успешна! Сейчас вы будете перенаправлены на страницу входа.");
        setTimeout(() => {
            router.push("/login");
        }, 2000);
    } catch (err) {
        errorMessage.value = err.response?.data?.detail || "Ошибка регистрации";
        showNotification(errorMessage.value, 'error');
    } finally {
        loading.value = false;
    }
};
</script>


<template>
    <div class="register-container">
        <!-- Уведомление -->
        <transition name="notification">
            <div v-if="notification.show" 
                 class="notification" 
                 :class="notification.type">
                <i :class="notification.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                {{ notification.message }}
            </div>
        </transition>

        <div class="register-card">
            <div class="register-header">
                <i class="fas fa-user-plus"></i>
                <h1>Регистрация</h1>
            </div>

            <form @submit.prevent="register" class="register-form">
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
                        <i class="fas fa-user"></i>
                        Имя пользователя
                    </label>
                    <input 
                        v-model="username" 
                        type="text" 
                        required
                        placeholder="Введите имя пользователя"
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

                <div class="input-group">
                    <label>
                        <i class="fas fa-lock"></i>
                        Подтверждение пароля
                    </label>
                    <input 
                        v-model="passwordConfirm" 
                        type="password" 
                        required
                        placeholder="Повторите пароль"
                        :disabled="loading"
                    />
                </div>

                <button type="submit" :disabled="loading" class="submit-button">
                    <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-user-plus'"></i>
                    {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
                </button>
            </form>

            <div class="login-link">
                <p>
                    Уже есть аккаунт? 
                    <router-link to="/login">
                        Войдите
                        <i class="fas fa-arrow-right"></i>
                    </router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.register-container {
    min-height: 100vh;
    padding: 2rem;
    background-color: #f5f6fa;
    display: flex;
    align-items: center;
    justify-content: center;
}

.register-card {
    width: 100%;
    max-width: 400px;
    padding: 2rem;
    background: white;
    border-radius: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    animation: slideUp 0.5s ease;
}

.register-header {
    text-align: center;
    margin-bottom: 2rem;
    color: #2c3e50;
}

.register-header i {
    font-size: 4rem;
    color: #3498db;
    margin-bottom: 1rem;
}

.register-header h1 {
    font-size: 2rem;
    font-weight: 600;
}

.register-form {
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

.login-link {
    margin-top: 2rem;
    text-align: center;
    color: #666;
}

.login-link a {
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
}

.login-link a:hover {
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

.notification-enter-active,
.notification-leave-active {
    transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
    transform: translateX(100%);
    opacity: 0;
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
    .register-container {
        padding: 1rem;
    }

    .register-card {
        padding: 1.5rem;
    }

    .register-header h1 {
        font-size: 1.8rem;
    }
}
</style>