<script>
import Multiselect from 'vue-multiselect'
import ButtonsMenu from "@/components/ChatElements/ButtonsMenu.vue"
import { ref, computed } from "vue";
import { useStore } from "vuex";

import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';

export default {
    components: {
        Multiselect,
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
                            "host": jwtDecode(Cookies.get('access'))['user_id']}
                })
            )
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

        const menu = ref(false);
        const showMenu = () => {
            menu.value = !menu.value
        }

        const updateSearchQuery = (event) => {
            emit('update:modelValue', event.target.value);
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
            errors,
            store,
            menu,
            showMenu,
            updateSearchQuery
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
            @showUpdate="showMenu"
            @private="showPrivateDialog"
            @group="showGroupDialog"></ButtonsMenu>

            <com-input type="text" :value="searchQuery" placeholder="Поиск" class="form-control search-input"
            @input="updateSearchQuery"></com-input>
        </div>

        <com-dialog v-model:show="privateAddVisible">
            <com-form @submit.prevent="createPrivateChatHook()" class="privateChatCreate">
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

        <com-dialog v-model:show="groupAddVisible">
            <p>Добавьте участников в группу</p>
            <com-form @submit.prevent="createGroupChatHook()" class="groupChatCreate">
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
    display: flex;
    align-items: center;
    justify-content: center;
}

</style>