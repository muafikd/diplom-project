<script setup>
import { Bar, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

// Данные о распределении диабета в датасете
const diabetesDistribution = {
  type: 'pie',
  data: {
    labels: ['Нет диабета', 'Есть диабет'],
    datasets: [{
      data: [65.1, 34.9], // Процентное соотношение в датасете PIMA
      backgroundColor: ['#2ecc71', '#e74c3c'],
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      },
      title: {
        display: true,
        text: 'Распределение диабета в исследовании'
      }
    }
  }
};

// Средние значения показателей
const averageMetrics = {
  type: 'bar',
  data: {
    labels: ['Глюкоза', 'Давление', 'ИМТ', 'Возраст'],
    datasets: [{
      label: 'Без диабета',
      data: [109.8, 68.2, 30.9, 31.2],
      backgroundColor: '#2ecc71',
    },
    {
      label: 'С диабетом',
      data: [141.3, 70.8, 35.4, 37.1],
      backgroundColor: '#e74c3c',
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      },
      title: {
        display: true,
        text: 'Сравнение средних показателей'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
};

// Распределение по возрастным группам
const ageDistribution = {
  type: 'bar',
  data: {
    labels: ['21-30', '31-40', '41-50', '51-60', '61+'],
    datasets: [{
      label: 'Количество случаев',
      data: [230, 290, 115, 80, 35],
      backgroundColor: '#3498db',
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      },
      title: {
        display: true,
        text: 'Распределение по возрастным группам'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
};

// Добавляем данные мировой статистики
const worldStats = {
  type: 'bar',
  data: {
    labels: ['2000', '2010', '2021', '2030 (прогноз)', '2045 (прогноз)'],
    datasets: [{
      label: 'Миллионы людей с диабетом',
      data: [151, 285, 537, 643, 783],
      backgroundColor: '#9b59b6',
      borderColor: '#8e44ad',
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      },
      title: {
        display: true,
        text: 'Рост числа людей с диабетом в мире'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Миллионы человек'
        }
      }
    }
  }
};
</script>

<template>
    <div class="dataset-visuals">
        <div class="world-stats-section">
            <h2><i class="fas fa-globe"></i> Диабет в мире</h2>
            <div class="stats-cards">
                <div class="stat-card">
                    <div class="stat-number">537 млн</div>
                    <div class="stat-label">людей живут с диабетом (2021)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">33.5 трлн ₸</div>
                    <div class="stat-label">расходы на лечение диабета в год</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">1 из 2</div>
                    <div class="stat-label">людей с диабетом не знают о своём диагнозе</div>
                </div>
            </div>
            
            <div class="chart-container world-chart">
                <Bar :data="worldStats.data" :options="worldStats.options" />
                <p class="chart-description">
                    По данным Международной федерации диабета (IDF), количество людей с диабетом 
                    стремительно растёт. К 2045 году ожидается увеличение числа больных до 783 миллионов человек.
                </p>
            </div>
        </div>

        <h2><i class="fas fa-chart-pie"></i> Данные исследования PIMA</h2>
        
        <div class="charts-grid">
            <div class="chart-container">
                <h3>Распространенность диабета</h3>
                <Pie :data="diabetesDistribution.data" :options="diabetesDistribution.options" />
                <p class="chart-description">
                    В исследовании приняли участие 768 женщин из племени пима. 
                    У 34.9% был диагностирован диабет.
                </p>
            </div>

            <div class="chart-container">
                <h3>Ключевые показатели</h3>
                <Bar :data="averageMetrics.data" :options="averageMetrics.options" />
                <p class="chart-description">
                    Сравнение средних показателей у людей с диабетом и без. 
                    Заметна существенная разница в уровне глюкозы и ИМТ.
                </p>
            </div>

            <div class="chart-container">
                <h3>Возрастные группы</h3>
                <Bar :data="ageDistribution.data" :options="ageDistribution.options" />
                <p class="chart-description">
                    Большинство участников исследования были в возрасте 21-40 лет, 
                    что делает результаты особенно актуальными для этой возрастной группы.
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dataset-visuals {
    margin-top: 3rem;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dataset-visuals h2 {
    color: #2c3e50;
    font-size: 1.8rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.dataset-visuals h2 i {
    color: #3498db;
}

.charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.chart-container {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
}

.chart-container h3 {
    color: #2c3e50;
    margin-bottom: 1.5rem;
    font-size: 1.2rem;
}

.chart-description {
    margin-top: 1.5rem;
    color: #666;
    font-size: 0.95rem;
    line-height: 1.6;
    text-align: left;
}

.world-stats-section {
    margin-bottom: 4rem;
    padding-bottom: 2rem;
    border-bottom: 2px solid #e0e0e0;
}

.stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    transition: transform 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-card:hover {
    transform: translateY(-5px);
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 1rem;
    opacity: 0.9;
    line-height: 1.4;
}

.world-chart {
    margin-top: 2rem;
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
    .dataset-visuals {
        padding: 1rem;
    }

    .charts-grid {
        grid-template-columns: 1fr;
    }

    .stats-cards {
        grid-template-columns: 1fr;
    }
    
    .stat-card {
        padding: 1.2rem;
    }

    .stat-number {
        font-size: 1.8rem;
    }
}
</style> 