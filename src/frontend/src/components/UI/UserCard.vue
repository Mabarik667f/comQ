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
    emits: ['changeRole', 'leaveUser', 'deleteUser'],
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

        const changeRole = (role) => {
            emit('changeRole', {role: role, user: user.value.id})
        }

        const leaveUser = () => {
            emit('leaveUser')
        }

        const deleteUser = () => {
            emit('deleteUser', user.value)
        }
        
        const popupTriggers = ref({
            buttonTrigger: false
        })

        const togglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }

        return {changeRole, leaveUser, deleteUser, store, chat, isAdmin, popupTriggers, togglePopup}
    }
}
</script>

<template>
    <div class="user-on-settings">
        {{ user }}
        <transition name="popup-fade">
            <com-popup 
                v-if="popupTriggers.buttonTrigger" 
                :togglePopup="() => togglePopup('buttonTrigger')">
                <com-button @click="leaveUser()">Покинуть</com-button>
            </com-popup>
        </transition>

        <div v-if="user.username == store.getters.getUserName && store.getters.getUserRole !== 'O'">
            <com-button @click="togglePopup('buttonTrigger')">Покинуть</com-button>
        </div>

        <div v-if="isAdmin() && user.username !== store.getters.getUserName">
            <com-button @click="deleteUser()">Исключить</com-button>
        </div>
        <div v-if="store.state.userData.id == chat.host">
            
            <com-button v-if="user?.group_settings_has_user?.role === 'D'" @click="changeRole('A')">Выдать Админа</com-button>                        
            <com-button v-else-if="user?.group_settings_has_user?.role === 'A'" @click="changeRole('D')">Дефолт</com-button>
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
</style>