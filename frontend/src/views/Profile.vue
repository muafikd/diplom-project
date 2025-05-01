<script setup>
import { ref, computed, onMounted} from "vue";
import { api, refreshTokenIfNeeded } from "../services/authService"; // Импорт API

const profile = ref({
  username: "",
  date_of_birth: "",
  weight: "",
  height: "",
  gender: "",
});
const isEditing = ref(false);
const errorMessage = ref("");

// 🔹 Автоматический расчет ИМТ
const bmi = computed(() => {
  const weight = parseFloat(profile.value.weight);
  const height = parseFloat(profile.value.height) / 100; // Перевод в метры
  return weight && height ? (weight / (height * height)).toFixed(2) : "Не рассчитан";
});

// 🔹 Поля для сброса пароля
const showResetForm = ref(false);
const email = ref("");
const resetCode = ref("");
const newPassword = ref("");
const resetMessage = ref("");
const isCodeSent = ref(false);

// 🔹 История предсказаний
const predictions = ref([]);
const showConfirmation = ref(false);
const predictionToDelete = ref(null);

// Добавим состояние для уведомлений
const notification = ref({
  show: false,
  message: '',
  type: 'success' // или 'error'
});

// Функция для показа уведомлений
const showNotification = (message, type = 'success') => {
  notification.value = {
    show: true,
    message,
    type
  };
  
  // Скрываем уведомление через 3 секунды
  setTimeout(() => {
    notification.value.show = false;
  }, 3000);
};

// 🟢 Получаем профиль
const fetchProfile = async () => {
  try {
    await refreshTokenIfNeeded();
    const response = await api.get("profile/");
    profile.value = response.data;
    email.value = response.data.email; // Заполняем email для формы сброса пароля
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "Ошибка загрузки профиля";
  }
};

// 🔹 Получаем историю предсказаний
const fetchPredictions = async () => {
  try {
    await refreshTokenIfNeeded();
    const response = await api.get("predict/");
    predictions.value = response.data;
  } catch (error) {
    console.error("Ошибка:", error);
  }
};

// 🔴 Удаление предсказания
const confirmDelete = (predictionId) => {
  showConfirmation.value = true;
  predictionToDelete.value = predictionId;
};

const deletePrediction = async () => {
  if (!predictionToDelete.value) return;

  try {
    await refreshTokenIfNeeded();
    await api.delete(`predict/${predictionToDelete.value}/`);
    predictions.value = predictions.value.filter((p) => p.id !== predictionToDelete.value);
    showConfirmation.value = false;
    predictionToDelete.value = null;
    showNotification('Запись успешно удалена');
  } catch (error) {
    console.error("Ошибка:", error);
    showNotification('Ошибка при удалении записи', 'error');
  }
};

// 🟢 Обновление профиля
const updateProfile = async () => {
  try {
    await refreshTokenIfNeeded();
    await api.put("profile/", profile.value);
    isEditing.value = false;
    showNotification('Профиль успешно обновлен');
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "Ошибка обновления профиля";
    showNotification('Ошибка при обновлении профиля', 'error');
  }
};

// 🔹 Отправка кода на почту
const requestPasswordReset = async () => {
  try {
    await refreshTokenIfNeeded();
    const response = await api.post("password-reset/request/", { email: email.value });
    resetMessage.value = "Код отправлен на почту.";
    isCodeSent.value = true;
  } catch (error) {
    resetMessage.value = error.response?.data?.detail || "Ошибка отправки кода";
  }
};

// 🔹 Подтверждение кода и смена пароля
const confirmPasswordReset = async () => {
  try {
    await refreshTokenIfNeeded();
    await api.post("password-reset/confirm/", {
      email: email.value,
      code: resetCode.value,
      new_password: newPassword.value,
    });
    
    showResetForm.value = false;
    resetCode.value = '';
    newPassword.value = '';
    isCodeSent.value = false;
    showNotification('Пароль успешно изменен');
  } catch (error) {
    console.error("Ошибка сброса пароля:", error.response?.data);
    showNotification(error.response?.data?.detail || "Ошибка сброса пароля", 'error');
  }
};


