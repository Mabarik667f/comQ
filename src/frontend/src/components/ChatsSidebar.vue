<script>
import ChatsHeader from '@/components/ChatsHeader.vue';
import ChatCard from '@/components/UI/ChatCard.vue';
import { useStore } from 'vuex';
import getChatData from "@/hooks/chatHooks/getChatData"
import cleanChatData from "@/hooks/chatHooks/cleanChatData"
import createMessage from '@/hooks/chatHooks/createMessage';
import { ref, computed, watch } from 'vue';
import router from '@/router';
import Cookies from "js-cookie";


export default {
    components: {
        ChatsHeader,
        ChatCard,
    },
    props: {
        userData: {
            type: Object,
            required: true
        }
    },
    
    setup(props) {
        const store = useStore();
        const chats = computed(() => store.getters.getChats);
        const websockets = computed(() => store.getters.getWebSockets)
        const userData = ref(props.userData)

        const reloadChats = async (chats) => {
            for (const chat of chats) {
                const {chatData} = await getChatData(chat.pk);
                await cleanChatData(chatData.value)
            }
        }

        const websocketInit = (ws, id) => {
            
                ws.onmessage = function(e) {
                    const data = JSON.parse(e.data);
                    console.log(data)
                    if (data.message) {
                        createMessage(data.message, id)  
                    } else if (data.deleted_message) {
                        store.dispatch('deleteMessage', {chatId: id, message: data.deleted_message})

                        if (data.deleted_message.user.username !== store.getters.getUserName
                        && data.delete_author.username !== store.getters.getUserName) {
                            store.commit('updateNotifications', { chatId: id, status: "del" });
                        }                           
                    } else if (data.edited_message) {
                        store.dispatch('editMessage', {chatId: id, message: data.edited_message})
                    } else if (data.deleted_chat) {
                        console.log(data.deleted_chat)
                        store.commit('deleteChat', {chatId: id})
                    } else if (data.clear_notifications) {
                        store.commit('clearNotifications', {chatId: id})
                    }
                };

                ws.onclose = function(e) {
                    console.log("WebSocket connection closed:", e);
                };

                ws.onerror = function(e) {
                    console.error("WebSocket error:", e);
                };            
        }

        const selectChat = async (chat) => {
            Cookies.set('chat', chat.pk);
            router.push({ name: 'chat-detail', params: { pk: chat.pk }});
        }

        watch(() => (props.userData), async (newData) => {
            userData.value = newData.value
        })

        watch(() => (userData.value), async () => {
            await reloadChats(userData.value.chats)
        })

        watch(() => (chats.value), async () => {
            if (userData.value.chats.length < chats.value.length) {
                await reloadChats(chats.value)
            }
        }, {deep: true})

        watch(() => (websockets.value), () => {
            for (const id in websockets.value) {
                const ws = websockets.value[id];
                if (ws && !ws.onmessage) {
                    websocketInit(ws, parseInt(id));
                }
            }
        }, { deep: true });

        return {chats, selectChat}
    },
}
</script>

<template>
    <div class="chats">
        <ChatsHeader></ChatsHeader>
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
