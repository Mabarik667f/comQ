import axios from "axios";

export const authModule = {
    state: () => ({
        isAuth: false,
        username: ''
    }),

    getters: {
        isAuth: state => state.authModule.isAuth,
        username: state => state.authModule.username
    },

    mutations: {
        setAuth(state, {isAuth, username}) {
            state.isAuth = isAuth;
            state.username = username;
        }
    },

    actions: {
        login({commit}, formData) {
            
            axios.post('v1/login/', {
                email: formData.email,
                password: formData.password
            },
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                console.log(response);
                commit('setAuth', {isAuth: true, username: ''});
                // redirect
            })
            .catch(error => {
                console.log(error);
            })

        },

        logout({commit}) {
            commit('setAuth', {isAuth: false, username: ''})
        },

        refreshToken() {

        },
        verifyToken() {

        }
        
    }
}