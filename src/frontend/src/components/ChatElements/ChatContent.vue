<script>
import ChatMessage from "@/components/ChatElements/ChatMessage.vue"
import { ref, watch, computed, onMounted, nextTick } from "vue";
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
            reply: null
        });

        const editingMessage = ref({});
        const replyMessage = ref({});
        
        const ws = computed(() => store.getters.getWebSocketById(chatId.value));
        const hub = computed(() => store.getters.getHub)
        
        const clearNotifications = () => {
            if (ws.value) {
                if (ws.value.readyState === WebSocket.OPEN) {
                ws.value.send(
                    JSON.stringify({
                        message_type: 'chat.clear_notifications',
                    })
                );
                } else {
                    // once - выполняем только один раз и удаляем обработчик
                    ws.value.addEventListener('open', () => {
                        store.dispatch('checkTokenLifeTime')
                        ws.value.send(
                            JSON.stringify({
                                message_type: 'chat.clear_notifications',
                            })
                        );
                    }, { once: true });
                }
            }
            
        }

        watch(() => (props.chatId), (newId) => {
            chatId.value = newId
            
        }, {immediate: true});

        watch(() => (ws.value), () => {
            clearNotifications()
        })

        const addMessage = () => {
            store.dispatch('checkTokenLifeTime')
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
            store.dispatch('checkTokenLifeTime')
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

        const deleteCandidat = ref(null);
        const deleteMessage = () => {
            store.dispatch('checkTokenLifeTime')
            ws.value.send(
                JSON.stringify({
                    message_type: 'chat.delete_message',
                    message_id: deleteCandidat.value
                })
            )
            togglePopup('buttonTrigger')
        }

        const deleteRoom = () => {
            store.dispatch('checkTokenLifeTime')
            ws.value.send(
                JSON.stringify({
                    message_type: 'chat.delete_chat',
                })
            )
            togglePopup('buttonTrigger')
        }

        const deleteUserToRoom = (user) => {
            store.dispatch('checkTokenLifeTime')
            hub.value.send(
                JSON.stringify({
                    message_type: 'chat.delete_user',
                    deleted_user: user,
                    chat_pk: chatId.value
                })
            )
        }

        const leaveUserToRoom = () => {
            store.dispatch('checkTokenLifeTime')
            hub.value.send(
                JSON.stringify({
                    message_type: 'chat.leave_user',
                    chat_pk: chatId.value
                })
            )
        }

        const addUserToRoom = (addedUsers) => {
            store.dispatch('checkTokenLifeTime')
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
            formData.value.reply = message.id;
            replyMessage.value = message;
            cancelEditMessage()
        }

        const cancelReply = () => {
            formData.value.reply = null;
            replyMessage.value = {};
        }

        const contextMenu = ref(null);
        const actions = ref([])

        const copyToClipboard = async (message) => {
            await navigator.clipboard.writeText(message.text_content);
        }

        const showContextMenu = (event, message) => {

            deleteCandidat.value = message.id
            actions.value = [
                {"name": "Ответить", "event": () => setReply(message)},
                {"name": "Копировать текст", "event": () => copyToClipboard(message)}
            ]
            
            // можно ли удалять
            if ((message.user.username == store.getters.getUserName ||
            ('A', 'O').includes(store.getters.getUserRole)) && !message.system) {
                actions.value.push({"name": "Удалить", "event": () => togglePopup('buttonTrigger')})
            }

            // можно ли редактировать
            if (message.user.username == store.getters.getUserName && !message.system) {
                actions.value.push({"name": "Редактировать", "event": () => setEditMessage(message)})
            }

            contextMenu.value.openMenu(event)
        }

        const popupTriggers = ref({
            buttonTrigger: false
        })

        const togglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }

        const messageRows = ref(1);
        const handleShiftBackspace = (event) => {
            if (event.shiftKey && messageRows.value > 1) {
                messageRows.value -= 1;
            }
        }
        const handleEnter = (event) => {
            if (event.shiftKey && event.key === 'Enter') {
                messageRows.value += 1; 
            }  else if (formData.value.message) {
                messageRows.value = 1;
                if (editingMessage.value.text_content) {
                    editMessage();
                } else {
                    addMessage();
                }
            }
        };

        const chatContainer = ref(null);
        const isAtBottom = ref(false);

        const handleScroll = () => {
            const el = chatContainer.value.$el
            isAtBottom.value = el.scrollHeight - el.scrollTop === el.clientHeight;
        }

        const scrollToBottom = async () => {
            const el = chatContainer.value.$el
            el.scrollTop = el.scrollHeight
        }

        onMounted(() => {
            const container = chatContainer.value.$el;
            container.addEventListener('scroll', handleScroll);
        });

        watch(() => (chat.value?.messages), () => {
            if (isAtBottom.value) {
                nextTick(() => {
                    scrollToBottom()
                })
            }
        }, {deep: true})

        return {
                chat, chatContainer, scrollToBottom, isAtBottom, messageRows, handleShiftBackspace,
                actions, contextMenu, showContextMenu,
                popupTriggers, togglePopup,
                addMessage, editMessage, deleteMessage,
                deleteUserToRoom, deleteRoom, leaveUserToRoom, addUserToRoom,
                setEditMessage, editingMessage, cancelEditMessage,
                setReply, replyMessage, cancelReply,
                formData, handleEnter};
    }
};
</script>

