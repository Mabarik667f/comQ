<script>
import ChatHeader from '@/components/ChatElements/ChatHeader.vue';
import ChatContent from "@/components/ChatElements/ChatContent.vue";
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import getChatData from '@/hooks/chatHooks/getChatData';

export default {
    components: {
        ChatHeader,
        ChatContent
    },
    data() {
        return {
            settingsVisible: false
        }
    },
    methods: {
        showSettings() {
            this.settingsVisible = true;
        }
    },
    setup() {
        const route = useRoute();
        const chatId = ref(route.params.pk);
        const chat = ref({});

        const fetchData = async () => {
            const {chatData} = await getChatData(chatId.value);
            chat.value = chatData.value;
        }

        onMounted( () => {
            fetchData();
        })

        watch(() => route.params.pk, (newChatId) => {
            chatId.value = newChatId;
            fetchData();
        })
        
        return {chat}
    }
}
</script>

<template>
    <div class="chat">
        <ChatHeader @click="showSettings()"></ChatHeader>
        <com-dialog v-model:show="settingsVisible">
            <h1>{{$store.state.currentChat.title}}</h1>
            <img>
            <h2>Информация</h2>
            <div v-if="chat.chat_type === 'G'">
                <div v-for="user in chat.current_users" :key="user">
                    {{ user }}
                </div>
            </div>
                
        </com-dialog>
        <ChatContent :chat="chat"></ChatContent>
    </div>
</template>

<style scoped>
.chat {
    height: 100vh;
    width: 100%;
    background-color: beige;
}
</style>