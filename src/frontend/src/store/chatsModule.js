export const chatsModule = {
    state: () => ({
        chats: []
    }),
    getters: {
        getChats(state) {
            return state.chats
        }
    },
    mutations: {
        setChats(state, {chats}) {
            state.chats = chats
        },
        updateNotifications(state, {chatId}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                chat.notifications = chat.notifications + 1
            }
        }
    },
    actions: {
        initializeChats({commit}, {chats}) {
            commit('setChats', {chats: chats})
        }
    }
}