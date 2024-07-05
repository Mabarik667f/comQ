<script>
import { computed, ref, watch} from 'vue';
import { useStore } from 'vuex';
import isAdmin from '@/hooks/permissionHooks/isAdmin';
export default {
    props: {
        user: {
            type: Object,
            require: true
        },
        chatId: {
            type: Number,
            require: true
        }
    },
    emits: ['showContextMenu'],
    setup(props, {emit}) {
        
        const user = ref(props.user);
        const store = useStore();
        const chatId = ref(props.chatId)
        const chat = computed(() => store.getters.getChat(chatId.value))

        watch(() => (props.chatId), (newId) => {
            chatId.value = newId;
        })

        watch(() => (props.user), (newUser) => {
            user.value = newUser;
        })
        
        const popupTriggers = ref({
            buttonTrigger: false
        })

        const togglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }

        const showContextMenu = (event) => {
            emit("showContextMenu", event, props.user)
        };

        return {store, chat, isAdmin, popupTriggers, 
            togglePopup, showContextMenu}
    }
}
</script>

<template>
    <div class="user-on-settings" @contextmenu.prevent="showContextMenu">
        <div class="wrapper">
                <img :src="user?.img" class="user-img">
        </div>
        <div class="user-info">
            <div class="user-text">
                <span class="user-name">{{ user?.name }}</span>
                <div v-if="user?.is_online" class="online">
                    Онлайн
                </div>
                <div v-else class="offline">
                    Не в сети
                </div>
            </div>
            <span v-if="user?.group_settings_has_user?.role === 'O'" class="role">
                Владелец
            </span>
            <span v-else-if="user?.group_settings_has_user?.role === 'A'" class="role">
                Админ
            </span>
        </div>
        <transition name="popup-fade">
            <com-popup 
                v-if="popupTriggers.buttonTrigger" 
                :togglePopup="() => togglePopup('buttonTrigger')">
                <com-button @click="leaveUser()">Покинуть</com-button>
            </com-popup>
        </transition>

        <div v-if="user?.username == store.getters.getUserName && store.getters.getUserRole !== 'O'">
            <com-button @click="togglePopup('buttonTrigger')">Покинуть</com-button>
        </div>
    </div>
</template>

<style scoped>
.popup-fade-enter-active, .popup-fade-leave-active {
    transition: opacity 0.5s;
}
.popup-fade-enter-from, .popup-fade-leave-to {
    opacity: 0;
}

.user-on-settings {
    display: flex;
    flex-direction: row;
    align-items: center;
}

.user-info {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-left: 10px;
}

.role {
    margin-left: auto;
    margin-right: 10px;
}

.user-text {
    display: flex;
    flex-direction: column;
}

.user-name {
    font-weight: bolder;
}

.wrapper {
    max-width: 65px;
    max-height: 65px;
    margin: 5px;
}

.user-img {
    width: 65px;
    height: 65px;
    border-radius: 50%;
}
</style>