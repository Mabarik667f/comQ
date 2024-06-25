import { addWebSocket, getWebSocketById } from '@/hooks/wsHooks/websockets';
import Cookies from 'js-cookie';
import getUserDataOnChat from '@/hooks/getUserDataOnChat';
import groupChatDetail from '@/hooks/chatHooks/groupChatDetail';
import store from '@/store';
import { ref } from 'vue';

const addUser = ref('');

async function getAddedUser(chat, userData) {
    if (typeof(chat.current_users[0]) === 'string') {
        addUser.value = chat.current_users.filter(c => c !== userData)[0];
    } else {
        addUser.value = chat.current_users.filter(c => c.username !== userData)[0].username;
    }
}

export default async function cleanChatData(chat, userData) {
    if (chat.chat_type === 'P') {
        await getAddedUser(chat, userData)
        const {userData: partnerData} = await getUserDataOnChat(addUser.value);
        chat.partner = partnerData.value;
    } else {
        const {chatData: groupSettings} = await groupChatDetail(chat.pk);
        chat.groupSettings = groupSettings.value.group_settings;
    }
    if (!getWebSocketById(chat.pk)) {
        const ws = new WebSocket(`ws://localhost:8000/ws/chat/${chat.pk}/?token=${Cookies.get("access")}`);
        addWebSocket(chat.pk, ws);
    }

    store.commit('updateChats', {chat: chat})
    
}