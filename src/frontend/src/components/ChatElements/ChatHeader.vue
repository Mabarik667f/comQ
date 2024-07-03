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
            isOnline: '',
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
                chatDescribe.value.isOnline = partner.is_online;
                header.value = partner.name;
                image.value = partner.img;
            }
        }, { immediate: true })

        watch(() => chatData.value?.groupSettings, (groupSettings) => {
            if (groupSettings) {
                group_settings.value = groupSettings;
                chatDescribe.value.amountUsers = chatData.value.current_users.length;
                chatDescribe.value.amountUsersIsOnline = chatData.value.current_users.filter(u => u.is_online).length - 1;
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

        watch(() => (chatData.value), () => {
            if (chatData.value?.chat_type === 'G') {
                chatDescribe.value.amountUsers = chatData.value.current_users.length
            }
            
        }, {deep: true})


        return {header, image, chatData, chatDescribe}
    }
}
</script>

<template>
    <div class="chat-header" :style="[chatData?.chat_type === 'G' ? {'cursor': 'pointer'} : {'cursor': 'auto'}]">
        <div class="chat-header-info">
            <div class="chat-img">
                <img :src="image" class="short-chat-img">
            </div>
            <div class="chat-header-text">
                <span class="header">{{ header }}
                    <span class="status" v-if="chatData?.chat_type === 'P'">"{{ chatDescribe.status }}"</span>
                </span>
                <span v-if="chatData?.chat_type === 'G'">
                    {{ chatDescribe.amountUsers }} участников
                </span>
                <span v-else>
                    <div v-if="chatDescribe.isOnline" class="online">
                        Онлайн
                    </div>
                    <div v-else class="offline">
                        Не в сети
                    </div>
                </span>
            </div>
        </div>
    </div>
</template>

<style scoped>

.chat-header{
    background-color: rgb(36, 36, 43);
    width: 100%;
    height: 7vh;
    color:whitesmoke;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}
.chat-header-info {
    display: flex;
    padding-left: 20px;
}

.chat-header-text {
    display: flex;
    flex-direction: column;
    align-content: center;
    justify-content: space-evenly;
    margin-left: 5px;
}

.header {
    font-weight: bolder;
    align-self: flex-start;
}
.chat-img {
    max-width: 60px;
    max-height: 60px;
    margin-top: 2px;
}
.short-chat-img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: 10px;
}
</style>