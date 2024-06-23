export const userDataModule = {
    state: () => ({
        username: '',
        id: '',
        relatedUsers: [],
        currentChatRole: 'D'
    }),

    getters: {
        getUserName(state) {
            return state.username;
        },
        getRelatedUsers(state) {
        return state.relatedUsers;
        },
        getUserRole(state) {
            return state.currentChatRole
        }
    },

    mutations: {
        setUserData(state, {username, id}) {
            state.username = username;
            state.id = id;
        },
        addRelatedUserMutation(state, {user}) {
            state.relatedUsers.push(user)
        },
        setUserRole(state, {role}) {
            state.currentChatRole = role;
        }
    },

    actions: {
        addRelatedUser({commit}, {user}) {
            commit('addRelatedUserMutation', {user: user})
        }
    }
}