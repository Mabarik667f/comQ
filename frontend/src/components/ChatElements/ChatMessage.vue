<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
export default {
    emits: ['delete-message', 'edit-message', 'replyToMessage', 'showContextMenu', 'goToMessage'],
    props: {
        message: {
            require: true,
            type: Object
        },
        chatType: {
            require: true
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

        const goToMessage = (id) => {
            emit('goToMessage', id)
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

            return `${parseInt(day)} ${monthGenitive} ${year} ${parseInt(hour)+3}:${minute}`;

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
             showContextMenu, contextMenu, editMessage, deleteMessage, goToMessage}
    }
}
</script>

<template>
    <div :class="{
        'system-message': message.system,
        'left': !message.system && message.user.username !== currentUserName,
        'right': !message.system && message.user.username === currentUserName,
        'message': true,
        ['message-' + message.id]: true
    }" @contextmenu.prevent="showContextMenu">
    
            <div class="message-content">
                <div class="msg-author" v-if="!message.system && chatType === 'G'">{{ message.user.name }}</div>
                <div v-if="message?.reply?.text_content" class="wrapper-reply" @click="goToMessage(message?.reply?.id)">
                    <div class="msg-author" v-if="!message.system && chatType === 'G'">{{ message.user.name }}</div>
                    <div class="msg-to-reply">{{ message?.reply?.text_content }}</div>
                </div>
                <pre>{{ message.text_content }}</pre>
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
    padding: 8px;
    color: whitesmoke;
    position: relative;
}
.message-content {
    display: flex;
    flex-direction: column;
}

.message-date {
    color: rgba(255, 255, 255, 0.4);
    font-size: 14px;
    align-self: flex-end;
}

.msg-author {
    font-weight: bolder;
}

.msg-to-reply {
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}

.left {
    align-self: flex-start;
}

.right {
    align-self: flex-end;
    background-color: orangered;
}

.wrapper-reply {
    padding: 5px;
    flex-grow: 1;
    background-color: rgb(224, 81, 29, 0.8);
    border: 1px solid rgba(30, 30, 35);
    border-left: 5px solid rgb(146, 42, 5);
    border-radius: 5px;
    margin-bottom: 5px;
    cursor: pointer;
}

.highlighted {
    animation: highlight 2s ease;
}

@keyframes highlight {
    0% {
        background-color: yellow;
    }
    100% {
        background-color: transparent;
    }
}

.system-message {
    border: 2px solid rgba(255, 255, 255, 0.4);
    text-align: center;
    align-self: center;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50%;
}

pre {
    margin: 0;
}
</style>