<script>
import ChatHeader from '@/components/ChatElements/ChatHeader.vue';
import ChatContent from "@/components/ChatElements/ChatContent.vue"
// import Cookies from "js-cookie";

export default {
    components: {
        ChatHeader,
        ChatContent
    },
    setup() {
        const ws = new WebSocket("ws://localhost:8000/ws/")
        console.log(ws);
    }
}
</script>

<template>
    <div class="chat">
        <ChatHeader></ChatHeader>
        <ChatContent></ChatContent>
    </div>
</template>

<style scoped>
.chat {
    height: 100vh;
    width: 100%;
    background-color: beige;
}
</style>