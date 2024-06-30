<script>
import SearchChat from "@/components/SearchChat";
import createPrivateChat from "@/hooks/chatHooks/createPrivateChat"
import createGroupChat from "@/hooks/chatHooks/createGroupChat"
import cleanChatData from "@/hooks/chatHooks/cleanChatData";
import Multiselect from 'vue-multiselect'
import ButtonsMenu from "@/components/ChatElements/ButtonsMenu.vue"
import { ref } from "vue";
import store from "@/store";
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

        const privateAddVisible = ref(false)
        const groupAddVisible = ref(false)

        const showPrivateDialog = (event) => {
            privateAddVisible.value = event;
        }
        const showGroupDialog = (event) => {
            groupAddVisible.value = event;
        }

        const createPrivateForm = ref({
            username: '',
            chatType: 'P'
        })

        const createGroupForm = ref({
            currentUsers: [],
            chatType: "G",
            title: ''
        })

        const errors = ref({
            newPrivateChat: '',
            newGroupChat: ''
        })

        const createPrivateChatHook = async () => {
            const {asyncCall} = createPrivateChat();
            const data = await asyncCall(createPrivateForm.value);
            if (data.error) {
                console.log(data.error)
                errors.value.newPrivateChat = data.error[0] || data.error.current_users[0];
            } else {
                errors.value.newPrivateChat = '';
                await cleanChatData(data.value)
            }
        }
            

        const createGroupChatHook = async () => {
            const {asyncCall} = createGroupChat();
            const {chat} = await asyncCall(createGroupForm.value);
            await cleanChatData(chat.value)
        }

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
            errors
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