export const userDataModule = {
    state: () => ({
        username: '',
        id: '',
        relatedUsers: []
    }),

    getters: {
        getUserName(state) {
            return state.username;
        },
        getRelatedUsers(state) {
        return state.relatedUsers;
        }
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