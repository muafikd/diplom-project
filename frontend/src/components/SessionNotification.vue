<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { authEvents } from '../services/authService';

const notification = ref({
    show: false,
    message: ''
});

const showNotification = (event) => {
    notification.value = {
        show: true,
        message: event.detail
    };

    // Автоматически скрываем через 5 секунд
    setTimeout(() => {
        notification.value.show = false;
    }, 5000);
};

onMounted(() => {
    authEvents.addEventListener('session-expired', showNotification);
});

onUnmounted(() => {
    authEvents.removeEventListener('session-expired', showNotification);
});
</script>

<template>
    <transition name="session-notification">
        <div v-if="notification.show" class="session-notification">
            <i class="fas fa-clock"></i>
            {{ notification.message }}
        </div>
    </transition>
</template>

<style scoped>
.session-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    background: #2c3e50;
    color: white;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-weight: 500;
    z-index: 2000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    animation: slideIn 0.3s ease;
}

.session-notification i {
    color: #f39c12;
}

.session-notification-enter-active,
.session-notification-leave-active {
    transition: all 0.3s ease;
}

.session-notification-enter-from,
.session-notification-leave-to {
    transform: translateX(100%);
    opacity: 0;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
</style> 