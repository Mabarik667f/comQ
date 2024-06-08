<script>
import ChatsHeader from '@/components/ChatsHeader.vue';
import ChatCard from '@/components/UI/ChatCard.vue';
import { mapActions, useStore } from 'vuex';
import getUserData from '@/hooks/getUserData';
import { ref, onMounted } from 'vue';
import getChatCardData from '@/hooks/chatHooks/getChatCardData';
import router from '@/router';
import { addWebSocket } from '@/hooks/wsHooks/websockets';
import Cookies from 'js-cookie';

export default {
    components: {
        ChatsHeader,
        ChatCard,
        
    },
    setup() {
        const chats = ref([]);
        const usersChoices = ref([]);
        const store = useStore();

        onMounted(async () => {
            const {asyncCall} = getUserData();
            const {userData} = await asyncCall();

            for (let chat of userData.value.chats) {
                if (chat.chat_type === 'P') {
                    const addUser = chat.current_users.filter(c => c !== userData.value.username)[0];
                    usersChoices.value.push({value: addUser,name: addUser})
                    const {chatData: partnerData} = await getChatCardData(addUser);
                    chat.partner = partnerData.value;
                    chats.value.push(chat);
                } else {
                    const {chatData: groupSettings} = await getChatCardData(chat.pk);
                    chat.groupSettings = groupSettings.value;
                    chats.value.push(chat);
                }
                const ws = new WebSocket(`ws://localhost:8000/ws/chat/${chat.pk}/?token=${Cookies.get("access")}`)
                addWebSocket(chat.pk, ws)

            }
        })

        const selectChat = async (chat) => {
            const title = ref('');
            const imagePath = ref('');
            if(chat.partner) {
                title.value = chat.partner.name;
                imagePath.value = chat.partner.img;
            } else {
                title.value = chat.groupSettings.group_settings.title;
                imagePath.value = chat.groupSettings.group_settings.avatar;
            }
            store.commit('setChatData', {title: title.value, imagePath: imagePath.value})
            store.dispatch('setChatDataCookies', {title: title.value, imagePath: imagePath});
            router.push({ name: 'chat-detail', params: { pk: chat.pk }});
        }
        return {chats, usersChoices, selectChat}
    },
    methods: {
    ...mapActions({
            logout: 'logout'
    })
  }
}
</script>

<template>
    <div class="chats">
        <ChatsHeader :options="usersChoices"></ChatsHeader>
        <div class="short-chat" v-for="chat in chats" :key="chat.pk">
            <ChatCard :chat="chat" @click="selectChat(chat)"></ChatCard>
        </div>
        <com-button
        @click="$router.push('/register')">Зарегистрироваться</com-button>
        <com-button
        @click="$router.push('/login')">Войти</com-button>
        <com-button @click.prevent="logout">Выйти</com-button>
    </div>
</template>

<style scoped>
.chats {
    background-color: black;
    height: 100vh;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: flex-start;
    justify-content: flex-start;
    align-items: flex-start;
    width: 500px;
    max-width: 900px;
    overflow: auto;
}

.short-chat {
    /* box-shadow: 0 0 10px rgba(255, 69, 0, 0.5);  */
    display: flex;
    width: 100%;
    margin: 10px 0;
    color: whitesmoke;
    border-radius: 15px;
}

.short-chat:hover {
    background-color: rgba(255, 255, 255, 0.2); /* осветление при наведении */
}
</style>
