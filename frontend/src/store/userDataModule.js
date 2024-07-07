export const userDataModule = {
    state: () => ({
        username: "",
        id: "",
        relatedUsers: [],
        currentChatRole: 'D',
        isOnline: false,
        errors: {
            newPrivateChat: "",
            newGroupChat: ""
        },
        sidebarWidth: 0
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
        },
        getCreateErrors(state) {
            return state.errors
        },
        getSidebarWidth(state) {
            return state.sidebarWidth
        }
    },

    mutations: {
        setUserData(state, {username, id}) {
            state.username = username;
            state.id = id;
        },
        updateSidebarWidth(state, {width}) {
            state.sidebarWidth = width
        },
        addRelatedUserMutation(state, {user}) {
            state.relatedUsers.push(user)
        },
        deleteUserMutation(state, {user}) {
            state.relatedUsers = state.relatedUsers.filter(u => u.id !== user.id)
        },
        setUserRole(state, {role}) {
            state.currentChatRole = role;
        },
        updateCreatePrivateError(state, {error}) {
            state.errors.newPrivateChat = error
        },
        updateCreateGroupError(state, {error}) {
            state.errors.newGroupChat = error
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