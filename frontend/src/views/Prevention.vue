<script setup>
import { ref } from 'vue';

const activeTab = ref('general');
</script>

<template>
    <div class="prevention-container">
        <div class="prevention-card">
            <h1 class="title">
                <i class="fas fa-shield-alt"></i>
                Профилактика диабета
            </h1>

            <div class="tabs">
                <button 
                    :class="['tab-button', { active: activeTab === 'general' }]"
                    @click="activeTab = 'general'"
                >
                    <i class="fas fa-info-circle"></i>
                    Общие рекомендации
                </button>
                <button 
                    :class="['tab-button', { active: activeTab === 'risk' }]"
                    @click="activeTab = 'risk'"
                >
                    <i class="fas fa-exclamation-triangle"></i>
                    Группы риска
                </button>
                <button 
                    :class="['tab-button', { active: activeTab === 'lifestyle' }]"
                    @click="activeTab = 'lifestyle'"
                >
                    <i class="fas fa-heart"></i>
                    Образ жизни
                </button>
                <button 
                    :class="['tab-button', { active: activeTab === 'cases' }]"
                    @click="activeTab = 'cases'"
                >
                    <i class="fas fa-user-friends"></i>
                    Истории пациентов
                </button>
            </div>

            <div class="tab-content">
                <!-- Общие рекомендации -->
                <div v-if="activeTab === 'general'" class="tab-pane">
                    <div class="info-block">
                        <h2><i class="fas fa-clipboard-list"></i> Ключевые меры профилактики</h2>
                        <div class="prevention-grid">
                            <div class="prevention-item">
                                <i class="fas fa-apple-alt"></i>
                                <h3>Правильное питание</h3>
                                <ul>
                                    <li>Ограничение простых углеводов</li>
                                    <li>Контроль размера порций</li>
                                    <li>Больше клетчатки и овощей</li>
                                    <li>Регулярный режим питания</li>
                                </ul>
                            </div>
                            <div class="prevention-item">
                                <i class="fas fa-running"></i>
                                <h3>Физическая активность</h3>
                                <ul>
                                    <li>150 минут умеренной активности в неделю</li>
                                    <li>Силовые тренировки 2-3 раза в неделю</li>
                                    <li>Ежедневная ходьба минимум 30 минут</li>
                                    <li>Регулярные перерывы при сидячей работе</li>
                                </ul>
                            </div>
                            <div class="prevention-item">
                                <i class="fas fa-weight"></i>
                                <h3>Контроль веса</h3>
                                <ul>
                                    <li>Поддержание нормального ИМТ (18.5-24.9)</li>
                                    <li>Снижение веса при необходимости</li>
                                    <li>Контроль окружности талии</li>
                                    <li>Регулярное взвешивание</li>
                                </ul>
                            </div>
                            <div class="prevention-item">
                                <i class="fas fa-clock"></i>
                                <h3>Регулярный мониторинг</h3>
                                <ul>
                                    <li>Проверка уровня глюкозы раз в год</li>
                                    <li>Контроль артериального давления</li>
                                    <li>Регулярные медосмотры</li>
                                    <li>Анализ на гликированный гемоглобин</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Группы риска -->
                <div v-if="activeTab === 'risk'" class="tab-pane">
                    <div class="risk-groups">
                        <div class="risk-group">
                            <h3><i class="fas fa-dna"></i> Генетическая предрасположенность</h3>
                            <p>Риск развития диабета увеличивается:</p>
                            <ul>
                                <li>На 40% при наличии диабета у одного из родителей</li>
                                <li>На 70% при наличии диабета у обоих родителей</li>
                                <li>На 30% при наличии диабета у брата или сестры</li>
                            </ul>
                        </div>
                        <div class="risk-group">
                            <h3><i class="fas fa-female"></i> Гестационный диабет</h3>
                            <p>У женщин, перенесших гестационный диабет:</p>
                            <ul>
                                <li>Риск развития диабета 2 типа в течение 10 лет: 50%</li>
                                <li>Необходимость ежегодного скрининга</li>
                                <li>Важность поддержания нормального веса после родов</li>
                            </ul>
                        </div>
                        <div class="risk-group">
                            <h3><i class="fas fa-chart-line"></i> Метаболический синдром</h3>
                            <p>Повышенный риск при наличии:</p>
                            <ul>
                                <li>Абдоминального ожирения</li>
                                <li>Повышенного артериального давления</li>
                                <li>Нарушения липидного обмена</li>
                                <li>Нарушения толерантности к глюкозе</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Образ жизни -->
                <div v-if="activeTab === 'lifestyle'" class="tab-pane">
                    <div class="lifestyle-blocks">
                        <div class="lifestyle-block">
                            <h3><i class="fas fa-utensils"></i> Питание</h3>
                            <div class="diet-plan">
                                <h4>Рекомендуемое распределение калорий:</h4>
                                <ul>
                                    <li>Углеводы: 45-60% (предпочтительно сложные)</li>
                                    <li>Белки: 15-20%</li>
                                    <li>Жиры: 20-35% (преимущественно ненасыщенные)</li>
                                </ul>
                                <h4>Продукты для профилактики диабета:</h4>
                                <div class="food-groups">
                                    <div class="food-group">
                                        <span class="food-label">Рекомендуются:</span>
                                        <ul>
                                            <li>Цельнозерновые продукты</li>
                                            <li>Бобовые</li>
                                            <li>Листовые овощи</li>
                                            <li>Ягоды</li>
                                            <li>Орехи</li>
                                        </ul>
                                    </div>
                                    <div class="food-group">
                                        <span class="food-label">Ограничить:</span>
                                        <ul>
                                            <li>Сахар и сладости</li>
                                            <li>Рафинированные крупы</li>
                                            <li>Газированные напитки</li>
                                            <li>Фастфуд</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="lifestyle-block">
                            <h3><i class="fas fa-dumbbell"></i> Физическая активность</h3>
                            <div class="exercise-plan">
                                <h4>Недельный план активности:</h4>
                                <div class="activity-types">
                                    <div class="activity-type">
                                        <h5>Кардио</h5>
                                        <ul>
                                            <li>Ходьба: 30-60 минут ежедневно</li>
                                            <li>Плавание: 2-3 раза в неделю</li>
                                            <li>Велосипед: 2-3 раза в неделю</li>
                                        </ul>
                                    </div>
                                    <div class="activity-type">
                                        <h5>Силовые тренировки</h5>
                                        <ul>
                                            <li>2-3 раза в неделю</li>
                                            <li>8-12 повторений</li>
                                            <li>Все основные группы мышц</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Истории пациентов -->
                <div v-if="activeTab === 'cases'" class="tab-pane">
                    <div class="patient-stories">
                        <div class="story">
                            <div class="story-header">
                                <i class="fas fa-user-circle"></i>
                                <h3>Елена, 45 лет</h3>
                            </div>
                            <p class="story-content">
                                "У меня был высокий риск развития диабета из-за наследственности и лишнего веса. 
                                После того как узнала о риске, изменила питание и начала ходить в бассейн. За год 
                                похудела на 15 кг, уровень глюкозы пришёл в норму. Теперь регулярно проверяюсь и 
                                поддерживаю здоровый образ жизни."
                            </p>
                            <div class="story-results">
                                <div class="result-item">
                                    <span>Начальный ИМТ:</span>
                                    <strong>32.5</strong>
                                </div>
                                <div class="result-item">
                                    <span>Текущий ИМТ:</span>
                                    <strong>24.8</strong>
                                </div>
                                <div class="result-item">
                                    <span>Глюкоза до:</span>
                                    <strong>6.8 ммоль/л</strong>
                                </div>
                                <div class="result-item">
                                    <span>Глюкоза после:</span>
                                    <strong>5.2 ммоль/л</strong>
                                </div>
                            </div>
                        </div>

                        <div class="story">
                            <div class="story-header">
                                <i class="fas fa-user-circle"></i>
                                <h3>Александр, 52 года</h3>
                            </div>
                            <p class="story-content">
                                "Работа офисная, двигался мало, питался нерегулярно. На обследовании выявили 
                                преддиабет. Начал каждый день ходить по 10000 шагов, записался в спортзал. 
                                Пересмотрел питание, отказался от сладкого. Через полгода все показатели 
                                нормализовались."
                            </p>
                            <div class="story-results">
                                <div class="result-item">
                                    <span>Шаги до:</span>
                                    <strong>2000/день</strong>
                                </div>
                                <div class="result-item">
                                    <span>Шаги после:</span>
                                    <strong>10000+/день</strong>
                                </div>
                                <div class="result-item">
                                    <span>Глюкоза до:</span>
                                    <strong>7.0 ммоль/л</strong>
                                </div>
                                <div class="result-item">
                                    <span>Глюкоза после:</span>
                                    <strong>5.5 ммоль/л</strong>
                                </div>
                            </div>
                        </div>

                        <div class="story">
                            <div class="story-header">
                                <i class="fas fa-user-circle"></i>
                                <h3>Мария, 38 лет</h3>
                            </div>
                            <p class="story-content">
                                "После беременности был гестационный диабет. Врач предупредил о высоком риске 
                                развития диабета 2 типа. Начала строго следить за питанием, занялась йогой. 
                                Регулярно проверяю уровень сахара. Уже 5 лет показатели в норме."
                            </p>
                            <div class="story-results">
                                <div class="result-item">
                                    <span>Вес до:</span>
                                    <strong>82 кг</strong>
                                </div>
                                <div class="result-item">
                                    <span>Вес после:</span>
                                    <strong>65 кг</strong>
                                </div>
                                <div class="result-item">
                                    <span>Глюкоза во время ГСД:</span>
                                    <strong>8.2 ммоль/л</strong>
                                </div>
                                <div class="result-item">
                                    <span>Глюкоза сейчас:</span>
                                    <strong>5.0 ммоль/л</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.prevention-container {
    min-height: 100vh;
    padding: 2rem;
    background-color: #f5f6fa;
}

