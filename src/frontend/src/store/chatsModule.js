import router from "@/router";
import Cookies from "js-cookie"

export const chatsModule = {
    state: () => ({
        chats: [],
        hub: new WebSocket(`ws://localhost:8000/ws/hub/?token=${Cookies.get("access")}`)
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
        }
    },
    mutations: {
        setChats(state, {chats}) {
            state.chats = chats
        },
        updateChats(state, {chat}) {
            state.chats.unshift(chat);
        },
        deleteChat(state, {chatId}) {
            state.chats = state.chats.filter(chat => chat.pk !== chatId);
            router.push('/')
        },
        updateChatData(state, {chatId, data}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                for (let attr of data) {
                    console.log(attr)
                }
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
        addUserInChat(state, {user, chatId}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                chat.current_users.push(user);
            }
        },
        deleteUserInChat(state, {user, chatId}) {
            const chat = state.chats.find(chat => chat.pk === chatId);
            if (chat) {
                chat.current_users = chat.current_users.filter(u => u.id !== user.id);
            }
        },
    },
    actions: {
        initializeChats({commit}, {chats}) {
            commit('setChats', {chats: chats})
        },
        addUser({commit, getters}, {user, chatId, chat}) {
            commit('addUserInChat', {user: user, chatId: chatId})
            console.log(getters.getUserName)
            if (getters.getUserName === user.username) {
                console.log(1)
                commit('updateChats', {chat: chat})
            }
        },
        deleteUser({commit}, {user, chatId}) {
            commit('deleteUserInChat', {user: user, chatId: chatId})
        },
        leaveUser({commit}, {user, chatId}) {
            commit('deleteUserInChat', {user: user, chatId: chatId})
        }
    }
}