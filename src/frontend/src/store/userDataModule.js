export const userDataModule = {
    state: () => ({
        username: '',
        id: '',
        relatedUsers: []
    }),

    getters: {
        username: state => state.username,
        id: state => state.id,
        relatedUsers: state => state.relatedUsers
    },

    mutations: {
        setUserData(state, {username, id}) {
            state.username = username;
            state.id = id;
        },
        addRelatedUserMutation(state, {user}) {
            state.relatedUsers.push(user)
        }
    },

    actions: {
        addRelatedUser({commit}, {user}) {
            commit('addRelatedUserMutation', {user: user})
        }
    }
}