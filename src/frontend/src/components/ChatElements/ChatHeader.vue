<script>
import { watch, ref, onMounted } from 'vue';
import { useStore } from 'vuex';

export default {
    setup() {
        const store = useStore();
        const header = ref(store.state.currentChat.title);
        const imagePath = ref(store.state.currentChat.imagePath);
        const updateHeaderAndImagePath = (newTitle, newImagePath) => {
            header.value = newTitle;
            imagePath.value = newImagePath;
        };

        watch(() => [store.state.currentChat.title, store.state.currentChat.imagePath], ([newTitle, newImagePath]) => {
            updateHeaderAndImagePath(newTitle, newImagePath);
        });

        onMounted( () => {
            updateHeaderAndImagePath(store.state.currentChat.title, store.state.currentChat.imagePath);
        });

        return {header, imagePath}
    }
}
</script>

<template>
    <div class="chat-header">
        <div class="chat-header-info">
            <div>{{header}}</div>
            <img :src="imagePath" class="short-chat-img">
        </div>
    </div>
</template>

<style scoped>
.chat-header{
    background-color: gainsboro;
    width: 100%;
    height: 7vh;
}
.chat-header-info {
    display: flex;
    flex-direction: column;
}
.short-chat-img {
  width: 65px;
  border-radius: 50%;
}
</style>