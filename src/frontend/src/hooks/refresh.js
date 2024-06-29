import Cookies from 'js-cookie';
import {baseHeaders} from "@/headers/baseHeaders";
import router from '@/router';
import store from '@/store';
import axios from 'axios';
export default async function refresh() {
    console.log(1)
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
        }
    } catch (refreshError) {
        store.dispatch('clearAuth')
        router.push('/login')
    }
}