<script setup>
import { ref } from 'vue';
import DatasetVisuals from '../components/DatasetVisuals.vue';

const sections = ref({
  about: false,
  importance: false,
  prevention: false,
  statistics: false,
  measurements: false,
  nextSteps: false
});

const toggleSection = (section) => {
  sections.value[section] = !sections.value[section];
};
</script>

<template>
    <div class="education-container">
        <div class="education-card">
            <h1 class="title">
                <i class="fas fa-book-medical"></i>
                Всё, что нужно знать о диабете
            </h1>

            <!-- О проекте -->
            <div class="collapsible-section">
                <div class="section-header" @click="toggleSection('about')">
                    <h2><i class="fas fa-bullseye"></i> О нашем проекте</h2>
                    <i :class="['fas', sections.about ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <transition name="collapse">
                    <div v-show="sections.about" class="section-content">
                        <p>
                            Мы создали этот сервис, чтобы помочь вам оценить риск развития диабета 2 типа. 
                            Наша цель - не напугать, а предупредить и дать возможность принять меры заранее. 
                            Используя современные технологии машинного обучения, мы анализируем ваши показатели 
                            здоровья и оцениваем вероятность развития заболевания.
                        </p>
                    </div>
                </transition>
            </div>

            <!-- Почему это важно -->
            <div class="collapsible-section">
                <div class="section-header" @click="toggleSection('importance')">
                    <h2><i class="fas fa-exclamation-triangle"></i> Почему это важно?</h2>
                    <i :class="['fas', sections.importance ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <transition name="collapse">
                    <div v-show="sections.importance" class="section-content">
                        <div class="info-cards">
                            <div class="info-card">
                                <i class="fas fa-heartbeat"></i>
                                <h3>Влияет на весь организм</h3>
                                <p>Затрагивает сердце, сосуды, зрение, почки и нервную систему</p>
                            </div>
                            <div class="info-card">
                                <i class="fas fa-chart-line"></i>
                                <h3>Растущая проблема</h3>
                                <p>Количество людей с диабетом увеличивается с каждым годом</p>
                            </div>
                            <div class="info-card">
                                <i class="fas fa-shield-alt"></i>
                                <h3>Можно предотвратить</h3>
                                <p>До 80% случаев диабета 2 типа можно предотвратить</p>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>

            <!-- Статистика -->
            <div class="collapsible-section">
                <div class="section-header" @click="toggleSection('statistics')">
                    <h2><i class="fas fa-chart-bar"></i> О модели и данных</h2>
                    <i :class="['fas', sections.statistics ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <transition name="collapse">
                    <div v-show="sections.statistics" class="section-content">
                        <div class="model-info-blocks">
                            <div class="info-block">
                                <h3><i class="fas fa-brain"></i> Модель машинного обучения</h3>
                                <p>
                                    Мы используем <strong>XGBoost (Extreme Gradient Boosting)</strong> – современный алгоритм 
                                    машинного обучения, который показывает высокую точность в задачах классификации. 
                                    Перед анализом все введённые данные нормализуются с помощью StandardScaler, что 
                                    обеспечивает точность предсказания независимо от масштаба входных параметров.
                                </p>
                            </div>

                            <div class="info-block">
                                <h3><i class="fas fa-database"></i> Датасет PIMA Indians</h3>
                                <p>
                                    Модель обучена на наборе данных PIMA Indians Diabetes Dataset. Среди индейцев племени пима, 
                                    живущих на территории США, зафиксирован самый высокий в мире процент заболеваемости 
                                    сахарным диабетом 2 типа. Данная проблема лишь частично обусловлена генетически, поскольку 
                                    заболеваемость этим типом диабета практически отсутствует среди индейцев-пима, живущих в 
                                    Мексике. Спусковым механизмом для данного заболевания стало разрушение традиционной 
                                    экономики племени и переход к новому питанию.
                                </p>
                            </div>

                            <div class="info-block parameters">
                                <h3><i class="fas fa-list-ul"></i> Параметры модели</h3>
                                <div class="parameters-grid">
                                    <div class="parameter">
                                        <span class="parameter-name">Pregnancies</span>
                                        <span class="parameter-desc">Количество беременностей</span>
                                    </div>
                                    <div class="parameter">
                                        <span class="parameter-name">Glucose</span>
                                        <span class="parameter-desc">Уровень глюкозы в плазме крови</span>
                                    </div>
                                    <div class="parameter">
                                        <span class="parameter-name">Blood Pressure</span>
                                        <span class="parameter-desc">Диастолическое давление крови (мм рт.ст.)</span>
                                    </div>
                                    <div class="parameter">
                                        <span class="parameter-name">Skin Thickness</span>
                                        <span class="parameter-desc">Толщина кожной складки трицепса (мм)</span>
                                    </div>
                                    <div class="parameter">
                                        <span class="parameter-name">Insulin</span>
                                        <span class="parameter-desc">Уровень инсулина в сыворотке крови</span>
                                    </div>
                                    <div class="parameter">
                                        <span class="parameter-name">BMI</span>
                                        <span class="parameter-desc">Индекс массы тела</span>
                                    </div>
                                    <div class="parameter">
                                        <span class="parameter-name">DiabetesPedigree</span>
                                        <span class="parameter-desc">Функция наследственности диабета</span>
                                    </div>
                                    <div class="parameter">
                                        <span class="parameter-name">Age</span>
                                        <span class="parameter-desc">Возраст (лет)</span>
                                    </div>
                                </div>
                            </div>

                            <DatasetVisuals />
                        </div>
                    </div>
                </transition>
            </div>

            <!-- Добавляем новую секцию после статистики -->
            <div class="collapsible-section">
                <div class="section-header" @click="toggleSection('measurements')">
                    <h2><i class="fas fa-flask"></i> Как получить данные для анализа?</h2>
                    <i :class="['fas', sections.measurements ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <transition name="collapse">
                    <div v-show="sections.measurements" class="section-content">
                        <div class="measurements-grid">
                            <div class="measurement-card">
                                <div class="measurement-header">
                                    <i class="fas fa-tint"></i>
                                    <h3>Уровень глюкозы</h3>
                                </div>
                                <div class="measurement-content">
                                    <p>Измеряется с помощью глюкометра натощак (не есть 8-12 часов).</p>
                                    <ul>
                                        <li>Норма натощак: 3.3-5.5 ммоль/л (60-100 мг/дл)</li>
                                        <li>Можно сдать анализ в любой лаборатории</li>
                                        <li>Лучше измерять утром до завтрака</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="measurement-card">
                                <div class="measurement-header">
                                    <i class="fas fa-syringe"></i>
                                    <h3>Уровень инсулина</h3>
                                </div>
                                <div class="measurement-content">
                                    <p>Определяется в лаборатории через анализ крови.</p>
                                    <ul>
                                        <li>Сдается натощак</li>
                                        <li>Норма: 2.6-24.9 мкЕд/мл</li>
                                        <li>Требуется направление врача</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="measurement-card">
                                <div class="measurement-header">
                                    <i class="fas fa-ruler"></i>
                                    <h3>Толщина кожной складки</h3>
                                </div>
                                <div class="measurement-content">
                                    <p>Измеряется калипером в области трицепса.</p>
                                    <ul>
                                        <li>Измеряется на задней поверхности руки</li>
                                        <li>Можно измерить у врача или фитнес-тренера</li>
                                        <li>Средние значения: 12-36 мм</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="measurement-card">
                                <div class="measurement-header">
                                    <i class="fas fa-dna"></i>
                                    <h3>Наследственность диабета</h3>
                                </div>
                                <div class="measurement-content">
                                    <p>Оценивается на основе семейного анамнеза.</p>
                                    <ul>
                                        <li>Узнайте о случаях диабета у родственников</li>
                                        <li>Учитывается степень родства</li>
                                        <li>Возраст начала заболевания у родственников</li>
                                    </ul>
                                    <p class="measurement-note">Коэффициент от 0.078 до 2.42, где:</p>
                                    <ul class="measurement-scale">
                                        <li>0.078-0.5: низкий риск</li>
                                        <li>0.5-1: средний риск</li>
                                        <li>>1: высокий риск</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="measurement-card">
                                <div class="measurement-header">
                                    <i class="fas fa-heartbeat"></i>
                                    <h3>Артериальное давление</h3>
                                </div>
                                <div class="measurement-content">
                                    <p>Измеряется тонометром.</p>
                                    <ul>
                                        <li>Измерять в состоянии покоя</li>
                                        <li>Норма: менее 120/80 мм рт.ст.</li>
                                        <li>Измерять 2-3 раза с интервалом</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>

            <!-- Как снизить риск -->
            <div class="collapsible-section">
                <div class="section-header" @click="toggleSection('prevention')">
                    <h2><i class="fas fa-heart"></i> Как снизить риск?</h2>
                    <i :class="['fas', sections.prevention ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <transition name="collapse">
                    <div v-show="sections.prevention" class="section-content">
                        <div class="prevention-tips">
                            <div class="tip">
                                <i class="fas fa-walking"></i>
                                <div class="tip-content">
                                    <h3>Больше движения</h3>
                                    <p>30 минут умеренной активности 5 раз в неделю значительно снижают риск</p>
                                </div>
                            </div>
                            <div class="tip">
                                <i class="fas fa-apple-alt"></i>
                                <div class="tip-content">
                                    <h3>Здоровое питание</h3>
                                    <p>Больше овощей, меньше сахара и простых углеводов</p>
                                </div>
                            </div>
                            <div class="tip">
                                <i class="fas fa-weight"></i>
                                <div class="tip-content">
                                    <h3>Контроль веса</h3>
                                    <p>Поддержание здорового веса снижает нагрузку на организм</p>
                                </div>
                            </div>
                            <div class="tip">
                                <i class="fas fa-clock"></i>
                                <div class="tip-content">
                                    <h3>Регулярные проверки</h3>
                                    <p>Измеряйте уровень сахара хотя бы раз в год</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>

            <!-- Что делать дальше -->
            <div class="collapsible-section">
                <div class="section-header" @click="toggleSection('nextSteps')">
                    <h2><i class="fas fa-check-circle"></i> Что делать дальше?</h2>
                    <i :class="['fas', sections.nextSteps ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <transition name="collapse">
                    <div v-show="sections.nextSteps" class="section-content">
                        <div class="action-steps">
                            <router-link to="/predict" class="action-button">
                                <i class="fas fa-calculator"></i>
                                Оценить свой риск
                            </router-link>
                            <p class="action-note">
                                Помните: наш сервис не заменяет консультацию врача. При наличии тревожных 
                                симптомов или высоком риске обязательно обратитесь к специалисту.
                            </p>
                        </div>
                    </div>
                </transition>
            </div>
        </div>
    </div>
