<script>
import ChatsHeader from '@/components/ChatsHeader.vue';
import ChatCard from '@/components/UI/ChatCard.vue';
import { useStore } from 'vuex';
import getUserData from '@/hooks/getUserData';
import cleanChatData from "@/hooks/chatHooks/cleanChatData"
import { computed, ref, onMounted } from 'vue';
import router from '@/router';


export default {
    components: {
        ChatsHeader,
        ChatCard,
        
    },
    
    setup() {
        const store = useStore();
        const chats = computed(() => store.getters.getChats);
        const userData = ref();
        const chatsLength = ref(0);
        
        // const getUserDataHook = async () => {
        //     const {asyncCall} = getUserData();
        //     const {userData: data} = await asyncCall();
        //     userData.value = data.value;
        //     chatsLength.value = userData.value.chats.length
        // }
        const reloadChats = async () => {
            const {asyncCall} = getUserData();
            const {userData: data} = await asyncCall();
            userData.value = data.value;
            chatsLength.value = data.value.chats.length
            for (let chat of data.value.chats) {
                await cleanChatData(chat, data.value.username)
            }
        }

        const selectChat = async (chat) => {
            router.push({ name: 'chat-detail', params: { pk: chat.pk }});
        }

        onMounted(async () => {
            await reloadChats();
        });

        
        const { relatedUsers } = store.state.userData;
        return {chats, selectChat, relatedUsers, userData}
    },
}
</script>

<template>
    <div class="chats">
        <ChatsHeader :options="relatedUsers" :userData="userData"></ChatsHeader>
        <div class="short-chat" v-for="chat in chats" :key="chat">
            <ChatCard :chat="chat" @click="selectChat(chat)"></ChatCard>
        </div>
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
    min-width: 200px;
    width: 300px;
    max-width: 500px;
    overflow: scroll;
    resize: horizontal;
    position: relative;
}

.chats::after{
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    width: 10px;
    cursor: ew-resize;
}

.short-chat {
    /* box-shadow: 0 0 10px rgba(255, 69, 0, 0.5);  */
    display: flex;
    width: 100%;
    margin: 10px 0;
    color: whitesmoke;
    border-radius: 15px;
    flex-direction: column;
    cursor: pointer;
}

.short-chat:hover {
    background-color: rgba(255, 255, 255, 0.2); /* осветление при наведении */
}
</style>
