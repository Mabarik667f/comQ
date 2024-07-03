<script>
import ChatHeader from '@/components/ChatElements/ChatHeader.vue';
import ChatContent from "@/components/ChatElements/ChatContent.vue";
import ChatGroupSettingsChange from "@/components/ChatElements/ChatGroupSettingsChange.vue";
import UserCard from '@/components/UI/UserCard.vue';
import Multiselect from 'vue-multiselect'

import { ref, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import isAdmin from "@/hooks/permissionHooks/isAdmin"
import isOwner from "@/hooks/permissionHooks/isOwner"
import changeRole from "@/hooks/chatHooks/changeRole"
export default {
    components: {
        ChatHeader,
        ChatContent,
        ChatGroupSettingsChange,
        Multiselect,
        UserCard
    },
    
    setup() {
        const route = useRoute();
        const store = useStore();

        const addedUsers = ref([]);
        const relatedUsersInGroup = ref([]);
        const settingsVisible = ref(false);

        const chatId = ref(parseInt(route.params.pk));
        const chat = computed(() => store.getters.getChat(chatId.value));
        const relatedUsers = computed(() => store.getters.getRelatedUsers);

        const fetchData = async () => {
            if (chat.value.chat_type === 'G') {
                relatedUsersInGroup.value = relatedUsers.value.filter(u => !chat.value.current_users.some(
                    currentUser => currentUser.username === u.value)
                )
                const currentUser = chat.value.current_users.filter(u => u.username === store.getters.getUserName)
                store.commit('setUserRole', {role: currentUser[0].group_settings_has_user.role});
            }
        }

        watch(() => route.params.pk, (newChatId) => {
            chatId.value = parseInt(newChatId);
            fetchData()
        }, {deep: true})

        watch(() => (chat.value?.current_users), () => {
            if (chat?.value) {
                fetchData();
            }
        }, {deep: true})

        const deleteUserToRoomHook = (event) => {
            child.value.deleteUserToRoom(event.username)
        }

        const leaveUserToRoomHook = () => {
            child.value.leaveUserToRoom()
        }

        const deleteRoomHook = () => {
            child.value.deleteRoom()
        }

        const addUserToRommHook = () => {
            child.value.addUserToRoom(addedUsers.value)
            addedUsers.value = []
        }

        const changeRoleHook = async (event) => {
            const {asyncCall} = changeRole();
            await asyncCall(event.role, event.user, chat.value.group_settings.id);
        }

        const child = ref(null);

        const popupTriggers = ref({
            buttonTrigger: false
        })

        const togglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }

        const showSettings = () => {
            if (chat.value?.chat_type === 'G') {
                settingsVisible.value = true;
            }
        }

        
        return {chat,
                chatId,
                child,
                relatedUsersInGroup,
                addedUsers,
                store,

                popupTriggers,
                togglePopup,

                deleteUserToRoomHook,
                leaveUserToRoomHook,
                deleteRoomHook,
                addUserToRommHook,
                changeRoleHook,

                settingsVisible,
                showSettings,

                isAdmin,
                isOwner}
    }
}
</script>

<template>
    <div class="chat">
        <transition name="popup-fade">
            <com-popup 
                v-if="popupTriggers.buttonTrigger" 
                :togglePopup="() => togglePopup('buttonTrigger')">
                <com-button @click="deleteRoomHook()" v-if="isOwner()">Удалить группу</com-button>
            </com-popup>
        </transition>

        <ChatHeader @click="showSettings()" :chatId="parseInt(chatId)"></ChatHeader>
        <com-dialog v-model:show="settingsVisible" v-if="chat && chat?.chat_type === 'G'">
            <div class="chat-settings">
                <div>
                    <ChatGroupSettingsChange
                    :groupSettings="chat?.groupSettings" :chatId="parseInt(chatId)"></ChatGroupSettingsChange>
                    
                    <com-button @click="togglePopup('buttonTrigger')" v-if="isOwner()">Удалить группу</com-button>
                    <div v-if="chat && chat.chat_type === 'G'">
                        <div class="add-users" v-if="isAdmin()">
                            <label class="typo__label">Tagging</label>
                            <multiselect c v-model="addedUsers"
                            required
                            placeholder="Кого добавим?" tag-placeholder="Участник" label="name"
                            track-by="value" :options="relatedUsersInGroup"
                            :multiple="true" :taggable="true" @tag="addTag">
                        </multiselect>
                            <com-button v-if="addedUsers.length > 0" @click=addUserToRommHook()>Добавить</com-button>
                        </div>
                        <div v-for="user in chat?.current_users" :key="user">
                            <UserCard :user="user" :chatId="parseInt(chatId)" 
                            @leaveUser="leaveUserToRoomHook" 
                            @changeRole="changeRoleHook"
                            @deleteUser="deleteUserToRoomHook">
                            </UserCard>
                        </div>
                    </div>
                </div>
            </div>
        </com-dialog>
        <ChatContent :chatId="parseInt(chatId)" ref="child"></ChatContent>
    </div>
</template>

<style scoped>
.chat {
    height: 100vh;
    width: 100%;
    background-color: rgb(30, 30, 35);
}

.chat-settings {
    border: 1px rgb(30, 30, 45) solid;
    background-color: rgb(41, 39, 38);
    border-radius: 20px;
    color: whitesmoke;
    overflow-y: auto;
    height: 95vh;
}

.popup-fade-enter-active, .popup-fade-leave-active {
    transition: opacity 0.5s;
}
.popup-fade-enter-from, .popup-fade-leave-to {
    opacity: 0;
}
</style>