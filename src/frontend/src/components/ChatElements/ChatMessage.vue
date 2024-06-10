<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
export default {
    props: {
        message: {
            require: true,
            type: Object
        }
    },

    setup(props) {
        const store = useStore();

        const currentUserName = store.state.userData.username;
        const messageDate = ref('');
        const user = ref({});

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
        return {user, messageDate, currentUserName}
    }
}
</script>

<template>
    <div :class="{'left': message.user.username !== currentUserName,
                'right': message.user.username === currentUserName,
                'message': true }">
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
</style>