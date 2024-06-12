<script>
import SearchChat from "@/components/SearchChat";
import createPrivateChat from "@/hooks/chatHooks/createPrivateChat"
import createGroupChat from "@/hooks/chatHooks/createGroupChat"
import Multiselect from 'vue-multiselect'
import { ref } from "vue";
export default {
    props: {
        options: {
            require: true,
            default: () => []
        }
    },
    data() {
        return {
            privateAddVisible: false,
            groupAddVisible: false
        }
    },
    components: {
        SearchChat,
        Multiselect
    },
    methods: {
        showPrivateDialog() {
            this.privateAddVisible = true;
        },
        showGroupDialog() {
            this.groupAddVisible = true;
        },
        
    },
    setup() {

        const createPrivateForm = ref({
            username: '',
            firstMessage: '',
            chatType: 'P'
        })

        const createGroupForm = ref({
            currentUsers: [],
            chatType: "G",
            title: ''
        })

        const createPrivateChatHook = async () => {
                const {asyncCall} = createPrivateChat();
                await asyncCall(createPrivateForm.value);
            }

        const createGroupChatHook = async () => {
            const {asyncCall} = createGroupChat();
            await asyncCall(createGroupForm.value);
        }

        return {
            createPrivateForm, 
            createGroupForm,

            createPrivateChatHook,
            createGroupChatHook,
        }
    }    
}
</script>

<template>
    <div class="chats-header">
        
        <com-button :class="'menu-button'">&#9776;</com-button>
        
        <SearchChat></SearchChat>
        <!--Модальное окно для создание лс-->
        <com-dialog v-model:show="privateAddVisible" class="privateChatCreate">
            <com-form @submit.prevent="createPrivateChatHook()">
                <template v-slot:header>
                    <h2>Новый чат</h2>
                </template>
                <template v-slot:fields>

                    <label :for="'newPrivateChat'">Идентификатор</label>
                    <com-input :id="'newPrivateChat'" 
                    class="form-control newPrivate"
                    :placeholder="'@Ivan1234'"
                    v-model="createPrivateForm.username"
                    required></com-input>

                    <label :for="'firstMessage'">Сообщение</label>
                    <com-text :id="'firstMessage'" class="form-control"
                    v-model="createPrivateForm.firstMessage"></com-text>


                </template>
                <template v-slot:button>
                    <com-button>Отправить</com-button>
                </template>
            </com-form>
        </com-dialog>

        <!--Модальное окно для создание группы-->
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
                        track-by="value" :options="options"
                        :multiple="true" :taggable="true" @tag="addTag">
                    </multiselect>
                    </div>
                </template>
                <template v-slot:button>
                    <com-button>Создать</com-button>
                </template>
            </com-form>
        </com-dialog>

        <com-button @click="showPrivateDialog">Новый чат</com-button>
        <com-button @click="showGroupDialog">Создать группу</com-button>
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

</style>@/hooks/chatHooks/createChat