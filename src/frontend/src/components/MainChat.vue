<script>
import ChatHeader from '@/components/ChatElements/ChatHeader.vue';
import ChatContent from "@/components/ChatElements/ChatContent.vue";
import ChatGroupSettingsChange from "@/components/ChatElements/ChatGroupSettingsChange.vue";
import ButtonsMenu from './ChatElements/ButtonsMenu.vue';
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
        UserCard,
        ButtonsMenu
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

        const deleteUserCandidat = ref(null);
        const deleteUserToRoomHook = () => {
            child.value.deleteUserToRoom(deleteUserCandidat.value.username);
            togglePopup('userDeleteTrigger')
        }

        const leaveUserToRoomHook = () => {
            child.value.leaveUserToRoom()
            togglePopup('userLeaveTrigger')
        }

        const deleteRoomHook = () => {
            child.value.deleteRoom()
            togglePopup('groupDeleteTrigger')
        }

        const addUserToRommHook = () => {
            child.value.addUserToRoom(addedUsers.value)
            addedUsers.value = []
        }

        const changeRoleHook = async (role, user) => {
            const {asyncCall} = changeRole();
            await asyncCall(role, user, chat.value.groupSettings.id);
            store.commit('changeUserRole', {chatId: chat.value.pk, userId: user, role: role})
        }

        const child = ref(null);

        const popupTriggers = ref({
            groupDeleteTrigger: false,
            userDeleteTrigger: false,
            userLeaveTrigger: false
        })

        const togglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }

        const showSettings = () => {
            if (chat.value?.chat_type === 'G') {
                settingsVisible.value = true;
            }
        }

        const contextMenu = ref(null);
        const actions = ref([]);

        const showContextMenu = (event, user) => {

            actions.value = [];

            if (user?.username == store.getters.getUserName && store.getters.getUserRole !== 'O') {
                actions.value.push({"name": 'Покинуть', "event": () => togglePopup('userLeaveTrigger')})
            }

            if (isAdmin() && user?.username !== store.getters.getUserName) {
                actions.value.push({"name": 'Исключить', "event": () => togglePopup('userDeleteTrigger')})
            }
            if (user?.group_settings_has_user?.role === 'D' && isAdmin()) {
                actions.value.push({"name": "Выдать Админа", "event": () => changeRoleHook('A', user.id)})
            }                      
            if(user?.group_settings_has_user?.role === 'A' && isAdmin()) {
                actions.value.push({"name": "Забрать Админа", "event": () => changeRoleHook('D', user.id)})
            }
            deleteUserCandidat.value = user;

            contextMenu.value.openMenu(event)
            
        }

        const menu = ref(false);
        const buttonsMenuActions = ref([{'name': 'Удалить группу', "event": () => togglePopup('groupDeleteTrigger')}]);
        const buttonPosition = ref({ top: 0, left: 0 });
        const showMenu = (event) => {
            if (event?.target?.getBoundingClientRect) {
                buttonPosition.value = {
                top: event.target.getBoundingClientRect().bottom,
                left: event.target.getBoundingClientRect().left,
            };
            }
            menu.value = !menu.value
        }

        
        return {chat,
                chatId,
                child,
                relatedUsersInGroup,
                addedUsers,
                store,
                contextMenu,
                actions,
                showContextMenu,
                buttonPosition,

                buttonsMenuActions,
                showMenu,
                menu,

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
                v-if="popupTriggers.groupDeleteTrigger" 
                :togglePopup="() => togglePopup('groupDeleteTrigger')">
                <com-button @click="deleteRoomHook()" :orange="false" v-if="isOwner()"
                style="color: orangered; font-weight: bolder;">Удалить</com-button>
            </com-popup>
        </transition>

        <ChatHeader @click="showSettings()" :chatId="parseInt(chatId)"></ChatHeader>
        <com-dialog v-model:show="settingsVisible" v-if="chat && chat?.chat_type === 'G'">
            <div class="chat-settings">
                <div>
                    <div class="menu-wrapper">
                        <com-button :class="'menu-button'" class="button-wrapper" :orange="false" @click.stop="showMenu">&#9776;</com-button>
                        <ButtonsMenu
                        :show="menu"
                        :options="buttonsMenuActions"
                        :position="buttonPosition"
                        @showUpdate="showMenu"></ButtonsMenu>
                    </div>
                    <ChatGroupSettingsChange
                    :groupSettings="chat?.groupSettings" :chatId="parseInt(chatId)"></ChatGroupSettingsChange>
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
                            @showContextMenu="showContextMenu">
                            </UserCard>
                        </div>
                    </div>
                </div>
            </div>
            <transition name="context-fade">
                <context-menu :options="actions" ref="contextMenu"/>
            </transition>

            <transition name="popup-fade">
                <com-popup 
                    v-if="popupTriggers.userLeaveTrigger" 
                    :togglePopup="() => togglePopup('userLeaveTrigger')">
                    <com-button @click="leaveUserToRoomHook()" :orange="false"
                    style="color: orangered; font-weight: bolder;">Покинуть</com-button>
                </com-popup>
            </transition>

            <transition name="popup-fade">
                <com-popup 
                    v-if="popupTriggers.userDeleteTrigger" 
                    :togglePopup="() => togglePopup('userDeleteTrigger')">
                    <com-button @click="deleteUserToRoomHook()" :orange="false"
                    style="color: orangered; font-weight: bolder;">Исключить</com-button>
                </com-popup>
            </transition>

        </com-dialog>
        <ChatContent :chatId="parseInt(chatId)" ref="child"></ChatContent>
    </div>
</template>

<style scoped>

.button-wrapper {
    margin-left: auto;
}
.menu-wrapper {
    display: flex;
    width: 100%;
}
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
    overflow: scroll;
    width: 50% !important;
    margin: auto !important;
    padding: 15px
}

.popup-fade-enter-active, .popup-fade-leave-active {
    transition: opacity 0.5s;
}
.popup-fade-enter-from, .popup-fade-leave-to {
    opacity: 0;
}
</style>