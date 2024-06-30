import cleanChatData from "@/hooks/chatHooks/cleanChatData";
import router from "@/router";
import Cookies from "js-cookie"

export const chatsModule = {
    state: () => ({
        chats: [],
        hub: new WebSocket(`ws://localhost:8000/ws/hub/?token=${Cookies.get("access")}`),
        websockets: {}
    }),
    getters: {
        getChats(state) {
            return state.chats
        },
        getChat: (state) => (pk) => {
            const chat = state.chats.find(chat => chat.pk === parseInt(pk));
            return chat
        },
        getHub(state) {
            return state.hub
        },
        getMessages: (state) => (pk) => {
            const chat = state.chats.find(chat => chat.pk === parseInt(pk));
            if (chat) {
                return chat.messages
            }
        },
        getWebSockets(state) {
            return state.websockets
        },
        getWebSocketById: (state) => (id) => {
            return state.websockets[id]
        }
    },
    mutations: {
        setChats(state, {chats}) {
            state.chats = chats
        },

        updateWebsockets(state, {id, ws}) {
            state.websockets[id] = ws
        },

        updateChats(state, {chat}) {
            state.chats.unshift(chat);
        },

        clearNotifications(state, {chatId}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            chat.notifications = 0
        },
        
        addMessage(state, {chatId, message}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            chat.messages.push(message)
        },

        deleteMessage(state, {chatId, index}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            console.log(index)
            chat.messages.splice(index, 1);
            console.log(1)
        },
        editMessage(state, {chatId, message}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            const index = chat.messages.findIndex(m => m.id === message.id);
            chat.messages[index].text_content = message.text_content
        },

        deleteChat(state, {chatId}) {
            state.chats = state.chats.filter(chat => chat.pk !== chatId);
            delete state.websockets[chatId]
            router.push('/')
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

        addUserInChat(state, {user, chatId}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                chat.current_users.push(user);
            }
        },

        deleteUserInChat(state, {user, chatId}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            console.log(chat.current_users)
            if (chat) {
                chat.current_users = chat.current_users.filter(u => u.id !== user.id);
                console.log(chat.current_users)
            }
        },
    },
    actions: {
        initializeChats({commit}, {chats}) {
            commit('setChats', {chats: chats})
        },

        async addUser({commit, getters}, {user, chatId, chat}) {
            commit('addUserInChat', {user: user, chatId: chatId})
            if (getters.getUserName === user.username) {
                await cleanChatData(chat)
            }
        },

        deleteUser({commit}, {user, chatId}) {
            commit('deleteUserInChat', {user: user, chatId: chatId})
        },

        leaveUser({commit}, {user, chatId}) {
            commit('deleteUserInChat', {user: user, chatId: chatId})
        },

        addMessage({state, commit}, {chatId, message}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                commit('addMessage', {chatId: chatId, message: message})
            }
            commit('updateLastMessage', {chatId: chatId, message: message})

        },
        deleteMessage({state, commit}, {chatId, message}) {

            const chat = state.chats.find(chat => chat.pk === chatId);
            const index = chat.messages.findIndex(m => m.id === message.id);
            if (index === chat.messages.length - 1) {
                let messageVal;
                if (index - 1 >= 0) {
                    messageVal = chat.messages[index - 1]
                } else {
                    messageVal = null
                }
                commit('updateLastMessage', {chatId: chatId, message: messageVal})
            }
            commit('deleteMessage', {chatId: chatId, index: index})

        },
        editMessage({state, commit}, {chatId, message}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            const index = chat.messages.findIndex(m => m.id === message.id);
            commit('editMessage', {chatId: chatId, message: message})
        
            if (index === chat.messages.length - 1) {
                commit('updateLastMessage', {chatId: chatId,
                message: message})
            }
        },
    }
}