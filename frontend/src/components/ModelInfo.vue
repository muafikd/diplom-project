<template>
    <div class="model-info">
        <div class="model-info-header" @click="isExpanded = !isExpanded">
            <div class="header-content">
                <i class="fas fa-info-circle"></i>
                <h3>Информация о предсказании</h3>
            </div>
            <i :class="['fas', isExpanded ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
        </div>
        
        <transition name="expand">
            <div v-if="isExpanded" class="model-info-content">
                <div class="tabs">
                    <button 
                        v-for="(tab, key) in tabs" 
                        :key="key"
                        :class="['tab-button', { active: activeTab === key }]"
                        @click="activeTab = key"
                    >
                        <i :class="['fas', tab.icon]"></i>
                        {{ tab.title }}
                    </button>
                </div>

                <div v-if="activeTab === 'model'" class="tab-content">
                    <p class="model-description">
                        Мы используем <strong>XGBoost (Extreme Gradient Boosting)</strong> – современный алгоритм 
                        машинного обучения для предсказания вероятности диабета. Модель обучена на реальных 
                        медицинских данных и показывает высокую точность в определении риска заболевания.
                    </p>
                </div>

                <div v-else-if="activeTab === 'measurements'" class="tab-content">
                    <div class="measurements-grid">
                        <div class="measurement-card">
                            <div class="measurement-header">
                                <i class="fas fa-tint"></i>
                                <h4>Уровень глюкозы</h4>
                            </div>
                            <div class="measurement-content">
                                <ul>
                                    <li>Измеряется натощак (не есть 8-12 часов)</li>
                                    <li>Норма: 60-100 мг/дл</li>
                                    <li>Сдается в любой лаборатории</li>
                                </ul>
                            </div>
                        </div>

                        <div class="measurement-card">
                            <div class="measurement-header">
                                <i class="fas fa-syringe"></i>
                                <h4>Инсулин</h4>
                            </div>
                            <div class="measurement-content">
                                <ul>
                                    <li>Анализ крови натощак</li>
                                    <li>Норма: 2.6-24.9 мкЕд/мл</li>
                                    <li>Нужно направление врача</li>
                                </ul>
                            </div>
                        </div>

                        <div class="measurement-card">
                            <div class="measurement-header">
                                <i class="fas fa-ruler"></i>
                                <h4>Кожная складка</h4>
                            </div>
                            <div class="measurement-content">
                                <ul>
                                    <li>Измеряется калипером</li>
                                    <li>Норма: 12-36 мм</li>
                                    <li>Измеряет врач/тренер</li>
                                </ul>
                            </div>
                        </div>

                        <div class="measurement-card">
                            <div class="measurement-header">
                                <i class="fas fa-dna"></i>
                                <h4>Наследственность</h4>
                            </div>
                            <div class="measurement-content">
                                <ul>
                                    <li>0.078-0.5: низкий риск</li>
                                    <li>0.5-1: средний риск</li>
                                    <li>>1: высокий риск</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const isExpanded = ref(false);
const activeTab = ref('model');

const tabs = {
    model: {
        icon: 'fa-brain',
        title: 'О модели'
    },
    measurements: {
        icon: 'fa-flask',
        title: 'Как получить данные'
    }
};
</script>

<style scoped>
.model-info {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    overflow: hidden;
}

.model-info-header {
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.header-content {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.model-info-header:hover {
    background: #edf2f7;
}

.model-info-header h3 {
    margin: 0;
    color: #2c3e50;
    font-size: 1.2rem;
}

.model-info-header i {
    color: #3498db;
}

.model-info-content {
    padding: 1.5rem;
    background: white;
}

.tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.tab-button {
    padding: 0.8rem 1.5rem;
    border: none;
    background: #f8f9fa;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #666;
    transition: all 0.3s ease;
}

.tab-button:hover {
    background: #edf2f7;
}

.tab-button.active {
    background: #3498db;
    color: white;
}

.tab-button i {
    font-size: 1rem;
}

.measurements-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.measurement-card {
    background: #f8f9fa;
    border-radius: 8px;
    overflow: hidden;
}

.measurement-header {
    background: #3498db;
    color: white;
    padding: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.measurement-header h4 {
    margin: 0;
    font-size: 1rem;
}

.measurement-content {
    padding: 1rem;
}

.measurement-content ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.measurement-content li {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    padding-left: 1.2rem;
    position: relative;
}

.measurement-content li:before {
    content: "•";
    color: #3498db;
    position: absolute;
    left: 0;
}

/* Анимация разворачивания */
.expand-enter-active,
.expand-leave-active {
    transition: all 0.3s ease-in-out;
    overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
    opacity: 0;
    max-height: 0;
}

.expand-enter-to,
.expand-leave-from {
    opacity: 1;
    max-height: 1000px;
}

@media (max-width: 768px) {
    .tabs {
        flex-direction: column;
    }
    
    .measurements-grid {
        grid-template-columns: 1fr;
    }
}
</style> 