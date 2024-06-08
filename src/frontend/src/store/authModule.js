import axiosInstance from "@/axiosInstance";
import Cookies from "js-cookie";
import router from "@/router";

export const authModule = {

    state: () => ({
        isAuth: false,
    }),

    getters: {
        isAuth: state => state.authModule.isAuth,
    },

    mutations: {
        setAuth(state, {isAuth}) {
            state.isAuth = isAuth;
        }
    },

    actions: {
        async login({dispatch}, {formData}) {
            try {
                const response = await axiosInstance.post('/v1/users/login/', {
                    username: formData.login.trim(),
                    password: formData.password.trim()
                })
                if (response.status === 200) {
                    Cookies.set('access', response.data.access);
                    Cookies.set('refresh', response.data.refresh);

                    Cookies.set('isAuth', true);
                    dispatch('setIsAuth');
                    router.push('/');

                }
            }
            catch(error) {
                console.log(error);
                throw error;
            }

        },

        logout({dispatch}) {
            if (Cookies.get('access')) {
                axiosInstance.post('/v1/users/logout/', {
                    refresh: Cookies.get('refresh')
                })
                .then(response => {
                    if (response.status === 204) {
                        dispatch('clearAuth');
                        router.push('/login')
                    }

                })
                .catch(error => {
                    console.log(error);
                    dispatch('clearAuth');
                    router.push('/login')
                })
            }

        },

        setIsAuth({commit}) {
            if (!Cookies.get('isAuth')) {
                Cookies.set('isAuth', false);
            }

            const isAuthValue = Cookies.get('isAuth');
            const val = isAuthValue === 'true';
            commit('setAuth', {isAuth: val});
        },

        clearAuth({dispatch}) {
            Cookies.remove('access');
            Cookies.remove('refresh');
            Cookies.set('isAuth', false);
            dispatch('setIsAuth');
            dispatch('clear')
        }
        
    }
}