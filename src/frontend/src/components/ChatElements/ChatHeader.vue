<script>
import { watch, ref, computed } from 'vue';
import { useStore } from 'vuex';

export default {
    props: {
        chatId: {
            type: Number,
            required: true
        }
    },
    setup(props) {
        const store = useStore();
        const group_settings = ref(null);
        const header = ref(null);
        const image = ref(null);
        const chatDescribe = ref({
            status: '',
            amountUsers: 0
        })

        const chatId = ref(props.chatId)
        const chatData = computed(() => store.getters.getChat(chatId.value))

        watch(() => (props.chatId), (newId) => {
            chatId.value = newId
        }, { immediate: true })

        watch(() => chatData.value?.partner, (partner) => {
            if (partner) {
                chatDescribe.value.status = partner.status;
                header.value = partner.name;
                image.value = partner.img;
            }
        }, { immediate: true })

        watch(() => chatData.value?.groupSettings, (groupSettings) => {
            if (groupSettings) {
                group_settings.value = groupSettings;
                chatDescribe.value.amountUsers = chatData.value.current_users.length;
                header.value = groupSettings.title;
                image.value = groupSettings.avatar;
            }
        }, { immediate: true })


        watch(() => chatData.value?.groupSettings?.avatar, (newAvatar) => {
            if (newAvatar) {
                image.value = newAvatar;
            }
        }, { immediate: true });

        watch(() => chatData.value?.groupSettings?.title, (newTitle) => {
            if (newTitle) {
                header.value = newTitle;
            }
        }, { immediate: true });


        return {header, image, chatData, chatDescribe}
    }
}
</script>

<template>
    <div class="chat-header">
        <div class="chat-header-info">
            <div class="chat-img">
                <img :src="image" class="short-chat-img">
            </div>
            <div class="chat-header-text">
                <span>{{ header }}</span>
                <span v-if="chatData?.chat_type === 'G'">{{ chatDescribe.amountUsers }}</span>
                <span v-else>{{ chatDescribe.status }}</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.chat-header{
    background-color: gainsboro;
    width: 100%;
    height: 7vh;
    cursor: pointer;
}
.chat-header-info {
    display: flex;
    padding-left: 20px;
    padding-top: 8px;
}

.chat-header-text {
    display: flex;
    flex-direction: column;
    align-content: center;
}

.chat-img {
    width: 65px;
}
.short-chat-img {
  width: 100%;
  height: auto;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}
</style>