// 📄 Скачать PDF
const downloadPDF = async () => {
  try {
    await refreshTokenIfNeeded();
    const response = await api.get("predict/download-pdf/", { responseType: "blob" });

    const blob = new Blob([response.data], { type: "application/pdf" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "predictions_history.pdf";
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Ошибка загрузки PDF:", error);
  }
};

// Добавляем вычисляемые свойства для анализа изменения риска
const getRiskChangeClass = () => {
  if (predictions.value.length < 2) return '';
  const currentRisk = predictions.value[0].probability;
  const previousRisk = predictions.value[1].probability;
  return currentRisk > previousRisk ? 'risk-increased' : 'risk-decreased';
};

const getRiskChangeIcon = () => {
  if (predictions.value.length < 2) return '';
  const currentRisk = predictions.value[0].probability;
  const previousRisk = predictions.value[1].probability;
  return currentRisk > previousRisk ? 'fas fa-arrow-up' : 'fas fa-arrow-down';
};

const getRiskChangeMessage = () => {
  if (predictions.value.length < 2) return '';
  const currentRisk = predictions.value[0].probability;
  const previousRisk = predictions.value[1].probability;
  const difference = Math.abs(currentRisk - previousRisk).toFixed(2);
  
  if (currentRisk > previousRisk) {
    return `Ухудшение на ${difference}%. Рекомендуется срочно обратиться к врачу!`;
  } else {
    return `Улучшение на ${difference}%. Продолжайте следить за здоровьем!`;
  }
};

// 🔄 Загружаем данные при открытии страницы
onMounted(() => {
  fetchProfile();
  fetchPredictions();
});
</script>


<template>
  <!-- Добавим компонент уведомления -->
  <transition name="notification">
    <div v-if="notification.show" 
         class="notification" 
         :class="notification.type">
      <i :class="notification.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
      {{ notification.message }}
    </div>
  </transition>

  <div class="profile-container">
    <div class="profile-card">
      <h1 class="title">Личный кабинет</h1>
      
      <div class="alert error" v-if="errorMessage">
        <i class="fas fa-exclamation-circle"></i>
        {{ errorMessage }}
      </div>

      <!-- Информация профиля -->
      <div class="profile-section" v-if="!isEditing">
        <div class="info-grid">
          <div class="info-item">
            <i class="fas fa-user"></i>
            <span class="label">Имя пользователя:</span>
            <span class="value">{{ profile.username }}</span>
          </div>
          <div class="info-item">
            <i class="fas fa-envelope"></i>
            <span class="label">Email:</span>
            <span class="value">{{ profile.email }}</span>
          </div>
          <div class="info-item">
            <i class="fas fa-calendar"></i>
            <span class="label">Дата рождения:</span>
            <span class="value">{{ profile.date_of_birth || "Не указано" }}</span>
          </div>
          <div class="info-item">
            <i class="fas fa-weight"></i>
            <span class="label">Вес:</span>
            <span class="value">{{ profile.weight || "Не указано" }} кг</span>
          </div>
          <div class="info-item">
            <i class="fas fa-ruler-vertical"></i>
            <span class="label">Рост:</span>
            <span class="value">{{ profile.height || "Не указано" }} см</span>
          </div>
          <div class="info-item">
            <i class="fas fa-venus-mars"></i>
            <span class="label">Пол:</span>
            <span class="value">{{ profile.gender === "male" ? "Мужской" : profile.gender === "female" ? "Женский" : "Не указано" }}</span>
          </div>
        </div>

        <!-- Выносим ИМТ в отдельный div -->
        <div class="bmi-item">
          <div class="info-item">
            <i class="fas fa-calculator"></i>
            <span class="label">ИМТ:</span>
            <span class="value">{{ bmi }}</span>
          </div>
        </div>

        <!-- Добавляем секцию изменения риска диабета -->
        <div class="diabetes-risk-change" v-if="predictions.length >= 2">
          <div class="info-item" :class="getRiskChangeClass()">
            <i :class="getRiskChangeIcon()"></i>
            <span class="label">Изменение риска диабета:</span>
            <span class="value">{{ getRiskChangeMessage() }}</span>
          </div>
        </div>

        <div class="profile-actions">
          <div class="button-group">
            <button @click="isEditing = true" class="edit-button">
              <i class="fas fa-edit"></i> Редактировать профиль
            </button>
            <button @click="showResetForm = true" class="reset-button">
              <i class="fas fa-key"></i> Сменить пароль
            </button>
          </div>
        </div>
      </div>

      <!-- Форма редактирования -->
      <div class="edit-form" v-else>
        <div class="form-grid">
          <div class="input-group">
            <label>Имя пользователя:</label>
            <input v-model="profile.username" type="text" />
          </div>

          <div class="input-group">
            <label>Дата рождения:</label>
            <input v-model="profile.date_of_birth" type="date" />
          </div>

          <div class="input-group">
            <label>Вес (кг):</label>
            <input v-model="profile.weight" type="number" min="1" step="0.1" />
          </div>

          <div class="input-group">
            <label>Рост (см):</label>
            <input v-model="profile.height" type="number" min="1" step="0.1" />
          </div>

          <div class="input-group">
            <label>Пол:</label>
            <select v-model="profile.gender">
              <option value="male">Мужской</option>
              <option value="female">Женский</option>
            </select>
          </div>
        </div>

        <div class="bmi-display">
          <span class="label">ИМТ:</span>
          <span class="value">{{ bmi }}</span>
        </div>

        <div class="button-group">
          <button @click="updateProfile" class="save-button">
            <i class="fas fa-save"></i> Сохранить
          </button>
          <button @click="isEditing = false" class="cancel-button">
            <i class="fas fa-times"></i> Отмена
          </button>
        </div>
      </div>

      <!-- После секции с информацией профиля, перед историей предсказаний -->
      <div class="history-section">
        <h2 class="section-title">
          <i class="fas fa-history"></i> История предсказаний
        </h2>
        
        <div v-if="predictions.length" class="predictions-wrapper">
          <table class="prediction-table">
            <thead>
              <tr>
                <th>Дата</th>
                <th>Результат</th>
                <th>Вероятность</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prediction in predictions" :key="prediction.id">
                <td>{{ new Date(prediction.created_at).toLocaleString() }}</td>
                <td>{{ prediction.prediction }}</td>
                <td class="probability-cell">
                  <div class="probability-wrapper">
                    <div class="probability-bar">
                      <div class="probability-fill" :style="{ width: prediction.probability + '%' }"></div>
                    </div>
                    <span class="probability-text">{{ prediction.probability.toFixed(2) }}%</span>
                  </div>
                </td>
                <td class="actions-cell">
                  <button @click="confirmDelete(prediction.id)" class="action-button delete-button">
                    <i class="fas fa-trash"></i>
                    <span>Удалить</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <button @click="downloadPDF" class="download-button">
            <i class="fas fa-file-pdf"></i> Скачать PDF
          </button>
        </div>
        <p v-else class="no-data">История предсказаний пуста</p>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showConfirmation" class="modal">
      <div class="modal-content">
        <button @click="showConfirmation = false" class="close-button">
          <i class="fas fa-times"></i>
        </button>
        <div class="modal-header">
          <i class="fas fa-exclamation-triangle warning-icon"></i>
          <h3>Подтверждение удаления</h3>
        </div>
        <p class="modal-text">Вы уверены, что хотите удалить этот результат?</p>
        <div class="modal-buttons">
          <button @click="deletePrediction" class="delete-button">
            <i class="fas fa-trash"></i> Удалить
          </button>
          <button @click="showConfirmation = false" class="cancel-button">
            <i class="fas fa-times"></i> Отмена
          </button>
        </div>
      </div>
    </div>

    <!-- Форма сброса пароля -->
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
            <input v-model="email" type="email" disabled />
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
.profile-container {
  min-height: 100vh;
  padding: 2rem;
  background-color: #f5f6fa;
}

.profile-card {
  max-width: 1000px;
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
}

.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error {
  background-color: #fde8e8;
  color: #e74c3c;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #eee;
  transition: all 0.3s ease;
}

.info-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.info-item i {
  color: #3498db;
  font-size: 1.4rem;
  width: 24px;
  text-align: center;
}

.label {
  color: #666;
  font-weight: 500;
}

.value {
  margin-left: auto;
  font-weight: 600;
  color: #2c3e50;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  color: #666;
  font-weight: 500;
}

.input-group input,
.input-group select {
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.input-group input:focus,
.input-group select:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  outline: none;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.edit-button,
.reset-button,
.action-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  font-weight: 500;
}

.edit-button {
  background: #3498db;
  color: white;
}

.edit-button:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.reset-button {
  background: #f39c12;
  color: white;
}

.reset-button:hover {
  background: #e67e22;
  transform: translateY(-2px);
}

.save-button,
.cancel-button,
.download-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.save-button {
  background: #2ecc71;
  color: white;
}

.cancel-button {
  background: #e74c3c;
  color: white;
}

.download-button {
  background: #3498db;
  color: white;
  margin-top: 1rem;
}

.history-section {
  margin-top: 3rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.prediction-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 2rem;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.prediction-table th,
.prediction-table td {
  padding: 1.2rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.prediction-table th {
  background: #f8f9fa;
  color: #2c3e50;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

.prediction-table tr:hover {
  background-color: #f8f9fa;
}

.actions-cell {
  width: 150px;
  text-align: center;
}

.action-button.delete-button {
  background: #fff0f0;
  color: #e74c3c;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  width: 100%;
  justify-content: center;
}

.action-button.delete-button:hover {
  background: #ffe5e5;
  color: #c0392b;
  transform: translateY(-2px);
}

.probability-cell {
  min-width: 200px;
}

.probability-wrapper {
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
  position: relative;
}

.probability-fill {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2980b9);
  transition: width 0.3s ease;
}

.probability-text {
  min-width: 60px;
  font-weight: 600;
  color: #2c3e50;
  text-align: right;
}

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

.warning-icon {
  color: #f39c12;
  font-size: 1.8rem;
}

.modal-icon {
  color: #3498db;
  font-size: 1.8rem;
}

.modal-text {
  color: #666;
  margin-bottom: 1.5rem;
  text-align: center;
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

.modal-body input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.modal-body label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
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
  animation: fadeIn 0.3s ease;
}

.reset-message.success {
  background: #edfbf3;
  color: #2ecc71;
}

.reset-message i {
  font-size: 1.2rem;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.modal-buttons button {
  min-width: 140px;
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

/* Обновим стили для кнопок в модальных окнах */
.modal-buttons .submit-button,
.modal-buttons .delete-button,
.modal-buttons .cancel-button {
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

.modal-buttons .delete-button {
  background: #e74c3c;
  color: white;
}

.modal-buttons .delete-button:hover {
  background: #c0392b;
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

.bmi-item {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  margin-bottom: 2rem;
}

.bmi-item .info-item {
  width: 350px; /* Фиксированная ширина как у других элементов */
}

/* Медиа-запросы для мобильной адаптации */
@media (max-width: 1024px) {
  .profile-container {
    padding: 1.5rem;
  }

  .profile-card {
    padding: 1.5rem;
  }

  .title {
    font-size: 2rem;
  }

  .info-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }

  .profile-card {
    padding: 1.2rem;
    border-radius: 15px;
  }

  .title {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .info-item {
    padding: 1rem;
    font-size: 0.95rem;
  }

  .info-item i {
    font-size: 1.2rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .button-group {
    flex-direction: column;
    gap: 0.8rem;
  }

  .edit-button,
  .reset-button,
  .save-button,
  .cancel-button {
    width: 100%;
    padding: 0.8rem;
    font-size: 0.95rem;
  }

  .prediction-table {
    font-size: 0.9rem;
    display: block;
    overflow-x: auto;
  }

  .prediction-table th,
  .prediction-table td {
    padding: 0.8rem;
    white-space: nowrap;
  }

  .actions-cell {
    width: auto;
    text-align: center;
  }

  .action-button.delete-button {
    padding: 0.5rem;
    width: auto;
    min-width: 40px;
    height: 40px;
    border-radius: 50%;
    justify-content: center;
  }

  .action-button.delete-button span {
    display: none;
  }

  .action-button.delete-button i {
    margin: 0;
    font-size: 1rem;
  }

  .probability-cell {
    min-width: 150px;
  }

  .probability-wrapper {
    gap: 0.5rem;
  }

  .probability-text {
    min-width: 50px;
    font-size: 0.9rem;
  }

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
  .profile-container {
    padding: 0.5rem;
  }

  .profile-card {
    padding: 1rem;
    border-radius: 12px;
  }

  .title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .info-item {
    padding: 0.8rem;
    font-size: 0.9rem;
  }

  .info-item i {
    font-size: 1.1rem;
  }

  .label {
    font-size: 0.9rem;
  }

  .value {
    font-size: 0.9rem;
  }

  .input-group input,
  .input-group select {
    padding: 0.7rem;
    font-size: 0.9rem;
  }

  .edit-button,
  .reset-button,
  .save-button,
  .cancel-button {
    padding: 0.7rem;
    font-size: 0.9rem;
  }

  .prediction-table {
    font-size: 0.85rem;
  }

  .prediction-table th,
  .prediction-table td {
    padding: 0.6rem;
  }

  .probability-cell {
    min-width: 120px;
  }

  .probability-bar {
    height: 10px;
  }

  .modal-content {
    padding: 1.2rem;
  }

  .modal-header h3 {
    font-size: 1.2rem;
  }

  .modal-text {
    font-size: 0.9rem;
  }

  .bmi-item .info-item,
  .diabetes-risk-change .info-item {
    width: 100%;
    padding: 0.8rem;
  }

  .notification {
    width: 90%;
    right: 5%;
    top: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
  }

  .action-button.delete-button {
    padding: 0.4rem;
    min-width: 36px;
    height: 36px;
  }

  .action-button.delete-button i {
    font-size: 0.9rem;
  }
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

/* Анимации для модальных окон при закрытии */
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-leave-to {
  opacity: 0;
}

.modal-leave-to .modal-content {
  transform: translateY(20px);
}

/* Обновим анимацию для сообщений в модальных окнах */
.reset-message {
  animation: slideUp 0.3s ease;
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

.diabetes-risk-change {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  margin-bottom: 2rem;
}

.diabetes-risk-change .info-item {
  width: 350px;
  transition: all 0.3s ease;
}

.risk-increased {
  background: #fde8e8;
  border-color: #e74c3c;
}

.risk-increased i {
  color: #e74c3c;
}

.risk-decreased {
  background: #edfbf3;
  border-color: #2ecc71;
}

.risk-decreased i {
  color: #2ecc71;
}
</style>
