import axios from 'axios';
import Cookies from 'js-cookie';
import {baseHeaders} from "@/headers/baseHeaders";
import router from './router';
import store from './store';

const axiosInstance = axios.create({
    headers: {
        ...baseHeaders,
    }
});

axiosInstance.interceptors.request.use(
    config => {
        const token = Cookies.get('access');
        store.dispatch('checkTokenLifeTime')
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const response = await axios.post('/v1/users/login/refresh/', {
                    refresh: Cookies.get('refresh')
                }, {
                    headers: {
                        ...baseHeaders,
                    }
                });

                if (response.status === 200) {
                    Cookies.set('access', response.data.access);
                    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
                    return axiosInstance(originalRequest);
                }
            } catch (refreshError) {
                store.dispatch('clearAuth')
                router.push('/login')
            }
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;
