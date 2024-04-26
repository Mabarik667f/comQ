import router from "@/router";
import axios from "axios";
import Cookies from "js-cookie";
import {baseHeaders} from "@/headers/baseHeaders";


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
        login({dispatch}, formData) {
            axios.post('v1/users/login/', {
                username: formData.login,
                password: formData.password
            },
            {
                headers: {
                    ...baseHeaders
                }
            })
            .then(response => {
                if (response.status === 200) {
                    Cookies.set('access', response.data.access);
                    Cookies.set('refresh', response.data.refresh);

                    Cookies.set('isAuth', true);
                    dispatch('setIsAuth');
                    router.push('/');

                }
            })
            .catch(error => {
                console.log(error);
            })

        },

        logout({dispatch}) {
            axios.post('v1/users/logout/', {
                refresh: Cookies.get('refresh')
            },
            {
                headers: {
                    ...baseHeaders
                }
            })
            .then(response => {
                if (response.status === 201) {
                    Cookies.remove('access');
                    Cookies.remove('refresh');

                    Cookies.set('isAuth', false);
                    dispatch('setIsAuth');
                }

            })
            .catch(error => {
                console.log(error);
            })

        },

        refreshToken({dispatch}) {
            axios.post('v1/users/refresh/', {
                refresh: Cookies.get('refresh')
            },
            {
                headers: {
                    ...baseHeaders
                }
            })
            .then(response => {
                if (response.status === 201) {
                    Cookies.set('access', response.data.access);
                } else {
                    dispatch('logout');
                }
            })
            .catch(error => {
                console.log(error);
            })
        },
        async verifyToken({dispatch}) {
            if(Cookies.get('access')) {
                
                try {
                    const response = await axios.post('v1/users/login/verify/', {
                      token: Cookies.get('access')
                    }, {
                      headers: {
                        ...baseHeaders
                      }
                    });
                    
                    if (response.status === 200) {
                      return true;
                    } else if (response.status !== 401){
                      dispatch('refreshToken');
                    }
                  } catch {
                    dispatch('logout');
                    return false
                  }
            }
        },

        setIsAuth({commit}) {
            commit('setAuth', {isAuth: Cookies.get('isAuth')});
        }
        
    }
}