<script>
import SearchChat from "@/components/SearchChat";
import Multiselect from 'vue-multiselect'
import ButtonsMenu from "@/components/ChatElements/ButtonsMenu.vue"
import { ref, computed } from "vue";
import { useStore } from "vuex";

import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';

export default {
    data() {
        return {
            menu: false
        }
    },
    components: {
        SearchChat,
        Multiselect,
        ButtonsMenu
    },
    methods: {
        showMenu() {
            this.menu = true;
        }
        
    },
    setup() {

        const store = useStore()
        const privateAddVisible = ref(false)
        const groupAddVisible = ref(false)
        const hub = computed(() => store.getters.getHub)
        const errors = computed(() => store.getters.getCreateErrors)

        const createPrivateChatHook = () => {
            hub.value.send(
                JSON.stringify({
                    "message_type": "chat.new_chat",
                    "data": {"current_users": [createPrivateForm.value.username],
                            "chat_type": createPrivateForm.value.chat_type,
                            "host": jwtDecode(Cookies.get('access'))['user_id']}
                })
            )
        }


        const createGroupChatHook = async () => {
            const currentUsers = [];
            for (const user of createGroupForm.value.currentUsers) {
                currentUsers.push(user.value);
            } 
            hub.value.send(
                JSON.stringify({
                    "message_type": "chat.new_chat",
                    "data": {"current_users": currentUsers,
                            "chat_type": createGroupForm.value.chat_type,
                            "host": jwtDecode(Cookies.get('access'))['user_id']},
                    "title": createGroupForm.value.title
                })
            )
        }

        const showPrivateDialog = (event) => {
            privateAddVisible.value = event;
        }
        const showGroupDialog = (event) => {
            groupAddVisible.value = event;
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

        const relatedUsers = store.getters.getRelatedUsers;

        return {
            createPrivateForm, 
            createGroupForm,

            createPrivateChatHook,
            createGroupChatHook,

            showPrivateDialog,
            showGroupDialog,
            privateAddVisible,
            groupAddVisible,

            relatedUsers,
            errors,
            store
        }
    }    
}
</script>

<template>
    <div class="chats-header">
        <com-button :class="'menu-button'" @click="showMenu">&#9776;</com-button>
        <ButtonsMenu
        v-model:show="menu"
        @private="showPrivateDialog"
        @group="showGroupDialog"></ButtonsMenu>
        <SearchChat></SearchChat>

        <com-dialog v-model:show="privateAddVisible" class="privateChatCreate">
            <com-form @submit.prevent="createPrivateChatHook()">
                <template v-slot:header>
                    <h2>Новый чат</h2>
                </template>
                <template v-slot:fields>
                    <span v-if="errors.newPrivateChat" class="form-errors">{{ errors.newPrivateChat }}</span>
                    <label :for="'newPrivateChat'">Идентификатор</label>
                    <com-input :id="'newPrivateChat'" 
                    class="form-control newPrivate"
                    :placeholder="'Ivan1234'"
                    v-model="createPrivateForm.username"
                    required></com-input>

                </template>
                <template v-slot:button>
                    <com-button>Создать</com-button>
                </template>
            </com-form>
        </com-dialog>

        <com-dialog v-model:show="groupAddVisible" class="groupChatCreate">
            <p>Добавьте участников в группу</p>
            <com-form @submit.prevent="createGroupChatHook()">
                <template v-slot:header>
                    <h2>Новая Группа</h2>
                </template>
                <template v-slot:fields>
                    <div>
                    <label :for="'newGroupChat'">Название группы</label>
                    <com-input :id="'newGroupChat'" 
                    class="form-control"
                    :placeholder="'Party'"
                    v-model="createGroupForm.title"
                    required></com-input>       

                    <label class="typo__label">Tagging</label>
                        <multiselect c v-model="createGroupForm.currentUsers"
                        required
                        placeholder="Кого добавим?" tag-placeholder="Участник" label="name"
                        track-by="value" :options="relatedUsers"
                        :multiple="true" :taggable="true" @tag="addTag">
                    </multiselect>
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
}
.menu-button {
    --bs-btn-color: #333; /* Цвет текста кнопки (темно-серый) */
    --bs-btn-bg: #f8f9fa; /* Цвет фона кнопки (светло-серый) */
    --bs-btn-border-color: #ced4da; /* Цвет рамки кнопки (серый) */
    --bs-btn-hover-color: #fff; /* Цвет текста при наведении (белый) */
    --bs-btn-hover-bg: #6c757d; /* Цвет фона при наведении (темно-серый) */
    --bs-btn-hover-border-color: #6c757d; /* Цвет рамки при наведении (темно-серый) */
    --bs-btn-focus-shadow-rgb: 49, 132, 253; /* Тень при фокусе (синий) */
    --bs-btn-active-color: #fff; /* Цвет текста при активном состоянии (белый) */
    --bs-btn-active-bg: #343a40; /* Цвет фона при активном состоянии (темно-серый) */
    --bs-btn-active-border-color: #343a40; /* Цвет рамки при активном состоянии (темно-серый) */
    --bs-btn-active-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125); /* Тень при активном состоянии */
    --bs-btn-disabled-color: #6c757d; /* Цвет текста для отключенного состояния (серый) */
    --bs-btn-disabled-bg: #f8f9fa; /* Цвет фона для отключенного состояния (светло-серый) */
    --bs-btn-disabled-border-color: #f8f9fa; /* Цвет рамки для отключенного состояния (светло-серый) */
}
.newPrivate {
    width: 300px;
}

</style>