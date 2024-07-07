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
            message: "",
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

        // const changeTextRows = () => {

        // }

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
        const handleBackspace = () => {
            const end = formData.value.message.length
            if (messageRows.value > 1 && formData.value.message[end - 1] == "\n") {
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
                    cancelEditMessage()
                } else {
                    addMessage();
                    cancelReply()
                }
                formData.value.message = "";
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

        const scrollToMessage = async (msgId) => {
            const msgElement = chatContainer.value.$el.querySelector(`.message-${msgId}`);
            
            msgElement.classList.add('highlighted');
            setTimeout(() => {
                msgElement.classList.remove('highlighted');
            }, 2000);

            msgElement.scrollIntoView({ behavior: "smooth" });
        };



        onMounted(() => {
            const container = chatContainer.value.$el;
            container.addEventListener('scroll', handleScroll);
        });

        watch(() => (chat.value?.messages), () => {
            if (isAtBottom.value || chat.value?.last_message?.user?.username === store.getters.getUserName) {
                nextTick(() => {
                    scrollToBottom()
                })
            }
        }, {deep: true})

        watch(() => (formData.value.message), () => {
            if(formData.value.message.slice(0, 2) === "\n" && messageRows.value === 1) {
                formData.value.message = "";
            }
        }, {deep: true})

        return {
                chat, chatContainer, scrollToBottom, isAtBottom, messageRows, handleBackspace,
                actions, contextMenu, showContextMenu,
                popupTriggers, togglePopup,
                addMessage, editMessage, deleteMessage,
                deleteUserToRoom, deleteRoom, leaveUserToRoom, addUserToRoom,
                setEditMessage, editingMessage, cancelEditMessage,
                setReply, replyMessage, cancelReply,
                formData, handleEnter, scrollToMessage};
    }
};
</script>

<template>
    <div class="chat-content">
        <transition-group name="message" tag="div" class="chat-messages" ref="chatContainer">
            <ChatMessage v-for="message in chat?.messages"
                :key="message.id" :message="message"
                :chatType="chat?.chat_type"
                @showContextMenu="showContextMenu"
                @goToMessage="scrollToMessage"
            ></ChatMessage>
        </transition-group>

        <com-popup v-if="popupTriggers.buttonTrigger"
            :togglePopup="() => togglePopup('buttonTrigger')">
            <com-button @click="deleteMessage" :orange="false"
            style="color: orangered; font-weight: bolder;">Удалить</com-button>
        </com-popup>

        <div class="input-group new-message">
            <div class="input-container">
                <div class="message-input-wrapper">
                    <div v-if="editingMessage.text_content" class="edit-message">
                        <div class="edited-message">{{ editingMessage.text_content }}</div>
                        <com-button :orange="false" @click="cancelEditMessage">&#x2717;</com-button>
                    </div>
                    <div v-if="replyMessage.text_content" class="reply-message">
                        <div class="replied-message">{{ replyMessage.text_content }}</div>
                        <com-button :orange="false" @click="cancelReply">&#x2717;</com-button>
                    </div>
                    <com-text class="new-message-input" v-model="formData.message"
                        :class="{ 'change-borders': editingMessage.text_content ||  formData.reply}"
                        :rows="messageRows" @keydown.enter="handleEnter"
                        @keydown.backspace="handleBackspace"
                        placeholder="Новое сообщение">
                    </com-text>
                </div>
                <transition name="slide-fade">
                    <div v-if="formData.message">
                        <com-button class="btn-send" @click="handleEnter">&#9658;</com-button>
                    </div>
                </transition>
            </div>
        </div>

        <transition name="context-fade">
            <context-menu :options="actions" ref="contextMenu" />
        </transition>
        <transition name="slide-fade">
            <com-button class="scroll-btn"
                @click="scrollToBottom()" v-show="!isAtBottom">↓</com-button>
        </transition>
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
    align-items: flex-end;
    width: 100%;
    position: relative;
    flex-direction: row;
}

.message-input-wrapper {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.edit-message,
.reply-message {
    width: 100%;
    padding-top: 5px;
    display: flex;
    color: whitesmoke;
    justify-content: space-between;
    background-color: rgb(36, 36, 43);
    border-radius: 15px 15px 0 0 !important;
    border-bottom: none !important;
    border-left: none !important;
    border-right: none !important;
}

.edited-message,
.replied-message {
    padding: 5px;
    flex-grow: 1;
    background-color: rgb(224, 81, 29, 0.8);
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
    border: 1px solid rgba(30, 30, 35);
    border-left: 5px solid orangered;
    border-radius: 5px;
}

.chat-content {
    background-color: rgba(30, 30, 35);
    margin: 0 20%;
    height: 93%;
    display: flex;
    flex-direction: column;
    position: relative;
}

.chat-messages {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    scroll-behavior: smooth;
}

.chat-content::-webkit-scrollbar {
    width: 20px;
}

.btn-attachment {
    border-radius: 0%;
}

.btn-send {
    border-radius: 50%;
    margin-left: 10px;
    flex-shrink: 0;
}

.new-message {
    display: flex;
    position: sticky;
    margin-top: 5px;
    margin-bottom: 20px;
}

.change-borders {
    border-top: none !important;
    margin-top: 0;
    border-top-left-radius: 0 !important;
    border-top-right-radius: 0 !important;
}

.new-message-input {
    width: 100%;
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

.scroll-btn {
    right: 0;
    bottom: 0;
    margin: 20px;
    width: 60px;
    height: 60px;
    margin-bottom: 100px;
    position: fixed !important;
    font-size: 30px;
    font-weight: bolder;
    border: 1px orangered solid; 
    border-radius: 50% !important;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
}

@media screen and (max-width: 750px) {
    .scroll-btn {
        display: none;
    }
}
</style>
