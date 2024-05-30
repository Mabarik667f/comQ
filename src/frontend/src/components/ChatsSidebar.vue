<script>
import ChatsHeader from '@/components/ChatsHeader.vue';
import ChatCard from '@/components/UI/ChatCard.vue';
import { mapActions } from 'vuex';
import {ref} from "vue";
export default {
    components: {
        ChatsHeader,
        ChatCard,
        
    },
    data() {
        return {
            chats: [{id: 1, title: 'Aboba', lastMessage: "Sos"},
                    {id: 2, title: 'Aboba', lastMessage: "Sos"},
                    {id: 3, title: 'Aboba', lastMessage: "Sos"},
                    {id: 4, title: 'Aboba', lastMessage: "Sos"},
                    {id: 5, title: 'Aboba', lastMessage: "Sos"}]
        }
    },
    setup() {
        const searchQuery = ref('')

        return {searchQuery};
    },
    methods: {
    ...mapActions({
            logout: 'logout'
    })
  }
}
</script>

<template>
    <div class="chats">
        <ChatsHeader></ChatsHeader>
        <div class="short-chat" v-for="chat in chats" :key="chat.id">
            <ChatCard :chat="chat"></ChatCard>
        </div>
        <com-button
        @click="$router.push('/register')">Зарегистрироваться</com-button>
        <com-button
        @click="$router.push('/login')">Войти</com-button>
        <com-button @click.prevent="logout">Выйти</com-button>
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
    width: 500px;
    max-width: 900px;
}

.short-chat {
    /* box-shadow: 0 0 10px rgba(255, 69, 0, 0.5);  */
    display: flex;
    width: 100%;
    margin: 10px 0;
    color: whitesmoke;
    border-radius: 15px;
}

.short-chat:hover {
    background-color: rgba(255, 255, 255, 0.2); /* осветление при наведении */
}

.short-chat-img {
    width: 65px;
    border-radius: 50%;
}
</style>