</template>

<style scoped>
.education-container {
    min-height: 100vh;
    padding: 2rem;
    background-color: #f5f6fa;
}

.education-card {
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

.collapsible-section {
    margin-bottom: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    overflow: hidden;
}

.section-header {
    padding: 1.5rem;
    background: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.section-header:hover {
    background: #edf2f7;
}

.section-header h2 {
    margin: 0;
    font-size: 1.4rem;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.section-header i {
    color: #3498db;
}

.section-content {
    padding: 1.5rem;
    background: white;
}

/* Анимация сворачивания/разворачивания */
.collapse-enter-active,
.collapse-leave-active {
    transition: all 0.3s ease-in-out;
    overflow: hidden;
}

.collapse-enter-from,
.collapse-leave-to {
    opacity: 0;
    max-height: 0;
}

.collapse-enter-to,
.collapse-leave-from {
    opacity: 1;
    max-height: 2000px;
}

.info-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.info-card {
    padding: 1.5rem;
    border-radius: 12px;
    background: #f8f9fa;
    text-align: center;
    transition: transform 0.3s ease;
}

.info-card:hover {
    transform: translateY(-5px);
}

.info-card i {
    font-size: 2rem;
    color: #e74c3c;
    margin-bottom: 1rem;
}

.info-card h3 {
    color: #2c3e50;
    margin-bottom: 0.8rem;
}

.info-card p {
    color: #666;
    font-size: 1rem;
}

.prevention-tips {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.tip {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 12px;
    transition: transform 0.3s ease;
}

.tip:hover {
    transform: translateX(5px);
}

.tip i {
    font-size: 1.5rem;
    color: #27ae60;
    margin-top: 0.2rem;
}

.tip-content h3 {
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.tip-content p {
    color: #666;
    font-size: 1rem;
    line-height: 1.5;
}

.action {
    text-align: center;
    background: #f1f8ff;
}

.action-steps {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}

.action-button {
    display: inline-flex;
    align-items: center;
    gap: 0.8rem;
    padding: 1rem 2rem;
    background: #3498db;
    color: white;
    border-radius: 8px;
    text-decoration: none;
    font-size: 1.2rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.action-button:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.action-note {
    color: #666;
    font-style: italic;
    max-width: 600px;
    margin: 0 auto;
}

.measurements-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.measurement-card {
    background: #f8f9fa;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.3s ease;
}

.measurement-card:hover {
    transform: translateY(-5px);
}

.measurement-header {
    background: #3498db;
    color: white;
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.measurement-header i {
    font-size: 1.5rem;
}

.measurement-header h3 {
    margin: 0;
    font-size: 1.2rem;
}

.measurement-content {
    padding: 1.5rem;
}

.measurement-content p {
    color: #2c3e50;
    margin-bottom: 1rem;
    line-height: 1.6;
}

.measurement-content ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.measurement-content ul li {
    color: #666;
    margin-bottom: 0.5rem;
    padding-left: 1.5rem;
    position: relative;
}

.measurement-content ul li:before {
    content: "•";
    color: #3498db;
    position: absolute;
    left: 0;
}

.measurement-note {
    margin-top: 1rem;
    font-weight: 500;
    color: #2c3e50;
}

.measurement-scale li {
    display: flex;
    justify-content: space-between;
    padding: 0.3rem 0;
}

.model-info-blocks {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.info-block {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.info-block h3 {
    color: #2c3e50;
    font-size: 1.3rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.info-block h3 i {
    color: #3498db;
}

.info-block p {
    color: #666;
    line-height: 1.8;
    text-align: justify;
}

.parameters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.parameter {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.parameter-name {
    color: #3498db;
    font-weight: 600;
    font-size: 1.1rem;
}

.parameter-desc {
    color: #666;
    font-size: 0.9rem;
}

@media (max-width: 768px) {
    .education-container {
        padding: 1rem;
    }

    .education-card {
        padding: 1.5rem;
    }

    .section {
        padding: 1.5rem;
    }

    .title {
        font-size: 1.8rem;
    }

    .info-cards {
        grid-template-columns: 1fr;
    }

    .prevention-tips {
        grid-template-columns: 1fr;
    }

    .measurements-grid {
        grid-template-columns: 1fr;
    }

    .parameters-grid {
        grid-template-columns: 1fr;
    }
}
</style> 