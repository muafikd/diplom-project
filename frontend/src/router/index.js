import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Predict from '../views/Predict.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Profile from '@/views/Profile.vue';
import Education from '@/views/Education.vue';

const routes = [
    { path: '/', component: Home },
    { path: '/predict', component: Predict },
    { path: '/login', component: Login},
    { path: '/register', component: Register},
    { path: '/profile', component: Profile},
    { path: '/education', component: Education},
    {
        path: '/prevention',
        name: 'Prevention',
        component: () => import('../views/Prevention.vue')
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
