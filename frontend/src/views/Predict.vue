<script setup>
import { ref, onMounted, watchEffect } from "vue";
import { api, refreshTokenIfNeeded } from "../services/authService";
import ModelInfo from '../components/ModelInfo.vue';

// Данные профиля
const profile = ref(null);

// Данные формы
const formData = ref({
    pregnancies: "",
    glucose: "",
    blood_pressure: "",
    skin_thickness: "",
    insulin: "",
    bmi: "",
    diabetes_pedigree_function: "",
    age: "",
});

const fieldLabels = {
    pregnancies: "Количество беременностей",
    glucose: "Уровень глюкозы (мг/дл)",
    blood_pressure: "Давление (мм рт. ст.)",
    skin_thickness: "Толщина кожной складки (мм)",
    insulin: "Уровень инсулина (мкЕд/мл)",
    bmi: "Индекс массы тела (BMI)",
    diabetes_pedigree_function: "Наследственность диабета",
    age: "Возраст (лет)",
};

const tooltips = {
    pregnancies: "Количество беременностей у женщины. У мужчин — 0.",
    glucose: "Концентрация глюкозы в крови натощак.",
    blood_pressure: "Диастолическое артериальное давление.",
    skin_thickness: "Толщина кожной складки в районе трицепса.",
    insulin: "Уровень инсулина в крови после еды.",
    bmi: "Показатель массы тела, рассчитывается как вес (кг) / рост² (м²).",
    diabetes_pedigree_function: "Вероятность диабета на основе генетики.",
    age: "Возраст пациента.",
};

const result = ref(null);
const probability = ref(null);
const message = ref(null);
const loading = ref(false);
const error = ref(null);
const showTooltip = ref(null);

// Функция вычисления возраста
const calculateAge = (birthDate) => {
    if (!birthDate) return "";
    const birthYear = new Date(birthDate).getFullYear();
    const currentYear = new Date().getFullYear();
    return currentYear - birthYear;
};

// Функция расчета ИМТ
const calculateBMI = (weight, height) => {
    if (!weight || !height) return "";
    return (parseFloat(weight) / ((parseFloat(height) / 100) ** 2)).toFixed(2);
};

// Функция проверки авторизации
const isAuthenticated = () => {
    return !!localStorage.getItem("access");
};

// Загрузка профиля
const fetchProfile = async () => {
    if (!isAuthenticated()) {
        return; // Если пользователь не авторизован, не загружаем профиль
    }

    try {
        await refreshTokenIfNeeded();
        const response = await api.get("profile/");
        profile.value = response.data;
        
        // Автоматическое заполнение полей только для авторизованных пользователей
        formData.value.age = calculateAge(profile.value.date_of_birth);
        formData.value.bmi = calculateBMI(profile.value.weight, profile.value.height);
        formData.value.pregnancies = profile.value.gender === "male" ? 0 : "";
    } catch (err) {
        console.error("Ошибка загрузки профиля:", err);
    }
};

// Отправка предсказания
const predictDiabetes = async () => {
    loading.value = true;
    error.value = null;

    try {
        const response = await api.post("predict/", {
            pregnancies: Number(formData.value.pregnancies),
            glucose: Number(formData.value.glucose),
            blood_pressure: Number(formData.value.blood_pressure),
            skin_thickness: Number(formData.value.skin_thickness),
            insulin: Number(formData.value.insulin),
            bmi: Number(formData.value.bmi),
            diabetes_pedigree_function: Number(formData.value.diabetes_pedigree_function),
            age: Number(formData.value.age)
        });

        result.value = response.data.prediction;
        probability.value = response.data.probability;
        
        // Определяем сообщение в зависимости от вероятности
        if (probability.value >= 70) {
            message.value = `<span class="high-risk">⚠️ Срочно проконсультируйтесь с врачом! У вас высокий риск развития диабета.</span>`;
        } else if (probability.value >= 30) {
            message.value = `<span class="medium-risk">
                ⚠️ У вас повышенный риск развития диабета. 
                <router-link to="/prevention">Узнайте больше о профилактике диабета</router-link>
            </span>`;
        } else {
            message.value = `<span class="low-risk">✅ У вас низкий риск развития диабета. Продолжайте вести здоровый образ жизни!</span>`;
        }
    } catch (err) {
        error.value = "Ошибка предсказания. Попробуйте снова.";
        console.error(err);
    } finally {
        loading.value = false;
    }
};

// Загружаем профиль при монтировании компонента
onMounted(() => {
    fetchProfile();
});

// Следим за изменением пола
watchEffect(() => {
    if (profile.value?.gender === 'male') {
        formData.value.pregnancies = 0;
    }
});
</script>

