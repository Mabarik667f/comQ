<script>
import ButtonsMenu from "@/components/ChatElements/ButtonsMenu.vue"
import { ref, computed } from "vue";
import { useStore } from "vuex";

import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';

export default {
    components: {
        ButtonsMenu
    },
    props: {
        searchQuery: {
            type: String,
            default: ''
        }
    },
    emits: ['update:modelValue'],
    setup(props, {emit}) {

        const store = useStore()
        const privateAddVisible = ref(false)
        const groupAddVisible = ref(false)
        const hub = computed(() => store.getters.getHub)
        const errors = computed(() => store.getters.getCreateErrors)

        const createPrivateChatHook = () => {
            store.dispatch('checkTokenLifeTime')
            hub.value.send(
                JSON.stringify({
                    "message_type": "chat.new_chat",
                    "data": {"current_users": [createPrivateForm.value.username],
                            "chat_type": createPrivateForm.value.chat_type,
                            "host": jwtDecode(Cookies.get("access"))["user_id"]}
                })
            )
            showPrivateDialog()
        }


        const createGroupChatHook = async () => {
            const currentUsers = [];
            for (const user of createGroupForm.value.currentUsers) {
                currentUsers.push(user.value);
            } 
            store.dispatch('checkTokenLifeTime')
            hub.value.send(
                JSON.stringify({
                    "message_type": "chat.new_chat",
                    "data": {"current_users": currentUsers,
                            "chat_type": createGroupForm.value.chat_type,
                            "host": jwtDecode(Cookies.get('access'))['user_id']},
                            "title": createGroupForm.value.title
                })
            )
            showGroupDialog()
        }

        const showPrivateDialog = () => {
            privateAddVisible.value = !privateAddVisible.value;
        }
        const showGroupDialog = () => {
            groupAddVisible.value = !groupAddVisible.value;
        }

        const createPrivateForm = ref({
            username: '',
            chat_type: 'P'
        })

        const createGroupForm = ref({
            currentUsers: [],
            chat_type: "G",
            title: ''
        })

        const menu = ref(false);
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

        const updateSearchQuery = (event) => {
            emit('update:modelValue', event.target.value);
        }

        const updateGroupFormData = (currentUsers) => {
            createGroupForm.value.currentUsers = currentUsers;
        }

        const relatedUsers = store.getters.getRelatedUsers;

        const logout = () => {
            store.dispatch("logout");
        }

        const actions = ref([
            {"name": 'Профиль', "to": '/profile'},
            {"name": "Новая группа", "event": showGroupDialog},
            {"name": "Новый чат", "event": showPrivateDialog},
            {"name": 'Выйти', "event": logout}
        ])

        return {
            createPrivateForm, 
            createGroupForm,

            createPrivateChatHook,
            createGroupChatHook,

            showPrivateDialog,
            showGroupDialog,
            privateAddVisible,
            groupAddVisible,
            buttonPosition,

            relatedUsers,
            errors,
            store,
            menu,
            showMenu,
            updateSearchQuery,
            updateGroupFormData,
            actions
        }
    }    
}
</script>

<template>
    <div class="chats-header">
        <div class="support-elements">
            <com-button :class="'menu-button'" :orange="false" @click.stop="showMenu">&#9776;</com-button>
            <ButtonsMenu
            :show="menu"
            :options="actions"
            :position="buttonPosition"
            @showUpdate="showMenu"></ButtonsMenu>

            <com-input type="text" :value="searchQuery" placeholder="Поиск" class="form-control search-input"
            @input="updateSearchQuery"></com-input>
        </div>

        <com-dialog v-model:show="privateAddVisible">
            <com-form @submit.prevent="createPrivateChatHook()" class="privateChatCreate">
                <template v-slot:header>
                    <div class="mb-4">
                    <h2 class="form-header">Новый чат</h2>
                    </div>
                </template>
                <template v-slot:fields>
                    <div class="mb-4">
                    <span v-if="errors.newPrivateChat" class="form-errors">{{ errors.newPrivateChat }}</span>
                    <label :for="'newPrivateChat'">Уникальное имя пользователя</label>
                    <com-input :id="'newPrivateChat'" 
                    class="form-control newPrivate"
                    :placeholder="'Ivan1234'"
                    v-model="createPrivateForm.username"
                    required></com-input>
                    </div>

                </template>
                <template v-slot:button>
                    <com-button>Создать</com-button>
                </template>
            </com-form>
        </com-dialog>

        <com-dialog v-model:show="groupAddVisible">
            <com-form @submit.prevent="createGroupChatHook()" class="groupChatCreate">
                <template v-slot:header>
                    <div class="mb-4">
                    <h2 class="form-header">Новая Группа</h2>
                    </div>
                </template>
                <template v-slot:fields>
                    <div class="mb-4">
                        <label :for="'newGroupChat'">Название группы</label>
                        <com-input :id="'newGroupChat'" 
                        class="form-control"
                        :placeholder="'Party'"
                        v-model="createGroupForm.title"
                        required></com-input>  
                    </div>

                    <div class="mb-4">     
                        <com-tagging :options="relatedUsers" v-model="createGroupForm.currentUsers"
                        @updateCurrentUsers="updateGroupFormData">
                        </com-tagging>
                    </div>
                </template>
                <template v-slot:button>
                    <com-button>Создать</com-button>
                </template>
            </com-form>
        </com-dialog>
    </div>
</template>

<style scoped>
.chats-header {
    display: flex;
    flex-direction: row;
    height: 7vh;
    width: 100%;
}

.support-elements {
    display: flex;
    flex-direction: row;
    width: 100%;
}

.menu-button {
    margin: 5px;
}

.search-input {
    margin: 10px;
    border-radius: 20px;
    border: 2px solid rgba(255, 255, 255, 0.4);
}
.newPrivate {
    width: 300px;
}

.form-control:focus {
    border-color: #a3a1a1;
    box-shadow: none;
}

.privateChatCreate {
    margin: auto;
}

:deep(.multiselect) {
    max-width: 250px !important;
}

@media (max-width: 768px) {
    .com-dialog {
        width: 90% !important;
        margin: 0 auto;
        padding: 10px;
    }

    :deep .modal__content {
        padding: 5px !important;
        width: 60% !important;
    }

    .form-header {
        font-size: 1.5em;
    }

    .form-control {
        width: 100%;
    }

    .privateChatCreate, .groupChatCreate {
        width: 100%;
    }

    .newPrivate, .search-input {
        width: 100%;
    }
}

</style>