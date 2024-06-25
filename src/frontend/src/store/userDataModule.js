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
        deleteUserMutation(state, {user}) {
            state.relatedUsers = state.relatedUsers.filter(u => u.id !== user.id)
        },
        setUserRole(state, {role}) {
            state.currentChatRole = role;
        }
    },

    actions: {
        addRelatedUser({commit}, {user}) {
            commit('addRelatedUserMutation', {user: user})
        },
        deleteUser({commit}, {user}) {
            commit('deleteUserMutation', {user: user})
        }
    }
}