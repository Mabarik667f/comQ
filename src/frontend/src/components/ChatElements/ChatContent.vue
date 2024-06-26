<script>
import ChatMessage from "@/components/ChatElements/ChatMessage.vue"
import { ref, watch, computed } from "vue";
import {getWebSocketById} from "@/hooks/wsHooks/websockets"
import { useToast } from "vue-toastification";
import { useStore } from "vuex";

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

        const toast = useToast();
        const store = useStore();

        const chatId = ref(props.chatId);
        const chat = computed(() => store.getters.getChat(chatId.value));

        const formData = ref({
            message: ''
        });

        const editingMessage = ref({});
        
        const messages = ref({});
        let ws = null;

        const createMessage = (message) => {
            messages.value.push(message);
            store.commit('updateLastMessage', {chatId: chatId.value, message: message})
            if (message.user.id != store.state.userData.id) {
                toast(`Новое сообщение в чате: test`);
                store.commit('updateNotifications', { chatId: chatId.value, status: "add" });
            }
        }

        const setWs = () => {
            ws = getWebSocketById(chatId.value);
            console.log("WebSocket connection updated");
            if (ws) {
                messages.value = chat?.value?.messages;
                console.log("WebSocket connection established");

                ws.onmessage = function(e) {
                    const data = JSON.parse(e.data);
                    console.log(data)
                    if (data.message) {
                        createMessage(data.message)
                    } else if (data.deleted_message) {
                        messages.value = messages.value.filter(m => m.id !== data.deleted_message);
                        let message = null;
                        if (messages.value.length >= 1) {
                            message = messages.value[messages.value.length - 1]
                        } 
                        store.commit('updateNotifications', { chatId: chatId.value, status: "del" });
                        store.commit('updateLastMessage', {chatId: chatId.value,
                            message: message})

                    } else if (data.edited_message) {
                        const index = messages.value.findIndex(m => m.id === data.edited_message.id);
                        messages.value[index].text_content = data.edited_message.text_content
                        if (index === messages.value.length - 1) {
                            store.commit('updateLastMessage', {chatId: chatId.value,
                            message: data.edited_message})
                        }
                    } else if (data.new_users) {
                        console.log(data.new_users)
                    } else if (data.deleted_user) {
                        console.log(data.deleted_user)
                        store.dispatch('deleteUser', {user: data.deleted_user, chatId: chatId.value});
                    } else if (data.deleted_chat) {
                        console.log(data.deleted_chat)
                    } else if (data.leaved_user) {
                        console.log(data.leaved_user)
                    } 
                };

                ws.onclose = function(e) {
                    console.log("WebSocket connection closed:", e);
                };

                ws.onerror = function(e) {
                    console.error("WebSocket error:", e);
                };
            } else {
                setTimeout(setWs, 1000);
            }
        }

        watch(() => (props.chatId), (newId) => {
            chatId.value = newId
            setWs();
        }, {immediate: true});
    

        const addMessage = () => {
            console.log(ws)
            ws.send(
                JSON.stringify({
                    message: formData.value.message,
                    message_type: 'chat.message'
                })
            );
            formData.value.message = '';
        };

        const editMessage = () => {
            ws.send(
                JSON.stringify({
                    message_type: 'chat.edit_message',
                    message_id: editingMessage.value.id,
                    message_text: formData.value.message,
                    chat: chat.value.pk
                })
            )
        }

        const deleteMessage = (message) => {
            ws.send(
                JSON.stringify({
                    message_type: 'chat.delete_message',
                    message_id: message.id
                })
            )
        }

        const setEditMessage = (message) => {
            formData.value.message = message.text_content;
            editingMessage.value = message;
            console.log(editingMessage.value)
        }

        const deleteUserToRoom = (user) => {
            ws.send(
                JSON.stringify({
                    message_type: 'chat.delete_user',
                    deleted_user: user
                })
            )
        }

        const deleteRoom = () => {
            ws.send(
                JSON.stringify({
                    message_type: 'chat.delete_chat',
                })
            )
        }

        const leaveUserToRoom = () => {
            ws.send(
                JSON.stringify({
                    message_type: 'chat.leave_user',
                })
            )
        }

        const addUserToRoom = (addedUsers) => {
            ws.send(
                JSON.stringify({
                    message_type: 'chat.add_user',
                    users: addedUsers
                })
            )
        }

        const cancelEditMessage = () => {

        }


        return { addMessage,
                editMessage,
                deleteMessage,

                deleteUserToRoom,
                deleteRoom,
                leaveUserToRoom,
                addUserToRoom,

                setEditMessage,
                editingMessage,
                cancelEditMessage,
            formData, messages};
    }
};
</script>

<template>
    <div class="chat-content">
        <div class="chat-messages">
            <ChatMessage v-for="message in messages"
             :key="message.id" :message="message"
             @delete-message="deleteMessage"
             @edit-message="setEditMessage"></ChatMessage>
        </div>
        <div class="input-group new-message">
            <div class="input-group-prepend">
                <com-button class="btn-attachment">&#128206;</com-button>
            </div>
            <com-input class="form-control" v-model="formData.message"></com-input>
            <div class="input-group-append">
                <com-button class="btn-send" @click="editingMessage.text_content ? editMessage() : addMessage()">&#9658;</com-button>
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
