<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
export default {
    emits: ['delete-message', 'edit-message', 'replyToMessage'],
    props: {
        message: {
            require: true,
            type: Object
        }
    },

    setup(props, {emit}) {
        const store = useStore();

        const currentUserName = store.state.userData.username;
        const messageDate = ref('');
        const user = ref({});

        const editMessage = () => {
            emit('edit-message', props.message);
        }
        const deleteMessage = () => {
            emit('delete-message', props.message);
        }

        const replyToMessage = () => {
            emit('replyToMessage', props.message)
        }

        const copyToClipboard = async () => {
            await navigator.clipboard.writeText(props.message.text_content);
        }

        const formattedDate = () => {
            const monthsGenitive = [
                'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
            ];

            const [datePart, timePart] = props.message.created_at_formatted.split(' ');
            const [day, month, year] = datePart.split('-');
            const [hour, minute] = timePart.split(':');

            const monthIndex = parseInt(month) - 1;
            const monthGenitive = monthsGenitive[monthIndex];

            return `${parseInt(day)} ${monthGenitive} ${year} ${hour}:${minute}`;

        }
        messageDate.value = formattedDate();


        const popupTriggers = ref({
            buttonTrigger: false
        })

        const togglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }

        const contextMenu = ref(null);

        const showContextMenu = (event) => {

            if (contextMenu.value) {
                contextMenu.value.openMenu(event);
            }
        };

        const actions = ref([
            {"name": "Ответить", "event": replyToMessage},
            {"name": "Копировать текст", "event": copyToClipboard}
        ])
        
        // можно ли удалять
        if ((props.message.user.username == store.getters.getUserName ||
        ('A', 'O').includes(store.getters.getUserRole)) && !props.message.system) {
            actions.value.push({"name": "Удалить", "event": () => togglePopup('buttonTrigger')})
        }

        // можно ли редактировать
        if (props.message.user.username == store.getters.getUserName && !props.message.system) {
            actions.value.push({"name": "Редактировать", "event": editMessage})
        }


        return {user, messageDate, currentUserName, togglePopup, popupTriggers,
             showContextMenu, contextMenu, actions, editMessage, deleteMessage}
    }
}
</script>

<template>
    <com-popup
    v-if="popupTriggers.buttonTrigger"
    :togglePopup="() => togglePopup('buttonTrigger')">
        <com-button @click="deleteMessage" v-if="!message.system">Удалить</com-button>
    </com-popup>
    <div :class="{
        'system-message': message.system,
        'left': !message.system && message.user.username !== currentUserName,
        'right': !message.system && message.user.username === currentUserName,
        'message': true
        }" @contextmenu.prevent="showContextMenu" >
            <com-context-menu :options="actions" ref="contextMenu" />
            {{ message.text_content }}
            {{ message.user.name }}
            {{ message.reply }}
        <div class="message-date">
            {{ messageDate }}
        </div>
        
    </div>

</template>

<style scoped>
.message {
    border: 1px solid black;
    border-radius: 20px;
    width: 60%;
    text-align: left;
    margin: 5px 20px;
}
.message-date {
    color: gray;
}

.left {
    align-self: flex-start;
}

.right {
    align-self: flex-end;
}

.system-message {
    border: 5px blue solid;
}
</style>