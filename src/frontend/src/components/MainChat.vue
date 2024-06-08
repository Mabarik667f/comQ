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
        <ChatHeader></ChatHeader>
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