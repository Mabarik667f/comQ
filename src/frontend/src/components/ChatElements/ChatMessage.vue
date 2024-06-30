<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
export default {
    emits: ['delete-message', 'edit-message', 'replyToMessage', 'showContextMenu'],
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
            emit("showContextMenu", event, props.message)
        };


        return {user, store, messageDate, currentUserName, togglePopup, popupTriggers,
             showContextMenu, contextMenu, editMessage, deleteMessage}
    }
}
</script>

<template>
    
    <div :class="{
        'system-message': message.system,
        'left': !message.system && message.user.username !== currentUserName,
        'right': !message.system && message.user.username === currentUserName,
        'message': true
        }" @contextmenu.prevent="showContextMenu"
        >
        <div class="img-wrapper" v-if="!message.system && message.user.username !== store.getters.getUserName">
                    <img :src="message.user.img" class="user-img">
                </div>
                <!-- <com-context-menu :options="actions" ref="contextMenu" /> -->
            <div class="message-content">
                <div v-if="!message.system">{{ message.user.name }}</div>
                <div>{{ message.text_content }}</div>
                <!-- <div v-if="!message.system">{{ message.reply }}</div> -->
                <div class="message-date" v-if="!message.system">
                    {{ messageDate }}
                </div>
            </div>
        
        
    </div>

</template>

<style scoped>
.message {
    border: 1px solid black;
    border-radius: 20px;
    min-width: 15%;
    max-width: 50%;
    text-align: left;
    margin: 5px 20px;
    padding: 5px;
}
.message-content {
    display: flex;
    flex-direction: column;
}

.message-date {
    color: gray;
    font-size: 14px;
    align-self: flex-end;
}

.left {
    align-self: flex-start;
}

.right {
    align-self: flex-end;
}

.img-wrapper {
    width: 65px;
}
.user-img {
    width: 100%;
    border-radius: 50%;
}

.system-message {
    border: 5px blue solid;
    text-align: center;
    align-self: center;
}
</style>