<template>
    <div class="predict-container">
        <div class="predict-card">
            <h1 class="title">
                <i class="fas fa-chart-line"></i>
                Предсказание диабета
            </h1>

            <!-- Добавляем компонент с информацией о модели -->
            <ModelInfo class="model-info-wrapper" />

            <form @submit.prevent="predictDiabetes" class="predict-form">
                <div class="form-grid">
                    <div v-for="(label, key) in fieldLabels" 
                         :key="key" 
                         class="input-group">
                        <label>
                            {{ label }}
                            <span class="tooltip-trigger" 
                                  @mouseover="showTooltip = key" 
                                  @mouseleave="showTooltip = null">
                                <i class="fas fa-question-circle"></i>
                            </span>
                        </label>
                        <input 
                            v-model="formData[key]" 
                            type="number" 
                            step="any" 
                            required 
                            :disabled="
                                (key === 'pregnancies' && profile?.gender === 'male') || 
                                (isAuthenticated() && (key === 'age' || key === 'bmi'))
                            "
                        />
                        <transition name="tooltip">
                            <div v-if="showTooltip === key" class="tooltip">
                                {{ tooltips[key] }}
                            </div>
                        </transition>
                    </div>
                </div>

                <button type="submit" :disabled="loading" class="submit-button">
                    <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-calculator'"></i>
                    {{ loading ? 'Обработка...' : 'Рассчитать риск' }}
                </button>
            </form>

            <transition name="fade">
                <div v-if="error" class="alert error">
                    <i class="fas fa-exclamation-circle"></i>
                    {{ error }}
                </div>
            </transition>

            <transition name="slide-fade">
                <div v-if="result" class="result-card">
                    <h2>Результат анализа</h2>
                    <div class="result-content">
                        <div class="prediction">
                            <span class="prediction-label">Заключение:</span>
                            <span class="prediction-value">{{ result }}</span>
                        </div>
                        <div class="probability">
                            <span class="probability-label">Вероятность:</span>
                            <div class="probability-wrapper">
                                <div class="probability-bar">
                                    <div class="probability-fill" :style="{ width: probability + '%' }"></div>
                                </div>
                                <span class="probability-text">{{ probability?.toFixed(2) }}%</span>
                            </div>
                        </div>
                        <p v-if="message" class="message" v-html="message"></p>
                    </div>
                </div>
            </transition>

            <!-- Добавим информационное сообщение для неавторизованных пользователей -->
            <div v-if="!isAuthenticated()" class="guest-info">
                <i class="fas fa-info-circle"></i>
                <p>Вы используете сервис без авторизации. Для сохранения истории предсказаний и автоматического заполнения данных, пожалуйста, 
                    <router-link to="/login">войдите</router-link> 
                    или 
                    <router-link to="/register">зарегистрируйтесь</router-link>.
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.predict-container {
    min-height: 100vh;
    padding: 2rem;
    background-color: #f5f6fa;
}

.predict-card {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
    color: #2c3e50;
    font-size: 2.2rem;
    margin-bottom: 2rem;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

.title i {
    color: #3498db;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.input-group {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.input-group label {
    color: #666;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.tooltip-trigger {
    cursor: pointer;
    color: #3498db;
    transition: color 0.3s ease;
}

.tooltip-trigger:hover {
    color: #2980b9;
}

.input-group input {
    padding: 0.8rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-size: 1rem;
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

.tooltip {
    position: absolute;
    top: 100%;
    left: 0;
    background: #2c3e50;
    color: white;
    padding: 0.8rem;
    border-radius: 8px;
    font-size: 0.9rem;
    width: 250px;
    z-index: 1000;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.submit-button {
    width: 100%;
    padding: 1rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 500;
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
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.alert.error {
    background: #fde8e8;
    color: #e74c3c;
    border-left: 4px solid #e74c3c;
}

.result-card {
    margin-top: 2rem;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-card h2 {
    color: #2c3e50;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.result-content {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.prediction, .probability {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.prediction-label, .probability-label {
    min-width: 120px;
    color: #666;
    font-weight: 500;
}

.prediction-value {
    font-weight: 600;
    color: #2c3e50;
}

.probability-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.probability-bar {
    flex: 1;
    height: 12px;
    background: #e0e0e0;
    border-radius: 6px;
    overflow: hidden;
}

.probability-fill {
    height: 100%;
    background: linear-gradient(90deg, #3498db, #2980b9);
    transition: width 0.6s ease;
}

.probability-text {
    min-width: 70px;
    font-weight: 600;
    color: #2c3e50;
}

.message {
    color: #666;
    font-style: normal;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 1rem;
    background: #fff;
    border-radius: 8px;
    margin-top: 1rem;
}

.message .high-risk {
    color: #e74c3c;
    font-weight: 600;
}

.message .medium-risk {
    color: #f39c12;
    font-weight: 500;
}

.message .medium-risk a {
    color: #3498db;
    text-decoration: none;
    border-bottom: 1px dashed #3498db;
}

.message .medium-risk a:hover {
    color: #2980b9;
    border-bottom-style: solid;
}

.message .low-risk {
    color: #27ae60;
    font-weight: 500;
}

/* Анимации */
.tooltip-enter-active,
.tooltip-leave-active {
    transition: all 0.3s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.slide-fade-enter-active {
    transition: all 0.3s ease;
}

.slide-fade-leave-active {
    transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    transform: translateY(20px);
    opacity: 0;
}

@media (max-width: 768px) {
    .predict-container {
        padding: 1rem;
    }

    .predict-card {
        padding: 1.5rem;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

    .title {
        font-size: 1.8rem;
    }

    .tooltip {
        width: 200px;
    }
}

.guest-info {
    margin-top: 1.5rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #3498db;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.guest-info i {
    color: #3498db;
    margin-top: 0.2rem;
}

.guest-info p {
    margin: 0;
    color: #666;
    line-height: 1.5;
}

.guest-info a {
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
}

.guest-info a:hover {
    text-decoration: underline;
}

.model-info-wrapper {
    margin-bottom: 2rem;
}
</style>
