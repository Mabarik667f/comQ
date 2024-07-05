<script>
import ChatsHeader from '@/components/ChatsHeader.vue';
import ChatCard from '@/components/UI/ChatCard.vue';
import { useStore } from 'vuex';
import getChatData from "@/hooks/chatHooks/getChatData"
import cleanChatData from "@/hooks/chatHooks/cleanChatData"
import createMessage from '@/hooks/chatHooks/createMessage';
import { ref, computed, watch, onMounted } from 'vue';
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
        const userData = ref(props.userData);
        const searchQuery = ref('');

        const filteredChats = computed(() => {
            if(!searchQuery.value) {
                return chats.value
            } 
            const res = ref([]);
            for (const chat of chats.value) {
                if (chat.chat_type === 'G') {
                    if(chat.groupSettings.title.toLowerCase().slice(0, searchQuery.value.length) === searchQuery.value.toLowerCase()) {
                        res.value.push(chat)
                    }
                } else {
                    if(chat.partner.name.toLowerCase().slice(0, searchQuery.value.length) === searchQuery.value.toLowerCase()) {
                        res.value.push(chat)
                    }
                }
            }
            return res.value
            
        })

        const reloadChats = async (chats) => {
            for (const chat of chats) {
                const {chatData} = await getChatData(chat.pk);
                await cleanChatData(chatData.value)
            }
        }

        const websocketInit = (ws, id) => {
            
            ws.onmessage = function(e) {
                const data = JSON.parse(e.data);
                if (data.message) {
                    createMessage(data.chat_title, data.message, id)  
                } else if (data.deleted_message && data.delete_author) {
                    store.dispatch('deleteMessage', {chatId: id, message: data.deleted_message})

                    if (data.deleted_message.user.username !== store.getters.getUserName
                    && data.delete_author.username !== store.getters.getUserName) {
                        store.commit('updateNotifications', { chatId: id, status: "del" });
                    }                           
                } else if (data.edited_message) {
                    store.dispatch('editMessage', {chatId: id, message: data.edited_message})
                } else if (data.deleted_chat) {
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

        const chatsContainter = ref(null);
        const startX = ref(0);
        const startWidth = ref(0);

        const onMouseMove = (event) => {
            const newWidth = startWidth.value + (event.clientX - startX.value);
            if (newWidth >= 200 && newWidth <= 600) {
                chatsContainter.value.style.width = `${newWidth}px`;
                store.commit('updateSidebarWidth', {width: newWidth})
            }
        };

        const onMouseUp = () => {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        };

        const onMouseDown = (event) => {
            startX.value = event.clientX;
            startWidth.value = chatsContainter.value.offsetWidth;
            document.addEventListener('mousemove', onMouseMove)
            document.addEventListener('mouseup', onMouseUp)
        };

        onMounted(() => {
            const resizeHandle = document.querySelector('.resize-handle')
            resizeHandle.addEventListener('mousedown', onMouseDown)
        })

        return {filteredChats, searchQuery, selectChat, chatsContainter}
    },
}
</script>

<template>
    <div class="chats" ref="chatsContainter">
        <ChatsHeader v-model="searchQuery"></ChatsHeader>
        <transition-group name="slide-fade" tag="div" class="short-chats">
        <div class="short-chat" v-for="chat in filteredChats" :key="chat">
            <ChatCard :chat="chat" @click="selectChat(chat)"></ChatCard>
        </div>
        </transition-group>
        <div class="resize-handle" @mousedown="onMouseDown"></div>
    </div>
</template>

<style scoped>

.slide-fade-enter-active, .slide-fade-leave-active {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-fade-enter-from, .slide-fade-leave-to {
    transform: translateY(20px);
    opacity: 0;
}

.chats {
    background-color: rgb(36, 36, 43);
    height: 100vh;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: flex-start;
    justify-content: flex-start;
    align-items: flex-start;
    min-width: 200px;
    width: 300px;
    max-width: 600px;
    resize: none;
    position: relative;
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    overflow-y: scroll;
    overflow-x: hidden;
}

.resize-handle {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    width: 10px;
    cursor: ew-resize;
}

.short-chats {
    display: flex;
    width: 100%;
    margin: 10px 0;
    color: whitesmoke;
    flex-direction: column;
    border: 1px solid rgb(36, 36, 43);
    border-radius: 20px;
}

.short-chat {
    cursor: pointer;
    margin: 0 10px;
}

.short-chat:hover {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 20px;
}
</style>
