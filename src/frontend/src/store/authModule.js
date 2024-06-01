import axios from "axios";
import Cookies from "js-cookie";
import {baseHeaders} from "@/headers/baseHeaders";
import {authHeaders} from "@/headers/authHeaders";


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
                const response = await axios.post('v1/users/login/', {
                    username: formData.login.trim(),
                    password: formData.password.trim()
                },
                {
                    headers: {
                        ...baseHeaders,
                        ...authHeaders
                    }
                })
                if (response.status === 201) {
                    Cookies.set('access', response.data.access);
                    Cookies.set('refresh', response.data.refresh);

                    Cookies.set('isAuth', true);
                    dispatch('setIsAuth');

                }
            }
            catch(error) {
                console.log(error);
                throw error;
            }

        },

        logout({dispatch}) {
            if (Cookies.get('access')) {
                axios.post('v1/users/logout/', {
                    refresh: Cookies.get('refresh')
                },
                {
                    headers: {
                        ...baseHeaders,
                        ...authHeaders
                    }
                    
                })
                .then(response => {
                    if (response.status === 200) {
                        Cookies.remove('access');
                        Cookies.remove('refresh');
                    }

                })
                .catch(error => {
                    console.log(error);
                })
            }
            Cookies.set('isAuth', false);
            dispatch('setIsAuth');
            window.location.reload();

        },

        async refreshToken({dispatch}) {
            try {
                const response = await axios.post('v1/users/login/refresh/', {
                    refresh: Cookies.get('refresh')
                },
                {
                    headers: {
                        ...baseHeaders,
                        ...authHeaders
                    }
                })
                
                if (response.status === 200) {
                    Cookies.set('access', response.data.access);
                }
            
            }
            catch{
                dispatch('logout');
            }
        },
        async verifyToken({dispatch}) {
            if(Cookies.get('access')) {
                try {
                    await axios.post('v1/users/login/verify/', {
                      token: Cookies.get('access')
                    }, {
                      headers: {
                        ...baseHeaders,
                        ...authHeaders
                      }
                    });
                  } catch {
                        dispatch('refreshToken');
                  }
            }
        },

        setIsAuth({commit}) {
            if (!Cookies.get('isAuth')) {
                Cookies.set('isAuth', false);
            }

            const isAuthValue = Cookies.get('isAuth');
            const val = isAuthValue === 'true';
            commit('setAuth', {isAuth: val});
        }
        
    }
}