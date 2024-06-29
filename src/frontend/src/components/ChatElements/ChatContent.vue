<script>
import ChatMessage from "@/components/ChatElements/ChatMessage.vue"
import { ref, watch, computed } from "vue";
import { useStore } from "vuex";
import router from "@/router";

export default {
    components: {
        ChatMessage
    },
    props: {
        chatId: {
            type: Number,
            required: true
        }
    },
    setup(props) {

        const store = useStore();

        const chatId = ref(props.chatId);
        const chat = computed(() => store.getters.getChat(chatId.value));

        const formData = ref({
            message: '',
            reply: false
        });

        const editingMessage = ref({});
        const replyMessage = ref({});
        
        const ws = computed(() => store.getters.getWebSocketById(chatId.value));
        const hub = computed(() => store.getters.getHub)
        
        const clearNotifications = () => {
            if (ws.value.readyState === WebSocket.OPEN) {
                ws.value.send(
                    JSON.stringify({
                        message_type: 'chat.clear_notifications',
                    })
                );
            } else {
                // once - выполняем только один раз и удаляем обработчик
                ws.value.addEventListener('open', () => {
                    ws.value.send(
                        JSON.stringify({
                            message_type: 'chat.clear_notifications',
                        })
                    );
                }, { once: true });
            }
        }

        watch(() => (props.chatId), (newId) => {
            chatId.value = newId
        }, {immediate: true});

        watch(() => (ws.value), () => {
            clearNotifications()
        })

        const addMessage = () => {
            if (!ws.value) {
                router.push('/')
            } else {
                ws.value.send(
                    JSON.stringify({
                        message: formData.value.message,
                        message_type: 'chat.message',
                        reply: formData.value.reply
                    })
                );
                formData.value.message = '';
                cancelReply()
            }
        };

        const editMessage = () => {
            ws.value.send(
                JSON.stringify({
                    message_type: 'chat.edit_message',
                    message_id: editingMessage.value.id,
                    message_text: formData.value.message,
                    chat: chat.value.pk
                })
            )
            cancelEditMessage()
        }

        const deleteMessage = (message) => {
            ws.value.send(
                JSON.stringify({
                    message_type: 'chat.delete_message',
                    message_id: message.id
                })
            )
        }

        const deleteRoom = () => {
            ws.value.send(
                JSON.stringify({
                    message_type: 'chat.delete_chat',
                })
            )
        }

        const deleteUserToRoom = (user) => {
            hub.value.send(
                JSON.stringify({
                    message_type: 'chat.delete_user',
                    deleted_user: user,
                    chat_pk: chatId.value
                })
            )
        }

        const leaveUserToRoom = () => {
            hub.value.send(
                JSON.stringify({
                    message_type: 'chat.leave_user',
                    chat_pk: chatId.value
                })
            )
        }

        const addUserToRoom = (addedUsers) => {
            hub.value.send(
                JSON.stringify({
                    message_type: 'chat.add_user',
                    users: addedUsers,
                    chat_pk: chatId.value
                })
            )
        }

        const setEditMessage = (message) => {
            formData.value.message = message.text_content;
            editingMessage.value = message;
            cancelReply()
        }

        const cancelEditMessage = () => {
            formData.value.message = "";
            editingMessage.value = {};
        }

        const setReply = (message) => {
            formData.value.reply = true;
            replyMessage.value = message;
            cancelEditMessage()
        }

        const cancelReply = () => {
            formData.value.reply = false;
            replyMessage.value = {};
        }

        const handleEnter = () => {
            if (formData.value.message) {
                if (editingMessage.value.text_content) {
                    editMessage();
                } else {
                    addMessage();
                }
            }
        };

        return {
                chat, 
                addMessage,
                editMessage,
                deleteMessage,

                deleteUserToRoom,
                deleteRoom,
                leaveUserToRoom,
                addUserToRoom,

                setEditMessage,
                editingMessage,
                cancelEditMessage,

                setReply,
                replyMessage,
                cancelReply,

                formData,
                handleEnter};
    }
};
</script>

<template>
    <div class="chat-content">
        <div class="chat-messages">
            <ChatMessage v-for="message in chat?.messages"
             :key="message.id" :message="message"
             @delete-message="deleteMessage"
             @edit-message="setEditMessage"
             @replyToMessage="setReply"></ChatMessage>
        </div>
        <div class="input-group new-message">
            <div v-if="editingMessage.text_content">
                <div>{{ editingMessage.text_content }}</div>
                <com-button @click="cancelEditMessage">&#x2717;</com-button>
            </div>
            <div v-if="replyMessage.text_content">
                <div>{{ replyMessage.text_content }}</div>
                <com-button @click="cancelReply">&#x2717;</com-button>
            </div>
            <com-input class="form-control" v-model="formData.message"
            @keydown.enter="handleEnter"></com-input>
            <div class="input-group-append" v-if="formData.message">
                <com-button class="btn-send" @click="handleEnter()">&#9658;</com-button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.chat-content {
    background-color: aquamarine;
    margin: 0 20%;
    height: 850px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
}

.chat-messages{
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow-y: auto;
}

.chat-content::-webkit-scrollbar {
    width: 20px;
}

.new-message {
    position: absolute;
    bottom: 0;
}

.btn-attachment,
.btn-send {
    border-radius: 0%;
}

.new-message {
    position: absolute;
    bottom: 0;
    width: 100%;
    display: flex;
}

.input-group {
    width: 100%; 
}

</style>
