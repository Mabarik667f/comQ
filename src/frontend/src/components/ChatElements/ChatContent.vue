<script>
import ChatMessage from "@/components/ChatElements/ChatMessage.vue"
import { ref, watch} from "vue";
import {getWebSocketById} from "@/hooks/wsHooks/websockets"
import store from "@/store";
export default {
    components: {
        ChatMessage
    },
    props: {
        chat: {
            default: () => {},
            type: Object,
            required: true
        }
    },
    setup(props) {
        const formData = ref({
            message: ''
        });
        
        const messages = ref({});
        let ws = null;

        const setWs = () => {
            const intervalId = setInterval(() => {
            ws = getWebSocketById(props.chat.pk);
                console.log("WebSocket connection updated");
            console.log(ws)
            if (ws) {
                messages.value = props.chat.messages;
                console.log("WebSocket connection established");
                clearInterval(intervalId);

                ws.onmessage = function(e) {
                    const data = JSON.parse(e.data);
                    if (data.message) {
                        messages.value.push(data.message)
                    }

                }
                    
                ws.onclose = function(e) {
                    console.log("WebSocket connection closed:", e);
                };

                ws.onerror = function(e) {
                    console.error("WebSocket error:", e);
                };
            }
        }, 1000);
        }

        watch(() => (props.chat), () => {
            setWs();
        })


        const addMessage = () => {
            ws.send(
                JSON.stringify({
                    message: formData.value.message,
                    sender: store.state.userData.id
                })
            );
            formData.value.message = '';
        };

        return { addMessage, formData, messages};
    }
};
</script>

<template>
    <div class="chat-content">
        <div class="chat-messages">
            <ChatMessage v-for="message in messages" :key="message.id" :message="message"></ChatMessage>
        </div>
        <div class="input-group new-message">
            <div class="input-group-prepend">
                <com-button class="btn-attachment">&#128206;</com-button>
            </div>
            <com-input class="form-control" v-model="formData.message"></com-input>
            <div class="input-group-append">
                <com-button class="btn-send" @click="addMessage">&#9658;</com-button>
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
