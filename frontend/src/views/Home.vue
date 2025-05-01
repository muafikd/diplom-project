<template>
    <div class="home-container">
        <div class="hero-section">
            <div class="hero-content">
                <h1>Ранняя диагностика диабета</h1>
                <p class="hero-subtitle">
                    Используйте наш сервис для оценки риска развития диабета на основе ваших медицинских показателей
                </p>
                <router-link to="/predict" class="cta-button">
                    <i class="fas fa-chart-line"></i>
                    Пройти диагностику
                </router-link>
            </div>
        </div>

        <div class="info-section">
            <div class="info-card">
                <div class="card-icon">
                    <i class="fas fa-question-circle"></i>
                </div>
                <h2>Что такое диабет?</h2>
                <p>
                    Диабет – это серьезное хроническое заболевание, при котором организм либо не вырабатывает инсулин, 
                    либо не может эффективно его использовать. Это приводит к повышенному уровню глюкозы в крови 
                    (гипергликемии).
                </p>
            </div>

            <div class="info-card">
                <div class="card-icon">
                    <i class="fas fa-list-ul"></i>
                </div>
                <h2>Типы диабета</h2>
                <div class="types-grid">
                    <div class="type-item">
                        <h3>Тип 1</h3>
                        <p>Аутоиммунное заболевание, при котором организм не производит инсулин. Требует ежедневных 
                        инъекций инсулина.</p>
                    </div>
                    <div class="type-item">
                        <h3>Тип 2</h3>
                        <p>Организм не может эффективно использовать инсулин. Развивается постепенно и часто связан 
                        с образом жизни.</p>
                    </div>
                </div>
            </div>

            <div class="info-card">
                <div class="card-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h2>Факторы риска</h2>
                <ul class="risk-factors">
                    <li><i class="fas fa-check"></i> Избыточный вес</li>
                    <li><i class="fas fa-check"></i> Малоподвижный образ жизни</li>
                    <li><i class="fas fa-check"></i> Наследственная предрасположенность</li>
                    <li><i class="fas fa-check"></i> Возраст старше 45 лет</li>
                    <li><i class="fas fa-check"></i> Высокое артериальное давление</li>
                </ul>
            </div>
        </div>

        <div class="action-section">
            <h2>Начните заботиться о своем здоровье уже сейчас</h2>
            <p>Пройдите быстрый тест для оценки риска развития диабета</p>
            <router-link to="/predict" class="secondary-button">
                <i class="fas fa-arrow-right"></i>
                Перейти к диагностике
            </router-link>
        </div>
    </div>
</template>

<style scoped>
.home-container {
    min-height: 100vh;
    background-color: #f5f6fa;
    overflow-x: hidden;
}

.hero-section {
    background: linear-gradient(135deg, #3498db, #2c3e50);
    color: white;
    padding: 3rem 1.5rem;
    text-align: center;
    position: relative;
}

.hero-content {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}

.hero-content h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    line-height: 1.5;
}

.cta-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: white;
    color: #3498db;
    padding: 1rem 2rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-section {
    max-width: 1200px;
    margin: -2rem auto 0;
    padding: 0 1.5rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    position: relative;
    z-index: 1;
}

.info-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.info-card:hover {
    transform: translateY(-5px);
}

.card-icon {
    width: 60px;
    height: 60px;
    background: #f0f7ff;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
}

.card-icon i {
    font-size: 1.8rem;
    color: #3498db;
}

.info-card h2 {
    color: #2c3e50;
    margin-bottom: 1rem;
    font-size: 1.5rem;
    line-height: 1.3;
}

.info-card p {
    color: #7f8c8d;
    line-height: 1.6;
}

.types-grid {
    display: grid;
    gap: 1rem;
}

.type-item {
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 10px;
}

.type-item h3 {
    color: #3498db;
    margin-bottom: 0.5rem;
}

.risk-factors {
    list-style: none;
    padding: 0;
}

.risk-factors li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0;
    color: #2c3e50;
}

.risk-factors i {
    color: #3498db;
}

.action-section {
    text-align: center;
    padding: 3rem 1.5rem;
    background: white;
    margin-top: 4rem;
    position: relative;
    z-index: 2;
}

.action-section h2 {
    color: #2c3e50;
    margin-bottom: 1rem;
    line-height: 1.3;
}

.action-section p {
    color: #7f8c8d;
    margin-bottom: 2rem;
    line-height: 1.5;
}

.secondary-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #3498db;
    color: white;
    padding: 1rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.secondary-button:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

/* Медиа-запросы для адаптации */
@media (max-width: 1024px) {
    .hero-section {
        padding: 2.5rem 1.5rem;
    }

    .info-section {
        margin-top: -1.5rem;
        gap: 1.5rem;
    }

    .info-card {
        padding: 1.8rem;
    }
}

@media (max-width: 768px) {
    .hero-section {
        padding: 2rem 1rem;
    }

    .hero-content h1 {
        font-size: 2rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        padding: 0 1rem;
    }

    .info-section {
        margin-top: -1rem;
        padding: 0 1rem;
        gap: 1.5rem;
    }

    .info-card {
        padding: 1.5rem;
    }

    .action-section {
        margin-top: 3rem;
        padding: 2rem 1rem;
    }
}

@media (max-width: 480px) {
    .hero-section {
        padding: 1.5rem 0.8rem;
    }

    .hero-content h1 {
        font-size: 1.8rem;
    }

    .hero-subtitle {
        font-size: 0.9rem;
        padding: 0 0.5rem;
    }

    .info-section {
        margin-top: -0.5rem;
        padding: 0 0.8rem;
        gap: 1rem;
    }

    .action-section {
        margin-top: 2rem;
        padding: 1.5rem 0.8rem;
    }
}
</style>