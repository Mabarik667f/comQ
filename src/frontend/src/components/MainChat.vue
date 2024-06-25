<script>
import ChatHeader from '@/components/ChatElements/ChatHeader.vue';
import ChatContent from "@/components/ChatElements/ChatContent.vue";
import ChatGroupSettingsChange from "@/components/ChatElements/ChatGroupSettingsChange.vue";
import UserCard from '@/components/UI/UserCard.vue';
import Multiselect from 'vue-multiselect'

import { onMounted, ref, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import getChatData from '@/hooks/chatHooks/getChatData';
import getUserDataOnChat from '@/hooks/getUserDataOnChat';
import groupChatDetail from "@/hooks/chatHooks/groupChatDetail"
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
    data() {
        return {
            settingsVisible: false,
        }
    },
    methods: {
        showSettings() {
            this.settingsVisible = true;
        }
    },
    setup() {
        const route = useRoute();
        const store = useStore();

        const chat = ref({});
        const addedUsers = ref([]);
        const relatedUsersInGroup = ref([]);

        const chatId = ref(route.params.pk);
        const relatedUsers = computed(() => store.getters.getRelatedUsers);

        const fetchData = async () => {
            const {chatData} = await getChatData(chatId.value);
            chat.value = chatData.value;
            if (chat.value.chat_type === 'G') {

                const {chatData: group_settings} = await groupChatDetail(chat.value.pk)
                chat.value.groupSettings = group_settings.value.group_settings
                relatedUsersInGroup.value = relatedUsers.value.filter(u => !chat.value.current_users.some(
                    currentUser => currentUser.username === u.value)
                )
                const currentUser = chat.value.current_users.filter(u => u.username === store.getters.getUserName)[0]
                store.commit('setUserRole', {role: currentUser.group_settings_has_user.role});

            } else {
                const addUser = chat.value.current_users.filter(c => c.username !== store.state.userData.username)[0];
                const {userData} = await getUserDataOnChat(addUser.username)
                chat.value.partner = userData.value
            }

        }

        onMounted( () => {
            fetchData();
        })

        watch(() => route.params.pk, (newChatId) => {
            // решить проблему с фантомным запросом
            chatId.value = newChatId;
            fetchData();
            
        })

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
        }

        const changeRoleHook = async (event) => {
            const {asyncCall} = changeRole();
            await asyncCall(event.role, event.user, chat.value.group_settings.id);
        }

        const child = ref(null);
        
        return {chat,
                child,
                relatedUsersInGroup,
                addedUsers,
                store,

                deleteUserToRoomHook,
                leaveUserToRoomHook,
                deleteRoomHook,
                addUserToRommHook,
                changeRoleHook,

                isAdmin,
                isOwner}
    }
}
</script>

<template>
    <div class="chat">

        <ChatHeader @click="showSettings()" :chat="chat"></ChatHeader>
        <com-dialog v-model:show="settingsVisible" class="chat-settings">
            
            <ChatGroupSettingsChange v-if="chat.chat_type === 'G'"
            :groupSettings="chat.groupSettings" :chat="chat"></ChatGroupSettingsChange>
            <h1>{{store.state.currentChat.title}}</h1>
            <h2>Информация</h2>

            <com-button @click="deleteRoomHook()" v-if="isOwner()">Удалить группу</com-button>
            <div v-if="chat.chat_type === 'G'">
                <div class="add-users" v-if="isAdmin()">
                    <label class="typo__label">Tagging</label>
                    <multiselect c v-model="addedUsers"
                    required
                    placeholder="Кого добавим?" tag-placeholder="Участник" label="name"
                    track-by="value" :options="relatedUsersInGroup"
                    :multiple="true" :taggable="true" @tag="addTag">
                </multiselect>
                    <com-button @click=addUserToRommHook()>Добавить</com-button>
                </div>
                <div v-for="user in chat.current_users" :key="user">
                    <UserCard :user="user" :chat="chat" 
                    @leaveUser="leaveUserToRoomHook" 
                    @changeRole="changeRoleHook"
                    @deleteUser="deleteUserToRoomHook">
                    </UserCard>
                </div>
            </div>
        </com-dialog>
        <ChatContent :chat="chat" ref="child"></ChatContent>
    </div>
</template>

<style scoped>
.chat {
    height: 100vh;
    width: 100%;
    background-color: beige;
}

.chat-settings {
    border: 1px blue solid;
    
}
</style>