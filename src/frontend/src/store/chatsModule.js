export const chatsModule = {
    state: () => ({
        chats: []
    }),
    getters: {
        getChats(state) {
            return state.chats
        },
        getChat: (state) => (pk) => {
            const chat = state.chats.find(chat => chat.pk === parseInt(pk));
            return chat
        }
    },
    mutations: {
        setChats(state, {chats}) {
            state.chats = chats
        },
        updateChats(state, {chat}) {
            state.chats.unshift(chat);
        },
        updateChatData(state, {chatId, data}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            console.log(state.chats)
            if (chat) {
                for (let attr of data) {
                    console.log(attr)
                }
                // chat.value = data;
                console.log(chat)
            }
            console.log(state.chats)
        },
        updateNotifications(state, {chatId, status}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                if (status === 'del') {
                    chat.notifications = chat.notifications > 0 ? chat.notifications - 1: chat.notifications
                } else if (status == 'add') {
                    chat.notifications = chat.notifications + 1
                }
            }
        },

        updateLastMessage(state, {chatId, message}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                if (message !== null) {
                    for (const attr in message) {
                        chat.last_message[attr] = message[attr];
                    }
                } else {
                    for (const attr in chat.last_message) {
                        chat.last_message[attr] = null;
                    }
                    chat.last_message['text_content'] = 'Чат создан'
                }
            }
        },
        updateGroupAvatar(state, {chatId, avatar}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat && chat.chat_type === 'G') {
                const spl = avatar.split('/')
                chat.groupSettings.avatar = `/${spl.slice(3).join('/')}`;
            }
        },
        updateGroupTitle(state, {chatId, title}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat && chat.chat_type === 'G') {
                chat.groupSettings.title = title;
            }
        },
        addRelatedUserInChat(state, {user, chatId}) {
            console.log(user)
            const chat = state.chats.find(chat => chat.pk === chatId);
            console.log(chat)
        },
        deleteUserInChat(state, {user, chatId}) {
            console.log(user)
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                // const current_users = chat.current_users.find(u => u.pk ===)
            }
            console.log(chat)
        },
    },
    actions: {
        initializeChats({commit}, {chats}) {
            commit('setChats', {chats: chats})
        },
        addUser({commit}, {user}) {
            commit('addRelatedUserInChat', {user: user})
        },
        deleteUser({commit}, {user, chatId}) {
            commit('deleteUserInChat', {user: user, chatId: chatId})
        }
    }
}