<template>
    <div class="chat-content">
        <transition-group name="message" tag="div" class="chat-messages" ref="chatContainer">
        <ChatMessage v-for="message in chat?.messages"
            :key="message.id" :message="message"
            @showContextMenu="showContextMenu"
            ></ChatMessage>
        </transition-group>

            <com-popup
        v-if="popupTriggers.buttonTrigger"
        :togglePopup="() => togglePopup('buttonTrigger')">
            <com-button @click="deleteMessage">Удалить</com-button>
        </com-popup>

        <div class="input-group new-message">
            <div v-if="editingMessage.text_content">
                <div>{{ editingMessage.text_content }}</div>
                <com-button @click="cancelEditMessage">&#x2717;</com-button>
            </div>
            <div v-if="replyMessage.text_content">
                <div>{{ replyMessage.text_content }}</div>
                <com-button @click="cancelReply">&#x2717;</com-button>
            </div>
            <div class="input-container">
                <com-text class="form-control new-message-input" v-model="formData.message"
                :rows="messageRows" @keydown.enter="handleEnter"
                @keydown.backspace="handleShiftBackspace"
                placeholder="Новое сообщение"></com-text>
                <transition name="slide-fade">
                    <div class="input-group-append" v-if="formData.message">
                        <com-button class="btn-send" @click="handleEnter">&#9658;</com-button>
                    </div>
                </transition>
            </div>

        <transition name="context-fade">
            <context-menu :options="actions" ref="contextMenu" />
        </transition>

        </div>
    </div>
</template>

<style scoped>
.message-enter-active, .message-leave-active {
    transition: opacity 0.5s;
}
.message-enter-from, .message-leave-to {
    opacity: 0;
}

.slide-fade-enter-active, .slide-fade-leave-active {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-fade-enter-from, .slide-fade-leave-to {
    transform: translateY(20px);
    opacity: 0;
}

.input-container {
    display: flex;
    align-items: center;
    width: 100%;
}

.chat-content {
    background-color: rgba(30, 30, 35);
    margin: 0 20%;
    height: 93%;
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
    scroll-behavior: smooth;
}

.chat-content::-webkit-scrollbar {
    width: 20px;
}

.btn-attachment,
.btn-send {
    border-radius: 0%;
}

.form-control:focus {
    border-color: #ccc;
    box-shadow: none;
}
.new-message {
    width: 100%;
    display: flex;
    position: sticky;
    margin-top: 5px;
    margin-bottom: 20px;
    border: 1px solid rgba(30, 30, 45);
    border-radius: 20px;
}

.new-message-input {
    background-color: rgb(36, 36, 43);
    border: 1px solid rgba(30, 30, 45);
    color: whitesmoke;
    cursor: text;
}

.new-message-input:focus {
    background-color: rgb(36, 36, 43);
    border: 1px solid rgba(30, 30, 45);
    color: whitesmoke;
    cursor: text;
}

.new-message-input::placeholder {
    color: whitesmoke;
    opacity: 0.4;
}

.input-group {
    width: 100%; 
}

.context-fade-enter-active, 
.context-fade-leave-active {
    transition: opacity 0.5s;
}

.context-fade-enter-from,
.context-fade-leave-to {
    opacity: 0;
}

</style>
