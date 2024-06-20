<script>
import ChatHeader from '@/components/ChatElements/ChatHeader.vue';
import ChatContent from "@/components/ChatElements/ChatContent.vue";
import ChatGroupSettingsChange from "@/components/ChatElements/ChatGroupSettingsChange.vue";
import Multiselect from 'vue-multiselect'

import { onMounted, ref, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import getChatData from '@/hooks/chatHooks/getChatData';
import getUserDataOnChat from '@/hooks/getUserDataOnChat';
import groupChatDetail from "@/hooks/chatHooks/groupChatDetail"

import changeRole from "@/hooks/chatHooks/changeRole"
import { useStore } from 'vuex';
export default {
    components: {
        ChatHeader,
        ChatContent,
        ChatGroupSettingsChange,
        Multiselect
    },
    data() {
        return {
            settingsVisible: false
        }
    },
    methods: {
        showSettings() {
            this.settingsVisible = true;
        }
    },
    setup() {
        const route = useRoute();
        const chatId = ref(route.params.pk);
        const chat = ref({});
        const store = useStore();
        const addedUsers = ref([]);
        const relatedUsers = computed(() => store.getters.getRelatedUsers);
        const relatedUsersInGroup = ref([]);

        const fetchData = async () => {
            const {chatData} = await getChatData(chatId.value);
            chat.value = chatData.value;
            if (chat.value.chat_type === 'G') {

                const {chatData: group_settings} = await groupChatDetail(chat.value.pk)
                chat.value.group_settings = group_settings.value.group_settings
                relatedUsersInGroup.value = relatedUsers.value.filter(u => !chat.value.current_users.some(
                    currentUser => currentUser.username === u.value)
                )

            } else {
                const addUser = chat.value.current_users.filter(c => c.username !== store.state.userData.username)[0];
                chat.value.partner = await getUserDataOnChat(addUser.username)
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

        const deleteUserToRoomHook = (user) => {
            child.value.deleteUserToRoom(user.username)
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

        const changeRoleHook = async (role, user) => {
            const {asyncCall} = changeRole();
            await asyncCall(role, user, chat.value.group_settings.id);
        }

        const child = ref(null);

        
        return {chat,
                deleteUserToRoomHook,
                leaveUserToRoomHook,
                deleteRoomHook,
                addUserToRommHook,
                changeRoleHook,
                child,
                relatedUsersInGroup,
                addedUsers}
    }
}
</script>

<template>
    <div class="chat">
        <label class="typo__label">Tagging</label>
                <multiselect c v-model="addedUsers"
                required
                placeholder="Кого добавим?" tag-placeholder="Участник" label="name"
                track-by="value" :options="relatedUsersInGroup"
                :multiple="true" :taggable="true" @tag="addTag">
            </multiselect>
        <ChatHeader @click="showSettings()"></ChatHeader>
        <com-dialog v-model:show="settingsVisible">
            
            <ChatGroupSettingsChange :img="$store.state.currentChat.imagePath"
            :groupSettings="chat.group_settings.id"></ChatGroupSettingsChange>
            <!--Нужно получать роли пользователей, сделать hook для получения пользователей
            для добавления-->
            <h1>{{$store.state.currentChat.title}}</h1>
            <h2>Информация</h2>
            <com-button @click=addUserToRommHook()>Добавить</com-button>
            <com-button @click="deleteRoomHook()">Удалить группу</com-button>
            <div v-if="chat.chat_type === 'G'">
                <div v-for="user in chat.current_users" :key="user">
                    {{ user }}
                    <div v-if="user.username == $store.state.userData.username">
                        <com-button @click="leaveUserToRoomHook()">Покинуть</com-button>
                    </div>

                    <div v-else>
                        <com-button @click="deleteUserToRoomHook(user)">Исключить</com-button>
                    </div>
                    <div v-if="$store.state.userData.id == chat.host">
                        
                        <com-button @click="changeRoleHook('A', user.id)">Выдать Админа</com-button>                        
                        <com-button @click="changeRoleHook('D', user.id)">Дефолт</com-button>
                    </div>
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
</style>