.prevention-card {
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
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

.title i {
    color: #3498db;
}

.tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.tab-button {
    padding: 0.8rem 1.5rem;
    border: none;
    background: #f8f9fa;
    border-radius: 8px;
    cursor: pointer;
    color: #666;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
}

.tab-button i {
    color: #3498db;
}

.tab-button.active {
    background: #3498db;
    color: white;
}

.tab-button.active i {
    color: white;
}

.tab-button:hover:not(.active) {
    background: #e9ecef;
}

.prevention-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.prevention-item {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
    transition: transform 0.3s ease;
}

.prevention-item:hover {
    transform: translateY(-5px);
}

.prevention-item i {
    font-size: 2rem;
    color: #3498db;
    margin-bottom: 1rem;
}

.prevention-item h3 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

.prevention-item ul {
    list-style: none;
    padding: 0;
}

.prevention-item ul li {
    color: #666;
    margin-bottom: 0.5rem;
    padding-left: 1.5rem;
    position: relative;
}

.prevention-item ul li:before {
    content: "•";
    color: #3498db;
    position: absolute;
    left: 0;
}

.risk-groups {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.risk-group {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
}

.risk-group h3 {
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1rem;
}

.risk-group h3 i {
    color: #e74c3c;
}

.risk-group p {
    color: #666;
    margin-bottom: 1rem;
}

.risk-group ul {
    list-style: none;
    padding: 0;
}

.risk-group ul li {
    color: #666;
    margin-bottom: 0.5rem;
    padding-left: 1.5rem;
    position: relative;
}

.risk-group ul li:before {
    content: "•";
    color: #e74c3c;
    position: absolute;
    left: 0;
}

.lifestyle-blocks {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.lifestyle-block {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
}

.lifestyle-block h3 {
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}

.lifestyle-block h3 i {
    color: #27ae60;
}

.diet-plan, .exercise-plan {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.food-groups, .activity-types {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

.food-group, .activity-type {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
}

.food-label {
    color: #2c3e50;
    font-weight: 600;
    display: block;
    margin-bottom: 1rem;
}

.patient-stories {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.story {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
}

.story-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.story-header i {
    font-size: 2rem;
    color: #3498db;
}

.story-content {
    color: #666;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    font-style: italic;
}

.story-results {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    background: white;
    padding: 1rem;
    border-radius: 8px;
}

.result-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.result-item span {
    color: #666;
    font-size: 0.9rem;
}

.result-item strong {
    color: #2c3e50;
    font-size: 1.1rem;
}

@media (max-width: 768px) {
    .prevention-container {
        padding: 1rem;
    }

    .prevention-card {
        padding: 1.5rem;
    }

    .tabs {
        flex-direction: column;
    }

    .tab-button {
        width: 100%;
        justify-content: center;
    }

    .title {
        font-size: 1.8rem;
    }

    .story-results {
        grid-template-columns: 1fr 1fr;
    }
}
</style> 