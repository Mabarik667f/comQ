export const userDataModule = {
    state: () => ({
        username: '',
        id: ''
    }),

    getters: {
        username: state => state.username,
        id: state => state.id
    },

    mutations: {
        setUserData(state, {username, id}) {
            state.username = username;
            state.id = id;
        }
    }
}