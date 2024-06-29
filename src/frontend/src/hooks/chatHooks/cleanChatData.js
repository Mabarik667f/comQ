import Cookies from 'js-cookie';
import getUserDataOnChat from '@/hooks/getUserDataOnChat';
import groupChatDetail from '@/hooks/chatHooks/groupChatDetail';
import { ref } from 'vue';
import store from '@/store';

const addUser = ref('');

async function getAddedUser(chat) {
    if (typeof(chat.current_users[0]) === 'string') {
        addUser.value = chat.current_users.filter(c => c !== store.getters.getUserName)[0];
    } else {
        addUser.value = chat.current_users.filter(c => c.username !== store.getters.getUserName)[0].username;
    }
}

export default async function cleanChatData(chat) {
    if (chat.chat_type === 'P') {
        await getAddedUser(chat)
        const {userData: partnerData} = await getUserDataOnChat(addUser.value);
        chat.partner = partnerData.value;
    } else {
        const {chatData: groupSettings} = await groupChatDetail(chat.pk);
        chat.groupSettings = groupSettings.value.group_settings;
    }

    if (!store.getters.getWebSocketById(chat.pk) && !store.getters.getChat(chat.pk)) {
        console.log(chat)
        const ws = new WebSocket(`ws://localhost:8000/ws/chat/${chat.pk}/?token=${Cookies.get("access")}`);
        store.commit('updateWebsockets', {id: chat.pk, ws: ws});
        store.commit('updateChats', {chat: chat})
    }
    
}