import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Подключаем маршрутизатор

// Подключаем Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';

library.add(fas);

const app = createApp(App);
app.use(router);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');
