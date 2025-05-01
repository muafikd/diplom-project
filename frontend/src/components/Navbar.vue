<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlusCircle, faHome, faBookMedical, faShieldAlt, faChartLine, faUser, faSignOutAlt, faSignInAlt } from '@fortawesome/free-solid-svg-icons';

const router = useRouter();
const isAuthenticated = ref(!!localStorage.getItem("access"));
const isMobileMenuOpen = ref(false);

const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh"); // ❗ Удаляем и refresh тоже
    isAuthenticated.value = false;
    window.location.href = "/"; // Теперь точно обновится состояние
};

const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
    isMobileMenuOpen.value = false;
};
</script>


<template>
    <nav class="navbar">
        <div class="navbar-container">
            <div class="navbar-brand">
                <font-awesome-icon :icon="faPlusCircle" class="brand-icon" />
            </div>

            <!-- Кнопка мобильного меню -->
            <button class="mobile-menu-button" @click="toggleMobileMenu">
                <font-awesome-icon :icon="isMobileMenuOpen ? 'times' : 'bars'" />
            </button>

            <div class="navbar-links" :class="{ 'mobile-menu-open': isMobileMenuOpen }">
                <router-link to="/" class="nav-link" @click="closeMobileMenu">
                    <font-awesome-icon :icon="faHome" />
                    <span>Главная</span>
                </router-link>
                <router-link to="/education" class="nav-link" @click="closeMobileMenu">
                    <font-awesome-icon :icon="faBookMedical" />
                    <span>Информация</span>
                </router-link>
                <router-link to="/prevention" class="nav-link" @click="closeMobileMenu">
                    <font-awesome-icon :icon="faShieldAlt" />
                    <span>Профилактика</span>
                </router-link>
                <router-link to="/predict" class="nav-link" @click="closeMobileMenu">
                    <font-awesome-icon :icon="faChartLine" />
                    <span>Тест</span>
                </router-link>
                <router-link v-if="isAuthenticated" to="/profile" class="nav-link" @click="closeMobileMenu">
                    <font-awesome-icon :icon="faUser" />
                    <span>Профиль</span>
                </router-link>

                <button v-if="isAuthenticated" @click="logout" class="logout-button">
                    <font-awesome-icon :icon="faSignOutAlt" />
                    <span>Выйти</span>
                </button>
                <router-link v-else to="/login" class="nav-link" @click="closeMobileMenu">
                    <font-awesome-icon :icon="faSignInAlt" />
                    <span>Войти</span>
                </router-link>
            </div>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 0.8rem 1rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    width: 100%;
}

.navbar-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    color: #3498db;
}

.brand-icon {
    font-size: 2.5rem;
    color: #e74c3c;
    display: inline-block;
}

.brand-name {
    font-size: 1.3rem;
    font-weight: 600;
    color: #2c3e50;
}

.navbar-links {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.nav-link,
.logout-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    color: #7f8c8d;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    transition: all 0.3s ease;
    background: none;
    border: none;
    cursor: pointer;
    white-space: nowrap;
}

.nav-link font-awesome-icon,
.logout-button font-awesome-icon {
    font-size: 1.1rem;
}

.nav-link:hover,
.logout-button:hover {
    color: #3498db;
    background: rgba(52, 152, 219, 0.1);
    transform: translateY(-2px);
}

.router-link-active {
    color: #3498db;
    background: rgba(52, 152, 219, 0.1);
}

.mobile-menu-button {
    display: none;
    background: none;
    border: none;
    color: #2c3e50;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
}

@media (max-width: 1024px) {
    .navbar-links {
        gap: 1rem;
    }
    
    .nav-link,
    .logout-button {
        padding: 0.5rem 0.8rem;
    }
}

@media (max-width: 768px) {
    .mobile-menu-button {
        display: block;
    }

    .navbar-links {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        flex-direction: column;
        background: white;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        gap: 0.5rem;
    }

    .navbar-links.mobile-menu-open {
        display: flex;
    }

    .nav-link,
    .logout-button {
        width: 100%;
        justify-content: flex-start;
        padding: 0.8rem 1rem;
    }

    .nav-link span,
    .logout-button span {
        display: inline-block;
    }

    .brand-icon {
        font-size: 2rem;
    }
}

@media (max-width: 480px) {
    .navbar {
        padding: 0.5rem;
    }

    .navbar-container {
        padding: 0 0.5rem;
    }

    .brand-icon {
        font-size: 1.8rem;
    }

    .mobile-menu-button {
        font-size: 1.3rem;
    }

    .nav-link,
    .logout-button {
        padding: 0.7rem 0.8rem;
        font-size: 0.9rem;
    }
}
</style>
