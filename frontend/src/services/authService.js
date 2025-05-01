import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/";
const REFRESH_URL = `${API_URL}token/refresh/`;

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// Создаем EventEmitter для уведомлений об аутентификации
export const authEvents = new EventTarget();

// Функция для обновления токена
export const refreshToken = async () => {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) {
        authEvents.dispatchEvent(new CustomEvent('session-expired', {
            detail: 'Сессия истекла. Пожалуйста, войдите снова.'
        }));
        throw new Error("Refresh token отсутствует");
    }

    try {
        const response = await axios.post(REFRESH_URL, { refresh });
        localStorage.setItem("access", response.data.access);
        return response.data.access;
    } catch (error) {
        console.error("Ошибка обновления токена:", error);
        authEvents.dispatchEvent(new CustomEvent('session-expired', {
            detail: 'Ваша сессия истекла. Необходима повторная авторизация.'
        }));
        logoutUser();
        throw error;
    }
};

// Функция для проверки срока действия токена
export const isTokenExpired = (token) => {
    if (!token) return true;
    try {
        const tokenData = JSON.parse(atob(token.split(".")[1]));
        const expTime = tokenData.exp * 1000;
        const currentTime = Date.now();
        return currentTime >= expTime;
    } catch {
        return true;
    }
};

// Функция, проверяющая и обновляющая токен при необходимости
export const refreshTokenIfNeeded = async () => {
    const token = localStorage.getItem("access");
    if (!token) return;

    try {
        const tokenData = JSON.parse(atob(token.split(".")[1]));
        const expTime = tokenData.exp * 1000;
        const currentTime = Date.now();

        // Обновляем токен за 5 минут до истечения
        if (currentTime >= expTime - 300000) {
            const newAccessToken = await refreshToken();
            api.defaults.headers["Authorization"] = `Bearer ${newAccessToken}`;
            return newAccessToken;
        }
    } catch (error) {
        console.error("Ошибка при проверке токена:", error);
        authEvents.dispatchEvent(new CustomEvent('session-expired', {
            detail: 'Произошла ошибка аутентификации. Пожалуйста, войдите снова.'
        }));
        logoutUser();
    }
};

// Функция выхода пользователя
export const logoutUser = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    delete api.defaults.headers["Authorization"];
    window.location.href = "/login";
};

// Интерцептор для запросов
api.interceptors.request.use(async (config) => {
    let token = localStorage.getItem("access");

    if (token && isTokenExpired(token)) {
        try {
            token = await refreshToken();
        } catch (error) {
            return Promise.reject(error);
        }
    }

    if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
});

// Интерцептор для ответов
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Если получили 401 и это не запрос на обновление токена
        if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('token/refresh')) {
            originalRequest._retry = true;

            try {
                const token = await refreshToken();
                originalRequest.headers["Authorization"] = `Bearer ${token}`;
                return api(originalRequest);
            } catch (refreshError) {
                authEvents.dispatchEvent(new CustomEvent('session-expired', {
                    detail: 'Сессия истекла. Пожалуйста, войдите снова.'
                }));
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

